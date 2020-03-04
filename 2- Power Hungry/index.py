def solution(xs):
    posArray = []
    negArray = []
    neg2posArray = []

    # detect special single values
    if len(xs) == 1:
        if xs[0] > 0:
            return str(xs[0])
        else:
            return "0"

    # remove zeros and separate neg/pos digits
    for v in xs:
        if v <= -1:
            negArray += [v]
        elif v >= 1:
            posArray += [v]

    # detect single negative input
    if len(posArray) == 0 and len(negArray) == 1:
        return "0"

    # considering `neg*neg=pos`
    if len(negArray) % 2 != 0:
        negArray = sorted(negArray)
        negArray.pop()

    # convert negative digits to positive
    for v in negArray:
        neg2posArray += [v * -1]

    # calculate the power
    res = "1"
    array = neg2posArray + posArray
    for i in array:
        res = str(int(res) * i)

    return res
