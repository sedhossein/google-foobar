def collectionSum(till):
    return (till * (1 + till)) / 2


def solution(x, y):
    if x < 1 or y < 1 or x > 100000 or y > 100000:
        raise ValueError("invalid address!")

    xPrim = collectionSum(x)
    yPrim = collectionSum(y) - (y - 1)

    return str(xPrim + yPrim + (x - 1)*(y - 1) - 1)
