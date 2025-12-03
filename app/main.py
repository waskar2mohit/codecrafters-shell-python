import sys
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
        try:
            command = input()
        except EOFError:
            return

        if not command.strip():
            continue

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
            # echo does NOT interpret redirections; shell does
            stdout_target = None
            cleaned_args = []
            i = 0
            while i < len(args):
                tok = args[i]
                if tok in (">", "1>"):
                    if i + 1 >= len(args):
                        print("redirection: missing filename")
                        stdout_target = None
                        cleaned_args = []
                        break
                    filename = args[i + 1]
                    # ensure directory exists if path has dirs
                    dir_name = os.path.dirname(filename)
                    if dir_name:
                        os.makedirs(dir_name, exist_ok=True)
                    try:
                        stdout_target = open(filename, "w")
                    except OSError as e:
                        print(f"redirection: {e}")
                        stdout_target = None
                        cleaned_args = []
                        break
                    i += 2
                else:
                    cleaned_args.append(tok)
                    i += 1

            output = " ".join(cleaned_args)
            if stdout_target is not None:
                stdout_target.write(output + "\n")
                stdout_target.close()
            else:
                print(output)
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

        # handle redirection for external commands
        stdout_target = None
        cleaned_args = []
        i = 0
        while i < len(args):
            tok = args[i]
            if tok in (">", "1>"):
                # need a filename after > / 1>
                if i + 1 >= len(args):
                    cleaned_args = []
                    break
                filename = args[i + 1]

                # create parent directory if needed
                dir_name = os.path.dirname(filename)
                if dir_name:
                    os.makedirs(dir_name, exist_ok=True)

                # open target file for stdout
                stdout_target = open(filename, "w")

                # skip both '>' and filename
                i += 2
            else:
                cleaned_args.append(tok)
                i += 1

        try:
            subprocess.run(
                [cmd] + cleaned_args,
                executable=exe,
                stdout=stdout_target if stdout_target is not None else None,
                stderr=None  # stderr to terminal
            )
        except Exception as e:
            print(f"Error executing {cmd}: {e}")
        finally:
            if stdout_target is not None:
                stdout_target.close()


if __name__ == "__main__":
    main()
