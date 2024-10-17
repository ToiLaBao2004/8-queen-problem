import random
import math
import tkinter as tk
from PIL import Image, ImageTk  # Sử dụng Pillow để hiển thị ảnh

# Lớp mô phỏng thuật toán Simulated Annealing
class SimulatedAnnealing:
    def __init__(self, n, max_steps, temperature, cooling_rate):
        self.n = n  # Số lượng quân hậu (ví dụ: 8 quân cho bài toán 8-queens)
        self.max_steps = max_steps  # Số bước tối đa trong quá trình tìm kiếm
        self.temperature = temperature  # Nhiệt độ ban đầu cho quá trình làm mát
        self.cooling_rate = cooling_rate  # Tỷ lệ giảm nhiệt độ (cooling rate)
        self.board = self.random_board()  # Khởi tạo bàn cờ ngẫu nhiên với n quân hậu

    # Hàm khởi tạo bàn cờ ngẫu nhiên
    def random_board(self):
        return [random.randint(0, self.n - 1) for _ in range(self.n)]  # Mỗi quân hậu được đặt ngẫu nhiên trên một hàng

    # Hàm tính số lượng cặp quân hậu tấn công nhau (hàm cost)
    def cost(self, board):
        attacks = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                # Nếu 2 quân hậu nằm trên cùng một hàng hoặc cùng đường chéo thì chúng tấn công nhau
                if board[i] == board[j] or abs(board[i] - board[j]) == j - i:
                    attacks += 1
        return attacks  # Trả về số lượng xung đột

    # Hàm tạo trạng thái lân cận (neighbour) bằng cách thay đổi vị trí của một quân hậu
    def get_neighbour(self, board):
        new_board = board[:]  # Sao chép bàn cờ hiện tại
        row = random.randint(0, self.n - 1)  # Chọn một hàng ngẫu nhiên để di chuyển quân hậu
        new_pos = random.randint(0, self.n - 1)  # Chọn vị trí mới cho quân hậu trong hàng đó
        new_board[row] = new_pos  # Cập nhật vị trí mới cho quân hậu
        return new_board

    # Hàm thực hiện thuật toán Simulated Annealing để giải bài toán
    def anneal(self):
        current_board = self.board  # Bắt đầu với bàn cờ hiện tại
        current_cost = self.cost(current_board)  # Tính số xung đột ban đầu

        for step in range(self.max_steps):
            if current_cost == 0:
                return current_board  # Nếu không có xung đột nào thì trả về bàn cờ

            next_board = self.get_neighbour(current_board)  # Tạo ra trạng thái lân cận
            next_cost = self.cost(next_board)  # Tính chi phí của trạng thái lân cận

            # Nếu trạng thái lân cận tốt hơn hoặc chấp nhận theo xác suất, cập nhật trạng thái hiện tại
            if next_cost < current_cost or random.uniform(0, 1) < math.exp((current_cost - next_cost) / self.temperature):
                current_board = next_board
                current_cost = next_cost

            # Giảm nhiệt độ sau mỗi bước
            self.temperature *= self.cooling_rate

        return current_board  # Trả về bàn cờ sau khi kết thúc quá trình

# Lớp giao diện đồ họa minh họa bài toán 8-queens
class NQueensGUI:
    def __init__(self, n, max_steps, temperature, cooling_rate):
        self.n = n  # Số lượng quân hậu
        self.sa = SimulatedAnnealing(n, max_steps, temperature, cooling_rate)  # Khởi tạo đối tượng Simulated Annealing
        self.window = tk.Tk()  # Tạo cửa sổ chính cho ứng dụng
        self.window.title("8-Queens Solver")  # Đặt tiêu đề cửa sổ

        # Thêm hình ảnh con hậu
        self.queen_image = Image.open("queen.png")  # Ảnh quân hậu
        self.queen_image = self.queen_image.resize((400 // n, 400 // n))  # Điều chỉnh kích thước hình ảnh cho phù hợp với ô bàn cờ
        self.queen_photo = ImageTk.PhotoImage(self.queen_image)  # Chuyển đổi ảnh để hiển thị trong Tkinter

        self.canvas = tk.Canvas(self.window, width=400, height=400)  # Tạo vùng vẽ (canvas) cho bàn cờ
        self.canvas.pack(padx=20, pady=20)  # Hiển thị vùng vẽ và tạo khoảng cách cho bố cục đẹp hơn
        self.cell_size = 400 // n  # Tính toán kích thước mỗi ô vuông

        self.frame = tk.Frame(self.window)  # Tạo khung chứa nút "Solve"
        self.frame.pack(pady=10)

        # Tạo nút "Solve" để bắt đầu giải bài toán
        self.solve_button = tk.Button(self.frame, text="Solve", command=self.solve, font=("Arial", 14), bg="lightblue")
        self.solve_button.pack()

        self.draw_board(self.sa.board)  # Vẽ bàn cờ ban đầu
        self.window.mainloop()  # Bắt đầu vòng lặp chính của giao diện

    # Hàm vẽ bàn cờ và các quân hậu trên canvas
    def draw_board(self, board):
        self.canvas.delete("all")  # Xóa tất cả nội dung cũ trên canvas
        for i in range(self.n):
            for j in range(self.n):
                x1, y1 = i * self.cell_size, j * self.cell_size  # Tính tọa độ góc trên bên trái của ô vuông
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size  # Tính tọa độ góc dưới bên phải của ô vuông

                # Màu sắc ô vuông xen kẽ giữa màu trắng và nâu
                color = "#F0D9B5" if (i + j) % 2 == 0 else "#B58863"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

                # Nếu có quân hậu tại ô đó, vẽ hình ảnh quân hậu
                if board[j] == i:
                    self.canvas.create_image(x1, y1, anchor=tk.NW, image=self.queen_photo)

    # Hàm bắt đầu giải bài toán khi nhấn nút "Solve"
    def solve(self):
        solution = self.sa.anneal()  # Sử dụng Simulated Annealing để tìm lời giải
        self.draw_board(solution)  # Vẽ lại bàn cờ với lời giải

# Thông số cho Simulated Annealing
n = 8  # Số lượng quân hậu
max_steps = 10000  # Số bước tối đa
temperature = 1000  # Nhiệt độ ban đầu
cooling_rate = 0.99  # Tỷ lệ làm lạnh

NQueensGUI(n, max_steps, temperature, cooling_rate)
