class HumanCustomerService:
    def __init__(self):
        pass

    def handle_transfer(self, customer_id, question, order_info):
        """
        处理转接人工客服的请求
        :param customer_id: 客户 ID
        :param question: 客户问题
        :param order_info: 客户订单信息
        :return: 转接结果信息
        """
        print(f"【转接人工客服】客户 ID: {customer_id}")
        print(f"订单信息: {order_info}")
        print(f"客户问题: {question}")
        print("人工客服已接手服务。")
        return {
            "status": "success",
            "message": f"客户 {customer_id} 的问题已成功转接给人工客服",
            "order_info": order_info
        }


def main():
    customer = HumanCustomerService()
    order_info = [{'客户 ID': '2', '客户姓名': '李四', '购买产品': '产品B', '订单日期': '2024/2/2'}]
    info = customer.handle_transfer(customer_id=1,question="产品怎么使用",order_info=order_info)
    print(info)


if __name__ == '__main__':
    main()