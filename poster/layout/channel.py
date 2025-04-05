from typing import Generic, Hashable, TypeVar
from abc import ABC



T = TypeVar("T", bound = Hashable)
class Channel(ABC, Generic[T]): 
    cons: set[T]
    def __init__(self, t: type[T] = int):
        self.cons = set()
    
    def __add__(self, con: T): 
        self.cons.add(con)
        return self
    


class SetoutChannel(Channel[T]): 
    """出发通道"""



class ToChannel(Channel[T]): 
    """迁出通道"""



class TrunkChannel(Channel[T]): 
    """纵向主通道"""



class GapChannel(Channel[T]): 
    """纵向间隙通道"""



class MetaChannel(Channel[T]): 
    """纵向副通道"""



class FromChannel(Channel[T]): 
    """迁入通道"""



class ArriveChannel(Channel[T]): 
    """到达通道"""