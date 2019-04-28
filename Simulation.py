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
    for active_node in active_nodes:
        area = function.caculate_area(grid_ponts, active_node, sensor)


if __name__ == '__main__':
    # 格点列表
    grid_points = []
    for i in range(1000):
        grid_point = grid_point.grid_point()

