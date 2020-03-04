def solution(s):
    r = ""
    for c in s:
        if c.isupper():
            r += "000001"

        c = c.lower()

        if c == 'a':
            r += "100000"
        elif c == 'b':
            r += "110000"
        elif c == 'c':
            r += "100100"
        elif c == 'd':
            r += "100110"
        elif c == 'e':
            r += "100010"
        elif c == 'f':
            r += "110100"
        elif c == 'g':
            r += "110110"
        elif c == 'h':
            r += "110010"
        elif c == 'i':
            r += "010100"
        elif c == 'j':
            r += "010110"
        elif c == 'k':
            r += "101000"
        elif c == 'l':
            r += "111000"
        elif c == 'm':
            r += "101100"
        elif c == 'n':
            r += "101110"
        elif c == 'o':
            r += "101010"
        elif c == 'p':
            r += "111100"
        elif c == 'q':
            r += "111110"
        elif c == 'r':
            r += "111010"
        elif c == 's':
            r += "011100"
        elif c == 't':
            r += "011110"
        elif c == 'u':
            r += "101001"
        elif c == 'v':
            r += "111001"
        elif c == 'w':
            r += "010111"
        elif c == 'x':
            r += "101101"
        elif c == 'y':
            r += "101111"
        elif c == 'z':
            r += "101011"
        elif c == ' ':
            r += "000000"

    return r
