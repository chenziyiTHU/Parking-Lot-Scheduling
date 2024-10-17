# 停车场自定义界面
import tkinter as tk
from tkinter import messagebox
from game import ParkingGame

class CustomParkingLot:
    def __init__(self, master: tk.Tk):
        '''
        自定义停车场大小界面

        :param master: Tkinter 根窗口
        '''
        self.master = master
        self.master.title("自定义停车场")

        self.grid_size_frame = tk.Frame(self.master)
        self.grid_size_frame.pack()

        self.label_rows = tk.Label(self.grid_size_frame, text="行数：")
        self.label_rows.pack(side=tk.LEFT)
        self.entry_rows = tk.Entry(self.grid_size_frame, width=5)
        self.entry_rows.pack(side=tk.LEFT)

        self.label_cols = tk.Label(self.grid_size_frame, text="列数：")
        self.label_cols.pack(side=tk.LEFT)
        self.entry_cols = tk.Entry(self.grid_size_frame, width=5)
        self.entry_cols.pack(side=tk.LEFT)

        self.consider_cost_frame = tk.Frame(self.master)
        self.consider_cost_frame.pack()
        
        self.label_consider_cost = tk.Label(self.consider_cost_frame, text="是否按照车辆大小考虑代价：")
        self.label_consider_cost.pack(side=tk.LEFT)
        self.consider_cost = tk.BooleanVar()
        self.consider_cost_button_y = tk.Radiobutton(self.consider_cost_frame, text="是", variable=self.consider_cost, value=True)
        self.consider_cost_button_y.pack()
        self.consider_cost_button_n = tk.Radiobutton(self.consider_cost_frame, text="否", variable=self.consider_cost, value=False)
        self.consider_cost_button_n.pack()

        self.confirm_button = tk.Button(self.master, text="确认", command=self.create_custom_grid)
        self.confirm_button.pack()

    
    def create_custom_grid(self):
        try:
            M = int(self.entry_rows.get())
            N = int(self.entry_cols.get())
            if M <= 1 or N <= 1:
                raise ValueError("网格大小至少为 2x2")
            
            self.consider_cost = self.consider_cost.get()

            self.custom_grid_window = tk.Toplevel(self.master)
            self.custom_grid_window.title("输入停车场车牌号")
            self.grid_entries = [[None for _ in range(N)] for _ in range(M)]
            
            self.grid_frame = tk.Frame(self.custom_grid_window)
            self.grid_frame.pack()

            for i in range(M):
                for j in range(N):
                    entry = tk.Entry(self.grid_frame, width=5)
                    entry.grid(row=i, column=j)
                    self.grid_entries[i][j] = entry

            self.submit_button = tk.Button(self.custom_grid_window, text="提交", command=lambda: self.submit_grid(M, N))
            self.submit_button.pack()

        except ValueError as e:
            messagebox.showerror("错误", f"无效输入: {e}")

    
    def submit_grid(self, M, N):
        try:
            start_state = {}
            has_empty = False
            for i in range(M):
                for j in range(N):
                    car_number = int(self.grid_entries[i][j].get())
                    if car_number == 0:
                        if has_empty:
                            raise ValueError("只能有一个空位！")
                        has_empty = True
                    start_state[car_number] = (i, j)

            if not has_empty:
                raise ValueError("必须指定一个空位！")

            self.master.destroy()
            start_game(M, N, start_state, self.consider_cost)

        except ValueError as e:
            messagebox.showerror("错误", f"输入无效: {e}")

    
def start_game(M, N, start_state, consider_cost):
    game_window = tk.Tk()
    game_window.title("停车场调度游戏开始！")
    game = ParkingGame(game_window, M, N, start_state, consider_cost)
    game_window.mainloop()



if __name__ == "__main__":
    root = tk.Tk()
    custom_parking_lot = CustomParkingLot(root)
    root.mainloop()