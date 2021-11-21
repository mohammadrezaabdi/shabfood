import psycopg2
import logging
import json
from model.db_driver import DBD
from model.handle import restaurant
from model.schema import *
from model.exceptions import *
from utils import Singleton


class Postgres_db(DBD, metaclass=Singleton):

    def __init__(self, cursor=None):
        self.cursor = cursor

    async def disconnect(self):
        self.cursor.close()
        self.cursor.connection.close()
        logging.info('database disconnected')

    @staticmethod
    async def connect():
        try:
            db_conf = json.load(open("db/database.json", "r"))
        except OSError as e:
            raise INTERNAL_SERVER_ERROR(str(e))
        # Connect to an existing database
        logging.info(
            f'conecting to database: jdbc:postgresql://{db_conf["host"]}:{db_conf["port"]}/{db_conf["user"]}')
        try:
            conn = psycopg2.connect(
                host=db_conf['host'], user=db_conf['user'], password=db_conf['password'], port=db_conf['port'])
        except psycopg2.OperationalError as e:
            raise INTERNAL_SERVER_ERROR(str(e))
        conn.autocommit = True
        cur = conn.cursor()
        # check if there is 'shabfood' database
        cur.execute(
            'SELECT EXISTS (SELECT datname FROM pg_database where datname=%s);', (db_conf['dbname'],))
        # create database if it doesn't exists
        if not cur.fetchone()[0]:
            cur.execute(f"CREATE database {db_conf['dbname']};")
        # connect to shabfood database
        conn.close()
        conn = psycopg2.connect(**db_conf)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(
            'SELECT EXISTS (SELECT * FROM information_schema.tables where table_name=%s);', ('customer',))
        # initial database if is empty
        if not cur.fetchone()[0]:
            logging.info('configure database...')
            try:
                cur.execute(open("db/schema.sql", "r").read())
            except psycopg2.Error as e:
                raise INTERNAL_SERVER_ERROR(str(e))
            except OSError as e:
                raise INTERNAL_SERVER_ERROR(str(e))
        # return database instance
        db = Postgres_db(conn.cursor())
        db.cursor.execute("SELECT version();")
        logging.info(
            'database connected successfully, version:\n        ' + db.cursor.fetchone()[0])
        return db

    ############################ Customer funcs ########################################################
    async def create_customer(self, customer: Customer):
        try:
            self.cursor.execute(
                f"INSERT INTO customer (id, password, address) values ('{customer.id}','{customer.password}','{customer.address}');")
        except psycopg2.errors.UniqueViolation as e:
            raise DUPLICATE_ENTITY_EXCEPTION(str(e))
        except psycopg2.errors.CheckViolation as e:
            raise FIELD_REGEX_FAILED(str(e))
        except psycopg2.errors.SyntaxError as e:
            raise SYNTAX_ERROR(str(e))
        except psycopg2.Error as e:
            raise INTERNAL_DATABASE_ERROR(str(e))

    async def get_customer(self, id: str) -> Customer:
        try:
            self.cursor.execute(f"SELECT * FROM customer where id='{id}';")
            res = self.cursor.fetchone()
            if res is None:
                raise ENTITY_NOT_FOUND('customer not found.')
            return Customer(id=res[0], password=res[1], address=res[2])
        except psycopg2.errors.SyntaxError as e:
            raise SYNTAX_ERROR(str(e))
        except psycopg2.Error as e:
            raise INTERNAL_DATABASE_ERROR(str(e))

    async def get_password_less_customer(self, id: str):
        password_less_customer = await self.get_customer(id=id)
        password_less_customer.password = None
        return password_less_customer

    async def update_customer(self, id: str, new_id: str = None, new_password: str = None, new_address: str = None):
        q = []
        if new_id is not None:
            q.append(f"id = '{new_id}'")
        if new_password is not None:
            q.append(f"password = '{new_password}'")
        if new_address is not None:
            q.append(f"address = '{new_address}'")
        if not q:
            return
        q = ", ".join(q)

        try:
            self.cursor.execute(f"UPDATE customer SET {q} WHERE id = '{id}';")
        except psycopg2.errors.UniqueViolation as e:
            raise DUPLICATE_ENTITY_EXCEPTION(str(e))
        except psycopg2.errors.CheckViolation as e:
            raise FIELD_REGEX_FAILED(str(e))
        except psycopg2.errors.SyntaxError as e:
            raise SYNTAX_ERROR(str(e))
        except psycopg2.Error as e:
            raise INTERNAL_DATABASE_ERROR(str(e))

    async def delete_customer(self, id: str):
        try:
            self.cursor.execute(f"DELETE FROM customer where id='{id}';")
        except psycopg2.errors.SyntaxError as e:
            raise SYNTAX_ERROR(str(e))
        except psycopg2.Error as e:
            raise INTERNAL_DATABASE_ERROR(str(e))

    ############################ Restaurant funcs ########################################################
    async def create_restaurant(self, restaurant: Restaurant):
        try:
            self.cursor.execute(
                f"INSERT INTO restaurant (id, password, name, address) values ('{restaurant.id}','{restaurant.password}','{restaurant.name}','{restaurant.address}');")
        except psycopg2.errors.UniqueViolation as e:
            raise DUPLICATE_ENTITY_EXCEPTION(str(e))
        except psycopg2.errors.CheckViolation as e:
            raise FIELD_REGEX_FAILED(str(e))
        except psycopg2.errors.SyntaxError as e:
            raise SYNTAX_ERROR(str(e))
        except psycopg2.Error as e:
            raise INTERNAL_DATABASE_ERROR(str(e))

    async def get_restaurant(self, id: str) -> Restaurant:
        try:
            self.cursor.execute(f"SELECT * FROM restaurant where id='{id}';")
            res = self.cursor.fetchone()
            if res is None:
                raise ENTITY_NOT_FOUND('restaurant not found.')
            return Restaurant(id=res[0], password=res[1], name=res[2], address=res[3])
        except psycopg2.errors.SyntaxError as e:
            raise SYNTAX_ERROR(str(e))
        except psycopg2.Error as e:
            raise INTERNAL_DATABASE_ERROR(str(e))

    async def get_password_less_restaurant(self, id: str):
        password_less_restaurant = await self.get_restaurant(id=id)
        password_less_restaurant.password = None
        return password_less_restaurant

    async def update_restaurant(self, id: str, new_id: str = None, new_password: str = None, new_name: str = None,
                                new_address: str = None):
        q = []
        if new_id is not None:
            q.append(f"id = '{new_id}'")
        if new_password is not None:
            q.append(f"password = '{new_password}'")
        if new_name is not None:
            q.append(f"name = '{new_name}'")
        if new_address is not None:
            q.append(f"address = '{new_address}'")
        if not q:
            return
        q = ", ".join(q)

        try:
            self.cursor.execute(f"UPDATE restaurant SET {q} WHERE id = '{id}';")
        except psycopg2.errors.UniqueViolation as e:
            raise DUPLICATE_ENTITY_EXCEPTION(str(e))
        except psycopg2.errors.CheckViolation as e:
            raise FIELD_REGEX_FAILED(str(e))
        except psycopg2.errors.SyntaxError as e:
            raise SYNTAX_ERROR(str(e))
        except psycopg2.Error as e:
            raise INTERNAL_DATABASE_ERROR(str(e))

    async def delete_restaurant(self, id: str):
        try:
            self.cursor.execute(f"DELETE FROM restaurant where id='{id}';")
        except psycopg2.errors.SyntaxError as e:
            raise SYNTAX_ERROR(str(e))
        except psycopg2.Error as e:
            raise INTERNAL_DATABASE_ERROR(str(e))

    async def get_all_restaurants(self) -> list:
        try:
            self.cursor.execute(f"SELECT * FROM restaurant;")
            res = self.cursor.fetchall()
            return [Restaurant(id=f[0], password=f[1], name=f[2], address=f[3]) for f in res]
        except psycopg2.errors.SyntaxError as e:
            raise SYNTAX_ERROR(str(e))
        except psycopg2.Error as e:
            raise INTERNAL_DATABASE_ERROR(str(e))

    ############################ Deliverer funcs ########################################################
    async def create_deliverer(self, deliverer: Deliverer):
        try:
            self.cursor.execute(
                f"INSERT INTO deliverer (id, password, status) values ('{deliverer.id}','{deliverer.password}','{Deliverer_Status.IDLE.value}');")
        except psycopg2.errors.UniqueViolation as e:
            raise DUPLICATE_ENTITY_EXCEPTION(str(e))
        except psycopg2.errors.CheckViolation as e:
            raise FIELD_REGEX_FAILED(str(e))
        except psycopg2.errors.SyntaxError as e:
            raise SYNTAX_ERROR(str(e))
        # TODO: is it needed to add distinct exception for invalid status? and how?
        except psycopg2.Error as e:
            raise INTERNAL_DATABASE_ERROR(str(e))

    async def get_deliverer(self, id: str) -> Deliverer:
        try:
            self.cursor.execute(f"SELECT * FROM deliverer where id='{id}';")
            res = self.cursor.fetchone()
            if res is None:
                raise ENTITY_NOT_FOUND('deliverer not found.')
            return Deliverer(id=res[0], password=res[1], status=res[2])
        except psycopg2.errors.SyntaxError as e:
            raise SYNTAX_ERROR(str(e))
        except psycopg2.Error as e:
            raise INTERNAL_DATABASE_ERROR(str(e))

    async def get_password_less_deliverer(self, id: str):
        password_less_deliverer = await self.get_deliverer(id=id)
        password_less_deliverer.password = None
        return password_less_deliverer

    async def get_deliverers(self, status: Deliverer_Status) -> list():
        try:
            self.cursor.execute(f"SELECT * FROM deliverer where status='{status.value}';")
            res = self.cursor.fetchall()
            return [Deliverer(id=d[0], status=d[2]) for d in res]
        except psycopg2.errors.SyntaxError as e:
            raise SYNTAX_ERROR(str(e))
        except psycopg2.Error as e:
            raise INTERNAL_DATABASE_ERROR(str(e))

    async def update_deliverer(self, id: str, new_id: str = None, new_password: str = None,
                               new_status: Deliverer_Status = None):
        q = []
        if new_id is not None:
            q.append(f"id = '{new_id}'")
        if new_password is not None:
            q.append(f"password = '{new_password}'")
        if new_status is not None:
            q.append(f"status = {new_status.value}")
        if not q:
            return
        q = ", ".join(q)

        try:
            self.cursor.execute(f"UPDATE deliverer SET {q} WHERE id = '{id}';")
        except psycopg2.errors.UniqueViolation as e:
            raise DUPLICATE_ENTITY_EXCEPTION(str(e))
        except psycopg2.errors.CheckViolation as e:
            raise FIELD_REGEX_FAILED(str(e))
        except psycopg2.errors.SyntaxError as e:
            raise SYNTAX_ERROR(str(e))
        # TODO: is it needed to add distinct exception for invalid status? and how?
        except psycopg2.Error as e:
            raise INTERNAL_DATABASE_ERROR(str(e))

    async def delete_deliverer(self, id: str):
        try:
            self.cursor.execute(f"DELETE FROM deliverer where id='{id}';")
        except psycopg2.errors.SyntaxError as e:
            raise SYNTAX_ERROR(str(e))
        except psycopg2.Error as e:
            raise INTERNAL_DATABASE_ERROR(str(e))

    ############################ Food funcs ########################################################
    async def create_food(self, restaurant_id: str, food: Food):
        try:
            # generate a random identifier for the food
            self.cursor.execute(f"SELECT uuid_generate_v1mc();")
            food_id = self.cursor.fetchone()[0]
            self.cursor.execute(
                f"INSERT INTO food (id, name, price, status) values ('{food_id}','{food.name}','{food.price}','{food.status.value}');")
            self.cursor.execute(
                f"INSERT INTO menu (food_id, restaurant_id) values ('{food_id}','{restaurant_id}');")
        except psycopg2.errors.UniqueViolation as e:
            raise DUPLICATE_ENTITY_EXCEPTION(str(e))
        except psycopg2.errors.CheckViolation as e:
            raise FIELD_REGEX_FAILED(str(e))
        except psycopg2.errors.SyntaxError as e:
            raise SYNTAX_ERROR(str(e))
        except psycopg2.Error as e:
            raise INTERNAL_DATABASE_ERROR(str(e))

    async def get_food(self, id: str) -> Food:
        try:
            self.cursor.execute(f"SELECT * FROM food where id='{id}';")
            res = self.cursor.fetchone()
            if res is None:
                raise ENTITY_NOT_FOUND('food not found.')
            return Food(id=res[0], name=res[1], price=res[2], status=res[3])
        except psycopg2.errors.SyntaxError as e:
            raise SYNTAX_ERROR(str(e))
        except psycopg2.Error as e:
            raise INTERNAL_DATABASE_ERROR(str(e))

    async def get_foods(self, restaurant_id: str) -> list:
        try:
            self.cursor.execute(
                f"SELECT * FROM food where id IN (SELECT food_id FROM menu where restaurant_id = '{restaurant_id}');")
            res = self.cursor.fetchall()
            return [Food(id=f[0], name=f[1], price=f[2], status=f[3]) for f in res]
        except psycopg2.errors.SyntaxError as e:
            raise SYNTAX_ERROR(str(e))
        except psycopg2.Error as e:
            raise INTERNAL_DATABASE_ERROR(str(e))

    async def update_food(self, id: str, new_name: str = None, new_price: str = None, new_status: Food_Status = None):
        q = []
        if new_name is not None:
            q.append(f"name = '{new_name}'")
        if new_price is not None:
            q.append(f"price = '{new_price}'")
        if new_status is not None:
            q.append(f"status = {new_status.value}")
        if not q:
            return
        q = ", ".join(q)

        try:
            self.cursor.execute(f"UPDATE food SET {q} WHERE id = '{id}';")
        except psycopg2.errors.CheckViolation as e:
            raise FIELD_REGEX_FAILED(str(e))
        except psycopg2.errors.SyntaxError as e:
            raise SYNTAX_ERROR(str(e))
        except psycopg2.Error as e:
            raise INTERNAL_DATABASE_ERROR(str(e))

    async def delete_food(self, id: str):
        try:
            self.cursor.execute(f"DELETE FROM food where id='{id}';")
        except psycopg2.errors.SyntaxError as e:
            raise SYNTAX_ERROR(str(e))
        except psycopg2.Error as e:
            raise INTERNAL_DATABASE_ERROR(str(e))

    ############################ Order funcs ########################################################
    async def create_order(self, order: Order):
        try:
            # generate a random identifier for the order
            self.cursor.execute(f"SELECT uuid_generate_v1mc();")
            order_id = self.cursor.fetchone()[0]
            self.cursor.execute(
                f"INSERT INTO food_order (id, customer_id, restaurant_id, timestamp, status) values\
                    ('{order_id}','{order.customer.id}','{order.restaurant.id}','{order.timestamp}','{order.status.value}');")
            for item in order.items:
                self.cursor.execute(
                    f"INSERT INTO order_items (order_id, food_id, quantity) values ('{order_id}','{item.food_id}','{item.quantity}');")
        except psycopg2.errors.UniqueViolation as e:
            raise DUPLICATE_ENTITY_EXCEPTION(str(e))
        except psycopg2.errors.CheckViolation as e:
            raise FIELD_REGEX_FAILED(str(e))
        except psycopg2.errors.SyntaxError as e:
            raise SYNTAX_ERROR(str(e))
        except psycopg2.Error as e:
            raise INTERNAL_DATABASE_ERROR(str(e))

    async def get_orders(self, status: List[Order_Status], customer_id: str = None, restaurant_id: str = None,
                         deliverer_id: str = None) -> list:
        all_status = [f"status = '{s.value}'" for s in status]
        status_condition = ' or '.join(all_status)
        # Set target entity's name and ID # TODO: May need to be reconsidered
        if customer_id is not None:
            entity_name = 'customer'
            entity_id = customer_id
        elif restaurant_id is not None:
            entity_name = 'restaurant'
            entity_id = restaurant_id
        elif deliverer_id is not None:
            entity_name = 'deliverer'
            entity_id = deliverer_id

        try:
            self.cursor.execute(
                f"SELECT * FROM food_order where {entity_name}_id = '{entity_id}' and ({status_condition});")
            res = self.cursor.fetchall()
            orders = []
            for ent in res:
                try:
                    deliverer = await self.get_password_less_deliverer(ent[3])
                except ENTITY_NOT_FOUND as e:
                    deliverer = None
                orders += [Order(id=ent[0], customer=await self.get_password_less_customer(ent[1]), \
                                 restaurant=await self.get_password_less_restaurant(ent[2]), \
                                 deliverer=deliverer, \
                                 timestamp=ent[4], status=ent[5])]
            return orders
        except psycopg2.errors.SyntaxError as e:
            raise SYNTAX_ERROR(str(e))
        except psycopg2.Error as e:
            raise INTERNAL_DATABASE_ERROR(str(e))

    async def get_order(self, order_id: str) -> Order:
        try:
            self.cursor.execute(f"SELECT * FROM food_order where id = '{order_id}';")
            res = self.cursor.fetchone()
            if res is None:
                raise ENTITY_NOT_FOUND('order not found.')

            try:
                deliverer = await self.get_password_less_deliverer(res[3])
            except ENTITY_NOT_FOUND as e:
                deliverer = None

            self.cursor.execute(f"SELECT * FROM order_items where order_id = '{order_id}';")
            ress = self.cursor.fetchall()
            items = [Order_item(food_id=oi[1], quantity=oi[2]) for oi in ress]

            return Order(id=res[0],
                         customer=await self.get_password_less_customer(res[1]),
                         restaurant=await self.get_password_less_restaurant(res[2]),
                         deliverer=deliverer,
                         timestamp=res[4],
                         items=items,
                         status=res[5])
        except psycopg2.errors.SyntaxError as e:
            raise SYNTAX_ERROR(str(e))
        except psycopg2.Error as e:
            raise INTERNAL_DATABASE_ERROR(str(e))

    async def update_order(self, order_id: str, new_status: Order_Status = None, new_deliverer_id: str = None):
        q = []
        if new_deliverer_id is not None:
            q.append(f"deliverer_id = '{new_deliverer_id}'")
        if new_status is not None:
            q.append(f"status = {new_status.value}")
        if not q:
            return
        q = ", ".join(q)

        try:
            self.cursor.execute(f"UPDATE food_order SET {q} WHERE id = '{order_id}';")
        except psycopg2.errors.CheckViolation as e:
            raise FIELD_REGEX_FAILED(str(e))
        except psycopg2.errors.SyntaxError as e:
            raise SYNTAX_ERROR(str(e))
        except psycopg2.Error as e:
            raise INTERNAL_DATABASE_ERROR(str(e))
