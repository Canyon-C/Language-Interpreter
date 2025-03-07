import io
import operator


def addition(value1, value2):
    return int(value1) + int(value2)


def subtraction(value1, value2):
    return int(value1) - int(value2)


def modulo(value1, value2):
    return int(value1) % int(value2)


def multiplecation(value1, value2):
    return int(value1) * int(value2)


def division(value1, value2):
    return int(value1) / int(value2)


def lessThan(value1, value2):
    return int(value1) < int(value2)


def greaterThan(value1, value2):
    return int(value1) > int(value2)


def equalTo(value1, value2):
    return int(value1) == int(value2)


def increment(value1):
    return int(value1) + 1


def decrement(value1):
    return int(value1) - 1


def mathematicalExpressions(s, expressions):
    operators = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.floordiv,
        "%": operator.mod,
        "==": operator.eq,
        "!=": operator.ne,
    }
    result = None
    op = None
    for x in range(0, len(expressions)):
        try:
            if expressions[x] in s:
                currentValue = int(s[expressions[x]])
            else:
                currentValue = int(expressions[x])
            if result == None:
                result = currentValue
            elif op != None:
                result = operators[op](result, currentValue)
                op = None
        except ValueError:
            op = expressions[x]
    return result


def inVarMap(s, value1, value2=None):
    value1Exists = False
    value2Exists = False
    if value1 in s.keys():
        value1Exists = True
    if value2 in s.keys():
        value2Exists = True

    return value1Exists, value2Exists


