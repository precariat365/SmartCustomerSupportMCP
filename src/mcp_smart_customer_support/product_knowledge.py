

class ProductKnowledgeBase:
    def __init__(self):
        # 初始化产品知识库
        self.knowledge = {
            "产品A": {
                "特点": "高性能、低能耗",
                "使用问题": "开机后按电源键，选择对应功能；若无法启动，请检查电源线连接",
                "售后流程": "拨打400-1234，提供订单号即可申请退换货"
            },
            "产品B": {
                "特点": "轻便、易携带",
                "使用问题": "打开设备后，通过蓝牙搜索‘设备B’即可连接",
                "售后流程": "登录官网，在‘我的订单’中提交售后申请"
            }
        }

    def get_product_info(self, product_name):
        """
        根据产品名称获取产品信息
        :param product_name: 产品名称
        :return: 产品信息字典，如果产品不存在则返回 None
        """
        return self.knowledge.get(product_name)

    def get_all_product_info(self):
        """
        根据产品名称获取产品信息
        :param product_name: 产品名称
        :return: 产品信息字典，如果产品不存在则返回 None
        """
        return self.knowledge


def main():
    knowledge =  ProductKnowledgeBase()
    info = knowledge.get_product_info("产品A")
    print(info)


if __name__ == '__main__':
    main()