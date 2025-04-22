from repositories.repository import PostgreSQLRepository

class UserService:
    def __init__(self, repository):  # Aceitando o repositório como argumento
        self.repository = repository

    def get_all_users(self):
        return self.repository.get_all()

    def get_user(self, user_id: int):
        return self.repository.get_by_id(user_id)

    def update_user(self, user_id: int, data: dict):
        return self.repository.update(user_id, data)

    def delete_user(self, user_id: int):
        return self.repository.delete(user_id)

