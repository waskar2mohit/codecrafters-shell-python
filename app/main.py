import sys
import shutil
import os
import shlex



BUILTINS = {"exit", "echo", "type"}


def main():
    while True:
        sys.stdout.write("$ ")
        command = input()
        if not command:
            continue

        if command == "exit":
            break

        if command.startswith("echo "):
            commandArr = shlex.split()
            for c in commandArr:
                print(c) 
            continue

        if command.startswith("type "):
            name = command[5:]
            if name in BUILTINS:
                print(f"{name} is a shell builtin")
            else:
                path = shutil.which(name)
                if path:
                    print(f"{name} is {path}")
                else:
                    print(f"{name}: not found")
            continue

        else :
            if shutil.which(command.split(" ")[0]):
                os.system(command)
            else:
                print(f"{command}: not found")
            




if __name__ == "__main__":
    main()
