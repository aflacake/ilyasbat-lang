# helpers/masukkan.py

import sys

def masukkan(varname: str = None):
    try:
        value = input("Masukkan nilai: ")
        if varname:
            print(f"{varname}={value}")
        else:
            print(value)
        return 0
    except Exception:
        print("")
        return 1

if __name__ == "__main__":
    varname = sys.argv[1] if len(sys.argv) > 1 else None
    code = masukkan(varname)
    sys.exit(code)
