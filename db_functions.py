import mysql.connector
import pandas as pd
import numpy as np
from config.db_config import DB_CONFIG

def connect_to_db():
    return mysql.connector.connect(**DB_CONFIG)

def get_basic_info(cursor):
    queries = {
        # -- 1 Total suppliers --
        "Total Suppliers": "SELECT COUNT(supplier_id) as total_suppliers FROM suppliers",
        # -- 2 Total products --
        "Total Products": "SELECT COUNT(*) AS total_products FROM products",

        # -- 3 Total categories dealing --
        "Total Categories Dealing": "SELECT COUNT(DISTINCT category) AS total_categories FROM products",

        # -- 4  Total sales value made in last 3 months --
        "Total Sale Value (Last 3 Months)": """
                                            select round(sum(abs(se.change_quantity) * p.price), 2) as total_sales_value_in_last_3_months
                                            from stock_entries as se
                                                     join products p on p.product_id = se.product_id
                                            where se.change_type = "Sale"
                                              and se.entry_date >= (select date_sub(max(entry_date), interval 3 month)
                                                                    from stock_entries)
                                            """,

        # -- 5  Total Restock value made in last 3 months --
        "Total Restock value (Last 3 Months)": """
                                               select round(sum(abs(se.change_quantity) * p.price), 2) as total_restock_value_in_last_3_months
                                               from stock_entries as se
                                                        join products p on p.product_id = se.product_id
                                               where se.change_type = "Restock"
                                                 and
                                                   se.entry_date >= (select date_sub(max(entry_date), interval 3 month)
                                                                     from stock_entries)
                                               """,

        # -- 6 Below Reorder & No Pending Reorders --
        "Below Reorder & No Pending Reorders": """
                                               select count(*)
                                               from products as p
                                               where p.stock_quantity < p.reorder_level
                                                 and product_id NOT IN (select distinct product_id
                                                                        from reorders
                                                                        where status = "Pending")
                                               """
    }

    result = {}
    for label, query in queries.items():
        cursor.execute(query)
        row = cursor.fetchone()
        result[label] = list(row.values())[0]
    return result

queries = {
    "Suppliers Contact Details": "SELECT supplier_name, contact_name, email, phone FROM suppliers",

    "Products with Supplier and Stock": """
                                    SELECT 
                                        p.product_name,
                                        s.supplier_name,
                                        p.stock_quantity,
                                        p.reorder_level
                                    FROM products AS p
                                    JOIN suppliers AS s 
                                        ON p.supplier_id = s.supplier_id
                                    ORDER BY p.product_name ASC
                                    """,


    "Products needing Reorder" : "select product_id, product_name,stock_quantity, reorder_level from products where stock_quantity < reorder_level"
}

def get_additional_tables(cursor):
    tables = {}
    for label, query in queries.items():
        cursor.execute(query)
        tables[label] = cursor.fetchall()

    return tables