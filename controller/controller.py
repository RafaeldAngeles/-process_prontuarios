from fastapi import APIRouter, Depends, HTTPException
from repositories.repository import PostgreSQLRepository
from service.service import UserService
from models.user import User
from typing import List

router = APIRouter()

def get_service():
    repo = PostgreSQLRepository()
    return UserService(repo)

@router.get("/", response_model=List[User])
def get_all(service: UserService = Depends(get_service)):
    return service.get_all_users()

@router.get("/{user_id}", response_model=User)
def get_by_id(user_id: int, service: UserService = Depends(get_service)):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

@router.patch("/{user_id}")
def update_user(user_id: int, data: dict, service: UserService = Depends(get_service)):
    service.update_user(user_id, data)
    return {"message": "Usuário atualizado com sucesso"}

@router.delete("/{user_id}")
def delete_user(user_id: int, service: UserService = Depends(get_service)):
    service.delete_user(user_id)
    return {"message": "Usuário deletado com sucesso"}
