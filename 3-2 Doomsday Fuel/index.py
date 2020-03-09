from __future__ import division
from fractions import Fraction
from fractions import gcd  # or can import gcd from `math` in Python 3
import numpy


def getTerminalStates(states):
    terminalStates = []
    for stateNumber, state in enumerate(states):
        if sum(state) == 0:
            terminalStates.append(stateNumber)

    return terminalStates


def getNonTerminalStates(states):
    nonTerminalStates = []
    for stateNumber, state in enumerate(states):
        if sum(state) != 0:
            nonTerminalStates.append(stateNumber)

    return nonTerminalStates


def getMarkovChainsMatrix(states):
    chainStates = getNonTerminalStates(states)
    chainStatesLen = len(chainStates)
    markovProbabilitiesMatrix = makeAxBMatrix(chainStatesLen, chainStatesLen)

    for stateNumber, state in enumerate(states):
        if stateNumber not in chainStates:
            continue

        for destination, probability in enumerate(state):
            if destination not in chainStates:
                continue

            x, y = pathForQMatrix(stateNumber, destination, states)
            markovProbabilitiesMatrix[x][y] = Fraction(probability, sum(state))
            # markovProbabilitiesMatrix[stateNumber][destination] = Fraction(probability, sum(state))

    return markovProbabilitiesMatrix


def pathForQMatrix(row, column, states):
    nonTerminalStates = getNonTerminalStates(states)
    if row not in nonTerminalStates or column not in nonTerminalStates:
        raise RuntimeWarning("pathFor: invalid request received")

    x, y = 0, 0
    for index, value in enumerate(nonTerminalStates):
        if value == row:
            x = index
        if value == column:
            y = index

    return x, y


def makeIMatrix(count):
    matrix = []
    index = 0
    while index < count:
        innerIndex = 0
        matrix.append([])
        while innerIndex < count:
            matrix[index].append(1 if index == innerIndex else 0)
            innerIndex += 1
        index += 1

    return matrix


def minusMatrix(a, b):
    aLen = len(a)
    bLen = len(b)

    if aLen != bLen:
        raise RuntimeWarning("minusMatrix: can not minus passed matrix")

    matrix = makeAxBMatrix(aLen, len(a[0]))
    index = 0

    count = len(a)
    while index < count:
        innerIndex = 0
        while innerIndex < count:
            matrix[index][innerIndex] = float(a[index][innerIndex] - b[index][innerIndex])
            innerIndex += 1

        index += 1

    return matrix


def inverseMatrix(matrix):
    return numpy.linalg.inv(matrix)


def multiMatrix(a, b):
    return numpy.dot(a, b)


def getNoChainStatesMatrix(states, terminalStates):
    noChainStatesLen = len(states) - len(terminalStates)
    matrix = makeAxBMatrix(noChainStatesLen, len(terminalStates))
    copyStates = states[:]

    # removing terminal states
    terminalStates.sort(reverse=True)
    for index in terminalStates:
        del copyStates[index]

    for stateNumber, state in enumerate(copyStates):
        denominator = sum(state)
        for to, probability in enumerate(state):
            if to in terminalStates:
                x, y = pathForRMatrix(stateNumber, to, states)
                matrix[x][y] = Fraction(probability / denominator)

    return matrix


def pathForRMatrix(row, column, states):
    terminalStates = getTerminalStates(states)
    nonTerminalStates = getNonTerminalStates(states)

    x, y = 0, 0
    for index, value in enumerate(nonTerminalStates):
        if value == row:
            x = index

    for index, value in enumerate(terminalStates):
        if value == column:
            y = index

    return x, y


def makeAxBMatrix(height, length):
    res = []
    column = 0
    while column < height:
        row = 0
        res.append([])
        while row < length:
            res[column].append(float(0))
            row += 1

        column += 1

    return res


def lcm(x, y):
    return x * y // gcd(x, y)


def solutionAdapter(FR):
    normalise = []
    res = []
    commonDenominator = 1

    for i, v in enumerate(FR[0]):
        normalise.append(str(Fraction(v).limit_denominator()))

    # calculate common denominator
    for value in normalise:
        if str(value) == "0":
            _, denominator = [0, commonDenominator]
        else:
            _, denominator = str(value).split('/')

        commonDenominator = lcm(commonDenominator, int(denominator))

    for index, value in enumerate(normalise):
        if str(value) == "0":
            numerator, denominator = [0, commonDenominator]
        else:
            numerator, denominator = str(value).split('/')
            denominator = int(denominator)

        res.append(int(commonDenominator / denominator) * int(numerator))

    res.append(commonDenominator)

    return res


