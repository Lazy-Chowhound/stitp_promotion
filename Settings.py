# 仿真有关的参数
import math

# 节点个数
node_count = 2000
# 覆盖区域
area = 300
# 邻近区域系数
a = 0.7
# 电路损耗
Eelec = 5 * 10 ** -9
# 自由空间模型
Efs = 10 ** -11
# 多路衰减模型
Emp = 13 * 10 ** -16

d0 = round(math.sqrt(Efs / Emp))

# 广播数据包大小
broadcast_datapack = 30
# 发送数据包大小
information_databack = 500
