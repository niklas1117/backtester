from typing import Protocol 

## broker obides the observer protocol and should implement everything that a 
## broker might do -> should be closesly connected to orders 

class Observer(Protocol):
    def update():
        ...
