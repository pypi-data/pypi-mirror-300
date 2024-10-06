"""
# File       : 创建表.py
# Time       ：2024/8/28 下午6:40
# Author     ：xuewei zhang
# Email      ：shuiheyangguang@gmail.com
# version    ：python 3.12
# Description：
"""


def create_tables():
    return """
    -- Create enum types
    CREATE TYPE order_status AS ENUM ('PENDING', 'PAID', 'CANCELED', 'REFUNDED');
    CREATE TYPE payment_method AS ENUM ('ALIPAY', 'WECHAT', 'STRIPE');

    -- Create products table
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name VARCHAR NOT NULL,
        app_id VARCHAR,
        price FLOAT NOT NULL
    );
    CREATE INDEX idx_products_app_id ON products(app_id);

    -- Create orders table
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        order_number VARCHAR UNIQUE,
        user_id VARCHAR,
        app_id VARCHAR,
        total_amount FLOAT NOT NULL,
        status order_status DEFAULT 'PENDING',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        product_id INTEGER REFERENCES products(id)
    );
    CREATE INDEX idx_orders_order_number ON orders(order_number);
    CREATE INDEX idx_orders_user_id ON orders(user_id);
    CREATE INDEX idx_orders_app_id ON orders(app_id);

    -- Create payments table
    CREATE TABLE IF NOT EXISTS payments (
        id SERIAL PRIMARY KEY,
        app_id VARCHAR,
        order_id INTEGER REFERENCES orders(id),
        payment_method payment_method NOT NULL,
        amount FLOAT NOT NULL,
        transaction_id VARCHAR UNIQUE,
        payment_status VARCHAR,
        callback_url VARCHAR,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX idx_payments_app_id ON payments(app_id);

    -- Create trigger for updating 'updated_at' columns
    CREATE OR REPLACE FUNCTION update_modified_column()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = CURRENT_TIMESTAMP;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER update_orders_modtime
        BEFORE UPDATE ON orders
        FOR EACH ROW
        EXECUTE FUNCTION update_modified_column();

    CREATE TRIGGER update_payments_modtime
        BEFORE UPDATE ON payments
        FOR EACH ROW
        EXECUTE FUNCTION update_modified_column();
    """
