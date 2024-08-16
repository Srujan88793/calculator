import tkinter as tk
from tkinter import messagebox
def button_click(value):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current + value)
def clear():
    entry.delete(0, tk.END)
def calculate():
    try:
        expression = entry.get()
        expression = expression.replace('÷', '/')
        expression = expression.replace('×', '*')
        result = eval(expression)
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except Exception as e:
        messagebox.showerror("Error", "Invalid Input")
root = tk.Tk()
root.title("Calculator")
root.geometry("400x500")
root.resizable(False, False)
entry = tk.Entry(root, width=16, font=('Arial', 24), borderwidth=2, relief="solid", justify='right')
entry.grid(row=0, column=0, columnspan=4, pady=10, padx=10)
buttons = [
    ('(', 1, 0), (')', 1, 1), ('%', 1, 2), ('AC', 1, 3),
    ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('÷', 2, 3),
    ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('×', 3, 3),
    ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
    ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('+', 5, 3),
]
for (text, row, column) in buttons:
    if text == '=':
        button = tk.Button(root, text=text, padx=40, pady=20, command=calculate, bg="#4CAF50", fg="white", font=('Arial', 18), activebackground="#45a049")
    elif text == 'AC':
        button = tk.Button(root, text=text, padx=40, pady=20, command=clear, bg="#f44336", fg="white", font=('Arial', 18), activebackground="#e57373")
    else:
        button = tk.Button(root, text=text, padx=40, pady=20, command=lambda t=text: button_click(t), font=('Arial', 18), bg="#E0E0E0", activebackground="#BDBDBD")
    button.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")
for i in range(4):
    root.grid_columnconfigure(i, weight=1)
for i in range(6):
    root.grid_rowconfigure(i, weight=1)
root.mainloop()