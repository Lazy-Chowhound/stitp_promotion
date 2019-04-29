import Settings
import math


def get_grid_sensor_distance(grid_point, node):
    """
    求格点与某个传感器间的距离
    :param grid_point:
    :param node:
    :return:
    """
    distance = math.sqrt((grid_point.x - node.x) ** 2 + (grid_point.y - node.y) ** 2)
    return distance


def get_sensor_distance(node1, node2):
    """
    求两传感器间的距离
    :param node1:
    :param node2:
    :return: 距离（保留两位小数）
    """
    distance = math.sqrt((node2.x - node1.x) ** 2 + (node2.y - node1.y) ** 2)
    # 发送广播数据包请求距离
    node1.send_datapack(Settings.broadcast_datapack, distance)
    node2.receive_databack(Settings.broadcast_datapack)
    # 发送距离数据包
    node2.send_datapack(Settings.information_databack, distance)
    node2.send_datapack(Settings.information_databack, distance)
    return round(distance, 2)


def judge_close(node1, node2):
    """
    判断node2是否在node1的邻近区域
    :param node1:
    :param node2:
    :return:
    """
    distance = get_sensor_distance(node1, node2)
    scope = Settings.a * node1.PERCEIVED_RADIUS
    if distance <= scope:
        return True
    else:
        return False


def get_all_sleeping_nodes(sensor):
    """
    获取当前所有处于休眠中的节点
    :param sensor:
    :return:节点列表
    """
    sleep_nodes = []
    for node in sensor:
        if node.is_alive and node.is_asleep:
            sleep_nodes.append(node)
    return sleep_nodes


def get_all_active_nodes(sensor):
    """
    获取所有处于活跃状态的结点
    :param sensor:
    :return:
    """
    all_active_nodes = []
    for node in sensor:
        if node.is_alive and not node.is_asleep:
            all_active_nodes.append(node)
    return all_active_nodes


def get_close_nodes(node, sensor):
    """
    获取节点邻近区域内的所有节点
    :param node:
    :param sensor:
    :return: 节点列表
    """
    node_list = []
    for node2 in sensor:
        if judge_close(node, node2):
            node_list.append(node2)
    return node_list


def get_close_active_nodes(node, sensor):
    """
    获取某个节点邻近区域内所有处于活跃状态的结点
    :param node:
    :param sensor:
    :return:节点列表
    """
    active_node_list = get_close_nodes(node, sensor)
    for node in active_node_list:
        if node.is_asleep:
            active_node_list.remove(node)
    return active_node_list


def judge_in_two_circles(grid_point, node1, node2):
    """
    判断某个格点是否在两个传感器感知范围
    :param grid_point:
    :param node1:
    :param node2:
    :return:
    """
    distance1 = get_grid_sensor_distance(grid_point, node1)
    distance2 = get_grid_sensor_distance(grid_point, node2)
    if distance1 < node1.PERCEIVED_RADIUS and distance2 < node2.PERCEIVED_RADIUS:
        return True
    else:
        return False


def get_grid_points_in_node(grid_points, node):
    """
    获取某个节点内的格点数（格点系数i）
    :param grid_points:
    :param node:
    :return:
    """
    num = 0
    for grid_point in grid_points:
        if get_grid_sensor_distance(grid_point, node) < node.PERCEIVED_RADIUS:
            num += 1
    return num


def get_grid_points_on_node_border(grid_points, node):
    """
    获取某个节点边界上的格点数（格点系数j）
    :param grid_points:
    :param node:
    :return:
    """
    num = 0
    for grid_point in grid_points:
        if get_grid_sensor_distance(grid_point, node) == node.PERCEIVED_RADIUS:
            num += 1
    return num


def get_points_in_two_nodes(grid_points, node1, node2):
    """
    获取两个传感器节点内的所有格点（格点系数i）
    :param grid_points:
    :param node1:
    :param node2:
    :return:
    """
    num = 0
    for grid_point in grid_points:
        if judge_in_two_circles(grid_point, node1, node2):
            num += 1
    return num


def judge_on_two_nodes_border(grid_point, node1, node2):
    """
    判断某个格点是否在两个传感器感知半径上
    :param grid_point:
    :param node1:
    :param node2:
    :return:
    """
    distance1 = get_grid_sensor_distance(grid_point, node1)
    distance2 = get_grid_sensor_distance(grid_point, node2)
    if distance1 == node1.PERCEIVED_RADIUS or distance2 == node2.PERCEIVED_RADIUS:
        return True
    else:
        return False


def get_points_on_two_node_border(grid_points, node1, node2):
    """
    获取两个传感器节点上的所有格点（格点系数j）
    :param grid_points:
    :param node1:
    :param node2:
    :return:
    """
    num = 0
    for grid_point in grid_points:
        if judge_on_two_nodes_border(grid_point, node1, node2):
            num += 1
    return num


def get_total_in_grid_points(grid_points, node, sensor):
    """
    获取某个节点邻近区域内所有感知范围内的格点（外围格点系数i）
    :param grid_points:
    :param node:
    :param sensor:
    :return:
    """
    num = 0
    close_nodes = get_close_active_nodes(node, sensor)
    for close_node in close_nodes:
        num += get_points_in_two_nodes(grid_points, node, close_node)
    return num


def get_total_on_grid_points(grid_points, node, sensor):
    """
    获取某个节点邻近区域内所有感知范围上的格点（外围格点系数j）
    :param grid_points:
    :param node:
    :param sensor:
    :return:
    """
    num = 0
    close_nodes = get_close_active_nodes(node, sensor)
    for close_node in close_nodes:
        num += get_points_on_two_node_border(grid_points, node, close_node)
    return num


def caculate_area(grid_points, node):
    """
    计算节点的格点区域
    :param grid_points:
    :param node:
    :return:
    """
    i = get_grid_points_in_node(grid_points, node)
    j = get_grid_points_on_node_border(grid_points, node)
    if i == 0:
        area = (math.sqrt(i) + 1) ** 2 / 2
    else:
        area = (j + 1) / 2
    return area


def caculate_outer_area(grid_points, node, sensor):
    """
    计算传感器外围格点区域
    :param grid_points:
    :param node:
    :param sensor:
    :return:
    """
    i = get_total_in_grid_points(grid_points, node, sensor)
    j = get_total_on_grid_points(grid_points, node, sensor)
    if i == 0:
        area = (math.sqrt(i) + 1) ** 2 / 2
    else:
        area = (j + 1) / 2
    return area
