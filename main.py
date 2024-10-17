# 停车场调度算法
import heapq

def manhattan_distance(a, b):
    '''计算两点之间的曼哈顿距离'''
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class ParkingLot:
    def __init__(self, start_state: dict, M, N, consider_cost=False):
        '''
        初始化停车场问题

        :param start_state: 初始状态的字典 {车牌号: (x, y)}，其中 0 表示空位
        :param goal_state: 目标状态的字典 {车牌号: (x, y)}
        :param M: 停车场的行数
        :param N: 停车场的列数
        '''
        self.start_state = start_state
        self.car_numbers = list(start_state.keys())
        self.sorted_car_numbers = sorted(self.car_numbers)
        self.M = M
        self.N = N
        self.consider_cost = consider_cost
        self.empty_pos = start_state[0]
        self.goal_state = self.generate_goal_state()
        self.cost = self.generate_cost()


    def generate_goal_state(self):
        '''
        根据停车场的大小动态生成目标状态，车牌号从小到大，最后一个空位为 0
        
        :return: 目标状态的字典 {车牌号: (x, y)}
        '''
        goal_state = {}
        num = 1
        for i in range(self.M):
            for j in range(self.N):
                if i == self.M - 1 and j == self.N - 1:
                    goal_state[0] = (i, j)  
                else:
                    goal_state[self.sorted_car_numbers[num]] = (i, j)
                    num += 1
        return goal_state
    

    def generate_cost(self):
        '''
        生成每个车辆每一步的移动代价

        :return: 代价字典 {车牌号: 代价}
        '''
        cost = {}
        if self.consider_cost:
            for i, car in enumerate(self.sorted_car_numbers):
                cost[car] = i
            return cost
        else:
            for car in self.car_numbers:
                cost[car] = 1
            return cost
    

    def is_goal(self, state):
        '''
        检查当前状态是否为目标状态

        :param state: 当前状态的字典 {车牌号: (x, y)}
        :return: 布尔值，是否为目标状态
        '''
        return state == self.goal_state
    

    def heuristic(self, state: dict):
        '''计算当前状态到目标状态的启发函数值，即曼哈顿距离
        
        :param state: 当前状态的字典 {车牌号: (x, y)}
        :return: 曼哈顿距离
        '''
        distance = 0
        for car, (x,y) in state.items():
            if car != 0:
                distance += manhattan_distance((x,y), self.goal_state[car])
        return distance


    def get_next_states(self, state: dict):
        '''
        获取下一步的所有可能状态

        :param state: 当前状态的字典 {车牌号: (x, y)}
        :return: 所有可能的下一个状态列表
        '''
        x, y = state[0] 
        next_states_costs = []
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for move in moves:
            new_x, new_y = x + move[0], y + move[1]
            if 0 <= new_x < self.M and 0 <= new_y < self.N: 
                # 空车位和新坐标上的车交换位置
                new_state = state.copy()
                for car, pos in state.items():
                    if pos == (new_x, new_y):
                        new_state[car] = (x, y)  # 车移动到原空位
                        new_state[0] = (new_x, new_y)  # 空位移动到车的原位置
                        cost = self.cost[car]  # 代价为车牌号
                        break
                next_states_costs.append((new_state, cost, car))
        return next_states_costs
    
    
    def a_star(self):
        '''
        A* 搜索算法，找到从初始状态到目标状态的最佳路径
        
        :return: 最短路径的步数以及最佳路径的状态列表
        '''
        pq = [] 
        heapq.heappush(pq, (0, tuple(self.start_state.items()), 0, [], []))  # （优先级，当前状态（转化为tuple），步数，完整状态路径，每一步移动车牌路径）
        visited = set()
        visited.add(frozenset(self.start_state.items()))

        while pq:
            _, current_state_tuple, g, path_state, path_car = heapq.heappop(pq)
            current_state = dict(current_state_tuple)

            if self.is_goal(current_state):
                return g, path_state, path_car

            next_states = self.get_next_states(current_state)
            for next_state_dict, cost, car in next_states:
                next_g = g + cost
                next_h = cost * self.heuristic(next_state_dict)
                next_f = next_g + next_h
                state_frozenset = frozenset(next_state_dict.items())

                if state_frozenset not in visited:
                    visited.add(state_frozenset)
                    next_state_tuple = tuple(next_state_dict.items())
                    heapq.heappush(pq, (next_f, next_state_tuple, next_g, path_state + [next_state_tuple], path_car + [car]))

        return None, None, None
    

    def visualize(self, state):
        '''
        可视化当前停车场状态

        :param state: 当前状态的字典 {车牌号: (x, y)}
        :return: 打印当前状态的停车场布局
        '''
        grid = [['' for _ in range(self.N)] for _ in range(self.M)]
        for car, (x, y) in state.items():
            if car == 0:
                grid[x][y] = '  '
            else:
                grid[x][y] = f'{car:2}' 

        for row in grid:
            print(' | '.join(row))
        print('-' * (self.N * 4 - 1))

    
    def check_solvable(self):
        '''
        检查初始状态是否可解

        :return: 是否可解
        '''
        inversions = 0
        flat_list = []
        empty_row = 0

        for i in range(self.M):
            for j in range(self.N):
                car = self.get_car_at(self.start_state, i, j)
                if car == 0:
                    empty_row = i
                else:
                    flat_list.append(car)

        # 计算逆序数
        inversions = 0
        for i in range(len(flat_list)):
            for j in range(i + 1, len(flat_list)):
                if flat_list[i] > flat_list[j]:
                    inversions += 1

        if self.M % 2 == 1:
            return inversions % 2 == 0
        else:
            return (inversions + empty_row) % 2 == 1
        

    def get_car_at(self, state, x, y):
        '''
        获取状态下(x, y)坐标上的车牌号

        :param x: 行索引
        :param y: 列索引
        '''
        for car, pos in state.items():
            if pos == (x, y):
                return car
        return None



