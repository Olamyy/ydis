def add(a, b):
    return a + b

def main():
    x = 10
    y = 20
    if x < y:
        print(f"{x} is less than {y}")
    else:
        print(f"{x} is greater than or equal to {y}")
    
    result = add(x, y)
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
