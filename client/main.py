from functools import partial
import tkinter as tk
from client import admin, customer
from server import util_funcs
from client import database
from sqlite3 import Error
import bcrypt
import hmac
import tkinter.ttk as ttk


def create_page(container, buttonframe):
    register_button = ttk.Button(buttonframe, text="Register", command=partial(register, container), width=20)
    register_button.pack(side='left', padx=(10, 5), pady=(10, 5))

    login_customer_button = ttk.Button(buttonframe, text="Login as customer", command=partial(customer_login, container, buttonframe), width=20)
    login_customer_button.pack(side='left', padx=(10, 5), pady=(10, 5))

    login_admin_button = ttk.Button(buttonframe, text="Login as admin", command=partial(admin_login, container, buttonframe), width=20)
    login_admin_button.pack(side='left', padx=(10, 5), pady=(10, 5))

    main(container)


def main(container):
    welcome = tk.Label(container, text="Welcome to our Pizza Store!", font=("Open Sans", 40, 'bold'), fg="#982121")
    welcome.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.1)
    pizzastore = tk.PhotoImage(file="src/icons/pizzastore.png")
    pizzastore_label = tk.Label(container, image=pizzastore)
    pizzastore_label.image = pizzastore
    pizzastore_label.place(relx=0.5, rely=0.6, anchor='center')


def register(container):
    util_funcs.clear_frame(container)
    global notif_register
    username = tk.StringVar()
    password = tk.StringVar()
    password2 = tk.StringVar()
    notif_register = tk.StringVar()
    register_label = tk.Label(container, text="Register a user", font=("Open Sans", 40, 'bold'))
    register_label.place(relx=0.3, rely=0.1, relwidth=0.4, relheight=0.1)
    username_label = tk.Label(container, text="Username", font=("Open Sans", 15))
    username_label.place(relx=0.445, rely=0.25, relwidth=0.11, relheight=0.04)
    username_entry = tk.Entry(container, textvariable=username, font=("Open Sans", 15))
    username_entry.place(relx=0.425, rely=0.30, relwidth=0.16, relheight=0.04)
    password_label = tk.Label(container, text="Password", font=("Open Sans", 15))
    password_label.place(relx=0.45, rely=0.35, relwidth=0.1, relheight=0.04)
    password_entry = tk.Entry(container, textvariable=password, font=("Open Sans", 15), show="*")
    password_entry.place(relx=0.425, rely=0.4, relwidth=0.16, relheight=0.04)
    confirm_label = tk.Label(container, text="Confirm password", font=("Open Sans", 15))
    confirm_label.place(relx=0.405, rely=0.45, relwidth=0.19, relheight=0.04)
    confirm_entry = tk.Entry(container, textvariable=password2, show="*", font=("Open Sans", 15))
    confirm_entry.place(relx=0.425, rely=0.5, relwidth=0.16, relheight=0.04)
    register_button = ttk.Button(container, text="Register", command=partial(check_creds_register, container, username, password, password2), width=20)
    register_button.place(relx=0.5, rely=0.6, anchor="center")
    notif_label = tk.Label(container, textvariable=notif_register, font=("Open Sans", 14, 'bold'))
    notif_label.place(relx=0.5, rely=0.68, anchor="center")
    util_funcs.set_colors(container)


