# ScientificCalculator

# Use file helper
- `@@expression@@`
- `@@!num + num_{num}@@`
- !: is_const=True
- _{num}: cnt_significant_figures=num
- !!: execute a line of python code.
- Difference between @@~@@ and !!: @@~@@ replace expression with result while !! doesn't.
- Variables declared in !! are local variables. So if you don't use `global`, it won't reached.

# Todo
- 레포트 작성할 폴더 자동으로 만들어 주기.. manual 넣어주고, data, tex 폴더 만들어주고...
- 자동으로 calced 만든 후에 그걸로 컴파일 하도록...
- 