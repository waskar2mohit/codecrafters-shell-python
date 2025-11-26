import sys
import shutil
import os



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
            print(command[5:])
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

        elif shutil.which(command.split(" ")[0]):
             os.system(command)
            




if __name__ == "__main__":
    main()
