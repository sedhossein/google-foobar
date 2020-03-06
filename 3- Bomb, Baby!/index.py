IMPOSSIBLE = "impossible"


def solution(x, y):
    machBomb, faculaBomb = int(x), int(y)
    iteration = 0

    while True:
        if machBomb == faculaBomb or machBomb < 1 or faculaBomb < 1:
            break

        if machBomb > faculaBomb:
            count = int((machBomb - 1) / faculaBomb)
            machBomb -= faculaBomb * count
            iteration += count
        else:
            count = int((faculaBomb - 1) / machBomb)
            faculaBomb -= machBomb * count
            iteration += count

    if machBomb == faculaBomb and machBomb == 1:
        return str(iteration)

    return IMPOSSIBLE
