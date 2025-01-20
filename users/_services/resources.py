from typing import Any


class UserResourceService:
    
    def get_by_id(self) -> None:
        ...

    def get_all(self, offset: int, limit: int) -> None:
        ...
    
    def create(self, data: dict[str, Any]) ->None:
        ...
    

    def update(self, data: dict[str, Any]) -> None:
        ...
    
    def delete(self, user_id: int) -> None:
        ...

    