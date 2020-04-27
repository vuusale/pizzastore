import tkinter as tk
from functools import partial
from client import main
from server import users
from client import database
from server import util_funcs
from sqlite3 import Error
import tkinter.ttk as ttk


def create_page(container, buttonframe):
    try:
        ords = database.pull_orders('admin')
        for order in ords:
            customer = users.Customer(order[0])
            customer.order_pizza(order)
    except Error:
        error = tk.PhotoImage(file="src/icons/error.png").subsample(4, 4)
        error_label = tk.Label(container, image=error)
        error_label.image = error
        error_label.pack(anchor='center')
        tk.Label(container, text="Sorry, there was en error.", font=("Open Sans", 30)).pack(anchor='center')
    else:
        global admin
        admin = users.Admin('Admin')

        waiting_orders = ttk.Button(buttonframe, text="Orders", command=partial(orders, container), width=20)
        waiting_orders.pack(side='left', padx=(10, 5), pady=(10, 5))

        profile = ttk.Button(buttonframe, text="Profile", command=partial(admin_profile, container), width=20)
        profile.pack(side='left', padx=(10, 5), pady=(10, 5))

        logout = ttk.Button(buttonframe, text="Logout", command=partial(admin_logout, container, buttonframe), width=20)
        logout.pack(side='left', padx=(10, 5), pady=(10, 5))

        admin_main(container)


def admin_logout(container, buttonframe):
    admin.orders = []
    main.logout(container, buttonframe)


def admin_main(container):
    welcome = tk.Label(container, text="Welcome admin!", font=("Open Sans", 40, 'bold'), fg="#982121")
    welcome.place(relx=0.5, rely=0.2, anchor='center')
    admin_icon = tk.PhotoImage(file="src/icons/admin.png").subsample(2, 2)
    admin_icon_label = tk.Label(container, image=admin_icon)
    admin_icon_label.image = admin_icon
    admin_icon_label.pack(side='bottom')


def orders(container):
    util_funcs.clear_frame(container)
    tk.Label(container, text="").pack()
    tk.Label(container, text="").pack()
    tk.Label(container, text="").pack()

    global notif_order
    global deliver_button
    notif_order = tk.StringVar()
    if admin.orders:
        temp_container = tk.Frame(container)
        temp_container.pack(side="top")
        pending = admin.pull_orders()
        util_funcs.pending_orders(temp_container, pending)
        deliver_button = ttk.Button(container, text="Deliver a pizza", command=partial(deliver_pizza, container), width=20)
        tk.Label(container, text="").pack(side="top")
        deliver_button.pack(side="top")
        tk.Label(container, text="").pack()
        notif_label = tk.Label(container, textvariable=notif_order, font=("Open Sans", 16), fg="#982121")
        notif_label.pack(side="top", anchor="center")
    else:
        notif_label = tk.Label(container, textvariable=notif_order, font=("Open Sans", 16), fg="#982121")
        notif_label.pack(side="top", anchor="center")
        notif_order.set("There is no order waiting")


def deliver_pizza(container):
    order = admin.deliver_pizza()
    if order:
        try:
            database.deliver(order)
        except Error:
            notif_order.set("Delivery failed")
        else:
            util_funcs.clear_frame(container)
            orders(container)
            if admin.orders:
                notif_order.set("Order delivered")


def admin_profile(container):
    util_funcs.clear_frame(container)

    tk.Label(container, text="").pack()
    label = tk.Label(container, text="Profile of admin", font=("Open Sans", 40, 'bold'), fg="#982121")
    label.pack(side="top", anchor="center")
    tk.Label(container, text="").pack()
    temp_container = tk.Frame(container)
    temp_container.pack(side='top')
    scrollbar = tk.Scrollbar(temp_container, bd=1, relief='sunken')
    listbox = tk.Listbox(temp_container, bg=container.cget("background"), width=50, height=15, font=("Open Sans", 16, 'bold'), fg="#982121")

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    user_list = database.pull_users()
    for user in user_list:
        if user[0] != 'admin':
            listbox.insert('end', f"{user[0]} => budget: {user[1]}")
    scrollbar.pack(side='right', fill='y')
    listbox.configure(justify='center')
    listbox.pack(side="top", anchor="center")

    global notif_profile
    name = tk.StringVar()
    notif_profile = tk.StringVar()
    amount = tk.IntVar()
    amount.set(100)

    name_lebel = tk.Label(container, text="Name", font=("Open Sans", 16), fg="#982121")
    amount_label = tk.Label(container, text="Amount", font=("Open Sans", 16), fg="#982121")

    name_entry = tk.Entry(container, textvariable=name, font=("Open Sans", 15), fg="#982121")
    amount_entry = tk.Entry(container, textvariable=amount, font=("Open Sans", 15), fg="#982121")

    add_button = ttk.Button(container, text="Update budget", command=partial(util, container, name, amount), width=20)

    tk.Label(container, text="").pack()
    name_lebel.pack()
    name_entry.pack()
    tk.Label(container, text="").pack()
    amount_label.pack()
    amount_entry.pack()
    tk.Label(container, text="").pack()
    add_button.pack()
    tk.Label(container, text="").pack()
    tk.Label(container, textvariable=notif_profile, font=("Open Sans", 16), fg="#982121").pack()


def util(container, name, amount):
    name = name.get()
    amount = amount.get()
    if not name or not amount:
        notif_profile.set("Provide details")
        return
    try:
        database.update_budget(name, amount)
    except ValueError as e:
        notif_profile.set("User does not exist")
    except Error:
        notif_profile.set("Failed to update amount")
    else:
        notif_profile.set(f"{amount} manat added")
        admin_profile(container)