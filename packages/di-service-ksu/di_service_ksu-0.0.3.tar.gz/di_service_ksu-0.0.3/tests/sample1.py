import sys
from pathlib import Path
sys.path[0] = str(Path(sys.path[0]).parent)

from example_package_alitrix1.Services.provider_service import ProviderService, DataModelView
from example_package_alitrix1.Decorators import ExtDecorators

@ExtDecorators.init_inject
def test():
    print(f"{test.__dict__}:SELF")

def sample1():
    data = DataModelView('Message from Test')
    provider = ProviderService("Test name", data)
    result = provider.get_info()

    print(f"Resultat class :{result}\n")

    test()


if __name__ == "__main__":
    sample1()