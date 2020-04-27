import sqlite3
from sqlite3 import Error


def create_connection():
    with open(r"db_file", "r") as f:
        db_uri = f.read()
        conn = sqlite3.connect(db_uri)
        return conn


def register_user(username, password):
    conn = create_connection()
    query_string = "INSERT INTO users(username,password) VALUES(?,?);"
    cursor = conn.cursor()
    cursor.execute(query_string, [username, password])
    conn.commit()
    if conn:
        conn.close()


def query(select_param, query_type):
    conn = create_connection()
    queries = {"password": "SELECT password FROM users WHERE username = ?;",
               "username": "SELECT username FROM users WHERE username = ?;",
               "budget": "SELECT budget FROM users WHERE username = ?;",
               "cost": "SELECT cost FROM orders where order_id = ?"}
    query_string = queries[query_type]
    cursor = conn.cursor()
    cursor.execute(query_string, [select_param])
    res = cursor.fetchone()
    if conn:
        conn.close()
    if not res and query_type != "username":
        raise Error
    if res:
        return res[0]
    return res


def order(pizza, username):
    conn = create_connection()
    query_string = "INSERT INTO orders(username,pizza_name,cost,receipt) VALUES(?,?,?,?);"
    cursor = conn.cursor()
    receipt = f"{pizza.ingredients_list}"[1:-1]
    pizza_cost = pizza.get_price()
    pizza_name = pizza.pizza_type
    cursor.execute(query_string, [username, pizza_name, pizza_cost, receipt])
    conn.commit()
    if conn:
        conn.close()


def deliver(order_id):
    conn = create_connection()
    cursor = conn.cursor()
    order_update_query = "UPDATE orders SET status = 'DELIVERED' WHERE order_id = ?"
    cursor.execute(order_update_query, [order_id])
    conn.commit()
    if conn:
        conn.close()


def update_budget(username, amount):
    conn = create_connection()
    cursor = conn.cursor()
    query_budget = "SELECT budget FROM users WHERE username = ?"
    cursor.execute(query_budget, [username])
    res = cursor.fetchone()
    if not res:
        raise ValueError
    budget = res[0]
    if amount < 0 and budget >= abs(amount) or amount > 0:
        budget += amount
    user_update_query = "UPDATE users SET budget = ? WHERE username = ?"
    cursor.execute(user_update_query, [budget, username])
    conn.commit()
    if conn:
        conn.close()


def pull_orders(mode, username=None, status=None):
    conn = create_connection()
    queries = {
        "admin": "SELECT username,pizza_name,cost,receipt,order_id FROM orders WHERE status = 'PENDING';",
        "customer": "SELECT username,pizza_name,cost,receipt FROM orders WHERE username = ? and status = ?;"}
    cursor = conn.cursor()
    query_string = queries[mode]
    execute_params = {"admin": [], "customer": [username, status]}
    cursor.execute(query_string, execute_params[mode])
    res = cursor.fetchall()
    if conn:
        conn.close()
    return res


def pull_users():
    conn = create_connection()
    cursor = conn.cursor()
    query_string = "SELECT username,budget FROM users"
    cursor.execute(query_string)
    res = cursor.fetchall()
    if conn:
        conn.close()
    return res
