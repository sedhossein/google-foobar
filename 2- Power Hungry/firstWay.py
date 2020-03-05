def solution(xs):
    posArray = []
    negArray = []

    # remove zeros and separate neg/pos digits
    for v in xs:
        if v < 0:
            negArray += [v]
        elif v > 0:
            posArray += [v]

    negArrayLen = len(negArray)
    posArrayLen = len(posArray)

    # detect empty/singe negative input
    if posArrayLen == 0 and (negArrayLen == 0 or negArrayLen == 1):
        return "0"

    # detect single positive input
    if posArrayLen == 1 and negArrayLen == 0:
        return str(posArray[0])

    # considering `neg*neg=pos`
    if negArrayLen % 2 == 1 and negArrayLen >= 1:
        negArray.remove(max(negArray))

    # calculate the power
    res = 1
    array = negArray + posArray
    for i in array:
        res *= i

    return str(res)
