import csv


class OrderOperations:

    def __init__(self):
        self.orders = [
            {'客户ID': '1', '客户姓名': '张三', '购买产品': '产品A', '订单日期': '2024/1/1'},
            {'客户ID': '2', '客户姓名': '李四', '购买产品': '产品B', '订单日期': '2024/2/2'}
        ]

    def get_customer_orders(self, customer_id):
        """
        根据客户 ID 获取客户的订单信息
        :param customer_id: 客户 ID
        :return: 订单信息列表，如果没有订单则返回空列表
        """
        order = []
        for row in self.orders:
            if row['客户ID'] == str(customer_id):
                order.append(row)
        return order


def main():
    result = OrderOperations().get_customer_orders(1)
    print(result)


if __name__ == '__main__':
    main()
