import tkinter as tk
from tkinter import messagebox
import math

# daftar fungsi matematika yang aman digunakan
allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
allowed_names.update({
    "ln": math.log,
    "log": math.log10,
    "√": math.sqrt,
    "pi": math.pi,
    "π": math.pi,
    "e": math.e,
    "abs": abs,
    "pow": pow,
    "sin": lambda x: math.sin(math.radians(x)),
    "cos": lambda x: math.cos(math.radians(x)),
    "tan": lambda x: math.tan(math.radians(x)),
})

def safe_eval(expr):
    expr = expr.replace("^", "**").replace("x", "*").replace("÷", "/")
    expr = expr.replace("π", "pi").replace("√", "sqrt")
    try:
        return eval(expr, {"__builtins__": None}, allowed_names)
    except Exception:
        raise

class SciCalc:
    def __init__(self, root):
        self.root = root
        root.title("Scientific Calculator")
        root.resizable(False, False)
        root.configure(bg="#2b2b2b")

        self.expr = ""
        self.ans = ""

        # layar input
        self.display = tk.Entry(
            root, font=("Consolas", 20, "bold"), bd=0, bg="#3c3f41",
            fg="#ffffff", insertbackground="white", justify="right", relief="sunken"
        )
        self.display.grid(row=0, column=0, columnspan=6, padx=10, pady=10, sticky="we")

        # daftar tombol
        btn_def = [
            ("7",1,0), ("8",1,1), ("9",1,2), ("÷",1,3), ("√",1,4), ("C",1,5),
            ("4",2,0), ("5",2,1), ("6",2,2), ("x",2,3), ("^",2,4), ("⌫",2,5),
            ("1",3,0), ("2",3,1), ("3",3,2), ("-",3,3), ("(",3,4), (")",3,5),
            ("0",4,0), (".",4,1), ("±",4,2), ("+",4,3), ("back",4,4), ("=",4,5),
            ("sin",5,0), ("cos",5,1), ("tan",5,2), ("ln",5,3), ("log",5,4), ("π",5,5),
            ("e",6,0), ("pow",6,1), ("abs",6,2), ("%",6,3)
        ]

        for (text, r, c) in btn_def:
            cmd = lambda x=text: self.on_button(x)
            if text == "=":
                bg, fg = "#0008FF", "white"
            elif text in ("C", "⌫"):
                bg, fg = "#f44336", "white"
            elif text in ("÷", "x", "-", "+", "^", "%"):
                bg, fg = "#FFE600", "#000000"
            else:
                bg, fg = "#4a4a4a", "#ffffff"

            tk.Button(
                root, text=text, width=6, height=2, font=("Consolas", 14, "bold"),
                bg=bg, fg=fg, relief="raised",
                activebackground="#FFD700", activeforeground="black",
                command=cmd
            ).grid(row=r, column=c, padx=4, pady=4)

    def on_button(self, label):
        if label == "C":
            self.expr = ""
        elif label == "⌫":
            self.expr = self.expr[:-1]
        elif label == "=":
            self.calculate()
            return
        elif label == "±":
            self.toggle_sign()
            return
        elif label == "Ans":
            self.expr += str(self.ans)
        elif label == "√":
            self.expr += "√("
        elif label in ("sin","cos","tan","ln","log","abs","pow"):
            self.expr += f"{label}("
        elif label in ("π", "pi"):
            self.expr += str(math.pi)
        elif label == "e":
            self.expr += "e"
        elif label == "%":
            self.expr += "/100"
        else:
            self.expr += label
        self.update_display()

    def toggle_sign(self):
        s = self.expr.rstrip()
        if not s:
            self.expr = "-"
        else:
            i = len(s)-1
            while i >= 0 and (s[i].isdigit() or s[i] == '.' or s[i].isalpha()):
                i -= 1
            token = s[i+1:]
            before = s[:i+1]
            if before.endswith("(-"):
                before = before[:-2] + "("
                self.expr = before + token
            else:
                self.expr = before + "(-" + token + ")"
        self.update_display()

    def update_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expr)

    def calculate(self):
        try:
            result = safe_eval(self.expr)
            if isinstance(result, float):
                result = round(result, 12)
                if float(result).is_integer():
                    result = int(result)
            self.ans = result
            self.expr = str(result)
            self.update_display()
        except Exception:
            messagebox.showerror("Error", "Input tidak valid")
            self.expr = ""
            self.update_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = SciCalc(root)
    root.mainloop()
