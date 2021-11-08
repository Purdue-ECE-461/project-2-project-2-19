import ranking_module

import sys
from Test import test

def main():
    test1 = 'Test/test1.txt'
    test2 = 'Test/test2.txt'
    print(str(sys.argv))
    if len(sys.argv) < 2:
        print("error, not enough arguments")
        return
    if sys.argv[1] == "install":
        print("install dependencies")
    elif sys.argv[1] == "test":
        print("test running")
        test.run_test_suite(test1, test2)
    else:
        ranking_module.run_files(sys.argv[1])

    return 0


if __name__ == '__main__':
    main()
