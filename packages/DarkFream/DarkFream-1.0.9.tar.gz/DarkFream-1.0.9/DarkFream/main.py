import sys

from .app import *

def main():
        if sys.argv[1] == "runserver":
            if len(sys.argv) == 2:
                run_server()
            elif len(sys.argv) == 3:
                run_server(sys.argv[2])
            else:
                run_server(sys.argv[2], sys.argv[3])
        if sys.argv[1] == "createapp":
            if len(sys.argv) != 3:
                print("Usage: python -m dark_fream.app createapp <app_name>")
                sys.exit(1)
            create_app(sys.argv[2])
        else:
            print("Unknown command")
            sys.exit(1)


if __name__ == '__main__':
    main()
