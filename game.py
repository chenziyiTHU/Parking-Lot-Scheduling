# 停车场调度游戏主界面
import tkinter as tk
from tkinter import messagebox
from main import ParkingLot, list_to_dict

class ParkingGame(ParkingLot):
    def __init__(self, master: tk, M, N, start_state: dict, consider_cost=False):
        """
        初始化游戏界面

        :param master: Tkinter 根窗口
        :param M: 行数
        :param N: 列数
        :param start_state: 初始停车场状态，字典 {车牌号: (x, y)}
        """
        super().__init__(start_state, M, N, consider_cost)
        self.master = master
        self.current_state = start_state.copy()
        self.total_cost = 0  
        self.buttons = {}

        if self.check_solvable():
            self.create_grid_play()
            self.create_cost_label()
        else:
            messagebox.showerror("无解", "该停车场状态无解！")
            self.master.destroy()

    
    def create_grid_play(self):
        '''创建停车场的按钮网格'''
        self.grid_frame = tk.Frame(self.master)
        self.grid_frame.pack(side=tk.LEFT)
        for i in range(self.M):
            for j in range(self.N):
                car_number = self.get_car_at(self.current_state, i, j)
                button_text = " " if car_number == 0 else str(car_number)
                button = tk.Button(self.grid_frame, text=button_text, width=6, height=3, command=lambda x=i, y=j: self.click_button(x, y), font=("Arial", 20))
                button.grid(row=i, column=j)
                self.buttons[(i, j)] = button


    def click_button(self, x, y):
        '''
        按钮点击事件处理

        :param x: 行索引
        :param y: 列索引
        '''
        clicked_car = self.get_car_at(self.current_state, x, y)
        if self.is_adjacent_empty(x, y):
            self.current_state[clicked_car] = self.current_state[0]
            self.current_state[0] = (x, y)
            self.update_grid()
            self.update_cost(self.cost[clicked_car])
            if self.is_goal(self.current_state):
                messagebox.showinfo("恭喜", f"你赢了！你的总代价为{self.total_cost}")
        else:
            messagebox.showwarning("无法移动", "请选择空位旁边的车！")
    
    def is_adjacent_empty(self, x, y):
        '''
        判断(x, y)是否在空位的邻接位置

        :param x: 行索引
        :param y: 列索引
        '''
        for i, j in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = x + i, y + j
            if 0 <= new_x < self.M and 0 <= new_y < self.N and self.get_car_at(self.current_state, new_x, new_y) == 0:
                return True
        return False
    

    def update_grid(self):
        '''更新按钮网格显示'''
        for (x, y), button in self.buttons.items():
            car_num = self.get_car_at(self.current_state, x, y)
            button_text = " " if car_num == 0 else str(car_num)
            button.config(text=button_text)

    
    def create_cost_label(self):
        '''在按钮右侧创建规则和代价显示标签'''
        self.cost_frame = tk.Frame(self.master)
        self.cost_frame.pack(side=tk.RIGHT, padx=20)
        rule_text = "规则：每一步代价为车牌号在由小到大排列中的顺序" if self.consider_cost else "规则：每一步代价为1"
        self.rule_label = tk.Label(self.cost_frame, text=rule_text, font=("Arial", 16))
        self.rule_label.pack(pady=20)
        self.cost_label = tk.Label(self.cost_frame, text=f"当前代价：{self.total_cost}", font=("Arial", 16))
        self.cost_label.pack()
        self.answer_button = tk.Button(self.cost_frame, text="查看答案", command=self.show_answer, font=("Arial", 16))
        self.answer_button.pack(pady=20)
        self.answer_button = tk.Button(self.cost_frame, text="退出游戏", command=self.exit, font=("Arial", 16))
        self.answer_button.pack()
    

    def update_cost(self, cost):
        '''每次移动后更新代价'''
        self.total_cost += cost
        self.cost_label.config(text=f"当前代价：{self.total_cost}")


    def show_answer(self):
        '''显示答案窗口'''
        self.answer_cost, self.path_state, self.path_car = self.a_star()

        self.answer_window = tk.Toplevel(self.master)
        self.answer_window.title("答案")

        self.step_label = tk.Label(self.answer_window, text="初始状态如下：", font=("Arial", 16))
        self.step_label.pack(pady=20)

        self.grid_frame_answer = tk.Frame(self.answer_window)
        self.grid_frame_answer.pack()
        self.labels_answer = {}
        for i in range(self.M):
            for j in range(self.N):
                car_number = self.get_car_at(self.start_state, i, j)
                label_text = " " if car_number == 0 else str(car_number)
                label = tk.Label(self.grid_frame_answer, text=label_text, width=6, height=3, font=("Arial", 20))
                label.grid(row=i, column=j)
                self.labels_answer[(i, j)] = label
        
        self.current_step = 0
        self.current_cost = 0
        self.next_step_button = tk.Button(self.answer_window, text="下一步", command=self.next_step, font=("Arial", 16))
        self.next_step_button.pack(pady=20)

    
    def next_step(self):
        '''显示答案的下一步'''
        if self.current_step < len(self.path_state):
            self.current_answer_state = self.path_state[self.current_step]
            self.current_cost += self.cost[self.path_car[self.current_step]]
            self.step_label.config(text=f"当前步数：{self.current_step + 1}/{len(self.path_state)}，移动车辆{self.path_car[self.current_step]}，\n当前代价：{self.current_cost}/{self.answer_cost}")
            self.current_step += 1
            self.update_grid_answer()
        else:
            messagebox.showinfo("完成", "已到达目标状态！")
            self.answer_window.destroy()

    
    def update_grid_answer(self):
        '''更新答案的网格显示'''
        for (x, y), label in self.labels_answer.items():
            car_num = self.get_car_at(dict(self.current_answer_state), x, y)
            label_text = " " if car_num == 0 else str(car_num)
            label.config(text=label_text)

    
    def exit(self):
        '''退出游戏'''
        self.master.destroy()


    
if __name__ == "__main__":
    start_state = [[1, 4, 2],
                   [7, 6, 3],
                   [8, 0, 5]]
    
    start_state = list_to_dict(start_state)

    M, N = 3, 3

    root = tk.Tk()
    root.title("停车场游戏")
    game = ParkingGame(root, M, N, start_state, True)
    
    root.mainloop()