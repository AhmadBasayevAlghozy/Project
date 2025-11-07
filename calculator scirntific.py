import tkinter as tk #gui
from tkinter import messagebox 
import math #fungsi matematika

# fungsi evaluasi aman
allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
allowed_names.update({
    "ln": math.log,
    "log": math.log10,
    "sqrt": math.sqrt, #akar dari x
    "pi": math.pi,
    "e": math.e, #nilai konstanta eluler
    "abs": abs, #mengembalikan nilai abslut
    "pow": pow #pangkat dari x
})

def safe_eval(expr):
    expr = expr.replace("^", "**")
    try:
        return eval(expr, {"__builtins__": None}, allowed_names)
    except Exception:
        raise

class SciCalc: #gui ddari kalkulator
    def __init__(self, root):
        self.root = root
        root.title("Scientific Calculator")
        root.resizable(False, False)
        root.configure(bg="#2b2b2b")

        self.expr = "" #input atau perintah dari pengguna
        self.ans = "" #output dari sistem

        # Tampilan layar
        self.display = tk.Entry(
            root, font=("Consolas", 20, "bold"), bd=0, bg="#3c3f41",
            fg="#ffffff", insertbackground="white", justify="right", relief="flat"
        )
        self.display.grid(row=0, column=0, columnspan=6, padx=10, pady=10, sticky="we")

        # Daftar tombol
        btn_def = [
            ("7",1,0), ("8",1,1), ("9",1,2), ("/",1,3), ("sqrt",1,4), ("C",1,5),
            ("4",2,0), ("5",2,1), ("6",2,2), ("*",2,3), ("^",2,4), ("⌫",2,5),
            ("1",3,0), ("2",3,1), ("3",3,2), ("-",3,3), ("(",3,4), (")",3,5),
            ("0",4,0), (".",4,1), ("±",4,2), ("+",4,3), ("Ans",4,4), ("=",4,5),
            ("sin",5,0), ("cos",5,1), ("tan",5,2), ("ln",5,3), ("log",5,4), ("pi",5,5),
            ("e",6,0), ("pow",6,1), ("abs",6,2), ("%",6,3)
        ]

        for (text, r, c) in btn_def:
            cmd = lambda x=text: self.on_button(x)

            # Warna tombol
            if text == "=":
                bg = "#4CAF50"
                fg = "white"
            elif text in ("C", "⌫"):
                bg = "#f44336"
                fg = "white"
            elif text in ("/", "*", "-", "+", "^", "%"):
                bg = "#6A5ACD"
                fg = "white"
            else:
                bg = "#4a4a4a"
                fg = "#ffffff"

            b = tk.Button(
                root, text=text, width=6, height=2, font=("Consolas", 14, "bold"),
                bg=bg, fg=fg, relief="flat", activebackground="#666", activeforeground="white",
                command=cmd
            )
            b.grid(row=r, column=c, padx=4, pady=4)

    def on_button(self, label):
        if label == "C":
            self.expr = ""
            self.update_display()
            return
        if label == "⌫":
            self.expr = self.expr[:-1]
            self.update_display()
            return
        if label == "=":
            self.calculate()
            return
        if label == "±":
            self.toggle_sign()
            return
        if label == "Ans": #memasukkan hasil perhitungan sebelumnya
            self.expr += str(self.ans)
            self.update_display()
            return
        if label == "sqrt":
            self.expr += "sqrt("
            self.update_display()
            return
        if label in ("sin","cos","tan","ln","log","abs","pow"):
            self.expr += f"{label}("
            self.update_display()
            return
        if label == "pi":
            self.expr += "pi"
            self.update_display()
            return
        if label == "e":
            self.expr += "e"
            self.update_display()
            return
        if label == "%":
            self.expr += "/100"
            self.update_display()
            return
        self.expr += label
        self.update_display()

    def toggle_sign(self): #menguah positif ke negatif pada angka terakhir yang diketik
        s = self.expr.rstrip()
        if not s:
            self.expr = "-"
            self.update_display()
            return
        i = len(s)-1
        while i >=0 and (s[i].isdigit() or s[i] == '.' or s[i].isalpha()):
            i -= 1
        token = s[i+1:]
        if not token:
            self.expr = "-" + s
            self.update_display()
            return
        before = s[:i+1]
        if before.endswith("(-"):
            before = before[:-2] + "("
            self.expr = before + token
        else:
            self.expr = before + "(-" + token + ")"
        self.update_display()

    def update_display(self): #menampilkan setiap perubahan pada kalkulator
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expr)

    def calculate(self):
        try:
            result = safe_eval(self.expr)
            if isinstance(result, float):
                result = round(result, 12) #hasil dibulatkan 12 digit agar rapi
                if float(result).is_integer(): #jika hasil bulat tidak ditampilkan ke desimal
                    result = int(result)
            self.ans = result #data disimpan di ans agar dapat dipakai lagi
            self.expr = str(result)
            self.update_display()
        except Exception:
            messagebox.showerror("Error", "Ekspresi tidak valid")
            self.expr = ""
            self.update_display()

if __name__ == "__main__":
    root = tk.Tk() #jendela utama
    app = SciCalc(root) #objek kalkulator
    root.mainloop() #menjaga GUI tetap berjalan hingga ditutup penguuna


#otak atik tampilan layar
    #relief = tsmpilsn bidang input 
        #biasa diganti dengan "raised", "sunken", "groove","ridge"
    