def list_to_dict(lst):
    '''
    将列表转化为字典
    
    :param lst: 列表每个元素为对应行的车牌号构成的列表
    '''
    state = {}
    for i in range(len(lst)):
        for j in range(len(lst[0])):
            state[lst[i][j]] = (i, j)
    return state
        


if __name__ == "__main__":
    # start_state_list = [[1, 4, 2],
    #                     [7, 6, 3],
    #                     [8, 0, 5]]
    
    # start_state = list_to_dict(start_state_list)
    # M, N = len(start_state_list), len(start_state_list[0])

    consider_cost = input("是否按照车牌号大小顺序考虑代价？（y/n）")
    consider_cost = True if consider_cost == 'y' else False

    M = int(input("请输入停车场的行数："))
    N = int(input("请输入停车场的列数："))
    start_state_list = []

    for i in range(M):
        row = input(f"请输入第{i + 1}行的车牌号，用空格分隔（空车位请用“0”代替）：")
        start_state_list.append(list(map(int, row.split())))
        while len(start_state_list[i]) != N:
            print(f"输入的列数不等于停车场的列数{N}，请重新输入！")
            row = input(f"请输入第{i + 1}行的车牌号，用空格分隔（空车位请用“0”代替）：")
            start_state_list[i] = list(map(int, row.split()))

    start_state = list_to_dict(start_state_list)

    puzzle = ParkingLot(start_state, M, N, consider_cost)

    print("初始状态:")
    puzzle.visualize(start_state)

    if puzzle.check_solvable():
        total_cost, path_state, path_car = puzzle.a_star()
        print(f"总代价: {total_cost}")
        for i, step in enumerate(path_state):
            print(f"第{i+1}步：移动车辆{path_car[i]}")
            puzzle.visualize(dict(step))
    else:
        print("该问题无解！")