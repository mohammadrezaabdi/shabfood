from model.schema import *


class DBD:
    # Customer
    async def create_customer(self, customer: Customer): pass

    async def get_customer(self, id: str) -> Customer: pass

    async def update_customer(self, id: str, new_id: str = None, new_password: str = None,
                              new_address: str = None): pass

    async def delete_customer(self, id: str): pass

    # Deliverer

    async def create_deliverer(self, deliverer: Deliverer): pass

    async def get_deliverer(self, id: str) -> Deliverer: pass

    async def get_deliverers(self, status: Deliverer_Status) -> list(): pass

    async def update_deliverer(self, id: str, new_id: str = None, new_password: str = None,
                               new_status: Deliverer_Status = None): pass

    async def delete_deliverer(self, id: str): pass

    # Restaurant

    async def create_restaurant(self, restaurant: Restaurant): pass

    async def get_restaurant(self, id: str) -> Restaurant: pass

    async def get_restaurants(self) -> list: pass

    async def update_restaurant(self, id: str, new_id: str = None, new_password: str = None, new_name: str = None,
                                new_address: str = None): pass

    async def delete_restaurant(self, id: str): pass

    # Food

    async def create_food(self, restaurant_id: str, food: Food): pass

    async def get_food(self, id: str) -> Food: pass

    # Showing menu of the restaurant
    async def get_foods(self, restaurant_id: str) -> list: pass

    async def update_food(self, id: str, new_name: str = None, new_price: str = None,
                          new_status: Food_Status = None): pass

    async def delete_food(self, id: str): pass

    # Order

    async def create_order(self, order: Order): pass

    async def get_order(self, id: str) -> Order: pass

    async def get_orders(
            self, status: List[Order_Status], customer_id: str = None, restaurant_id: str = None,
            deliverer_id: str = None) -> list: pass

    async def update_order(
            self, id: str, new_status: Order_Status = None, new_deliverer_id: str = None): pass
