import Node
import Settings
import function
import Grid_point


def one_turn(grid_points, sensor):
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
        print(area)
        outer_area = function.caculate_outer_area(grid_points, active_node, sensor)
        print(outer_area)
        if outer_area >= Settings.alpha * area:
            active_node.sleep()

    for sleeping_node in sleeping_nodes:
        # 计算每个sleeping_node的格点区域
        area = function.caculate_area(grid_points, sleeping_node)
        outer_area = function.caculate_outer_area(grid_points, sleeping_node, sensor)
        if outer_area < Settings.alpha * area:
            sleeping_node.revive()
    function.remove_deadnodes(sensor)


if __name__ == '__main__':
    t = 0
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

    # function.draw(sensor)
    # while function.count_alive_nodes(sensor) != 0:
    #     t = t + 1
    #     if t == Settings.interval:
    function.draw(sensor)
    one_turn(grid_points, sensor)
    function.draw(sensor)

