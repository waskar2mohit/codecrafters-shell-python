import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    while(True):
        sys.stdout.write("$ ")
        command = input()
        if command != "hello" and command!="exit" and command != "echo":
            print(f"{command}: command not found")
        elif command == "echo":
            print(command[4:])
        else:
            break
        pass


if __name__ == "__main__":
    main()
