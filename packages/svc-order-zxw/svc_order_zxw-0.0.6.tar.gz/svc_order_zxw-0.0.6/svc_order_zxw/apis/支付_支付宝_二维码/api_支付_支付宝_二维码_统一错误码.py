"""
# File       : api_支付_支付宝_二维码.py
# Time       ：2024/8/25 12:02
# Author     ：xuewei zhang
# Email      ：shuiheyangguang@gmail.com
# version    ：python 3.12
# Description：
"""
from datetime import datetime
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from svc_order_zxw.db.models import Order, Payment, Product, get_db, PaymentMethod
from svc_order_zxw.apis.异常管理 import 订单_异常代码, 商品_异常代码, 支付_异常代码, 其他_异常代码
from svc_order_zxw.config import AliPayConfig
from svc_order_zxw.apis.schemas_payments import OrderStatus
from svc_order_zxw.apis.schemas_微信支付宝支付 import 请求_支付宝url_创建订单, 返回_支付宝url_订单信息, \
    请求_支付宝url_发起支付, 返回_支付宝url_支付信息

from app_tools_zxw.Funcs.fastapi_logger import logger
from app_tools_zxw.SDK_支付宝.支付服务_async import 支付服务
from app_tools_zxw.Errors.api_errors import HTTPException_AppToolsSZXW

router = APIRouter(prefix="/alipay/pay_qr", tags=["支付宝支付"])

alipay_client = 支付服务(app_id=AliPayConfig.appid,
                         key应用私钥=AliPayConfig.key应用私钥,
                         key支付宝公钥=AliPayConfig.key支付宝公钥,
                         回调路径的根地址=AliPayConfig.回调地址的根地址 + '/alipay/pay_qr')


@router.post("/create_order/", response_model=返回_支付宝url_订单信息)
async def 创建订单(request: 请求_支付宝url_创建订单, db: AsyncSession = Depends(get_db)):
    try:
        # 验证产品是否存在
        product = await db.execute(select(Product).filter(Product.id == request.product_id))
        product = product.scalar_one_or_none()
        if not product:
            raise HTTPException_AppToolsSZXW(
                error_code=商品_异常代码.商品不存在.value,
                detail="Product not found",
                http_status_code=404
            )

        # 创建新订单
        new_order = Order(
            order_number=支付服务.生成订单号(),
            user_id=request.user_id,
            total_amount=request.amount,
            product_id=request.product_id,
            app_id=request.app_id,
            status=OrderStatus.PENDING.value
        )
        db.add(new_order)
        await db.commit()
        await db.refresh(new_order)

        logger.info(f"Order created successfully: {new_order.order_number}")
        return 返回_支付宝url_订单信息(**new_order.to_dict())

    except IntegrityError as e:
        await db.rollback()
        logger.error(f"IntegrityError while creating order: {str(e)}")
        raise HTTPException_AppToolsSZXW(
            error_code=订单_异常代码.订单号已存在.value,
            detail="Order creation failed due to data integrity error",
            http_status_code=400
        )

    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Database error while creating order: {str(e)}")
        raise HTTPException_AppToolsSZXW(
            error_code=其他_异常代码.未知错误.value,
            detail=f"Database error occurred.{e}",
            http_status_code=500
        )

    except Exception as e:
        await db.rollback()
        logger.error(f"Unexpected error while creating order: {str(e)}")
        raise HTTPException_AppToolsSZXW(
            error_code=其他_异常代码.未知异常.value,
            detail=f"{str(e)}",
            http_status_code=500
        )


@router.post("/pay/", response_model=返回_支付宝url_支付信息)
async def 发起支付(request: 请求_支付宝url_发起支付, db: AsyncSession = Depends(get_db)):
    # 查询订单 by order_number , 主动查询关联表Product
    order = await db.execute(
        select(Order).options(selectinload(Order.product)).
        filter_by(order_number=request.order_number)
    )
    order = order.scalar_one_or_none()

    if not order:
        raise HTTPException_AppToolsSZXW(
            error_code=订单_异常代码.订单号不存在.value,
            detail="Order not found",
            http_status_code=404
        )

    # 查询支付记录
    payment_query = await db.execute(select(Payment).filter(Payment.transaction_id == order.order_number))
    payment: Payment | None = payment_query.scalar_one_or_none()

    # 如果payment已存在，且上次更新时间在五分钟内，直接返回支付信息
    if payment is None:
        # 发起支付宝支付
        支付链接 = await alipay_client.发起二维码支付(
            商户订单号=order.order_number,
            价格=order.total_amount,
            商品名称=order.product.name)

        # 记录支付信息
        payment = Payment(
            order_id=order.id,
            app_id=order.app_id,
            payment_method=PaymentMethod.ALIPAY_QR,
            amount=order.total_amount,
            transaction_id=order.order_number,
            payment_status=OrderStatus.PENDING.value,
            callback_url=request.callback_url,
            payment_url=支付链接
        )
        db.add(payment)
        await db.commit()
        await db.refresh(payment)
    elif (datetime.now() - payment.updated_at).seconds > 300:
        # 发起支付宝支付
        支付链接 = await alipay_client.发起二维码支付(
            商户订单号=order.order_number,
            价格=order.total_amount,
            商品名称=order.product.name)
        payment.payment_url = 支付链接
        await db.commit()
        await db.refresh(payment)

    # 返回支付信息
    return 返回_支付宝url_支付信息(
        transaction_id=payment.transaction_id,
        payment_status=payment.payment_status,
        amount=payment.amount,
        order_id=payment.order_id,
        app_id=payment.app_id,
        qr_uri=payment.payment_url
    )


@router.get("/payment_status/{transaction_id}", response_model=返回_支付宝url_支付信息)
async def 查询支付状态(transaction_id: str, db: AsyncSession = Depends(get_db)):
    # 查询支付记录
    payment = await db.execute(select(Payment).filter(Payment.transaction_id == transaction_id))
    payment = payment.scalar_one_or_none()

    if not payment:
        raise HTTPException_AppToolsSZXW(
            error_code=支付_异常代码.支付单号不存在.value,
            detail="Payment not found",
            http_status_code=404
        )

    # 检查支付状态
    payment_status = await alipay_client.查询订单(payment.transaction_id)

    if payment_status != payment.payment_status:
        print(f"支付状态更新：{payment.payment_status} -> {payment_status}")
        payment.payment_status = payment_status.value
        await db.commit()

    # to PaymentResponse
    print(f"支付状态：{payment_status.value}{OrderStatus.PAID.value}")
    print(f"支付状态：{payment_status.value == OrderStatus.PAID.value}")

    res = 返回_支付宝url_支付信息(
        transaction_id=payment.transaction_id,
        payment_status=payment.payment_status,
        amount=payment.amount,
        order_id=payment.order_id,
        app_id=payment.app_id,
        qr_uri=payment.payment_url
    )

    return res
