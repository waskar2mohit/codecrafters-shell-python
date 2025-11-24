import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    while(True):
        sys.stdout.write("$ ")
        command = input()
        if command != "hello" and command!="exit" and command[:4] != "echo" and command[:4]!="type":
            print(f"{command}: command not found")
        elif command[:4] == "echo":
            print(command[5:])
        elif command[:4]=="type":
            if command [5:] == "exit" and  command [5:] == "echo":
                print(f"{command[5:]} is a shell builtin")
        else:
            break
        pass
    #echo is a shell builtin


if __name__ == "__main__":
    main()
