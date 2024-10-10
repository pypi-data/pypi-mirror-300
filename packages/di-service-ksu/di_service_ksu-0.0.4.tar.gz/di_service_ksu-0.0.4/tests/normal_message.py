from base_message import BaseMessage
from enum_type_message import EnumTypeMessage


class UserNormalMessage(BaseMessage):
    def __init__(self) -> None:
        super().__init__()
        self.__Message:EnumTypeMessage
        self.__TypeMsg:str

    @property
    def TypeMsg(self):
        return self.__TypeMessage
    
    @TypeMsg.setter
    def TypeMsg(self, value:EnumTypeMessage):
        self.__TypeMessage = value

    @property
    def Message(self):
        return self.__Message
    
    @Message.setter
    def Message(self, value:str):
        self.__Message = value
        
    def set_msg(self, msg_type:EnumTypeMessage, msg:str):
        self.__Message = msg
        self.__TypeMsg = msg_type

    def show_message(self):
        match self.__TypeMsg:
            case EnumTypeMessage.Normal:
                print(f"\nNormal: {self.__Message}")
            case _:
                print(f"Unsupported message type")
