from uuid import UUID, uuid4
from base_random_uuid import BaseRandomGUID

class UserRndGUID(BaseRandomGUID):
    def __init__(self) -> None:
        super().__init__()
        self.__init_rnd = uuid4()
    
    def get_id(self)->UUID:
        return self.__init_rnd
    
    def get_next(self)->UUID:
        self.__init_rnd = uuid4()
        return self.get_id()