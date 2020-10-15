import numpy as np
from IPython.display import display, Markdown
import copy


class ChemNumBuilder():
    def __init__(self, printfunction=print):
        self.pf = printfunction

    def define(self, number, units=dict(), label=None):
        if type(units) == str:
            units = {units: 1}
        return ChemNum(number, units, self.pf, label)

    @staticmethod
    def printMarkdown(txt):
        display(Markdown(txt))

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


class ChemNum():
    def __init__(self, number, units, pf, label):
        """
        - number:float
        - unit:dict:key=name:value=dimention
        """
        self.num = number
        self.units = units
        self.print = pf
        self.label = label
        self.degC2K()
        self.forceSI()

    def setlabel(self, label):
        self.label = label

    def resetlabel(self,):
        self.label = None

    def degC2K(self,):
        if self.units == {"degC": 1}:
            self.num += 273.15
            self.units = {"K": 1}

    def forceSI(self, soft=True):
        defaultDict = {
            "mg": (1e-6, (("kg", 1))),
            "g": (1e-3, (("kg", 1))),
            "atm": (101325, (("Pa"))),
            "%": (1e-2, ()),
            "ton": (1e3, (("kg", 1))),
            "kJ": (1e3, (("J", 1))),
            "cp": (1e-3, (("Pa", 1), ("s", 1))),
            "day": (24 * 3600, (("s", 1))),
            "mm": (1e-3, (("m", 1))),
            "km": (1e3, (("m", 1))),
            "cm": (1e-2, (("m", 1))),
            "L": (1e-3, (("m", 3)))
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
            print(
                '\033[31m' +
                'units or their dimention are not same' +
                '\033[0m')
            raise TypeError("dimention or unit differ")

    @staticmethod
    def _check_zerounit(othr):
        if isinstance(othr, ChemNum):
            if len(othr.units) != 0:
                print(
                    '\033[31m' +
                    'You cant put number with unit as an input of power' +
                    '\033[0m')
                raise TypeError()
        elif isinstance(othr, int) or isinstance(othr, float):
            pass
        else:
            print(
                '\033[31m' +
                'Input have to be int,float or ChemNum class ' +
                '\033[0m')
            raise TypeError()

    def __add__(self, othr):
        new = self._copy()
        new._check_sameunit(othr)
        new.num += othr.num
        return new

    def __sub__(self, othr):
        new = self._copy()
        new._check_sameunit(othr)
        new.num -= othr.num
        return new

    def __mul__(self, othr):
        new = self._copy()
        new.num *= othr.num
        for unt in othr.units.keys():
            if unt in new.units.keys():
                new.units[unt] += othr.units[unt]
            else:
                new.units[unt] = othr.units[unt]
        nu_items = list(new.units.items())
        for k, v in nu_items:
            if v == 0:
                del new.units[k]
        return new

    def __truediv__(self, othr):
        new = self._copy()
        new.num /= othr.num
        for unt in othr.units.keys():
            if unt in new.units.keys():
                new.units[unt] -= othr.units[unt]
            else:
                new.units[unt] = othr.units[unt]
        nu_items = list(new.units.items())
        for k, v in nu_items:
            if v == 0:
                del new.units[k]
        return new

    def __pow__(self, pownum):
        new = self._copy()
        new._check_zerounit(pownum)
        new.num = new.num**pownum
        for unt in new.units.keys():
            new.units[unt] *= pownum
        return new

    def show(self, n=3):
        """
        n:int:number of digits:
        """
        if self.label is not None:
            pre = f"${self.label}: "
        else:
            pre = "$"
        end = ""
        for k, v in self.units.items():
            end += r"\, "
            if v == 1:
                end += k + " "
            else:
                end += k + "^{" + str(v) + "} "
        main = "{:." + str(n) + "e} "
        main = main.format(self.num)
        n, p = main.split("e")
        p = int(p)
        if p == 0:
            power = ""
        else:
            power = "\\times 10^{" + str(p) + "}"
        main = n + power
        self.print(pre + main + end + "$")

    def _copy(self,):
        new = copy.deepcopy(self)
        new.resetlabel()
        return new
