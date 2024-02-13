from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from app.cruds import UserCruds, pwd_context, ReceiptCruds
from app.database import db
from app.schemas import UserWithPasswordSchema, Payment, ProductSchema, ReceiptSchema
from fastapi import HTTPException
from app.utils import create_access_token, get_username_from_token, refresh_access_token, token_auth_scheme

router = APIRouter()


@router.post("/refresh-token/", tags=["Login"])
async def refresh_token(token: str = Depends(token_auth_scheme)):
    response = JSONResponse(status_code=200, content={
        "access_token": refresh_access_token(token=token)
    })
    return response


@router.post("/user/login/", tags=["Login"])
async def user_login(user: UserWithPasswordSchema):
    user_db = await UserCruds(db=db).get_user_by_username(user.username)
    if pwd_context.verify(user.password, user_db.password):
        return {'access_token': create_access_token(user_db.username)}
    raise HTTPException(status_code=404, detail="User with this id does not exist")


@router.get("/user/get/", tags=["User"])
async def get_by_id(id: int):
    return await UserCruds(db=db).get_user_by_id(id)


@router.get("/user/getall/", tags=["User"])
async def get_all_user():
    return await UserCruds(db=db).get_user_all()


@router.post("/user/register/", tags=["User"])
async def add_user(new_user: UserWithPasswordSchema):
    await UserCruds(db=db).create_user(new_user)
    return {
        "result": "user added successfully"
    }


@router.put("/user/update/", tags=["User"])
async def update_user(new_user: UserWithPasswordSchema, username_from_jwt: str = Depends(get_username_from_token)):
    await UserCruds(db=db).update_user(new_user, username_from_jwt)
    return {
        "result": "user update successfully"
    }


@router.delete("/user/delete/", tags=["User"])
async def delete_user(username_from_jwt: str = Depends(get_username_from_token)):
    await UserCruds(db=db).delete_user(username_from_jwt)
    return {
        "result": "user delete successfully"
    }


@router.post("/receipts/create", tags=["Receipt"])
async def create_receipt(
        products: List[ProductSchema],
        payment: Payment,
        username_from_jwt: str = Depends(get_username_from_token)
):
    total = sum(product.price * product.quantity for product in products)
    rest = payment.amount - total
    if rest < 0: return {"result": "amount is less than total price"}
    await ReceiptCruds(db=db).create_receipt(ReceiptSchema(
        products=products,
        payment=payment,
        total=total,
        rest=rest,
        created_at=datetime.now()
    ), username_from_jwt)
    return {
        "result": "receipt created successfully"
    }


@router.get("/receipts/get_user_receipts", tags=["Receipt"])
async def get_receipts(username_from_jwt: str = Depends(get_username_from_token)):
    return await ReceiptCruds(db=db).get_users_receipt(username_from_jwt)

@router.get("/receipts/get_user_receipt_by_id", tags=["Receipt"])
async def get_receipt_by_id(id: int, username_from_jwt: str = Depends(get_username_from_token)):
    return await ReceiptCruds(db=db).get_receipt_by_id(id)


@router.delete("/receipts/delete_receipts", tags=["Receipt"])
async def delete_receipt(id: int, username_from_jwt: str = Depends(get_username_from_token)):
    return await ReceiptCruds(db=db).delete_receipt(id)
