import numpy as np
from IPython.display import display, Markdown
import copy


def printMarkdown(txt):
    display(Markdown("$" + txt + "$"))


class ChemNumBuilder():
    def __init__(self, printfunction=printMarkdown):
        self.pf = printfunction

    def define(
            self,
            number,
            units=dict(),
            expr=dict(),
            sig_digits=3,
            label=None):
        if type(units) == str:
            units = {units: 1}
        if type(expr) == str:
            units = {expr: 1}
        return ChemNum(number, units, expr, self.pf, sig_digits, label)

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
    def __init__(self, number, units, expr, pf, sig_digits, label):
        """
        - number:float
        - unit:dict:key=name:value=dimention
        """
        self.num = number
        self.units = units
        self.expr = expr
        self.print = pf
        self.label = label
        self.degF2degC()
        self.degC2K()
        self.forceSI()
        self.sig_digits = sig_digits

    def setlabel(self, label):
        self.label = label

    def setdigits(self, digits):
        self.sig_digits = digits

    def resetlabel(self,):
        self.label = None

    def degC2K(self,):
        if self.units == {"degC": 1}:
            self.num += 273.15
            self.units = {"K": 1}

    def degF2degC(self,):
        if self.units == {"degF": 1}:
            self.num = (self.num - 32) * 5 / 9
            self.units = {"degC": 1}

    def forceSI(self, soft=True):
        defaultDict = {
            "mg": (1e-6, ("kg", 1)),
            "g": (1e-3, ("kg", 1)),
            "atm": (101325, ("Pa", 1)),
            "%": (1e-2, ()),
            "ton": (1e3, ("kg", 1)),
            "kJ": (1e3, ("J", 1)),
            "cp": (1e-3, (("Pa", 1), ("s", 1))),
            "day": (24 * 3600, ("s", 1)),
            "mm": (1e-3, ("m", 1)),
            "km": (1e3, ("m", 1)),
            "cm": (1e-2, ("m", 1)),
            "L": (1e-3, ("m", 3)),
            "mL": (1e-6, ("m", 3)),
            "inch": (2.54e-2, ("m", 1)),
            "foot": (30.48e-2, ("m", 1)),
            "feet": (30.48e-2, ("m", 1)),
            "yard": (0.9144, ("m", 1)),
            "mile": (1609, ("m", 1)),
            "lb": (0.45359237, ("kg", 1)),
            "oz": (28.349523125e-3, ("kg", 1)),
            "gr": (0.06479891e-3, ("kg", 1)),
            "impgal": (4.54609e-3, ("m", 3)),
            "impqt": (1.137e-3, ("m", 3)),
            "imppt": (568.3e-6, ("m", 3)),
            "gal": (3.785412e-3, ("m", 3)),
            "qt": (3.785412e-3 / 4, ("m", 3)),
            "pt": (3.785412e-3 / 8, ("m", 3))
        }
        self.convertUnits(defaultDict)

    def convertUnits(self, dct):
        cnvtarget = set(self.units.keys()) & set(dct.keys())
        for unt in cnvtarget:
            self.num *= dct[unt][0]**self.units[unt]
            if len(dct[unt][1]) != 0 and not isinstance(dct[unt][1][0], tuple):
                dct[unt] = (dct[unt][0], (dct[unt][1],))
            for tmp in dct[unt][1]:
                new_unit, new_dim = tmp
                if new_unit in self.units.keys():
                    self.units[new_unit] += new_dim * self.units[unt]
                else:
                    self.units[new_unit] = new_dim * self.units[unt]
            del self.units[unt]

    def subs(self, vars, inplace=False):
        cnvtarget = set(self.expr.keys()) & set(vars.keys())
        new = self._copy()
        for key in cnvtarget:
            new *= vars[key]**new.expr[key]
            del new.expr[key]
        if inplace:
            self = new
        else:
            return new

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
        if isinstance(othr, int) or isinstance(othr, float):
            self._check_zerounit(self)
            new.num += othr
            return new
        elif isinstance(othr, ChemNum):
            new._check_sameunit(othr)
            new.num += othr.num
            return new

    def __sub__(self, othr):
        new = self._copy()
        if isinstance(othr, int) or isinstance(othr, float):
            self._check_zerounit(self)
            new.num -= othr
            return new
        elif isinstance(othr, ChemNum):
            new._check_sameunit(othr)
            new.num -= othr.num
            return new

    @staticmethod
    def _muldiv(cn1, cn2, isMul=True):
        for key in cn2.keys():
            if key in cn1.keys():
                if isMul:
                    cn1[key] += cn2[key]
                else:
                    cn1[key] -= cn2[key]
            else:
                if isMul:
                    cn1[key] = cn2[key]
                else:
                    cn1[key] = -cn2[key]
        nu_items = list(cn1.items())
        for k, v in nu_items:
            if v == 0:
                del cn1[k]
        return cn1

    def __mul__(self, othr):
        new = self._copy()
        if isinstance(othr, int) or isinstance(othr, float):
            new.num *= othr
            return new
        elif isinstance(othr, ChemNum):
            new.num *= othr.num
            new.units = self._muldiv(new.units, othr.units, True)
            new.expr = self._muldiv(new.expr, othr.expr, True)
            return new

    def __truediv__(self, othr):
        new = self._copy()
        if isinstance(othr, int) or isinstance(othr, float):
            new.num /= othr
            return new
        elif isinstance(othr, ChemNum):
            new.num /= othr.num
            new.units = self._muldiv(new.units, othr.units, False)
            new.expr = self._muldiv(new.expr, othr.expr, False)
            return new

    def __pow__(self, pownum):
        new = self._copy()
        new._check_zerounit(pownum)
        new.num = new.num**pownum
        for unt in new.units.keys():
            new.units[unt] *= pownum
        return new

    def __str__(self, n=None):
        """
        n:int:number of digits:
        """
        if n is not None:
            digits = n
        else:
            digits = self.sig_digits
        if self.label is not None:
            pre = f"{self.label}: "
        else:
            pre = ""
        end = ""
        for k, v in self.units.items():
            end += r"\, "
            if v == 1:
                end += k + " "
            else:
                end += k + "^{" + str(v) + "} "
        for k, v in self.expr.items():
            end += r"\, "
            if v == 1:
                end += k + " "
            else:
                end += k + "^{" + str(v) + "} "
        main = "{:." + str(digits) + "e} "
        main = main.format(self.num)
        n, p = main.split("e")
        p = int(p)
        if p == 0:
            power = ""
        else:
            power = "\\times 10^{" + str(p) + "}"
        main = n + power
        return pre + main + end + ""

    def _copy(self,):
        new = copy.deepcopy(self)
        new.resetlabel()
        return new

    def __repr__(self,):
        self.print(self.__str__())
        return ""

    def __float__(self,):
        return float(self.num)

    def show(self, n):
        self.print(self.__str__(n))
