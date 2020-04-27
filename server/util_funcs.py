import tkinter as tk


def pending_orders(container, pending):
    clear_frame(container)
    tk.Label(container, text="").pack()
    label_pending = tk.Label(container, text='Pending orders', font=("Open Sans", 40, 'bold'), fg="#982121")
    label_pending.pack()
    tk.Label(container, text="").pack()
    tk.Label(container, text="").pack()

    scrollbar = tk.Scrollbar(container, borderwidth=2)
    scrollbar.pack(side='right', fill='y')

    mylist = tk.Listbox(container, yscrollcommand=scrollbar.set, width=150, height=15, bg=container.cget("background"),
                        fg="#982121", font=("Open Sans", 16, 'bold'), justify='center')
    num = 1
    for orderp in pending:
        mylist.insert(tk.END,
                      f"{num}.{orderp[0]}: Pizza {orderp[1]}; Ingredients: {orderp[3]}; Total cost: {orderp[2]}\n\n")
        num += 1
    mylist.pack()
    scrollbar.config(command=mylist.yview)


def delivered_orders(container, delivered):
    clear_frame(container)
    tk.Label(container, text="").pack()
    label_pending = tk.Label(container, text='Delivered orders', font=("Open Sans", 40, 'bold'), fg="#982121")
    label_pending.pack()
    tk.Label(container, text="").pack()
    tk.Label(container, text="").pack()

    scrollbar = tk.Scrollbar(container, borderwidth=2)
    scrollbar.pack(side='right', fill='y')

    mylist = tk.Listbox(container, yscrollcommand=scrollbar.set, width=150, height=15, bg=container.cget("background"),
                        font=("Open Sans", 16, 'bold'), fg="#982121", justify='center')
    num = 1
    for orderd in delivered:
        mylist.insert(tk.END,
                      f"{num}.{orderd[0]}: Pizza {orderd[1]}; Ingredients: {orderd[3]}; Total cost: {orderd[2]}\n\n")
        num += 1
    mylist.pack()
    scrollbar.config(command=mylist.yview)


def set_colors(container):
    for widget in container.winfo_children():
        if isinstance(widget, tk.Frame):
            set_colors(widget)
        elif isinstance(widget, tk.Label) or isinstance(widget, tk.Entry):
            widget.configure(foreground="#982121")


def disable_container(container):
    for widget in container.winfo_children():
        if isinstance(widget, tk.Button) or isinstance(widget, tk.Entry):
            widget.config(state=tk.DISABLED)


def clear_frame(container):
    for widget in container.winfo_children():
        widget.destroy()
