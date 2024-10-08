import request from '@/utils/request';

const BASE_URL = 'http://192.168.10.102:8109';
const APP_ID = "AutoJiaoAn";
const PRODUCT_ID = 1; // 商品id, 根据商品表内id而定

interface OrderData {
    user_id: string;
    amount: number;
}

interface PaymentData {
    order_number: string;
    user_id: string;
}


export async function createOrder({user_id, amount}: OrderData): Promise<any> {
    const requestData = {
        user_id,
        amount,
        product_id: PRODUCT_ID,
        callback_url: "",
        app_id: APP_ID
    };

    try {
        return await request({
            url: `${BASE_URL}/alipay/pay_qr/create_order/`,
            method: 'POST',
            data: requestData
        });
    } catch (error: any) {
        throw error;
    }
}

export async function initiatePayment({order_number, user_id}: PaymentData): Promise<any> {
    const requestData = {
        order_number,
        user_id,
        amount: 0,
        product_id: PRODUCT_ID,
        callback_url: "",
        app_id: APP_ID
    };

    try {
        const res = await request({
            url: `${BASE_URL}/alipay/pay_qr/pay/`,
            method: 'POST',
            data: requestData
        });
        console.log("res ========", res);
        return res;
    } catch (error: any) {
        throw error;
    }
}

export async function checkPaymentStatus(transaction_id: string): Promise<any> {
    try {
        return await request({
            url: `${BASE_URL}/alipay/pay_qr/payment_status/${transaction_id}`,
            method: 'GET'
        });
    } catch (error: any) {
        throw error;
    }
}
