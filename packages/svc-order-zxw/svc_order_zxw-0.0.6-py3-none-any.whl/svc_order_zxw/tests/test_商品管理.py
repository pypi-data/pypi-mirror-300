import pytest
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Product, Order, Payment, Base, OrderStatus, PaymentMethod

# 数据库连接设置
DATABASE_URL = "postgresql://my_zxw:my_zxw@localhost:5433/svc_order"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# API基础URL
BASE_URL = "http://127.0.0.1:8102"


@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="module")
def cleanup_db(db_session):
    yield
    # 清理测试数据
    db_session.query(Payment).delete()
    db_session.query(Order).delete()
    db_session.query(Product).delete()
    db_session.commit()


def test_创建产品(db_session, cleanup_db):
    # 创建产品
    product_data = {
        "name": "测试产品",
        "app_id": "test_app",
        "price": 99.99
    }
    response = requests.post(f"{BASE_URL}/products", json=product_data)
    assert response.status_code == 200
    product = response.json()
    assert product["name"] == product_data["name"]
    assert product["app_id"] == product_data["app_id"]
    assert product["price"] == product_data["price"]

    # 验证数据库中的产品
    db_product = db_session.query(Product).filter_by(id=product["id"]).first()
    assert db_product is not None
    assert db_product.name == product_data["name"]


def test_获取所有产品(db_session):
    response = requests.get(f"{BASE_URL}/products")
    assert response.status_code == 200
    products = response.json()["products"]
    assert len(products) > 0


def test_创建订单(db_session):
    # 获取第一个产品的ID
    products = requests.get(f"{BASE_URL}/products").json()["products"]
    product_id = products[0]["id"]

    order_data = {
        "user_id": "test_user",
        "app_id": "test_app",
        "total_amount": 99.99,
        "product_id": product_id
    }
    response = requests.post(f"{BASE_URL}/orders", json=order_data)
    print("test_创建订单", response.json())
    assert response.status_code == 200
    order = response.json()
    assert order["user_id"] == order_data["user_id"]
    assert order["total_amount"] == order_data["total_amount"]

    # 验证数据库中的订单
    db_order = db_session.query(Order).filter_by(id=order["id"]).first()
    assert db_order is not None
    assert db_order.user_id == order_data["user_id"]


def test_获取所有订单(db_session):
    response = requests.get(f"{BASE_URL}/orders")
    assert response.status_code == 200
    orders = response.json()["orders"]
    assert len(orders) > 0


def test_更新订单状态(db_session):
    # 获取第一个订单的ID
    orders = requests.get(f"{BASE_URL}/orders").json()["orders"]
    order_id = orders[0]["id"]

    new_status = {"status": OrderStatus.PAID.value}
    response = requests.put(f"{BASE_URL}/orders/{order_id}/status", json=new_status)
    assert response.status_code == 200
    updated_order = response.json()
    assert updated_order["status"] == OrderStatus.PAID.value

    # 验证数据库中的订单状态
    db_order = db_session.query(Order).filter_by(id=order_id).first()
    assert db_order.status == OrderStatus.PAID


def test_创建支付(db_session):
    # 获取第一个订单的ID
    orders = requests.get(f"{BASE_URL}/orders").json()["orders"]
    order_id = orders[0]["id"]

    payment_data = {
        "app_id": "test_app",
        "order_id": order_id,
        "payment_method": PaymentMethod.WECHAT_H5.value,
        "amount": 99.99,
        "transaction_id": "test_transaction",
        "payment_status": "success"
    }
    response = requests.post(f"{BASE_URL}/payments", json=payment_data)
    assert response.status_code == 200
    payment = response.json()
    assert payment["order_id"] == payment_data["order_id"]
    assert payment["amount"] == payment_data["amount"]

    # 验证数据库中的支付记录
    db_payment = db_session.query(Payment).filter_by(id=payment["id"]).first()
    assert db_payment is not None
    assert db_payment.transaction_id == payment_data["transaction_id"]

    # 验证订单状态
    ...


def test_获取所有支付(db_session):
    response = requests.get(f"{BASE_URL}/payments")
    assert response.status_code == 200
    payments = response.json()["payments"]
    assert len(payments) > 0


def test_获取单个支付(db_session):
    # 获取第一个支付记录的ID
    payments = requests.get(f"{BASE_URL}/payments").json()["payments"]
    payment_id = payments[0]["id"]

    response = requests.get(f"{BASE_URL}/payments/{payment_id}")
    assert response.status_code == 200
    payment = response.json()
    assert payment["id"] == payment_id
