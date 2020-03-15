def countLuckyTriples(list, listLen):
    tripleCnt = 0
    for i in range(1, listLen - 1):
        xCnt = [x for x in list[:i] if list[i] % x == 0]
        zCnt = [z for z in list[i + 1:] if z % list[i] == 0]

        tripleCnt += len(xCnt) * len(zCnt)

    return tripleCnt


def solution(l):
    lLen = len(l)
    if lLen < 3:
        return 0

    return countLuckyTriples(l, lLen)


print(solution([1, 1, 1]))
