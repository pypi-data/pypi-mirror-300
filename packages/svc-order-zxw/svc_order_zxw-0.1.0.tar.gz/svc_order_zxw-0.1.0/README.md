# 常用函数包

-
    1. 项目根目录下必须包含config.py文件

# 更细说明

- 0.0.4 : 取消对 app-tools-zxw.msvc_order_payments 的依赖
- 0.0.5 : config.py中, 支付宝key配置为路径格式
- 0.0.6 : 新增支付宝二维码支付vue页面示例, config新增自动导入
- 0.0.7 : config自动导入 目录优化
-
- 0.1.0 : 重大更新
    1. 表结构3NF优化,
    2. 增加CRUD层,
    3. 取消schemas, 在CRUD中定义数据模型
    4. 重构interface层,
        - 使用 函数驱动
        - 删除 "通用管理", 用户调用CRUD完成所需操作
    5. 支付宝手机url支付, 完成
    6. 微信支付, 未完成
