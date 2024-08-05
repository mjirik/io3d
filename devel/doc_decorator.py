def is_documented_by(original):
    def wrapper(target):
        target.__doc__ = original.__doc__
        return target

    return wrapper


def one_fcn(a, b, c):
    """

    :param a: acko
    :param b: becko
    :param c: ceko
    :return:
    """


@is_documented_by(one_fcn)
def second(a, b, c):
    pass


help(second)
