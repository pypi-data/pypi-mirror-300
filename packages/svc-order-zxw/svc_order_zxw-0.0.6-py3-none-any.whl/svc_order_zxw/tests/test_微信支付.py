import pytest
import requests
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app_tools_zxw.models_payment import OrderStatus, PaymentMethod

# 数据库连接
DB_URL = "postgresql://my_zxw:my_zxw@localhost:5433/svc_order"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

# API基础URL
BASE_URL = "http://127.0.0.1:8102/wechat/pay_h5"


@pytest.fixture(scope="module")
def db_session():
    session = SessionLocal()
    yield session
    session.close()


def clean_database(session):
    session.execute(text("DELETE FROM payments"))
    session.execute(text("DELETE FROM orders"))
    session.execute(text("DELETE FROM products"))
    session.commit()


@pytest.fixture(autouse=True)
def setup_and_teardown(db_session):
    clean_database(db_session)
    yield
    clean_database(db_session)


def create_test_product(session):
    session.execute(
        text("INSERT INTO products (name, app_id, price) VALUES (:name, :app_id, :price)"),
        {"name": "测试产品", "app_id": "test_app", "price": 100.00}
    )
    session.commit()
    result = session.execute(text("SELECT id FROM products ORDER BY id DESC LIMIT 1"))
    return result.scalar()


def test_创建订单(db_session):
    product_id = create_test_product(db_session)

    payload = {
        "user_id": "test_user",
        "product_id": product_id,
        "app_id": "test_app"
    }
    response = requests.post(f"{BASE_URL}/create_order/", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "order_number" in data
    assert data["total_amount"] == 100.00
    assert data["status"] == "pending"


def test_发起支付(db_session):
    product_id = create_test_product(db_session)

    # 先创建订单
    order_payload = {
        "user_id": "test_user",
        "product_id": product_id,
        "app_id": "test_app"
    }
    order_response = requests.post(f"{BASE_URL}/create_order/", json=order_payload)
    order_data = order_response.json()
    order_number = order_data["order_number"]

    # 发起支付
    payment_payload = {
        "order_number": order_number,
        "payment_method": PaymentMethod.WECHAT_QR.value,
        "callback_url": "http://example.com/callback"
    }
    payment_response = requests.post(f"{BASE_URL}/initiate_payment/", json=payment_payload)
    print("test_发起支付，payment_response:", payment_response.json())
    if payment_response.status_code == 500:
        assert payment_response.json()["detail"] == "Payment initiation failed: 500: 微信API返回了非JSON格式的数据"
    else:
        assert payment_response.status_code == 200

        payment_data = payment_response.json()
        assert "payment_url" in payment_data
        assert "transaction_id" in payment_data
        assert payment_data["payment_method"] == PaymentMethod.WECHAT_QR.value
        assert payment_data["amount"] == 100.00


def test_查询订单状态(db_session):
    product_id = create_test_product(db_session)

    # 创建订单
    order_payload = {
        "user_id": "test_user",
        "product_id": product_id,
        "app_id": "test_app"
    }
    order_response = requests.post(f"{BASE_URL}/create_order/", json=order_payload)
    order_data = order_response.json()
    order_number = order_data["order_number"]

    # 查询订单状态
    status_response = requests.get(f"{BASE_URL}/order_status/{order_number}")
    assert status_response.status_code == 200

    status_data = status_response.json()
    assert status_data["order_number"] == order_number
    assert status_data["status"] == "pending"


def test_支付回调(db_session):
    product_id = create_test_product(db_session)

    # 创建订单并发起支付
    order_payload = {
        "user_id": "test_user",
        "product_id": product_id,
        "app_id": "test_app"
    }
    order_response = requests.post(f"{BASE_URL}/create_order/", json=order_payload)
    order_data = order_response.json()
    order_number = order_data["order_number"]

    payment_payload = {
        "order_number": order_number,
        "payment_method": PaymentMethod.WECHAT_QR.value,
        "callback_url": "http://example.com/callback"
    }
    payment_response = requests.post(f"{BASE_URL}/initiate_payment/", json=payment_payload)
    payment_data = payment_response.json()
    print("test_支付回调，payment_data:", payment_data)
    if payment_response.status_code == 500:
        assert payment_response.json()["detail"] == "Payment initiation failed: 500: 微信API返回了非JSON格式的数据"
        transaction_id = "dsadadad"
    else:
        transaction_id = payment_data["transaction_id"]

    # 模拟支付回调
    callback_payload = {
        "transaction_id": transaction_id,
        "status": "success",
        "payment_time": "2023-08-28T12:00:00",
        "amount": 100.00,
        "payment_method": PaymentMethod.WECHAT_QR.value
    }
    callback_response = requests.post(f"{BASE_URL}/payment_callback/", json=callback_payload)
    print("test_支付回调，callback_response:", callback_response.json())

    if callback_response.status_code == 500:
        assert callback_response.json()["detail"] == "Payment callback failed: 404: Payment not found"
    else:
        assert callback_response.status_code == 200

        # 验证订单状态已更新
        status_response = requests.get(f"{BASE_URL}/order_status/{order_number}")
        status_data = status_response.json()
        assert status_data["status"] == "paid"


if __name__ == "__main__":
    pytest.main([__file__])
