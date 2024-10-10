import sys
from pathlib import Path
sys.path.insert(0,str(Path(sys.path[0]).parent))

from example_package_alitrix1.Abstractions.base_di_container import BaseDIConteiner
from example_package_alitrix1.Abstractions.base_service_collection import BaseServiceCollection
from example_package_alitrix1.service_collection import ServiceCollection

from base_random_uuid import BaseRandomGUID
from base_message import BaseMessage
from base_composit import BaseComposit
from user_random_id import UserRndGUID
from normal_message import UserNormalMessage
from generate_uuid_print import GenerateUuidAndPrint


def registration_services(services:BaseServiceCollection)->None:
    services.RegisterSingleton(BaseRandomGUID, UserRndGUID) 
    services.RegisterSingleton(BaseMessage, UserNormalMessage)
    services.RegisterTransient(BaseComposit, GenerateUuidAndPrint)

def sample1(services:BaseServiceCollection):
    
    container:BaseDIConteiner = services.GenerateContainer() # Get dependency container

    composit0:BaseComposit = container.GetService(BaseComposit) # Get an instance of the service by the specified base class
    msg = composit0.run_once()
    print(f"Composit0 Return value: {msg.Message}")

    composit1:BaseComposit = container.GetService(BaseComposit) # Get an instance of the service by the specified base class
    msg = composit1.run_once()
    print(f"Composit1 Return value: {msg.Message}")

    rnd = container.GetService(BaseRandomGUID)
    print(f"Get random value uuid4: {rnd.get_next()}") # Get an instance of the service by the specified base class

if __name__ == "__main__":
    services:BaseServiceCollection = ServiceCollection() # Dependency Services
    registration_services(services) # Dependency registration
    sample1(services) # Example use getting dependency service 