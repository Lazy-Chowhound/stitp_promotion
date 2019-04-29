import Node
import Settings
import function
import grid_point
import numpy as np
import matplotlib.pyplot as plt

# 类似于界面大小
x = y = np.arange(-5, 5, 0.1)
x, y = np.meshgrid(x, y)
plt.contour(x, y, x ** 2 + y ** 2, [9])

plt.axis('scaled')
plt.show()


def one_turn(grid_ponts, sensor):
    """
    每一轮操作
    :param grid_ponts:
    :param sensor:
    :return:
    """
    active_nodes = function.get_all_active_nodes(sensor)
    sleeping_nodes = function.get_all_sleeping_nodes(sensor)
    for active_node in active_nodes:
        # 计算每个active_node的格点区域
        area = function.caculate_area(grid_ponts, active_node)
        outer_area = function.caculate_outer_area(grid_points, active_node, sensor)
        if outer_area >= Settings.alpha * area:
            active_node.sleep()
            active_node.is_changed = True
    for sleeping_node in sleeping_nodes:
        # 计算每个active_node的格点区域
        area = function.caculate_area(grid_ponts, sleeping_node)
        outer_area = function.caculate_outer_area(grid_points, sleeping_node, sensor)
        if outer_area < Settings.alpha * area:
            sleeping_node.revive()
            sleeping_node.is_changed = True


if __name__ == '__main__':
    # 格点列表
    grid_points = []
    for i in range(Settings.area ** 2):
        grid_point = grid_point.grid_point()
    sensor = []
    for i in range(Settings.node_count):
        node = Node.Node()
        node.set_scope(Settings.area)
        node.random_position()
        sensor.append()