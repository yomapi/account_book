from user.repositories import user_repo, token_repo
from providers.auth_provider import auth_provider


class UserService:
    def sign_up(self, email: str, password: str):
        password = auth_provider.hashpw(password)
        return user_repo.create({"email": email, "password": password})

    def login(self, email: str, password: str) -> str:
        return {"access": auth_provider.login(email, password)}

    def logout(self, user_id: str):
        token_repo.delete_by_user_id(user_id)
        return True


user_service = UserService()
