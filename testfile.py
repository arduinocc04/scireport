import file

if __name__ == "__main__":
    print(file.change_line("@@1.234 + 2.1@@", "@@"))
    print(file.change_line("@@1.234 + !2.1@@", "@@"))
    print(file.change_line("@@1.234_{1} + !2.1@@", "@@"))