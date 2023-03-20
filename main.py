import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from interface import Interface

def main():
    app = Interface()
    app.start()

if __name__ == "__main__":
    main()
