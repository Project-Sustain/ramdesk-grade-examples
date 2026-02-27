import sys

for arg in sys.argv[1:]:
    num = int(arg)
    if num % 2 == 0:
        print("even", end=" ")
    else:
        print("odd", end=" ")