def interpret(s: dict, lines):
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if not line:
            i += 1
            continue
        if line.startswith("#"):
            i += 1
            continue
        elif line.startswith("for "):
            if "range" in line:
                expression = line.split("for ")[1].strip()[:-2]
                variable = expression.split("in ")[0].strip()
                incrementer = expression.split("in ")[1].strip()
                start = incrementer.split(",")[0].strip()[6:]
                finish = incrementer.split(", ")[1].strip()[:-1]

                forBody = []
                braceCount = 1
                while i < len(lines) and braceCount > 0:
                    i += 1
                    line = lines[i]
                    if "{" in line:
                        braceCount += line.count("{")
                    if "}" in line:
                        braceCount -= line.count("}")
                    if braceCount > 0:
                        forBody.append(line)
                varInMap, temp = inVarMap(s, variable)
                if varInMap:
                    for s[variable] in range(int(start), int(finish)):
                        interpret(s, forBody)
                else:
                    s[variable] = 0
                    for s[variable] in range(int(start), int(finish)):
                        interpret(s, forBody)

                    s.pop(variable)
                i += 1
        elif line.startswith("while "):
            if "<" in line:
                condition = line.split("while ")[1].strip()[:-2]
                value1 = condition.split("<")[0].strip()
                value2 = condition.split("<")[1].strip()
                result = None
                value1Exist, value2Exist = inVarMap(s, value1, value2)
                result = lessThan(
                    s[value1] if value1Exist else value1,
                    s[value2] if value2Exist else value2,
                )
                whileBody = []
                braceCount = 1
                while i < len(lines) and braceCount > 0:
                    i += 1
                    line = lines[i]
                    if "{" in line:
                        braceCount += line.count("{")
                    if "}" in line:
                        braceCount -= line.count("}")
                    if braceCount > 0:
                        whileBody.append(line)

                if result:
                    while lessThan(
                        s[value1] if value1Exist else value1,
                        s[value2] if value2Exist else value2,
                    ):
                        interpret(s, whileBody)

                i += 1
            elif ">" in line:
                condition = line.split("while ")[1].strip()[:-2]
                value1 = condition.split(">")[0].strip()

                value2 = condition.split(">")[1].strip()
                result = None
                value1Exist, value2Exist = inVarMap(s, value1, value2)

                result = greaterThan(
                    s[value1] if value1Exist else value1,
                    s[value2] if value2Exist else value2,
                )
                whileBody = []
                braceCount = 1
                while i < len(lines) and braceCount > 0:
                    i += 1
                    line = lines[i]
                    if "{" in line:
                        braceCount += line.count("{")
                    if "}" in line:
                        braceCount -= line.count("}")
                    if braceCount > 0:
                        whileBody.append(line.strip())
                if result:
                    while greaterThan(
                        s[value1] if value1Exist else value1,
                        s[value2] if value2Exist else value2,
                    ):

                        interpret(s, whileBody)
                i += 1
        elif line.startswith("if "):
            if "&&" in line:
                expression1 = line.split("if ")[1].strip()[:-2]
                expression2 = expression1.split("&&")[1].strip()
                expression1 = expression1.split("&&")[0].strip()
                expression1Arr = expression1.split(" ")
                expression2Arr = expression2.split(" ")
                for x in range(0, len(expression1Arr)):
                    try:
                        inMap = inVarMap(s, expression1Arr[x], None)
                        if inMap:
                            expression1Arr[x] = s[expression1Arr[x]]
                    except:
                        pass
                for x in range(0, len(expression2Arr)):
                    try:
                        inMap = inVarMap(s, expression2Arr[x], None)
                        if inMap:
                            expression2Arr[x] = s[expression2Arr[x]]
                    except:
                        pass
                result1 = mathematicalExpressions(s, expression1Arr)
                result2 = mathematicalExpressions(s, expression2Arr)
                ifbody = []
                braceCount = 1
                while i < len(lines) and braceCount > 0:
                    i += 1
                    line = lines[i]
                    if "{" in line:
                        braceCount += line.count("{")
                    if "}" in line:
                        braceCount -= line.count("}")
                    if braceCount > 0:
                        ifbody.append(line)
                if result1 and result2:
                    interpret(s, ifbody)
                i += 1
            elif "==" in line:
                expression1 = line.split("if ")[1][:-2]
                expression1Arr = expression1.split(" ")

                for x in range(0, len(expression1Arr)):
                    try:
                        inMap = inVarMap(s, expression1Arr[x], None)
                        if inMap:
                            expression1Arr[x] = s[expression1Arr[x]]
                    except:
                        pass
                result1 = mathematicalExpressions(s, expression1Arr)
                ifbody = []
                braceCount = 1
                while i < len(lines) and braceCount > 0:
                    i += 1
                    line = lines[i]
                    if "{" in line:
                        braceCount += line.count("{")
                    if "}" in line:
                        braceCount -= line.count("}")
                    if braceCount > 0:
                        ifbody.append(line)
                if result1:
                    interpret(s, ifbody)
                i += 1
            elif "<" in line:
                condition = line.split("if ")[1].strip()[:-2]
                value1 = condition.split("<")[0].strip()
                value2 = condition.split("<")[1].strip()
                result = None
                value1Exist, value2Exist = inVarMap(s, value1, value2)
                result = lessThan(
                    s[value1] if value1Exist else value1,
                    s[value2] if value2Exist else value2,
                )
                ifbody = []
                braceCount = 1
                while i < len(lines) and braceCount > 0:
                    i += 1
                    line = lines[i]
                    if "{" in line:
                        braceCount += line.count("{")
                    if "}" in line:
                        braceCount -= line.count("}")
                    if braceCount > 0:
                        ifbody.append(line)
                if result:
                    interpret(s, ifbody)
                i += 1
            elif ">" in line:
                condition = line.split("if ")[1].strip()[:-2]
                value1 = condition.split(">")[0].strip()
                value2 = condition.split(">")[1].strip()
                result = None
                value1Exist, value2Exist = inVarMap(s, value1, value2)
                result = greaterThan(
                    s[value1] if value1Exist else value1,
                    s[value2] if value2Exist else value2,
                )
                ifbody = []
                braceCount = 1
                while i < len(lines) and braceCount > 0:
                    i += 1
                    line = lines[i]
                    if "{" in line:
                        braceCount += line.count("{")
                    if "}" in line:
                        braceCount -= line.count("}")
                    if braceCount > 0:
                        ifbody.append(line)
                if result:
                    interpret(s, ifbody)
                i += 1
        elif line.startswith("let "):
            definition = line.split("let ")[1]
            var, val = definition.split("=")
            var = var.strip()
            val = val.strip()
            if len(val) == 1 or len(val) == 2:
                valExist, value2Exist = inVarMap(s, val)
                if valExist:
                    try:
                        s[var] = s[val]
                    except:
                        raise SyntaxError(
                            f"Unrecognized Variable: '{val}' at line '{i}' "
                        )
                else:
                    try:
                        s[var] = int(val)
                    except ValueError:
                        raise SyntaxError(
                            f"Unrecognized Variable: '{val}' at line '{i}' "
                        )
            else:
                expression = []
                for x in range(0, len(val)):
                    if val[x] != " ":
                        expression.append(val[x])
                s[var] = mathematicalExpressions(s, expression)

            i += 1
        elif line.startswith("print("):
            print_text = (
                line.split("print")[1].replace("(", "").replace(")", "").strip()
            )
            if '"' in print_text:
                print_text = print_text.replace('"', "")
                print(print_text)
            else:
                variable_name = print_text
                val = s[variable_name]
                print(val)
            i += 1
        elif "++" in line:
            variable = line.split("++")[0].strip()
            value1Exist, value2Exist = inVarMap(s, variable)
            if value1Exist:
                s[variable] = increment(s[variable])
            i += 1
        elif "--" in line:
            variable = line.split("--")[0].strip()
            value1Exist, value2Exist = inVarMap(s, variable)
            if value1Exist:
                s[variable] = decrement(s[variable])
            i += 1
        else:
            raise SyntaxError(f"Unrecognized Statement: '{line}' at line '{i}' ")
    return


def main(filename):
    state = dict()
    with io.open(filename) as file:
        lines = file.readlines()
        interpret(state, lines)


main("fizzbuzz.ez")
