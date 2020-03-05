def solution(xs):
    posArray = []
    negArray = []

    # remove zeros and separate neg/pos digits
    for v in xs:
        if v < 0:
            negArray += [v]
        elif v > 0:
            posArray += [v]

    # detect empty/singe negative input
    if len(posArray) == 0 and (len(negArray) == 0 or len(negArray) == 1):
        return "0"

    # detect single positive input
    if len(posArray) == 1 and len(negArray) == 0:
        return str(posArray[0])

    # considering `neg*neg=pos`
    if len(negArray) % 2 != 0:
        negArray.remove(max(negArray))

    # calculate the power
    res = 1
    array = negArray + posArray
    for i in array:
        res *= i

    return str(res)


print(solution([-1, -2, -3, 1]))
print(solution([-2, -3, 4, -5]))
print(solution([2, 0, 2, 2, 0]))
