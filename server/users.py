from client import database
from _sqlite3 import Error


class Customer:
    def __init__(self, username):
        self.observer = Admin('Admin')
        self.__username = username
        try:
            self.__budget = database.query(username, 'budget')
        except Error:
            self.__budget = 0
        self.pizzas = []

    def do_notify(self):
        self.observer.receive_order(self.pizzas[-1])

    def order_pizza(self, order):
        self.pizzas.append((self, order))
        self.do_notify()

    @property
    def username(self):
        return self.__username

    @property
    def budget(self):
        return self.__budget

    @budget.setter
    def budget(self, value):
        self.__budget = value


class SingletonMeta(type):
    __instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls.__instance


class Admin(metaclass=SingletonMeta):
    def __init__(self, username):
        self.username = username
        self.orders = []

    def receive_order(self, order):
        self.orders.append(order)

    def pull_orders(self):
        for order in self.orders:
            yield order[1]

    def deliver_pizza(self):
        if self.orders:
            order = self.orders[0]
            order[0].budget -= 5
            order[0].pizzas.remove(order)
            self.orders.remove(order)
            return order[1][4]
