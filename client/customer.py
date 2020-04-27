import tkinter as tk
from functools import partial
from client import main
from server import pizza_builder
from server import users
from client import database
from server import util_funcs
from sqlite3 import Error
import tkinter.ttk as ttk


def create_page(container, buttonframe, username):
    try:
        global budget
        budget = tk.DoubleVar()
        budget.set(database.query(username, 'budget'))
    except Error:
        error = tk.PhotoImage(file="src/icons/error.png").subsample(4, 4)
        error_label = tk.Label(container, image=error)
        error_label.image = error
        error_label.pack(anchor='center')
        tk.Label(container, text="Sorry, there was en error.", font=("Open Sans", 30)).pack(anchor='center')
    else:
        global customer
        global pizzas
        custom_image = tk.PhotoImage(file="src/pizzas/custom.png").subsample(2, 2)
        supreme_image = tk.PhotoImage(file="src/pizzas/supreme.png")
        pepperoni_image = tk.PhotoImage(file="src/pizzas/pepperoni.png")
        margarita_image = tk.PhotoImage(file="src/pizzas/margarita.png").subsample(2, 2)
        pizzas = {'Supreme': supreme_image, 'Pepperoni': pepperoni_image, 'Margarita': margarita_image,
                  'Custom': custom_image}

        customer = users.Customer(username)

        default_pizza = ttk.Button(buttonframe, text="Default pizzas",
                                   command=partial(default_pizzas, container, username), width=20)
        default_pizza.pack(side='left', padx=(10, 5), pady=(10, 5))

        custom_pizza = ttk.Button(buttonframe, text="Custom pizza",
                                  command=partial(pizza_menu, container, 'Custom', username), width=20)
        custom_pizza.pack(side='left', padx=(10, 5), pady=(10, 5))

        profile = ttk.Button(buttonframe, text="Profile", command=partial(customer_profile, container, username), width=20)
        profile.pack(side='left', padx=(10, 5), pady=(10, 5))

        logout = ttk.Button(buttonframe, text="Logout", command=partial(main.logout, container, buttonframe), width=20)
        logout.pack(side='left', padx=(10, 5), pady=(10, 5))
        customer_main(container, username)


def customer_main(container, username):
    tk.Label(container, text="").pack()
    tk.Label(container, text="").pack()
    welcome = tk.Label(container, text=f"Welcome {username}!", font=("Open Sans", 40, 'bold'), fg="#982121")
    welcome.place(relx=0.5, rely=0.2, anchor='center')
    pizza_icon = tk.PhotoImage(file="src/icons/customer.png").subsample(5, 5)
    pizza_icon_label = tk.Label(container, image=pizza_icon)
    pizza_icon.image = pizza_icon
    pizza_icon_label.place(relx=0.5, rely=0.6, anchor='center')


def default_pizzas(container, username):
    util_funcs.clear_frame(container)
    label = tk.Label(container, text="Our default pizzas", font=("Open Sans", 40, 'bold'), fg="#982121")
    label.place(relx=0.5, rely=0.07, anchor="center")

    buttons = ['Supreme', 'Pepperoni', 'Margarita']
    num = 0
    for pizza in buttons:
        button = ttk.Button(container, text=pizza,
                            command=partial(pizza_menu, container, pizza, username), width=20)
        button.place(relx=0.5, rely=0.2 + num * 0.14, anchor="center")
        num += 1


def pizza_menu(container, name, username):
    util_funcs.clear_frame(container)
    pizza = pizza_builder.PizzaBuilder(name)

    global status_pizza
    global notif_pizza
    global cost_pizza

    label = "Create your own pizza" if name == 'Custom' else name
    budget_image = tk.PhotoImage(file="src/icons/budget.png").subsample(4, 4)

    name_label = tk.Label(container, text=label, font=("Open Sans", 40, 'bold'))
    name_label.place(relx=0.5, rely=0.07, anchor="center")

    budget_icon = tk.Label(container, image=budget_image)
    budget_icon.image = budget_image
    budget_icon.place(relx=0.83, rely=0.15, anchor='center')

    budget_label = tk.Label(container, text="Budget:", font=("Open Sans", 14))
    budget_money = tk.Label(container, textvariable=budget, font=("Open Sans", 14))

    budget_label.place(relx=0.8, rely=0.3, anchor="center")
    budget_money.place(relx=0.86, rely=0.3, anchor="center")

    ingredients = pizza.default

    create_buttons(container, pizza, 'add', ingredients)
    create_buttons(container, pizza, 'remove', ingredients)

    status_pizza = tk.StringVar()
    set_status(pizza)
    cost_pizza = tk.DoubleVar()
    cost_pizza.set(pizza.get_price())

    status_label = tk.Label(container, textvariable=status_pizza, font=("Open Sans", 16))
    status_label.place(relx=0.6, rely=0.2, anchor='n')
    price_word = tk.Label(container, text="Cost:", font=("Open Sans", 18))
    price_word.place(relx=0.58, rely=0.67, anchor='center')
    price_label = tk.Label(container, textvariable=cost_pizza, font=("Open Sans", 18, 'bold'))
    price_label.place(relx=0.62, rely=0.67, anchor='center')
    order_button = ttk.Button(container, text="Order", command=partial(order, container, pizza, username), width=20)
    order_button.place(relx=0.6, rely=0.76, anchor='center')
    notif_pizza = tk.StringVar()
    notif_label = tk.Label(container, textvariable=notif_pizza, font=("Open Sans", 18))
    notif_label.place(relx=0.83, rely=0.76, anchor='center')
    pizza_image = pizzas[name]

    pizza_label = tk.Label(container, image=pizza_image)
    pizza_label.image = pizza_image
    pizza_label.place(relx=0.83, rely=0.55, anchor='center')
    util_funcs.set_colors(container)


