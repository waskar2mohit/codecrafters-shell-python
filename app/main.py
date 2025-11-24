import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    while(True):
        sys.stdout.write("$ ")
        command = input()
        if command != "hello":
            print(f"{command}: command not found")
        else:
            break
        pass


if __name__ == "__main__":
    main()
