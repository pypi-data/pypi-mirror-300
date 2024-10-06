"""
# File       : api_商品管理.py
# Time       ：2024/8/28 上午5:42
# Author     ：xuewei zhang
# Email      ：shuiheyangguang@gmail.com
# version    ：python 3.12
# Description：
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from svc_order_zxw.db.models import get_db
from svc_order_zxw.db import models as db_models

from svc_order_zxw.apis.schemas_通用管理 import *
from svc_order_zxw.apis.异常管理 import 商品_异常代码, 订单_异常代码, 支付_异常代码, 其他_异常代码

from app_tools_zxw.Funcs.生成订单号 import 生成订单号
from app_tools_zxw.Errors.api_errors import HTTPException_AppToolsSZXW

router = APIRouter(prefix="", tags=["商品管理"])


@router.post("/products", response_model=返回_创建产品)
async def 创建产品(product: 请求_创建产品, db: AsyncSession = Depends(get_db)):
    try:
        db_product = db_models.Product(**product.model_dump())
        db.add(db_product)
        await db.commit()
        return 返回_创建产品(**db_product.to_dict())
    except IntegrityError:
        await db.rollback()
        raise HTTPException_AppToolsSZXW(商品_异常代码.商品已存在.value, "产品名称已存在", 400)
    except Exception as e:
        await db.rollback()
        raise HTTPException_AppToolsSZXW(其他_异常代码.未知错误.value, f"发生错误: {str(e)}", 500)


@router.put("/products/{product_id}", response_model=返回_更新产品)
async def 更新产品(product_id: int, product: 请求_更新产品, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        db_product = await db.get(db_models.Product, product_id)
        if db_product is None:
            raise HTTPException_AppToolsSZXW(商品_异常代码.商品不存在.value, "未找到产品", 404)

        update_data = product.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)

        try:
            await db.commit()
            return 返回_更新产品.model_validate(db_product)
        except IntegrityError:
            await db.rollback()
            raise HTTPException_AppToolsSZXW(商品_异常代码.商品已存在.value, "更新违反唯一约束", 400)
        except Exception as e:
            await db.rollback()
            raise HTTPException_AppToolsSZXW(其他_异常代码.未知错误.value, f"发生错误: {str(e)}", 500)


@router.get("/products/{product_id}", response_model=返回_获取产品)
async def 获取产品(product_id: int, db: AsyncSession = Depends(get_db)):
    product: db_models.Product | None = await db.get(db_models.Product, product_id)
    if product is None:
        raise HTTPException_AppToolsSZXW(商品_异常代码.商品不存在.value, "未找到产品", 404)
    return 返回_获取产品(**product.to_dict())


@router.get("/products", response_model=返回_获取所有产品)
async def 获取所有产品(db: AsyncSession = Depends(get_db)):
    async with db.begin():
        result = await db.execute(select(db_models.Product))
        products = result.scalars().all()
        return 返回_获取所有产品(products=[返回_获取产品(**product.to_dict()) for product in products])


@router.post("/orders", response_model=返回_创建订单)
async def 创建订单(order: 请求_创建订单, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        product = await db.get(db_models.Product, order.product_id)
        if not product:
            raise HTTPException_AppToolsSZXW(商品_异常代码.商品不存在.value, "未找到产品", 404)

        if order.total_amount != product.price:
            raise HTTPException_AppToolsSZXW(订单_异常代码.订单金额错误.value, "订单总金额与产品价格不符", 400)

        db_order = db_models.Order(
            order_number=生成订单号(),
            **order.dict()
        )
        db.add(db_order)
        try:
            await db.commit()
            return 返回_创建订单(**db_order.__dict__)
        except IntegrityError:
            await db.rollback()
            raise HTTPException_AppToolsSZXW(订单_异常代码.订单号已存在.value, "该订单号已存在", 400)
        except Exception as e:
            await db.rollback()
            raise HTTPException_AppToolsSZXW(其他_异常代码.未知错误.value, f"发生错误: {str(e)}", 500)


@router.put("/orders/{order_id}/status", response_model=返回_更新订单状态)
async def 更新订单状态(order_id: int, status_update: 请求_更新订单状态, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        try:
            result = await db.execute(select(db_models.Order).filter(db_models.Order.id == order_id))
            db_order = result.scalars().first()
            if db_order is None:
                raise HTTPException_AppToolsSZXW(订单_异常代码.订单号不存在.value, "订单不存在", 404)

            db_order.status = status_update.status
            db_order.updated_at = datetime.utcnow()

            await db.commit()

            return 返回_更新订单状态(
                id=db_order.id,
                order_number=db_order.order_number,
                status=db_order.status,
                updated_at=db_order.updated_at
            )
        except Exception as e:
            await db.rollback()
            raise HTTPException_AppToolsSZXW(其他_异常代码.未知错误.value, f"发生错误: {str(e)}", 500)


@router.get("/orders/{order_id}", response_model=返回_获取订单)
async def 获取订单(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await db.get(db_models.Order, order_id)
    if order is None:
        raise HTTPException_AppToolsSZXW(订单_异常代码.订单号不存在.value, "未找到订单", 404)
    return 返回_获取订单(**order.to_dict())


@router.get("/orders", response_model=返回_获取所有订单)
async def 获取所有订单(db: AsyncSession = Depends(get_db)):
    async with db.begin():
        result = await db.execute(select(db_models.Order))
        orders = result.scalars().all()
        order_list = []
        for order in orders:
            tmp = 返回_获取订单(**order.to_dict())
            order_list.append(tmp)
        return 返回_获取所有订单(orders=order_list)


@router.post("/payments", response_model=返回_创建支付)
async def 创建支付(payment: 请求_创建支付, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        order = await db.get(db_models.Order, payment.order_id)
        if not order:
            raise HTTPException_AppToolsSZXW(订单_异常代码.订单号不存在.value, "未找到订单", 404)

        if payment.amount != order.total_amount:
            raise HTTPException_AppToolsSZXW(支付_异常代码.支付单金额错误.value, "支付金额与订单总额不符", 400)

        db_payment = db_models.Payment(**payment.dict())
        db.add(db_payment)
        try:
            await db.commit()
            return 返回_创建支付(**db_payment.to_dict())
        except IntegrityError:
            await db.rollback()
            raise HTTPException_AppToolsSZXW(支付_异常代码.支付单号已存在.value, "该交易ID已存在", 400)
        except Exception as e:
            await db.rollback()
            raise HTTPException_AppToolsSZXW(其他_异常代码.未知错误.value, f"发生错误: {str(e)}", 500)


@router.get("/payments/{payment_id}", response_model=返回_获取支付)
async def 获取支付(payment_id: int, db: AsyncSession = Depends(get_db)):
    payment = await db.get(db_models.Payment, payment_id)
    if payment is None:
        raise HTTPException_AppToolsSZXW(支付_异常代码.支付单号不存在.value, "未找到支付记录", 404)
    return 返回_获取支付(**payment.to_dict())


@router.get("/payments", response_model=返回_获取所有支付)
async def 获取所有支付(db: AsyncSession = Depends(get_db)):
    async with db.begin():
        result = await db.execute(select(db_models.Payment))
        payments = result.scalars().all()
        return 返回_获取所有支付(payments=[返回_获取支付(**payment.to_dict()) for payment in payments])
