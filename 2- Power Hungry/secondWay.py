def solution(xs):
    maxNeg = -9999999
    count = 0
    countNeg = 0
    res = 1

    for i in xs:
        if i == 0:
            continue

        count += 1
        if i < 0:
            countNeg += 1
            if maxNeg < i:
                maxNeg = i

        res *= i

    if countNeg == 1:
        return "0"

    if countNeg % 2 == 1:
        res /= maxNeg

    return str(res) if count > 0 else "0"
