import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("간단한 계산기")
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        # 결과 표시창
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        
        self.result_frame = tk.Frame(root, bg="#f0f0f0")
        self.result_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        self.result_display = tk.Entry(
            self.result_frame, 
            textvariable=self.result_var, 
            font=("Arial", 24), 
            bd=5, 
            relief=tk.RIDGE, 
            justify=tk.RIGHT,
            bg="white"
        )
        self.result_display.pack(fill=tk.BOTH, expand=True)

        # 버튼 프레임
        self.buttons_frame = tk.Frame(root, bg="#f0f0f0")
        self.buttons_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 버튼 텍스트
        self.button_texts = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", ".", "=", "+"
        ]
        
        # 계산기 버튼 생성
        self.buttons = {}
        row, col = 0, 0
        
        for text in self.button_texts:
            btn = tk.Button(
                self.buttons_frame,
                text=text,
                font=("Arial", 18),
                bd=3,
                relief=tk.RAISED,
                width=3,
                height=1,
                command=lambda t=text: self.button_click(t)
            )
            if text == "=":
                btn.configure(bg="#ff9966")
            elif text in ["+", "-", "*", "/"]:
                btn.configure(bg="#cccccc")
            else:
                btn.configure(bg="#ffffff")
                
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            self.buttons[text] = btn
            
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        # 추가 버튼: 지우기(C), 뒤로가기(←)
        clear_btn = tk.Button(
            self.buttons_frame,
            text="C",
            font=("Arial", 18),
            bd=3,
            relief=tk.RAISED,
            bg="#ff6666",
            width=3,
            height=1,
            command=self.clear
        )
        clear_btn.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")
        
        backspace_btn = tk.Button(
            self.buttons_frame,
            text="←",
            font=("Arial", 18),
            bd=3,
            relief=tk.RAISED,
            bg="#ffcc99",
            width=3,
            height=1,
            command=self.backspace
        )
        backspace_btn.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")
        
        # 제곱근 버튼
        sqrt_btn = tk.Button(
            self.buttons_frame,
            text="√",
            font=("Arial", 18),
            bd=3,
            relief=tk.RAISED,
            bg="#cccccc",
            width=3,
            height=1,
            command=self.square_root
        )
        sqrt_btn.grid(row=4, column=3, padx=5, pady=5, sticky="nsew")
        
        # 열과 행 크기 설정
        for i in range(5):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.buttons_frame.grid_columnconfigure(i, weight=1)
        
        # 현재 표현식
        self.current_expression = "0"
        self.last_button_was_operator = False
        
    def button_click(self, button_text):
        if button_text == "=":
            self.calculate()
        elif button_text in ["+", "-", "*", "/"]:
            # 연산자가 연속으로 입력되면 마지막 연산자로 대체
            if self.last_button_was_operator:
                self.current_expression = self.current_expression[:-1] + button_text
            else:
                self.current_expression += button_text
                self.last_button_was_operator = True
            self.result_var.set(self.current_expression)
        else:
            if self.current_expression == "0":
                self.current_expression = button_text
            else:
                self.current_expression += button_text
            self.last_button_was_operator = False
            self.result_var.set(self.current_expression)
    
    def calculate(self):
        try:
            self.current_expression = str(eval(self.current_expression))
            self.result_var.set(self.current_expression)
            self.last_button_was_operator = False
        except Exception as e:
            messagebox.showerror("오류", "계산할 수 없는 수식입니다.")
            self.clear()
    
    def clear(self):
        self.current_expression = "0"
        self.result_var.set(self.current_expression)
        self.last_button_was_operator = False
    
    def backspace(self):
        if len(self.current_expression) == 1:
            self.current_expression = "0"
        else:
            self.current_expression = self.current_expression[:-1]
        self.result_var.set(self.current_expression)
        # 마지막 문자가 연산자인지 확인
        if self.current_expression and self.current_expression[-1] in ["+", "-", "*", "/"]:
            self.last_button_was_operator = True
        else:
            self.last_button_was_operator = False
    
    def square_root(self):
        try:
            if float(self.current_expression) < 0:
                messagebox.showerror("오류", "음수의 제곱근은 계산할 수 없습니다.")
                return
            result = float(self.current_expression) ** 0.5
            # 결과가 정수인지 확인
            if result.is_integer():
                self.current_expression = str(int(result))
            else:
                self.current_expression = str(result)
            self.result_var.set(self.current_expression)
        except Exception:
            messagebox.showerror("오류", "계산할 수 없습니다.")

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
