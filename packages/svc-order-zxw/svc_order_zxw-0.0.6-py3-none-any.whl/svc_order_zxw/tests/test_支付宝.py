"""
# File       : test_支付宝.py
# Time       ：2024/8/28 下午10:06
# Author     ：xuewei zhang
# Email      ：shuiheyangguang@gmail.com
# version    ：python 3.12
# Description：
"""
import time

import pytest
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base, Product, Order, Payment, OrderStatus, PaymentMethod

# 数据库连接
DATABASE_URL = "postgresql://my_zxw:my_zxw@localhost:5433/svc_order"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# API基础URL
BASE_URL = "http://127.0.0.1:8102"


@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture(scope="module")
def test_product(db):
    product = Product(name="测试产品", app_id="test_app", price=100.0)
    db.add(product)
    db.commit()
    db.refresh(product)
    yield product
    db.delete(product)
    db.commit()


def test_创建订单(db, test_product):
    """
    1、创建一个订单，信息全新
    2、创建一个订单，信息不全
    3、创建一个订单，信息错误
    4、创建一个订单，信息重复
    5、循环创建50条
    :param db:
    :param test_product:
    :return:
    """
    url = f"{BASE_URL}/alipay/pay_qr/create_order/"
    data = {
        "amount": 100.0,
        "user_id": "test_user",
        "product_id": test_product.id,
        "callback_url": "http://example.com/callback",
        "app_id": "test_app"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["user_id"] == "test_user"
    assert result["total_amount"] == 100.0
    assert result["product_id"] == test_product.id
    assert result["app_id"] == "test_app"
    assert result["status"] == OrderStatus.PENDING.value

    # 验证数据库中的订单
    order = db.query(Order).filter_by(order_number=result["order_number"]).first()
    assert order is not None


def test_创建订单_信息不全(db, test_product):
    url = f"{BASE_URL}/alipay/pay_qr/create_order/"
    data = {
        "amount": 100.0,
        "user_id": "incomplete_user",
        # 缺少 product_id
        "callback_url": "http://example.com/incomplete",
        "app_id": "incomplete_app"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 422  # 预期会返回验证错误


def test_创建订单_信息错误(db, test_product):
    url = f"{BASE_URL}/alipay/pay_qr/create_order/"
    data = {
        "amount": -100.0,  # 负数金额
        "user_id": "error_user",
        "product_id": 99999,  # 不存在的产品ID
        "callback_url": "invalid_url",
        "app_id": "error_app"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 422 or response.status_code == 500  # 预期会返回验证错误或者业务逻辑错误


def test_创建订单_信息重复(db, test_product):
    url = f"{BASE_URL}/alipay/pay_qr/create_order/"
    data = {
        "amount": 100.0,
        "user_id": "duplicate_user",
        "product_id": test_product.id,
        "callback_url": "http://example.com/duplicate",
        "app_id": "duplicate_app"
    }
    # 第一次创建订单
    response1 = requests.post(url, json=data)
    assert response1.status_code == 200

    # 使用完全相同的信息再次创建订单
    response2 = requests.post(url, json=data)
    assert response2.status_code == 200

    # 虽然信息重复，但应该创建了新的订单（订单号不同）
    assert response1.json()["order_number"] != response2.json()["order_number"]


def test_循环创建50条订单(db, test_product):
    url = f"{BASE_URL}/alipay/pay_qr/create_order/"
    base_data = {
        "amount": 100.0,
        "product_id": test_product.id,
        "callback_url": "http://example.com/batch",
        "app_id": "batch_app"
    }

    order_numbers = set()
    for i in range(50):
        data = base_data.copy()
        data["user_id"] = f"batch_user_{i}"
        response = requests.post(url, json=data)
        assert response.status_code == 200
        result = response.json()
        order_numbers.add(result["order_number"])

    # 确保创建了50个不同的订单
    assert len(order_numbers) == 50

    # 验证数据库中的订单数量
    order_count = db.query(Order).filter(Order.app_id == "batch_app").count()
    assert order_count == 50


def test_发起支付(db, test_product):
    # 首先创建一个订单
    order = Order(
        order_number="TEST123456",
        user_id="test_user",
        app_id="test_app",
        total_amount=100.0,
        status=OrderStatus.PENDING,
        product_id=test_product.id
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    url = f"{BASE_URL}/alipay/pay_qr/pay/"
    data = {
        "order_number": order.order_number,
        "user_id": "test_user",
        "product_id": test_product.id,
        "callback_url": "http://example.com/callback",
        "app_id": "test_app"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["transaction_id"] is not None
    print(result["payment_status"], OrderStatus.PENDING.value)
    assert result["payment_status"] == OrderStatus.PENDING.value
    assert result["amount"] == 100.0
    assert result["order_id"] == order.id
    assert result["app_id"] == "test_app"
    assert result["qr_uri"] is not None

    # 验证数据库中的支付记录
    payment = db.query(Payment).filter_by(order_id=order.id).first()
    assert payment is not None


def test_查询支付状态(db, test_product):
    # 创建一个订单和支付记录
    order = Order(
        order_number="TEST78901222",
        user_id="test_user",
        app_id="test_app",
        total_amount=0.01,
        status=OrderStatus.PENDING.value,
        product_id=test_product.id
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    payment = Payment(
        app_id="test_app",
        order_id=order.id,
        payment_method=PaymentMethod.ALIPAY_QR,
        amount=0.01,
        transaction_id=order.order_number,
        payment_status=OrderStatus.PENDING.value
    )
    db.add(payment)
    db.commit()

    # 发起交易
    url = f"{BASE_URL}/alipay/pay_qr/pay/"
    data = {
        "order_number": order.order_number,
        "user_id": "test_user",
        "product_id": test_product.id,
        "callback_url": "http://example.com/callback",
        "app_id": "test_app"
    }
    response = requests.post(url, json=data)
    print("发起交易结果 = ", response.json())

    # 查询交易
    print("查询交易，暂停60秒，等待支付...")
    time.sleep(1)

    url = f"{BASE_URL}/alipay/pay_qr/payment_status/{payment.transaction_id}"
    response = requests.get(url)
    print("test_查询支付状态", response.json())
    assert response.status_code == 200
    result = response.json()
    assert result["transaction_id"] == payment.transaction_id
    assert result["amount"] == payment.amount
    assert result["order_id"] == order.id
    assert result["app_id"] == "test_app"


@pytest.fixture(scope="module")
def cleanup(db):
    yield
    # 清理测试数据
    db.query(Payment).delete()
    db.query(Order).delete()
    db.commit()


def test_清理数据(cleanup):
    # 这个测试用例不做任何事情，只是为了触发cleanup fixture
    pass
