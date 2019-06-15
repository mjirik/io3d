import pyqtgraph

def params_and_values(p:pyqtgraph.parametertree.Parameter, pth="", dct={}, separator=";"):
    """
    Get dict of all parameters. Key is the path to the parameter, value is value of the parameter.
    :param p:
    :param pth:
    :param dct:
    :param separator:  default ";"
    :return:
    """
    for name in p.getValues():
        # print(f"name: {name}, type {type(name)}")
        pth = pth + separator + name
        # print(pth)
        ch = p.child(name)
        # print(f"name: {name}, type {type(ch)}")
        if type(ch) is pyqtgraph.parametertree.parameterTypes.SimpleParameter:
            dct[pth] = ch.value()
            # print(pth)
        else:
            params_and_values(ch, pth)

    return dct


