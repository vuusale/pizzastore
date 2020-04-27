# Pizza Store
Pizza store application developed with Tkinter  for university project. Main technologies used include Tkinter library of Python and SQLite as DBMS. Main page:
![Main page](https://github.com/vuusale/pizzastore/blob/master/pizzastore.PNG)

## Description
There are two types of roles: admin and customer. 

Customers have options to choose from default pizzas, still being able to modify its ingredients, or to create custom pizza from scratch. They can also view their pending and delivered orders.

There is only one admin, who is notified as soon as a customer orders a pizza. To achieve this feature, singleton and observer design patterns have been applied combined:

![Class diagram](https://github.com/vuusale/pizzastore/blob/master/users.png)

Admin has rights to view pending orders, deliver a pizza at a time and update budget of a user.

For pizza creation, decorator design pattern has been implemented:

![Class diagram](https://github.com/vuusale/pizzastore/blob/master/pizzabuilder.png)

### Entity relationship diagram
![Entity relationship diagram](https://github.com/vuusale/pizzastore/blob/master/entity_relationship_diagram.png)

## Installation
It is enough to clone repository to local folder and run `client.py`. Admin password: adminpass.

