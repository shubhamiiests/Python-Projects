import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# Functions to manage tasks
def add_task():
    task = task_var.get()
    deadline = deadline_var.get()
    if task and deadline:
        try:
            datetime.strptime(deadline, '%Y-%m-%d')
            task_list.insert('', 'end', values=(task, deadline))
            task_var.set('')
            deadline_var.set('')
        except ValueError:
            messagebox.showerror("Input Error", "Deadline must be in YYYY-MM-DD format")
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")

def update_task():
    selected_item = task_list.selection()
    if selected_item:
        task_list.item(selected_item, values=(task_var.get(), deadline_var.get()))
        task_var.set('')
        deadline_var.set('')
    else:
        messagebox.showwarning("Selection Error", "Please select a task to update")

def delete_task():
    selected_item = task_list.selection()
    if selected_item:
        task_list.delete(selected_item)
    else:
        messagebox.showwarning("Selection Error", "Please select a task to delete")

def select_task(event):
    selected_item = task_list.selection()
    if selected_item:
        task, deadline = task_list.item(selected_item, 'values')
        task_var.set(task)
        deadline_var.set(deadline)

# GUI setup
root = tk.Tk()
root.title("To-Do List Application")
root.geometry("600x400")
root.configure(bg="#f0f8ff")

# Task form
form_frame = tk.Frame(root, bg="#f0f8ff")
form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

tk.Label(form_frame, text="Task", bg="#f0f8ff").grid(row=0, column=0, padx=5, pady=5)
task_var = tk.StringVar()
tk.Entry(form_frame, textvariable=task_var).grid(row=0, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Deadline (YYYY-MM-DD)", bg="#f0f8ff").grid(row=1, column=0, padx=5, pady=5)
deadline_var = tk.StringVar()
tk.Entry(form_frame, textvariable=deadline_var).grid(row=1, column=1, padx=5, pady=5)

# Buttons
button_frame = tk.Frame(root, bg="#f0f8ff")
button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

tk.Button(button_frame, text="Add Task", command=add_task, bg="#4caf50", fg="white").grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Update Task", command=update_task, bg="#ff9800", fg="white").grid(row=0, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Delete Task", command=delete_task, bg="#f44336", fg="white").grid(row=0, column=2, padx=5, pady=5)

# Task list
columns = ('Task', 'Deadline')
task_list = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    task_list.heading(col, text=col)
task_list.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
task_list.bind('<<TreeviewSelect>>', select_task)

root.mainloop()
