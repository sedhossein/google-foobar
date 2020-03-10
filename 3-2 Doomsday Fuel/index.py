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
    nonTerminalStates = getNonTerminalStates(states)
    noChainStatesLen = len(states) - len(terminalStates)
    matrix = makeAxBMatrix(noChainStatesLen, len(terminalStates))
    copyStates = states[:]

    for stateNumber, state in enumerate(copyStates):
        denominator = sum(state)
        for to, probability in enumerate(state):
            if to in terminalStates:
                if (stateNumber in nonTerminalStates) and to in terminalStates:
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

    # make Loop states probability(markov chains) => (Q)
    Q = getMarkovChainsMatrix(states)

    # calculate I-Q => Z
    Z = minusMatrix(makeIMatrix(len(Q)), Q)

    # calculate (I-Q)^(-1) => F
    F = inverseMatrix(Z)

    # calculate the probability of non markov chains => (R)
    R = getNoChainStatesMatrix(states, terminalStates)

    # calculate FR
    FR = multiMatrix(F, R)

    # adapt result to wanted structure
    return solutionAdapter(FR)

