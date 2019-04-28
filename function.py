import Node
import Settings
import math


def find_distance(node1, node2):
    """
    求两节点间的距离
    :param node1:
    :param node2:
    :return: 距离（保留两位小数）
    """
    distance = math.sqrt((node2.x - node1.x) * (node2.x - node1.x) + (node2.y - node1.y) * (node2.y - node1.y))
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
    distance = find_distance(node1, node2)
    scope = Settings.a * node1.PERCEIVED_RADIUS
    if distance <= scope:
        return True
    else:
        return False


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


def get_active_nodes(node, sensor):
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
