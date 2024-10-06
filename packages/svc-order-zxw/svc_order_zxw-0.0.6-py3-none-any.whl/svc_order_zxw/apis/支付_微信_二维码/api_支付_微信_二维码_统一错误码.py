"""
# File       : api_wechat_h5_pay.py
# Time       ：2024/8/24 08:40
# Author     ：xuewei zhang
# Email      ：shuiheyangguang@gmail.com
# version    ：python 3.12
# Description：
# Prompt:
下面是已经定义好的的表结构文件内容，使用fastapi异步框架，创建一个微信支付服务，能健壮的满足如下功能：
1、前端网页发起支付请求，并支付的全部流程；
2、订单与支付状态记录；
3、对多个app通用（此功能如果需要修改表结构，请修改）。
4、接口的输入输出规定出明确格式
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from svc_order_zxw.config import WeChatPay
from svc_order_zxw.apis.异常管理 import 订单_异常代码, 商品_异常代码, 支付_异常代码, 其他_异常代码
from svc_order_zxw.db.models import Payment, Order, Product, get_db
from svc_order_zxw.apis.schemas_payments import PaymentMethod, OrderStatus
from svc_order_zxw.apis.schemas_微信支付宝支付 import (
    返回_微信url_订单状态, 请求_微信url_创建订单,
    返回_微信url_创建订单, 请求_微信url_发起支付,
    返回_微信url_发起支付)

from app_tools_zxw.SDK_微信.SDK_微信支付v2.支付服务_二维码 import 支付服务_二维码等
from app_tools_zxw.Errors.api_errors import HTTPException_AppToolsSZXW

router = APIRouter(prefix="/wechat/pay_h5", tags=["微信二维码支付"])


#
# class 请求_微信url_创建订单(BaseModel):
#     user_id: str = Field(..., description="用户ID")
#     product_id: int = Field(..., description="产品ID")
#     app_id: str = Field(..., description="应用ID")
#
#
# class 返回_微信url_创建订单(BaseModel):
#     order_number: str = Field(..., description="订单号")
#     total_amount: float = Field(..., description="订单总金额")
#     status: OrderStatus = Field(..., description="订单状态")
#     created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
#
#
# class 请求_微信url_发起支付(BaseModel):
#     order_number: str = Field(..., description="订单号")
#     payment_method: PaymentMethod = Field(..., description="支付方式")
#     callback_url: Optional[str] = Field(None, description="回调URL")
#
#
# class 返回_微信url_发起支付(BaseModel):
#     payment_url: str = Field(..., description="支付链接")
#     transaction_id: str = Field(..., description="交易ID")
#     payment_method: PaymentMethod = Field(..., description="支付方式")
#     amount: float = Field(..., description="支付金额")
#     created_at: datetime = Field(default_factory=datetime.now, description="创建时间")


@router.post("/create_order/", response_model=返回_微信url_创建订单)
async def 创建订单(order_request: 请求_微信url_创建订单, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        try:
            result = await db.execute(select(Product).where(Product.id == order_request.product_id))
            product = result.scalars().first()

            if not product:
                raise HTTPException_AppToolsSZXW(
                    error_code=商品_异常代码.商品不存在.value,
                    detail="Product not found",
                    http_status_code=404
                )

            order_number = 支付服务_二维码等.生成订单号()
            order = Order(
                order_number=order_number,
                app_id=product.app_id,
                user_id=order_request.user_id,
                total_amount=product.price,
                status=OrderStatus.PENDING,
                product_id=product.id
            )
            db.add(order)
            await db.commit()

            return 返回_微信url_创建订单(
                order_number=order_number,
                total_amount=product.price,
                status=OrderStatus.PENDING
            )

        except Exception as e:
            await db.rollback()
            raise HTTPException_AppToolsSZXW(
                error_code=其他_异常代码.未知错误.value,
                detail=f"Order creation failed: {str(e)}",
                http_status_code=500
            )


@router.post("/initiate_payment/", response_model=返回_微信url_发起支付)
async def 发起支付(
        payment_request: 请求_微信url_发起支付,
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    async with db.begin():
        try:
            result = await db.execute(select(Order).where(Order.order_number == payment_request.order_number))
            order = result.scalars().first()

            if not order:
                raise HTTPException_AppToolsSZXW(
                    error_code=订单_异常代码.订单号不存在.value,
                    detail="Order not found",
                    http_status_code=404
                )

            if order.status != OrderStatus.PENDING:
                raise HTTPException_AppToolsSZXW(
                    error_code=订单_异常代码.订单状态错误.value,
                    detail="Order is not in pending status",
                    http_status_code=400
                )

            payment = Payment(
                order_id=order.id,
                app_id=order.app_id,
                payment_method=payment_request.payment_method,
                amount=order.total_amount,
                transaction_id=order.order_number,
                payment_status="pending",
                callback_url=WeChatPay.PAYMENT_NOTIFY_URL_二维码 if payment_request.callback_url is None else payment_request.callback_url
            )
            db.add(payment)
            await db.flush()

            product = await db.get(Product, order.product_id)

            pay = 支付服务_二维码等(WeChatPay.APP_ID, WeChatPay.MCH_ID)
            支付链接 = await pay.生成支付链接(
                payment_request.payment_method,
                payment.transaction_id,
                order.total_amount,
                payment.callback_url,
                request.client.host,
                product.name
            )
            await db.commit()
            return 返回_微信url_发起支付(
                payment_url=支付链接,
                transaction_id=payment.transaction_id,
                payment_method=payment_request.payment_method,
                amount=order.total_amount
            )

        except Exception as e:
            await db.rollback()
            raise HTTPException_AppToolsSZXW(
                error_code=其他_异常代码.未知错误.value,
                detail=f"Payment initiation failed: {str(e)}",
                http_status_code=500
            )


@router.get("/order_status/{order_number}", response_model=返回_微信url_订单状态)
async def get_order_status(order_number: str, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        result = await db.execute(select(Order).where(Order.order_number == order_number))
        order = result.scalars().first()

        if not order:
            raise HTTPException_AppToolsSZXW(
                error_code=订单_异常代码.订单号不存在.value,
                detail="Order not found",
                http_status_code=404
            )

    return 返回_微信url_订单状态(order_number=order_number, status=order.status)


class PaymentCallbackRequest(BaseModel):
    transaction_id: str
    status: str


@router.post("/payment_callback/")
async def payment_callback(callback: PaymentCallbackRequest, db: AsyncSession = Depends(get_db)):
    try:
        async with db.begin():
            result = await db.execute(select(Payment).where(Payment.transaction_id == callback.transaction_id))
            payment = result.scalars().first()

            if not payment:
                raise HTTPException_AppToolsSZXW(
                    error_code=支付_异常代码.支付单号不存在.value,
                    detail="Payment not found",
                    http_status_code=404
                )

            payment.payment_status = callback.status
            await db.flush()

            if callback.status == "success":
                payment.order.status = OrderStatus.PAID
            else:
                payment.order.status = OrderStatus.FAILED

            await db.commit()

    except Exception as e:
        await db.rollback()
        raise HTTPException_AppToolsSZXW(
            error_code=其他_异常代码.未知错误.value,
            detail=f"Payment callback failed: {str(e)}",
            http_status_code=500
        )
