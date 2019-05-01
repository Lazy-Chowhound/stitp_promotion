import Node
import Settings
import function
import Grid_point
import copy
import matplotlib.pyplot as pyplot
import matplotlib

# 使matplotlib能正常显示中文
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False


def one_turn_improved(grid_points, sensor):
    """
    每一轮操作
    :param grid_points:
    :param sensor:
    :return:
    """
    active_nodes = function.get_all_active_nodes(sensor)
    sleeping_nodes = function.get_all_sleeping_nodes(sensor)
    for active_node in active_nodes:
        # 计算每个active_node的格点区域
        area = function.caculate_area(grid_points, active_node)
        outer_area = function.caculate_outer_area(grid_points, active_node, sensor)
        if outer_area >= Settings.alpha * area:
            active_node.sleep()

    for sleeping_node in sleeping_nodes:
        # 计算每个sleeping_node的格点区域
        area = function.caculate_area(grid_points, sleeping_node)
        outer_area = function.caculate_outer_area(grid_points, sleeping_node, sensor)
        if outer_area < Settings.alpha * area:
            sleeping_node.revive()

    function.remove_deadnodes(sensor)


def one_turn(sensor):
    sleeping_nodes = function.get_all_sleeping_nodes(sensor)
    for node in sleeping_nodes:
        active_nodes = function.get_close_active_nodes(node, sensor)
        # 没有处于活跃状态的节点
        if len(active_nodes) == 0:
            node.revive()

    function.remove_deadnodes(sensor)


if __name__ == '__main__':
    # 格点列表
    grid_points = []
    for i in range(Settings.area):
        for j in range(Settings.area):
            grid_point = Grid_point.grid_point(i, j)
            grid_points.append(grid_point)
    # 节点列表
    sensor = []
    for i in range(Settings.node_count):
        node = Node.Node()
        node.set_scope(Settings.area)
        node.random_position()
        node.choose_sleep()
        sensor.append(node)

    # 存活时间
    sensor2 = copy.deepcopy(sensor)
    t = 0
    x = []
    y = []
    z = []
    x2 = []
    y2 = []
    z2 = []
    while function.count_alive_nodes(sensor) != 0:
        x.append(t)
        y.append(function.count_alive_nodes(sensor))
        z.append(function.get_coverage(grid_points, sensor))
        function.consume_energy_per_second(sensor)
        t = t + 1
        if t % Settings.interval == 0:
            one_turn_improved(grid_points, sensor)
        if t == 700:
            break

    t = 0
    while function.count_alive_nodes(sensor2) != 0:
        x2.append(t)
        y2.append(function.count_alive_nodes(sensor2))
        z2.append(function.get_coverage(grid_points, sensor2))
        function.consume_energy_per_second(sensor2)
        t = t + 1
        if t % Settings.interval == 0:
            one_turn(sensor2)
        if t == 700:
            break

    line, = pyplot.plot(x, y, linewidth=2)
    line2, = pyplot.plot(x2, y2, linewidth=2)
    legend = pyplot.legend([line, line2], ['原有的算法', '改进的算法'], loc='upper right')
    pyplot.xlabel("时间")
    pyplot.ylabel("生存节点数")
    pyplot.show()

    z.sort(reverse=True)
    z2.sort(reverse=True)
    line3, = pyplot.plot(x, z, linewidth=2)
    line4, = pyplot.plot(x2, z2, linewidth=2)
    legend = pyplot.legend([line3, line4], ['原有的算法', '改进的算法'], loc='upper right')
    pyplot.xlabel("时间")
    pyplot.ylabel("覆盖率")
    pyplot.show()
