import os

import mysql.connector

class Product:
    def __init__(self, name, price, garantie):
        self.name = name
        self.price = round(price*100)
        self.garantie = garantie

    def save(self, cursor, date):
        cursor.execute("SELECT id FROM Product WHERE name=%s", (self.name,))
        product = cursor.fetchone()
        if product is None:
            cursor.execute("INSERT INTO Product (name, garantie) VALUES (%s, %s)", (self.name, self.garantie))
            product_id = cursor.lastrowid
            cursor.execute("INSERT IGNORE INTO PriceHistory (date, product_id, store_id, price) VALUE (%s, %s, 2, %s)", (date, product_id, self.price))
            return product_id
        cursor.execute("SELECT price FROM PriceHistory WHERE product_id=%s ORDER BY date LIMIT 1", (product[0],))
        price = cursor.fetchone()
        if price[0] != self.price:
            cursor.execute("INSERT IGNORE INTO PriceHistory (date, product_id, store_id, price) VALUE (%s, %s, 2, %s)", (date, product[0], self.price))
        return product[0]

class ShoppingList:
    def __init__(self, location, date):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="leroideskiwis",
                password=os.getenv("MYSQL_PASSWORD"),
                database="shopping"
            )
            self.cursor = self.conn.cursor(buffered=True)
        except mysql.connector.Error as e:
            print(e)
        self.products = []
        self.store = "E.Leclerc"
        self.location = location
        self.date = date

    def save(self):
        # get the id of the store from storeloc (table with location and store)
        self.cursor.execute("SELECT StoreLoc.id FROM StoreLoc "
                                    "JOIN shopping.Store S on S.id = StoreLoc.store "
                                    "JOIN shopping.Location L on L.id = StoreLoc.loc "
                                    "WHERE L.city=%s AND StoreLoc.store = 1", (self.location,))

        store = self.cursor.fetchone()
        if store is None:
            self.cursor.execute("INSERT INTO Location (city, postal_code) VALUES (%s, 0)", (self.location,))
            self.cursor.execute("INSERT INTO StoreLoc (store, loc) VALUES (1, %s)", (self.cursor.lastrowid,))
            store = self.cursor.lastrowid
        else:
            store = store[0]
        self.cursor.execute("INSERT INTO ShoppingList (store_id, date) VALUES (%s, %s)", (store, self.date))
        shopping_id = self.cursor.lastrowid
        for product in self.products:
            p = product.save(self.cursor, self.date)
            self.cursor.execute("INSERT INTO RelationShoppingProduct (shopping_id, product_id) VALUE (%s, %s)", (shopping_id, p))
        self.conn.commit()