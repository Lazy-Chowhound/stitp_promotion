import random
import Settings


class Node():
    """
        传感器节点类
    """

    def __init__(self):
        # 部署范围
        self.scope = 0
        # 通信半径
        self.TRANSMISSION_RANGE = 30
        # 感知半径
        self.PERCEIVED_RADIUS = 10
        # x,y坐标
        self.x = 0
        self.y = 0
        # 节点能量
        self.energy = 3
        # 节点是否处于休眠状态
        self.is_asleep = True
        # 节点改变状态 0代表未改变 1代表这一轮改变
        self.is_changed = 0
        # 节点是否存活
        self.is_alive = True

    # 设置部署范围
    def set_scope(self, scope):
        self.scope = scope

    # 随机部署到区域里
    def random_position(self):
        self.x = random.randint(0, self.scope)
        self.y = random.randint(0, self.scope)

    def choose_sleep(self):
        """
        判断节点是休眠还是苏醒
        :return:
        """
        coef = random.randint(1, 10)
        # 节点苏醒
        if coef <= 5:
            self.revive()
        # 节点休眠
        elif coef > 5:
            self.sleep()

    # 节点休眠
    def sleep(self):
        self.is_asleep = True

    # 节点苏醒
    def revive(self):
        self.is_asleep = False

    def send_datapack(self, size, distance):
        """
        发送时节点消耗的能量
        :param size: 数据包大小
        :param distance: 距离
        :return:
        """
        if distance < Settings.d0:
            sending_energy = Settings.Eelec * size + size * Settings.Efs * distance ** 2
        else:
            sending_energy = Settings.Eelec * size + size * Settings.Emp * distance ** 4
        self.energy -= sending_energy
        if self.energy <= 0:
            self.is_alive = False

    def receive_datapack(self, size):
        """
        接收时消耗的能量
        :param size: 数据包大小
        :return:
        """
        receving_energy = Settings.Eelec * size
        self.energy -= receving_energy
        if self.energy <= 0:
            self.is_alive = False
