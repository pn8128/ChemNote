import numpy as np


class ChemNum():
    def __init__(self, number, units):
        """
        - number:float
        - unit:dict:key=name:value=dimention
        """
        self.num = number
        self.units = units

    def forceSI(self, soft=True):
        defaultDict = {
            "g": (1e-3, (("kg", 1))),
            "atm": (101325, (("Pa"))),
            "%": (1e-2, ()),
            "ton": (1e3, (("kg", 1))),
            "kJ": (1e3, (("J", 1))),
            "cp": (1e-3, (("Pa", 1), ("s", 1))),
            "day": (24 * 3600, (("s", 1)))
        }
        self.convertUnits(defaultDict)

    def convertUnits(self, dct):
        cnvtarget = set(self.units.keys()) & set(dct.keys())
        for unt in cnvtarget:
            self.num *= dct[unt][0]**self.units[unt]
            new_unit, new_dim = dct[unt][1]
            if new_unit in self.units.keys():
                self.units[new_unit] += new_dim * self.units[unt]
            else:
                self.units[new_unit] = new_dim * self.units[unt]
            del self.units[unt]

    def _check_sameunit(self, othr):
        if not self.units == othr.units:
            raise TypeError("dimention or unit differ")

    @staticmethod
    def _check_zerounit(othr):
        if isinstance(othr, ChemNum):
            if len(othr.units) != 0:
                raise TypeError("Power number must not have dimention")
        elif isinstance(othr, int) or isinstance(othr, float):
            pass
        else:
            raise TypeError("Power number must be int,float or ChemNum")

    def __add__(self, othr):
        self._check_sameunit()
        self.num += othr.num

    def __mul__(self, othr):
        self.num *= othr.num
        for unt in othr.units.keys():
            if unt in self.units.keys():
                self.units[unt] += othr.units[unt]
            else:
                self.units[unt] = othr.units[unt]
        for k, v in self.units.items():
            if v == 0:
                del self.units[k]

    def __truediv__(self, othr):
        self.num /= othr.num
        for unt in othr.units.keys():
            if unt in self.units.keys():
                self.units[unt] -= othr.units[unt]
            else:
                self.units[unt] = othr.units[unt]
        for k, v in self.units.items():
            if v == 0:
                del self.units[k]

    def __pow__(self, pownum):
        self._zerounit(pownum)
        self.num = self.num**pownum
        for unt in self.units.keys():
            self.units[unt] *= pownum

    @staticmethod
    def exp(othr):
        if isinstance(othr, ChemNum):
            if len(othr.units) != 0:
                raise TypeError("Power number must not have dimention")
            return np.exp(othr.num)
        elif isinstance(othr, int) or isinstance(othr, float):
            return np.exp(othr)
        else:
            raise TypeError("Power number must be int,float or ChemNum")

    def show(self, n=3, label=""):
        """
        n:int:number of digits:
        """
        if len(label):
            pre = f"{label} is "
        else:
            pre = ""
        end = ""
        for k, v in self.units.items():
            if v == 1:
                end += k + " "
            else:
                end += k + "^{" + str(v) + "} "
        main = "{:." + str(n) + "e} "

        print(pre + main.format(self.num) + end + "$")
