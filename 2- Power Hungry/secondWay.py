def solution(xs):
    maxNeg = -9999999
    count = 0
    countNeg = 0
    res = "1"

    for i in xs:
        if i == 0:
            continue

        count += 1
        if i < 0:
            countNeg += 1
            if maxNeg < i:
                maxNeg = i

        res = str(int(res) * i)

    if countNeg == 1 and count == 1:
        return "0"

    if countNeg % 2 == 1:
        res = str(int(res) / maxNeg)

    return str(res) if count > 0 else "0"


print(solution([0]) == "0")
print(solution([2]) == "2")
print(solution([-2]) == "0")
print("===========================")
print(solution([0, 0]) == "0")
print(solution([-2, 0]) == "0")
print(solution([2, 0]) == "2")
print(solution([-2, 2]) == "2")
print(solution([-2, -2]) == "4")
print(solution([2, 2]) == "4")
print("===========================")
print(solution([0, 0, 0]) == "0")
print(solution([0, 0, 2]) == "2")
print(solution([0, 2, 2]) == "4")
print(solution([2, 2, 2]) == "8")
print(solution([-2, -2, -2]) == "4")
print(solution([0, -2, -2]) == "4")
print(solution([0, 0, -2]) == "0")
print(solution([0, 0, 0]) == "0")
print(solution([2, 2, -2]) == "4")
print(solution([2, -2, -2]) == "8")
print("===========================")
print(solution([0, 0, 0, 0]) == "0")
print(solution([0, 0, 0, -2]) == "0")
print(solution([0, 0, -2, -2]) == "4")
print(solution([0, -2, -2, -2]) == "4")
print(solution([-2, -2, -2, -2]) == "16")
print(solution([2, 2, 2, 2]) == "16")
print(solution([2, 2, 2, 0]) == "8")
print(solution([2, 2, 0, 0]) == "4")
print(solution([2, 0, 0, 0]) == "2")
print(solution([2, -2, 2, -2]) == "16")
print(solution([2, -2, 0, -2]) == "8")
print(solution([2, 2, 0, -2]) == "4")
print(solution([2, -2, 0, 0]) == "2")
