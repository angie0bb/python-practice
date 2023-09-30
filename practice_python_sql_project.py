# Practice python, sql project
# sql, database, tables, visualization


import pandas as pd
from matplotlib import pyplot as plt
from rich.console import Console  # 'rich' package to create pretty table
from rich.table import Table
import sqlite3 as db

# read data file to pd dataframe
file_name = "user_data.xlsx"
# xlsx to pd dataframe
user_data = pd.read_excel(file_name, sheet_name=None)
sheet_name = list(user_data.keys())

users_column_name = list(user_data["users"].columns)
order_column_name = list(user_data["order"].columns)
plan_column_name = list(user_data["plan"].columns)

users_value = user_data["users"].values.tolist()
orders_value = user_data["order"].values.tolist()
plans_value = user_data["plan"].values.tolist()


class UsersDbSql:
    def __init__(self):
        self.conn = db.connect("user.db")
        self.cursor = self.conn.cursor()
        self.data = None
        self.col_names = None

    def execute_query(self, query):
        self.cursor.execute(query)
        self.col_names = [description[0] for description in self.cursor.description] # save it to use in other functions
        self.data = self.cursor.fetchall()

    def create_table(self, table_name, table_info):
        query = f"CREATE TABLE IF NOT EXISTS {table_name}({table_info});"
        self.cursor.execute(query)

    def populate_table(self, table_name, col_names, values):
        # to create the same number of question marks with the number of columns
        question_mark = ""
        for i in range(len(col_names)):
            question_mark += "?,"
        question_mark = question_mark.rstrip(",")

        col_names_revised = []
        for i in col_names:
            col_names_revised.append(f'"{i}"')
        col_names_string = ",".join(col_names_revised)  # to put in the query as a string, not list

        query = f"INSERT INTO {table_name}({col_names_string}) VALUES({question_mark});"
        self.cursor.executemany(query, values)

    # def close(self):
    #     self.conn.close()

    def print_table(self, query, title):
        self.execute_query(query)
        df = pd.DataFrame(self.data, columns=self.col_names)  # column_name = list
        console = Console()
        table = Table(title)  # table visualization, adjusts the table size automatically to the console size
        table.add_row(df.to_string(index=False, float_format=lambda _: '{:.2f}'.format(_)))
        console.print(table)

    def print_chart(self, query, chart_type, title, xlabel=None, ylabel=None):
        self.execute_query(query)

        x = []
        y = []
        for row in self.data:
            x.append(row[0])
            y.append(row[1])

        if chart_type == "bar":
            # add data label
            for i, v in enumerate(x):
                plt.text(v, y[i], y[i], ha="center", va="bottom")
            plt.bar(x, y, color='skyblue')
            plt.xlabel(f"<{xlabel}>", weight='bold')
            plt.ylabel(f"<{ylabel}>", weight='bold')

        elif chart_type == "pie":
            fig = plt.figure(figsize = (10,7))
            plt.pie(y, labels=x, autopct='%1.1f%%', shadow=True)
            plt.legend(loc="best")

        elif chart_type == "line":
            # add data label
            for i, v in enumerate(x):
                plt.text(v, y[i], y[i], ha="center", va="bottom")
            plt.plot(x, y, color='orange', marker='o')
            plt.xlabel(f"<{xlabel}>", weight='bold')
            plt.ylabel(f"<{ylabel}>", weight='bold')
            plt.grid(True)

        plt.title(title, weight='bold', fontsize=15)
        plt.show()


user_db = UsersDbSql()

user_db.create_table("users", """user_id CHAR(5),
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        email VARCHAR(50),
        country VARCHAR(50),
        plan_id VARCHAR(10),
        PRIMARY KEY(user_id),
        FOREIGN KEY(plan_id) REFERENCES plan """)
user_db.create_table("orders", """
        order_id VARCHAR(10),
        order_amount REAL(10),
        user_id CHAR(5),
        PRIMARY KEY(order_id),
        FOREIGN KEY(user_id) REFERENCES users""")
user_db.create_table("plans", """
        plan_id VARCHAR(10),
        plan_desc VARCHAR(50),
        amount REAL(10),
        PRIMARY KEY(plan_id) """)

user_db.populate_table("users", users_column_name, users_value)
user_db.populate_table("orders", order_column_name, orders_value)
user_db.populate_table("plans", plan_column_name, plans_value)

# Show the content of all tables in console, LIMIT 10
user_db.print_table("SELECT * FROM users LIMIT 10", "users")
user_db.print_table("SELECT * FROM orders LIMIT 10", "orders")
user_db.print_table("SELECT * FROM plans LIMIT 10", "plans")


# Questions & Visualizations
# 1. Get the user id, first name and last name of users who live in the United States, order by first name.
query1 = """
    SELECT user_id, first_name || " " || last_name as name 
    FROM users 
    WHERE country = 'United States'
    ORDER BY first_name;
"""
user_db.print_table(query1, "Question 1")

# 2. (Join)Get the user_id, first name, last name, email, ordered amount of users who ordered the most expensive product
query2 = """
    SELECT u.user_id, first_name, last_name, email, order_amount 
    FROM orders as o
    LEFT JOIN users as u ON u.user_id = o.user_id
    WHERE order_amount = (SELECT MAX(order_amount) FROM orders);
"""
user_db.print_table(query2, "Question 2")

# 3. (Join, Aggregate) Get the total amount($) of order for each country, order by total amount in descending order.
query3 = """
    SELECT country, SUM(order_amount) as total_amount
    FROM orders as o
    LEFT JOIN users as u ON u.user_id = o.user_id
    GROUP BY country
    ORDER BY total_amount DESC;
"""
user_db.print_table(query3, "Question 3")
user_db.print_chart(query3, "line", "Total Amount of Sales", "country", 'total amount ($)')

# 4. (Join, Aggregate) Get the revenue of plans and plan description, limit to TOP 10 plans ordered by revenue.
query4 = """
    SELECT plan_desc, p.amount * count(u.user_id) as revenue
    FROM plans as p
    LEFT JOIN users as u ON p.plan_id = u.plan_id
    GROUP BY p.plan_id
    ORDER BY revenue DESC
    LIMIT 11;
"""
user_db.print_table(query4, "Question 4")
user_db.print_chart(query4, "bar", "TOP 10 Revenue Plans", "plan description", "revenue")

# 5. (Aggregate) Get the distribution of user's country in percentage. (pie chart?)
query5 = """
    SELECT country, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM users), 2) AS distribution
    FROM users
    GROUP BY country
    ORDER BY distribution DESC;
"""
user_db.print_table(query5, "Question 5")
user_db.print_chart(query5, "pie", "Distribution of Country")

