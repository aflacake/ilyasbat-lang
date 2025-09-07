# helpers/melompat.py

import sys

def main():
    if len(sys.argv) < 2:
        print("Kesalahan: Label tujuan tidak diberikan.")
        sys.exit(1)

    label = sys.argv[1].strip()
    if not label:
        print("Kesalahan: Label kosong.")
        sys.exit(2)

    print(f"Melompat ke label: {label}")

    sys.exit(0)

if __name__ == "__main__":
    main()
