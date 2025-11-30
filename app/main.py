import sys
import shutil
import os
import shlex
import subprocess

BUILTINS = {"exit", "echo", "type"}

def find_executable(name):
    """Search PATH for executables, even with spaces in name."""
    path_env = os.environ.get("PATH", "")
    for directory in path_env.split(os.pathsep):
        full = os.path.join(directory, name)
        if os.path.isfile(full) and os.access(full, os.X_OK):
            return full
    return None

def main():
    while True:
        sys.stdout.write("$ ")
        command = input().strip()

        if not command:
            continue

        # Parse using shlex to handle quotes, spaces, etc.
        try:
            parts = shlex.split(command)
        except ValueError:
            print("Invalid quoting")
            continue

        if not parts:
            continue

        cmd = parts[0]
        args = parts[1:]

        # -------- BUILTINS --------

        if cmd == "exit":
            return

        if cmd == "echo":
            print(" ".join(args))
            continue

        if cmd == "type":
            if not args:
                print("type: missing operand")
                continue

            name = args[0]

            if name in BUILTINS:
                print(f"{name} is a shell builtin")
            else:
                exe = find_executable(name)
                if exe:
                    print(f"{name} is {exe}")
                else:
                    print(f"{name}: not found")
            continue

        # -------- EXTERNAL COMMANDS --------

        exe = find_executable(cmd)

        if exe is None:
            print(f"{cmd}: not found")
            continue

        try:
            subprocess.run([cmd] + args, executable=exe)

        except Exception as e:
            print(f"Error executing {cmd}: {e}")

if __name__ == "__main__":
    main()
