"""
# File       : schemes.py
# Time       ：2024/8/28 上午12:55
# Author     ：xuewei zhang
# Email      ：shuiheyangguang@gmail.com
# version    ：python 3.12
# Description：
"""
from typing import Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field
from svc_order_zxw.apis.schemas_payments import PaymentMethod, OrderStatus


class 请求_微信url_创建订单(BaseModel):
    user_id: str = Field(..., description="用户ID")
    product_id: int = Field(..., description="产品ID")
    app_id: str = Field(..., description="应用ID")


# 创建订单的响应模型
class 返回_微信url_创建订单(BaseModel):
    order_number: str = Field(..., description="订单号")
    total_amount: float = Field(..., description="订单总金额")
    status: OrderStatus = Field(..., description="订单状态")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")


# 发起支付的请求模型
class 请求_微信url_发起支付(BaseModel):
    order_number: str = Field(..., description="订单号")
    payment_method: PaymentMethod = Field(..., description="支付方式")
    callback_url: Optional[str] = Field(None, description="回调URL")


# 发起支付的响应模型
class 返回_微信url_发起支付(BaseModel):
    payment_url: str = Field(..., description="支付链接")
    transaction_id: str = Field(..., description="交易ID")
    payment_method: PaymentMethod = Field(..., description="支付方式")
    amount: float = Field(..., description="支付金额")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")


class 返回_微信url_订单状态(BaseModel):
    order_number: str
    status: OrderStatus


##################################################



