from dsp import dsp_items
from typing import Union
import yaml



class IconRolCol: 
    def __init__(self, r: int, c: int):
        self.__r, self.__c = r, c
    
    @property
    def value(self): 
        return self.__r, self.__c
    
    def __add__(self, rc: "IconRolCol") -> "IconRolCol": 
        r, c = rc.value
        return IconRolCol(
            self.__r + r, 
            self.__c + c
        )
    
    def __repr__(self):
        return str(self.value)
    
    @staticmethod
    def parse_str(string: str): 
        return IconRolCol(*(
            int(i) for i in string.split(", ")
        ))



class IconPos: 
    def __init__(self, pos_dict: dict[Union["IconPos", int], IconRolCol]):
        self.data = pos_dict
    
    @property
    def unpack(self): 
        unpack: dict[int, IconRolCol] = {}
        for k, v in self.data.items(): 
            if isinstance(k, int) or isinstance(k, str): 
                unpack[k] = v
            else: 
                for ke, ve in k.unpack.items(): 
                    unpack[ke] = v + ve
        return unpack

    @staticmethod
    def parse_dicts(raw_dict: dict[str, dict[str, str]]): 
        ip_dict: dict[str, IconPos] = {}

        def add_ip(name: str): 
            init_dict: dict[IconPos | int | str, IconRolCol] = {}
            for k, v in raw_dict[name].items(): 
                try: 
                    idk = int(k)
                except ValueError: 
                    if isinstance(k, str) and k.startswith("$"): 
                        idk = k[1:]
                    else: 
                        idk = get_ip(k)
                init_dict[idk] = IconRolCol.parse_str(v)
            ip_dict[name] = IconPos(init_dict)
        
        def get_ip(name: str): 
            if name not in ip_dict.keys(): 
                add_ip(name)
            return ip_dict[name]

        for k in raw_dict.keys(): 
            get_ip(k)
        return ip_dict



def yaml2icon_pos(path: str, **loading_kwargs): 
    with open(path, 'r', **loading_kwargs) as file:
        yml = yaml.safe_load(file)
    return {
        dsp_items[k]: v.value for k, v in IconPos.parse_dicts(yml)["main"].unpack.items()
    }