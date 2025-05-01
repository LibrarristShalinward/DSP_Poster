from .channel import (
    ArriveChannel, 
    Channel, 
    FromChannel, 
    GapChannel, 
    MetaChannel, 
    RolCol, 
    SetoutChannel, 
    ToChannel, 
    TrunkChannel, 
)
from typing import Generic, Hashable, Iterable, TypeVar



T = TypeVar("T", bound = Hashable)
class ChannelCollector(Generic[T]): 
    setouts: list[list[SetoutChannel[T]]]
    froms: list[FromChannel[T]]
    trunk: TrunkChannel[T]
    gaps: list[list[GapChannel[T]]]
    meta: MetaChannel[T]
    tos: list[ToChannel[T]]
    arrives: list[list[ArriveChannel[T]]]
    def __init__(self, 
            rows: int, cols: int, 
            t: type[T] = int
        ):
        self.nrow, self.ncol = rows, cols
        self.setouts = [[SetoutChannel(t) for __ in range(self.ncol)] for _ in range(self.nrow)]
        self.froms = [FromChannel(t) for _ in range(self.nrow)]
        self.trunk = TrunkChannel(t)
        self.gaps = [[GapChannel(t) for __ in range(self.ncol)] for _ in range(self.nrow)]
        self.meta = MetaChannel(t)
        self.tos = [ToChannel(t) for _ in range(self.nrow)]
        self.arrives = [[ArriveChannel(t) for __ in range(self.ncol)] for _ in range(self.nrow)]
    
    def __legal_setout(self, setout: RolCol): 
        if setout[0] < 0 or setout[0] >= self.nrow: 
            raise IndexError(f"Therer's only {self.nrow} rows. ")
        if setout[1] < 0 or setout[1] >= self.ncol: 
            raise IndexError(f"Therer's only {self.ncol} colonms. ")
    
    def __legal_arrive(self, arrive: RolCol): 
        self.__legal_setout(arrive)
        if arrive[0] == 0: 
            raise IndexError(r"Arriving in first row is not allowed. ")

    def get_channels(self, 
            setout: RolCol, 
            arrive: RolCol
        ) -> list[Channel[T]]: 
        self.__legal_setout(setout), self.__legal_arrive(arrive)
        if setout[0] + 1 == arrive[0]: 
            return [
                self.setouts[setout[0]][setout[1]], 
                self.tos[arrive[0]], 
                self.arrives[arrive[0]][arrive[1]], 
            ]
        else: 
            if setout[0] < arrive[0]: 
                trunk = self.trunk
            elif setout[0] == arrive[0]: 
                trunk = self.gaps[setout[0]][setout[1]]
            else: 
                trunk = self.meta
            return [
                self.setouts[setout[0]][setout[1]], 
                self.froms[setout[0]], 
                trunk, 
                self.tos[arrive[0]], 
                self.arrives[arrive[0]][arrive[1]], 
            ]
    
    def add_con(self, 
            setout: RolCol, 
            arrive: RolCol, 
            item: T
        ): 
        chs = self.get_channels(setout, arrive)
        for ch in chs: ch + item
    
    def add_cons(self, 
            setouts: Iterable[RolCol], 
            arrives: Iterable[RolCol], 
            item: T
        ): 
        setouts_ = set(setouts)
        arrives_ = set(arrives)
        for s in set(setouts_): 
            for a in set(arrives_): 
                self.add_con(s, a, item)
    
    # 通道宽度需求属性
    @property
    def gap_cap(self) -> int: 
        return max(
            max(
                len(c) for c in cs
            ) for cs in self.gaps
        )
    
    @property
    def inner_cap(self) -> int: 
        return max(
            len(i1.cons) + len(i2.cons) for i1, i2 in zip(
                self.froms, 
                self.tos[1:] + [ToChannel(T)]
            )
        )
    
    @property
    def left_cap(self) -> int: 
        return len(self.trunk)
    
    @property
    def right_cap(self) -> int: 
        return len(self.meta)