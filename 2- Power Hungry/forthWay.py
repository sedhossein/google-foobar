import numpy


def solution(xs):
    temp = list(filter((0).__ne__, xs))
    result = numpy.prod(temp)
    if result < 0:
        result /= max([n for n in temp if n < 0])
    return str(result)
