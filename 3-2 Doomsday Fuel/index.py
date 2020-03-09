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
    chainStates = []

    for stateNumber, state in enumerate(states):
        for to, probability in enumerate(state):

            if probability == 0:
                continue

            # states[stateNumber][to] is equal to probability
            if states[stateNumber][to] != 0 and states[to][stateNumber] != 0:
                if to == stateNumber:
                    raise RuntimeWarning("invalid data received")

                chainStates.append(stateNumber)
                continue

    chainStates = list(set(chainStates))

    chainStatesLen = len(chainStates)
    markovProbabilitiesMatrix = makeAxBMatrix(chainStatesLen, chainStatesLen)
    for stateNumber, state in enumerate(states):
        if stateNumber not in chainStates:
            continue

        for destination, probability in enumerate(state):
            if not (destination in chainStates):
                continue

            markovProbabilitiesMatrix[stateNumber][destination] = Fraction(probability, sum(state))

    return markovProbabilitiesMatrix


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
    nonTerminalStates = getNonTerminalStates(states)
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
            if to not in nonTerminalStates:
                x, y = pathFor(stateNumber, to, states)
                matrix[x][y] = Fraction(probability / denominator)

    return matrix


def pathFor(row, column, states):
    terminalStates = getTerminalStates(states)
    nonTerminalStates = getNonTerminalStates(states)

    if not (row in nonTerminalStates) or not (column in terminalStates):
        raise RuntimeWarning("pathFor: invalid request received")

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
    print("FR[0][0]", Fraction(FR[0][0]).limit_denominator())
    print("FR[0][1]", Fraction(FR[0][1]).limit_denominator())
    print("FR[0][2]", Fraction(FR[0][2]).limit_denominator())
    print("FR[0][3]", Fraction(FR[0][3]).limit_denominator())

    print("FR[1][0]", Fraction(FR[1][0]).limit_denominator())
    print("FR[1][1]", Fraction(FR[1][1]).limit_denominator())
    print("FR[1][2]", Fraction(FR[1][2]).limit_denominator())
    print("FR[1][3]", Fraction(FR[1][3]).limit_denominator())

    print("final res:", solutionAdapter(FR))
    # adapt result to wanted structure
    return solutionAdapter(FR)


print(solution(
    [
        [0, 1, 0, 0, 0, 1],  # s0, the initial state, goes to s1 and s5 with equal probability
        [4, 0, 0, 3, 2, 0],  # s1 can become s0, s3, or s4, but with different probabilities
        [0, 0, 0, 0, 0, 0],  # s2 is terminal, and unreachable (never observed in practice)
        [0, 0, 0, 0, 0, 0],  # s3 is terminal
        [0, 0, 0, 0, 0, 0],  # s4 is terminal
        [0, 0, 0, 0, 0, 0],  # s5 is terminal
    ]
))
