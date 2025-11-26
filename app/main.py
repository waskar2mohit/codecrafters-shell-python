import sys
import shutil


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

        else:
            splitedCom = command.split()
            print(f"Program was passed {len(splitedCom)} args (including program name).")
            print(f"Arg #{0} (program name): {splitedCom[0]}")
            for i in range(1,len(splitedCom)):
                print(f"Arg #{i}: {splitedCom[i]}")




if __name__ == "__main__":
    main()
