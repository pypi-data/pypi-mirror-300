from etiket_client.remote.client import client
from etiket_client.remote.endpoints.models.user import UserReadWithScopes, UserCreate

def create_user(data: UserCreate):
    client.post("/user/", json_data=data.model_dump(mode="json"))
    

def user_read_me() -> UserReadWithScopes:
    response = client.get("/user/me/")
    return UserReadWithScopes.model_validate(response)