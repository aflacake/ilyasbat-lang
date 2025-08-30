import sys

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("0")
        sys.exit(1)

    try:
        a = int(sys.argv[1])
        op = sys.argv[2]
        b = int(sys.argv[3])

        result = {
            '+': a + b,
            '-': a - b,
            '*': a * b,
            '/': a // b if b != 0 else 'Err'
        }.get(op, "Err")

        print(result)
    except:
        print("Err")
