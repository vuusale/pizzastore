import abc


class Pizza(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_price(self):
        pass

    @abc.abstractmethod
    def get_status(self):
        pass


class Pepperoni(Pizza):
    __pizza_price = 7
    default_ingredients = {'Tomato': 1, 'Pepper': 1, 'Chicken': 1, "Mushroom": 0, "Olive": 1, 'Meat': 1}

    def get_price(self):
        return self.__pizza_price

    def get_status(self):
        return {}


class Supreme(Pizza):
    __pizza_price = 9
    default_ingredients = {'Tomato': 1, 'Pepper': 1, 'Mozzarella': 1, 'Chicken': 1, "Olive": 1, 'Meat': 1}

    def get_price(self):
        return self.__pizza_price

    def get_status(self):
        return {}


class Margarita(Pizza):
    __pizza_price = 6.5
    default_ingredients = {'Tomato': 1, 'Pepper': 0, 'Mozzarella': 1, "Olive": 1, 'Mushroom': 1}

    def get_price(self):
        return self.__pizza_price

    def get_status(self):
        return {}


class Custom(Pizza):
    __pizza_price = 5
    default_ingredients = {'Tomato': 0, 'Pepper': 0, 'Mozzarella': 0, 'Chicken': 0, 'Mushroom': 0, 'Olive': 0, 'Meat': 0}

    def get_price(self):
        return self.__pizza_price

    def get_status(self):
        return {}


class PizzaDecorator(Pizza):
    def __init__(self, pizza):
        self.pizza = pizza

    def get_price(self):
        return self.pizza.get_price()

    def get_status(self):
        return self.pizza.get_status()


class Tomato(PizzaDecorator):
    def __init__(self, pizza):
        super(Tomato, self).__init__(pizza)
        self.__price = 1.5

    @property
    def price(self):
        return self.__price

    def get_price(self):
        return super(Tomato, self).get_price() + self.__price

    def get_status(self):
        status = super(Tomato, self).get_status()
        if "Tomato" in status.keys():
            status["Tomato"] += 1
        else:
            status["Tomato"] = 1
        return status


class Chicken(PizzaDecorator):
    def __init__(self, pizza):
        super(Chicken, self).__init__(pizza)
        self.__price = 3.5

    @property
    def price(self):
        return self.__price

    def get_price(self):
        return super(Chicken, self).get_price() + self.__price

    def get_status(self):
        status = super(Chicken, self).get_status()
        if "Chicken" in status.keys():
            status["Chicken"] += 1
        else:
            status["Chicken"] = 1
        return status


class Pepper(PizzaDecorator):
    def __init__(self, pizza):
        super(Pepper, self).__init__(pizza)
        self.__price = 1.5

    @property
    def price(self):
        return self.__price

    def get_price(self):
        return super(Pepper, self).get_price() + self.__price

    def get_status(self):
        status = super(Pepper, self).get_status()
        if "Pepper" in status.keys():
            status["Pepper"] += 1
        else:
            status["Pepper"] = 1
        return status


class Mozzarella(PizzaDecorator):
    def __init__(self, pizza):
        super(Mozzarella, self).__init__(pizza)
        self.__price = 2.5

    @property
    def price(self):
        return self.__price

    def get_price(self):
        return super(Mozzarella, self).get_price() + self.__price

    def get_status(self):
        status = super(Mozzarella, self).get_status()
        if "Mozzarella" in status.keys():
            status["Mozzarella"] += 1
        else:
            status["Mozzarella"] = 1
        return status


class Mushroom(PizzaDecorator):
    def __init__(self, pizza):
        super(Mushroom, self).__init__(pizza)
        self.__price = 3.0

    @property
    def price(self):
        return self.__price

    def get_price(self):
        return super(Mushroom, self).get_price() + self.__price

    def get_status(self):
        status = super(Mushroom, self).get_status()
        if "Mushroom" in status.keys():
            status["Mushroom"] += 1
        else:
            status["Mushroom"] = 1
        return status


class Olive(PizzaDecorator):
    def __init__(self, pizza):
        super(Olive, self).__init__(pizza)
        self.__price = 2.5

    @property
    def price(self):
        return self.__price

    def get_price(self):
        return super(Olive, self).get_price() + self.__price

    def get_status(self):
        status = super(Olive, self).get_status()
        if "Olive" in status.keys():
            status["Olive"] += 1
        else:
            status["Olive"] = 1
        return status


class Meat(PizzaDecorator):
    def __init__(self, pizza):
        super(Meat, self).__init__(pizza)
        self.__price = 4.5

    @property
    def price(self):
        return self.__price

    def get_price(self):
        return super(Meat, self).get_price() + self.__price

    def get_status(self):
        status = super(Meat, self).get_status()
        if "Meat" in status.keys():
            status["Meat"] += 1
        else:
            status["Meat"] = 1
        return status


class PizzaBuilder:
    def __init__(self, pizza_type):
        self.pizza_type = pizza_type
        self.ingredients_list = {}
        self.pizza = eval(pizza_type)()
        self.default = eval(pizza_type).default_ingredients
        for ext in self.default.keys():
            if eval(pizza_type).default_ingredients[ext]:
                self.add_ingredient(ext)
            else:
                self.ingredients_list[ext] = 0

    def add_ingredient(self, ingredient):
        if ingredient in self.ingredients_list.keys():
            if self.ingredients_list[ingredient] < 3:
                self.pizza = eval(ingredient)(self.pizza)
                self.ingredients_list[ingredient] += 1
                return 1
            return 0
        else:
            self.pizza = eval(ingredient)(self.pizza)
            self.ingredients_list[ingredient] = 1
            return 1

    def remove_ingredient(self, ingredient):
        if ingredient in self.ingredients_list.keys():
            if self.ingredients_list[ingredient] > 0:
                self.ingredients_list[ingredient] -= 1

            temp_pizza = eval(self.pizza_type)()
            for ex in self.ingredients_list.keys():
                if self.ingredients_list[ex]:
                    for _ in range(self.ingredients_list[ex]):
                        temp_pizza = eval(ex)(temp_pizza)
                else:
                    self.ingredients_list[ex] = 0

            self.pizza = temp_pizza
            return 1
        return 0

    def get_price(self):
        return self.pizza.get_price()

    def get_status(self):
        return self.pizza.get_status()
