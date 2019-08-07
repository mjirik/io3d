import pyqtgraph

def params_and_values(p:pyqtgraph.parametertree.Parameter, pth=None, dct={}, separator=";"):
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
        if pth is not None:
            pth_local = pth + separator + name
        else:
            pth_local = name
        # print(pth)
        ch = p.child(name)
        # print(f"name: {name}, type {type(ch)}")
        if type(ch) is pyqtgraph.parametertree.parameterTypes.SimpleParameter:
            dct[pth_local] = ch.value()
            # print(pth)
        else:
            params_and_values(ch, pth_local)

    return dct
