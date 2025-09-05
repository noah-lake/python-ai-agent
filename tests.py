from functions.run_python_file import run_python_file


def test():
    result = run_python_file("calculator", "main.py")
    print("Result for current file:")
    print(result)
    print("")

    result = run_python_file("calculator", "main.py", args=["3 + 5"])
    print("Result for current file:")
    print(result)
    print("")

    result = run_python_file("calculator", "tests.py")
    print("Result for current file:")
    print(result)
    print("")

    result = run_python_file("calculator", "../main.py")
    print("Result for current file:")
    print(result)
    print("")

    result = run_python_file("calculator", "nonexistent.py")
    print("Result for current file:")
    print(result)
    print("")


if __name__ == "__main__":
    test()
