from passlib.context import CryptContext
from fastapi import HTTPException
import databases
from app.models import users, receipts
from app.schemas import UserSchema, UserWithPasswordSchema, ReceiptSchema, Payment, ProductSchema
from app.serializer import ProductSerializer

# This is used to hash passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserCruds:
    def __init__(self, db: databases.Database):
        self.db = db

    async def get_user_by_id(self, id: int):
        user = await self.db.fetch_one(users.select().where(users.c.id == id))
        if user == None:
            raise HTTPException(status_code=404, detail="User with this id does not exist")
        return UserSchema(id=user.id, username=user.username, password=user.password)

    async def get_user_by_username(self, username: str):
        user = await self.db.fetch_one(users.select().where(users.c.username == username))
        if user == None:
            raise HTTPException(status_code=404, detail="User with this username does not exist")
        return UserWithPasswordSchema(id=user.id, username=user.username, password=user.password)

    async def get_user_all(self):
        user_db = await self.db.fetch_all(users.select())
        if user_db == None:
            return None
        return [UserSchema(id=user.id, username=user.username, password=user.password) for
                user in user_db]

    async def create_user(self, new_user: UserWithPasswordSchema):
        user = await self.db.fetch_one(users.select().where(users.c.username == new_user.username))
        if user != None:
            raise HTTPException(status_code=404, detail="User with this username already exists")
        hashed_password = pwd_context.hash(new_user.password)
        query = users.insert().values(username=new_user.username, password=hashed_password)
        await self.db.execute(query)
        return "success"

    async def update_user(self, new_user: UserWithPasswordSchema, username: str):
        query = users.update().values(username=new_user.username, password=pwd_context.hash(new_user.password)).where(
            users.c.username == username)
        await self.db.execute(query)
        return "success"

    async def delete_user(self, username: str):
        query = users.delete().where(users.c.username == username)
        await self.db.execute(query)
        return "success"


class ReceiptCruds:
    def __init__(self, db: databases.Database):
        self.db = db

    async def create_receipt(self, new_receipt: ReceiptSchema, username_from_jwt):
        user = await self.db.fetch_one(users.select().where(users.c.username == username_from_jwt))
        serialized_products = [ProductSerializer(product.name, product.price, product.quantity).to_dict() for product in
                               new_receipt.products]
        query = receipts.insert().values(user_id=user.id, created_at=new_receipt.created_at,
                                         products=serialized_products,
                                         payment_type=new_receipt.payment.type,
                                         payment_amount=new_receipt.payment.amount,
                                         total=new_receipt.total, rest=new_receipt.rest)
        await self.db.execute(query)
        return "success"

    async def delete_receipt(self, id: int):
        query = receipts.delete().where(receipts.c.id == id)
        await self.db.execute(query)
        return "success"

    async def get_users_receipt(self, username_from_jwt):
        user = await self.db.fetch_one(users.select().where(users.c.username == username_from_jwt))
        if user is None:
            return None

        user_receipts = await self.db.fetch_all(receipts.select().where(receipts.c.user_id == user.id))
        receipts_data = []
        for receipt in user_receipts:
            products = [
                ProductSchema(name=product.get('name'), price=product.get('price'), quantity=product.get('quantity'))
                for product in receipt['products']
            ]
            payment = Payment(type=receipt['payment_type'], amount=receipt['payment_amount'])
            receipt_data = ReceiptSchema(products=products, payment=payment, total=receipt['total'],
                                         rest=receipt['rest'], created_at=receipt['created_at'])
            receipts_data.append(receipt_data)

        return receipts_data

    async def get_receipt_by_id(self, receipt_id):
        receipt = await self.db.fetch_one(receipts.select().where(receipts.c.id == receipt_id))
        if receipt is None:
            return None

        products = [
            ProductSchema(name=product.get('name'), price=product.get('price'), quantity=product.get('quantity'))
            for product in receipt['products']
        ]
        payment = Payment(type=receipt['payment_type'], amount=receipt['payment_amount'])
        receipt_data = ReceiptSchema(products=products, payment=payment, total=receipt['total'],
                                     rest=receipt['rest'], created_at=receipt['created_at'])

        return receipt_data