def solution(m):
    # validate inputs (is 2D array, has valid states, len of states, len of arrays)
    states = m

    if len(states) == 1:
        return [1, 1]

    # finding terminal states
    terminalStates = getTerminalStates(states)

    print("terminalStates", terminalStates)

    # make Loop states probability(markov chains) => (Q)
    Q = getMarkovChainsMatrix(states)

    print("Q", Q)

    # calculate I-Q => Z
    Z = minusMatrix(makeIMatrix(len(Q)), Q)

    print("Z", Z)
    print("Z[1][0]", Fraction(Z[1][0]).limit_denominator())

    # calculate (I-Q)^(-1) => F
    F = inverseMatrix(Z)

    print("F", F)
    print("F[1][0]", Fraction(F[1][0]).limit_denominator())
    print("F[1][1]", Fraction(F[1][1]).limit_denominator())

    # calculate the probability of non markov chains => (R)
    R = getNoChainStatesMatrix(states, terminalStates)

    print("R", R)

    # calculate FR
    FR = multiMatrix(F, R)

    print("FR", FR)
    # print("FR[0][0]", Fraction(FR[0][0]).limit_denominator())
    # print("FR[0][1]", Fraction(FR[0][1]).limit_denominator())
    # print("FR[0][2]", Fraction(FR[0][2]).limit_denominator())
    # print("FR[0][3]", Fraction(FR[0][3]).limit_denominator())
    #
    # print("FR[1][0]", Fraction(FR[1][0]).limit_denominator())
    # print("FR[1][1]", Fraction(FR[1][1]).limit_denominator())
    # print("FR[1][2]", Fraction(FR[1][2]).limit_denominator())
    # print("FR[1][3]", Fraction(FR[1][3]).limit_denominator())

    print("final res:", solutionAdapter(FR))

    # adapt result to wanted structure
    return solutionAdapter(FR)


# print(solution([
#     [0, 2, 1, 0, 0],
#     [0, 0, 0, 3, 4],
#     [0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0]
# ]) == [7, 6, 8, 21]
#       )

# print(solution(
#     [
#         [0, 1, 0, 0, 0, 1],  # s0, the initial state, goes to s1 and s5 with equal probability
#         [4, 0, 0, 3, 2, 0],  # s1 can become s0, s3, or s4, but with different probabilities
#         [0, 0, 0, 0, 0, 0],  # s2 is terminal, and unreachable (never observed in practice)
#         [0, 0, 0, 0, 0, 0],  # s3 is terminal
#         [0, 0, 0, 0, 0, 0],  # s4 is terminal
#         [0, 0, 0, 0, 0, 0],  # s5 is terminal
#     ]) == [0, 3, 2, 9, 14]
#       )
#
# print(solution([
#                    [0, 0, 0, 0, 3, 5, 0, 0, 0, 2],
#                    [0, 0, 4, 0, 0, 0, 1, 0, 0, 0],
#                    [0, 0, 0, 4, 4, 0, 0, 0, 1, 1],
#                    [13, 0, 0, 0, 0, 0, 2, 0, 0, 0],
#                    [0, 1, 8, 7, 0, 0, 0, 1, 3, 0],
#                    [1, 7, 0, 0, 0, 0, 0, 2, 0, 0],
#                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#                ]) == [1, 1, 1, 2, 5]
#       )
#
# print(solution([
#     [0, 86, 61, 189, 0, 18, 12, 33, 66, 39],
#     [0, 0, 2, 0, 0, 1, 0, 0, 0, 0],
#     [15, 187, 0, 0, 18, 23, 0, 0, 0, 0],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# ]) == [6, 44, 4, 11, 22, 13, 100]
#       )
#

# print(solution(([
#     [0, 7, 0, 17, 0, 1, 0, 5, 0, 2],
#     [0, 0, 29, 0, 28, 0, 3, 0, 16, 0],
#     [0, 3, 0, 0, 0, 1, 0, 0, 0, 0],
#     [48, 0, 3, 0, 0, 0, 17, 0, 0, 0],
#     [0, 6, 0, 0, 0, 1, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# ])
#                ) == [4, 5, 5, 4, 2, 20]
#       )
#
# print(solution([
#     [0, 0, 12, 0, 15, 0, 0, 0, 1, 8],
#     [0, 0, 60, 0, 0, 7, 13, 0, 0, 0],
#     [0, 15, 0, 8, 7, 0, 0, 1, 9, 0],
#     [23, 0, 0, 0, 0, 1, 0, 0, 0, 0],
#     [37, 35, 0, 0, 0, 0, 3, 21, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# ]) == [1, 2, 3, 4, 5, 15]
#       )

# print(solution(([
#     [0]
# ])) == [1, 1]
#       )


# print(solution(([
#     [1, 2, 3, 0, 0, 0],
#     [4, 5, 6, 0, 0, 0],
#     [7, 8, 9, 1, 0, 0],
#     [0, 0, 0, 0, 1, 2],
#     [0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0]
# ]) )== [1, 2, 3])
#

###!!!!!!!!!!!!!
# print(solution(([
#     [1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 0, 1, 1, 1, 0, 1, 0, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# ])
# ) == [2, 1, 1, 1, 1, 6]
#       )

print(solution(([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
               )== [1, 1, 1, 1, 1, 5]
      )


#