def set_status(pizza):
    stat = str(pizza.get_status())[1:-1].split(',')
    res = ''
    for s in stat:
        res += s.strip().replace("'", "") + '\n\n'
    status_pizza.set(res)


def create_buttons(container, pizza, mode, ingredients):
    ings = list(ingredients.keys())
    lenn = len(ings)
    if mode == 'add':
        for i in range(lenn):
            ing = ings[i]
            button = ttk.Button(container, text=f"Add {ing.lower()}",
                                command=partial(add_ingredient, pizza, ing), width=20)
            button.place(relx=0.15, rely=0.17 + i * 0.12, anchor='center')

    elif mode == 'remove':
        for i in range(lenn):
            ing = ings[i]
            button = ttk.Button(container, text=f"Remove {ing.lower()}",
                                command=partial(remove_ingredient, pizza, ing), width=20)
            button.place(relx=0.38, rely=0.17 + i * 0.12, anchor='center')


def add_ingredient(pizza, ext):
    added = pizza.add_ingredient(ext)
    if added:
        cost_pizza.set(pizza.get_price())
        set_status(pizza)


def remove_ingredient(pizza, ext):
    removed = pizza.remove_ingredient(ext)
    if removed:
        cost_pizza.set(pizza.get_price())
        set_status(pizza)


def customer_profile(container, username):
    util_funcs.clear_frame(container)
    tk.Label(container, text="").pack()
    tk.Label(container, text="").pack()
    try:
        pending = database.pull_orders('customer', username, 'PENDING')
        delivered = database.pull_orders('customer', username, 'DELIVERED')
    except Error:
        error = tk.PhotoImage(file="src/icons/error.png").subsample(4, 4)
        error_label = tk.Label(container, image=error)
        error_label.image = error
        error_label.pack(anchor='center')
        tk.Label(container, text="Sorry, there was en error.", font=("Open Sans", 30)).pack(anchor='center')
    else:
        profile = tk.Label(container, text=f"Profile of {username}", font=("Open Sans", 40, 'bold'), fg="#982121")
        profile.place(relx=0.5, rely=0.08, anchor='center')

        pending_button = ttk.Button(container, text="Pending orders",
                                    command=partial(call_pending, container, pending), width=20)
        pending_button.place(relx=0.5, rely=0.2, anchor='center')

        delivered_button = ttk.Button(container, text="Delivered orders",
                                      command=partial(call_delivered, container, delivered), width=20)
        delivered_button.place(relx=0.5, rely=0.3, anchor='center')


def call_delivered(container, delivered):
    util_funcs.clear_frame(container)
    temp_container = tk.Frame(container)
    temp_container.pack()
    util_funcs.delivered_orders(temp_container, delivered)


def call_pending(container, pending):
    util_funcs.clear_frame(container)
    temp_container = tk.Frame(container)
    temp_container.pack()
    util_funcs.pending_orders(temp_container, pending)


def order(container, pizza, username):
    pizza_price = pizza.get_price()
    if budget.get() >= pizza.get_price():
        try:
            database.order(pizza, username)
        except Error:
            notif_pizza.set("There was an error")
        else:
            new_budget = budget.get() - pizza_price
            budget.set(new_budget)
            database.update_budget(username, -pizza_price)
            util_funcs.disable_container(container)
            notif_pizza.set("Your pizza is on its way")
    else:
        notif_pizza.set("You do not have enough money")
