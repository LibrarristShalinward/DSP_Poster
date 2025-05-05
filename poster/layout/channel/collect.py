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
from typing import Callable, Generic, Hashable, Iterable, TypeVar



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
            allow_direct: Callable[[T], bool] = lambda con: False, 
            t: type[T] = int
        ):
        self.nrow, self.ncol = rows, cols
        self.allow_direct = allow_direct
        self.setouts = [[SetoutChannel((r, c), t) for c in range(self.ncol)] for r in range(self.nrow)]
        self.froms = [FromChannel(r, t) for r in range(self.nrow)]
        self.trunk = TrunkChannel(t)
        self.gaps = [[GapChannel(t) for __ in range(self.ncol)] for _ in range(self.nrow)]
        self.meta = MetaChannel(t)
        self.tos = [ToChannel(r, t) for r in range(self.nrow)]
        self.arrives = [[ArriveChannel((r, c), t) for c in range(self.ncol)] for r in range(self.nrow)]
    
    def __legal_rc(self, rc: RolCol): 
        r, c = rc
        if r < 0 or r >= self.nrow: 
            raise IndexError(f"Therer's only {self.nrow} rows. ")
        if c < 0 or c >= self.ncol: 
            raise IndexError(f"Therer's only {self.ncol} colonms. ")
    def get_channels(self, 
            setout: RolCol, 
            arrive: RolCol, 
            direct: bool = False
        ) -> list[Channel[T]]: 
        self.__legal_rc(setout), self.__legal_rc(arrive)
        if setout[0] + 1 == arrive[0] or direct: 
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
        chs = self.get_channels(
            setout, arrive, 
            self.allow_direct(((setout, arrive), item))
        )
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

    @property
    def top_cap(self) -> int: 
        return len(self.tos[0].cons)