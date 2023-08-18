import ast
import os.path
import re

def indentationCheck(line: str):
    indentationCounter = 0
    for letter in line:
        if letter == " ":
            indentationCounter += 1
        else:
            break

    if indentationCounter % 4 == 0:
        return False
    else:
        return True


def semicolonCheck(line: str):
    line = line.split("#")
    code = line[0].strip()
    if code.endswith(";"):
        return True
    else:
        return False


def commentCheck(line: str):
    line = line.split("#")
    if len(line) == 1:
        return False

    code = line[0]
    if code == "":
        return False

    lineEnd = len(code) - 1
    spaceCounter = 0
    while lineEnd >= 0 and code[lineEnd] == " ":
        spaceCounter += 1
        lineEnd -= 1

    if spaceCounter < 2:
        return True
    else:
        return False


def lengthCheck(line: str) -> bool:
    if len(line) > 79:
        return True
    else:
        return False


def todoCheck(line: str):
    line = line.split("#")
    if len(line) > 1:
        comment = line[1]
        if comment.lower().find("todo") != -1:
            return True
        else:
            return False
    return False


def checkS007(line: str) -> bool:
    line = line.strip()
    if line.startswith("def") or line.startswith("class"):
        counter = 0
        if line.startswith("def"):
            line = line.split("def")[1]
        if line.startswith("class"):
            line = line.split("class")[1]
        for letter in line:
            if letter == " ":
                counter += 1
            else:
                break

        if counter > 1:
            return True
        else:
            return False


def checkS008(line: str, lineCount: int, filePath: str):
    line = line.strip()
    if line.startswith("class"):
        line = line.split()[1].split(":")[0]
        if re.match("[A-Z]\w*", line) is None:
            print(f"{filePath}: line {lineCount}: S008 Class name " + line + " should use CamelCase")
            return True

    return False


def checkS009(line: str, lineCount: int, filePath: str) -> bool:
    line = line.strip()
    if line.strip().startswith("def"):
        line = line.split()[1].split(":")[0]
        if re.match("[_]*[a-z_]+", line) is None:
            print(f"{filePath}: line {lineCount}: S009 Function name " + line + " should use snake_case")
            return True

    return False


def check010(filePath: str) -> bool:
    file = open(filePath).read()
    tree = ast.parse(file)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for arguments in node.args.args:
                if re.search("[A-Z]", arguments.arg) is not None:
                    print(f"{filePath}: line {arguments.lineno}: S010 Argument name '{arguments.arg}' should be snake_case")
            for defaultArgument in node.args.defaults:
                if isinstance(defaultArgument, ast.List):
                    print(f"{filePath}: line {arguments.lineno}: S012 Default argument value is mutable")
            for assignment in ast.walk(node):
                if isinstance(assignment, ast.Name) and isinstance(assignment.ctx, ast.Store):
                    if re.search("[A-Z]", assignment.id) is not None:
                        print(f"{filePath}: line {assignment.lineno}: S011 Variable '{assignment.id}' in function should be snake_case")



def checkLine(line: str, lineCount: int):
    if lengthCheck(line):
        print(f"line {lineCount}: S001 Too long")

    if indentationCheck(line):
        print(f"line {lineCount}: S002 Wrong indentation")

    if semicolonCheck(line):
        print(f"line {lineCount}: S003 Unnecessary semicolon")

    if commentCheck(line):
        print(f"line {lineCount}: S004 At least two spaces required before inline comments")

    if todoCheck(line):
        print(f"line {lineCount}: S005 TODO found")


def checkLineOfFile(filePath, line, lineCount):
    if lengthCheck(line):
        print(f"{filePath}: line {lineCount}: S001 Too long")

    if indentationCheck(line):
        print(f"{filePath}: line {lineCount}: S002 Wrong indentation")

    if semicolonCheck(line):
        print(f"{filePath}: line {lineCount}: S003 Unnecessary semicolon")

    if commentCheck(line):
        print(f"{filePath}: line {lineCount}: S004 At least two spaces required before inline comments")

    if todoCheck(line):
        print(f"{filePath}: line {lineCount}: S005 TODO found")


def checkLineOfFile2(filePath, line, lineCount):
    if checkS007(line):
        print(f"{filePath}: line {lineCount}: S007 Too many spaces after 'class'")

    checkS008(line, lineCount, filePath)
    checkS009(line, lineCount, filePath)



def getFilesFromDirectory(directoryPath: str, fileList: list):
    if os.path.isfile(directoryPath):
        fileList.append(directoryPath)
        return
    else:
        for directory in os.listdir(directoryPath):
            getFilesFromDirectory(directoryPath + "\\" + directory, fileList)


def getFilesWithEndingFromDirectory(directoryPath: str, ending: str) -> list:
    fileList = []
    filesWithEnding = []
    getFilesFromDirectory(directoryPath, fileList)
    for file in fileList:
        if file.endswith(ending):
            filesWithEnding.append(file)

    return filesWithEnding



# # directoryPath = "C:\\Users\\larsr\\PycharmProjects\\Static Code Analyzer\\Static Code Analyzer\\task\\test"
# file = open(r"C:\Users\larsr\PycharmProjects\Static Code Analyzer\Static Code Analyzer\task\test\this_stage\test_3.py").read()
# file2 = open(r"C:\Users\larsr\PycharmProjects\TryStuff\test.py").read()
#
# tree = ast.parse(file2)
#
# print(ast.dump(tree))
#
# for node in ast.walk(tree):
#     if isinstance(node, ast.FunctionDef):
#         for arguments in node.args.args:
#             if re.search("[A-Z]", arguments.arg) is not None:
#                 print(f": line {arguments.lineno}: S010 Argument name '{arguments.arg}' should be snake_case")
#         for defaultArgument in node.args.defaults:
#             print(defaultArgument)
#             if isinstance(defaultArgument, ast.List):
#                 print("mutable")
#         for assignment in ast.walk(node):
#             if isinstance(assignment, ast.Name) and isinstance(assignment.ctx, ast.Store):
#                 if re.search("[A-Z]", assignment.id) is not None:
#                     print(f": line {assignment.lineno}: S011 Variable '{assignment.id}' in function should be snake_case")
#
#
# # print(re.match('[^A-Z]*', "AaaAb"))
# #
# # print(re.search("[A-Z]", "aaaA"))