def customer_login(container, buttonframe):
    util_funcs.clear_frame(container)
    global notif_customer
    username = tk.StringVar()
    password = tk.StringVar()
    notif_customer = tk.StringVar()
    login_label = tk.Label(container, text="Log in", font=("Open Sans", 40, 'bold'))
    login_label.place(relx=0.3, rely=0.1, relwidth=0.4, relheight=0.1)
    username_label = tk.Label(container, text="Username", font=("Open Sans", 15))
    username_label.place(relx=0.445, rely=0.25, relwidth=0.11, relheight=0.04)
    username_entry = tk.Entry(container, textvariable=username, font=("Open Sans", 15))
    username_entry.place(relx=0.425, rely=0.3, relwidth=0.15, relheight=0.04)
    password_label = tk.Label(container, text="Password", font=("Open Sans", 15))
    password_label.place(relx=0.45, rely=0.35, relwidth=0.1, relheight=0.04)
    password_entry = tk.Entry(container, textvariable=password, show="*", font=("Open Sans", 15))
    password_entry.place(relx=0.425, rely=0.4, relwidth=0.15, relheight=0.04)
    login_button = ttk.Button(container, text="Login", command=partial(check_creds_login, container, buttonframe, username, password, mode='customer'), width=20)
    login_button.place(relx=0.5, rely=0.5, anchor="center")
    notif_label = tk.Label(container, textvariable=notif_customer, font=("Open Sans", 14, 'bold'))
    notif_label.place(relx=0.5, rely=0.58, anchor="center")
    util_funcs.set_colors(container)


def admin_login(container, buttonframe):
    util_funcs.clear_frame(container)
    password = tk.StringVar()
    global notif_admin
    notif_admin = tk.StringVar()
    login_label = tk.Label(container, text="Log in as admin", font=("Open Sans", 40, 'bold'))
    login_label.place(relx=0.3, rely=0.1, relwidth=0.42, relheight=0.1)
    password_label = tk.Label(container, text="Password", font=("Open Sans", 15))
    password_label.place(relx=0.445, rely=0.25, relwidth=0.11, relheight=0.04)
    password_entry = tk.Entry(container, textvariable=password, show="*", font=("Open Sans", 15))
    password_entry.place(relx=0.425, rely=0.3, relwidth=0.15, relheight=0.04)
    login_button = ttk.Button(container, text="Login", command=partial(check_creds_login, container, buttonframe, uname=None, pass1=password, mode='admin'), width=20)
    login_button.place(relx=0.5, rely=0.4, anchor="center")
    notif_label = tk.Label(container, textvariable=notif_admin, font=("Open Sans", 14, 'bold'))
    notif_label.place(relx=0.5, rely=0.48, anchor="center")
    util_funcs.set_colors(container)


def check_creds_register(container, uname, pass1, pass2):
    username = uname.get()
    password1 = pass1.get()
    password2 = pass2.get()
    if not username or not password1 or not password2:
        notif_register.set('Please fill in all fields.')
        return
    if password1 == password2:
        try:
            if database.query(username, 'username') is None:
                hashed_password = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt(12))
                database.register_user(username, hashed_password)
                notif_register.set('Registered successfully.\nNow please log in.')
                util_funcs.disable_container(container)
            else:
                notif_register.set('User exists')
        except Error:
            notif_register.set('Try again.')
    else:
        notif_register.set('Passwords do not match')


def check_creds_login(container, buttonframe, uname, pass1, mode):
    password = pass1.get()
    if mode == 'customer':
        username = uname.get()
        if not username or not password:
            notif_customer.set('Please fill in all fields.')
            return
        try:
            user = database.query(username, 'password')
            stored = user
            hashed = bcrypt.hashpw(password.encode('utf-8'), stored)
            if hmac.compare_digest(hashed, stored):
                util_funcs.clear_frame(container)
                util_funcs.clear_frame(buttonframe)
                customer.create_page(container, buttonframe, username)
                return
            notif_customer.set('Invalid credentials')
            return
        except Error:
            notif_customer.set('Invalid credentials')
    elif mode == 'admin':
        if not pass1.get():
            notif_admin.set('Please enter admin password')
            return
        try:
            user = database.query('admin', 'password')
            hashed = bcrypt.hashpw(password.encode('utf-8'), user)
            if hmac.compare_digest(hashed, user):
                util_funcs.clear_frame(container)
                util_funcs.clear_frame(buttonframe)
                admin.create_page(container, buttonframe)
                return
            notif_admin.set('Wrong password')
        except Error:
            notif_admin.set('Try again')


def logout(container, buttonframe):
    util_funcs.clear_frame(container)
    util_funcs.clear_frame(buttonframe)
    create_page(container, buttonframe)


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
