from .ChemNum import ChemNumBuilder

ChemNum4Jupyter = ChemNumBuilder()


def define(*arg):
    return ChemNum4Jupyter.define(*arg)


def exp(*arg):
    return ChemNum4Jupyter.exp(*arg)
