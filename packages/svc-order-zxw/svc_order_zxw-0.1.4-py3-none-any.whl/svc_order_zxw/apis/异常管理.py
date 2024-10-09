"""
# File       : 异常管理.py
# Time       ：2024/8/29 上午8:19
# Author     ：xuewei zhang
# Email      ：shuiheyangguang@gmail.com
# version    ：python 3.12
# Description：
"""
from enum import Enum


class 其他_异常代码(int, Enum):
    未知错误 = 9999
    未知异常 = 9998
    未知错误_请联系管理员 = 9997


class 订单_异常代码(int, Enum):
    订单号不存在 = 1001
    订单号已存在 = 1002
    订单状态错误 = 1003
    订单金额错误 = 1004
    订单支付失败 = 1005
    订单退款失败 = 1006
    订单查询失败 = 1007
    订单支付中 = 1008
    订单退款中 = 1009


class 商品_异常代码(int, Enum):
    商品不存在 = 1101
    商品已存在 = 1102
    商品状态错误 = 1103
    商品数量错误 = 1104
    商品价格错误 = 1105
    商品库存不足 = 1106


class 支付_异常代码(int, Enum):
    支付单号已存在 = 2001
    支付单号不存在 = 2002
    支付单状态错误 = 2003
    支付单金额错误 = 2004
