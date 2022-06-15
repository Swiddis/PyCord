total = 0
print("Enter your numbers for a running total!")
while True:
    x = input().strip().lower()
    if x == "quit":
        break
    else:
        try:
            total += float(x)
            print("Running total:", total)
        except ValueError():
            print("Not a number, enter `quit` to quit")
print("Goodbye!")
