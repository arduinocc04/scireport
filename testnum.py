import num
import typing

if __name__ == "__main__":
    # a:typing.List[num.NumSig] = [num.NumSig('0.0000'), num.NumSig("1", True), num.NumSig("1.234"), num.NumSig("1"), num.NumSig("0.00000013"), num.NumSig("1000.13")]
    # for n in a:
    #     print(f"{n.string=}", f"{n.sigCnt=}", f"{n.sigFormatString=}", f"{n.isConst=}", sep="\n", end=f"\n{n.string}===================\n")

    # print(num.NumSig('1.34634') + num.NumSig("24.22"))
    # print(num.NumSig('1.34134') + num.NumSig("24.22"))
    # print(num.NumSig("234234.3") * num.NumSig("1.111"))
    
    # a = num.NumSig("12312.11")
    # print(a.sciNotString)
    # print(num.changeENot2LaTeXNot(a.sciNotString))

    # print(num.NumSig("50.").sigCnt)
    # print(num.countSigFig("50000"), num.countSigFig("50000", True))
    two = num.SuperFloat("2", True)
    three = num.SuperFloat("3", True)
    ans = two+three*two
    print(ans.float, ans.is_const, ans.num_e_string, ans.cnt_significant_figures)
    # print(num.NumSig("50.")/(num.NumSig("0.075")**num.NumSig("2", True)))