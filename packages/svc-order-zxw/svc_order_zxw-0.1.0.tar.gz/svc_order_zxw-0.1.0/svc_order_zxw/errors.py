"""
# File       : errors.py
# Time       ：2024/10/7 05:51
# Author     ：xuewei zhang
# Email      ：shuiheyangguang@gmail.com
# version    ：python 3.12
# Description：
"""
from fastapi import HTTPException


class HTTPException_AppToolsSZXW(HTTPException):
    """自定义异常类"""

    def __init__(self, error_code: int,
                 detail: str,
                 http_status_code: int = 404):
        super().__init__(http_status_code,
                         detail={"error_code": error_code,
                                 "detail": detail})


class ErrorCode:
    """错误码"""
    支付宝支付接口调用失败 = 50001
    签名验证失败 = 50002
    商户订单号不能为空或超过32位 = 50003
    价格不能为空或小于0 = 50004
    商品名称不能为空 = 50005
    数据库错误 = 50006
    产品未找到 = 50007
    订单未找到 = 50008
    支付记录未找到 = 50009
    应用未找到 = 50010
