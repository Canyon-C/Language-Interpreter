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


def mathematicalExpressions(expressions):

    operators = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
        "%": operator.mod,
    }
    result = None
    op = None
    for x in range(0, len(expressions)):
        try:
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
        elif line.startswith("if "):
            if "&&" in line:
                expression1 = line.split("if ")[1].strip()[:-2]
                equivalenceRelation = expression1.split("==")[1].strip().split(" ")[0]
                expression1 = expression1.split("==")[0].strip()
                if mathematicalExpressions(expression1.split(" ")) == int(
                    equivalenceRelation
                ):
                    result = True
                else:
                    result = False
                expression2 = line.split("&& ")[1].strip()[:-2]
                equivalenceRelation2 = expression2.split("!=")[1].strip().split(" ")[0]
                expression2 = expression1.split("!=")[0].strip()
                if mathematicalExpressions(expression2.split(" ")) == int(
                    equivalenceRelation2
                ):
                    result2 = True
                else:
                    result2 = False
                body = []
                braceCount = 1
                while i < len(lines) and braceCount > 0:
                    i += 1
                    line = lines[i]
                    if "{" in line:
                        braceCount += line.count("{")
                    if "}" in line:
                        braceCount -= line.count("}")
                    if braceCount > 0:
                        body.append(line)

                    if result and result2:
                        interpret(s, body)

            elif "==" in line:
                if "+" in line:
                    expression = line.split("if ")[1].strip()[:-2]
                    value1 = expression.split("+")[0].strip()
                    value2 = expression.split("+")[1].strip().split(" ")[0]
                    equivalenceRelation = expression.split("==")[1].strip()
                    result = None
                    value1Exist, value2Exist = inVarMap(s, value1, value2)
                    binResult = addition(
                        s[value1] if value1Exist else value1,
                        s[value2] if value2Exist else value2,
                    )
                    expressionResult = equalTo(binResult, equivalenceRelation)
                    i += 1
                    body = []
                    while "}" not in lines[i]:
                        body.append(lines[i].strip())
                        i += 1
                    if expressionResult:
                        interpret(s, body)
                    i += 1
                elif "%" in line:
                    expression = line.split("if ")[1].strip()[:-2]
                    value1 = expression.split("%")[0].strip()
                    value2 = expression.split("%")[1].strip().split(" ")[0]
                    equivalenceRelation = expression.split("==")[1].strip()
                    result = None
                    value1Exist, value2Exist = inVarMap(s, value1, value2)
                    binResult = modulo(
                        s[value1] if value1Exist else value1,
                        s[value2] if value2Exist else value2,
                    )
                    expressionResult = equalTo(binResult, equivalenceRelation)

                    body = []
                    braceCount = 1
                    while i < len(lines) and braceCount > 0:
                        i += 1
                        line = lines[i]
                        if "{" in line:
                            braceCount += line.count("{")
                        if "}" in line:
                            braceCount -= line.count("}")
                        if braceCount > 0:
                            body.append(line)

                    if expressionResult:
                        interpret(s, body)
                    i += 1
                elif "-" in line:
                    expression = line.split("if ")[1].strip()[:-2]
                    value1 = expression.split("-")[0].strip()
                    value2 = expression.split("-")[1].strip().split(" ")[0]
                    equivalenceRelation = expression.split("==")[1].strip()
                    result = None
                    value1Exist, value2Exist = inVarMap(s, value1, value2)
                    binResult = subtraction(
                        s[value1] if value1Exist else value1,
                        s[value2] if value2Exist else value2,
                    )
                    expressionResult = equalTo(binResult, equivalenceRelation)
                    i += 1
                    body = []
                    while "}" not in lines[i]:
                        body.append(lines[i].strip())
                        i += 1
                    if expressionResult:
                        interpret(s, body)
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

                i += 1
                body = []
                while "}" not in lines[i]:
                    body.append(lines[i].strip())
                    i += 1
                if result:
                    interpret(s, body)
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
                i += 1
                body = []
                while "}" not in lines[i]:
                    body.append(lines[i].strip())
                    i += 1

                if result:
                    interpret(s, body)
                i += 1
        elif line.startswith("let "):
            definition = line.split("let ")[1]
            var, val = definition.split("=")
            var = var.strip()
            val = val.strip()
            if len(val) == 1:
                valExist, value2Exist = inVarMap(s, val)
                if valExist:
                    s[var] = s[val]
                else:
                    s[var] = int(val)
            else:
                expression = []
                for x in range(0, len(val)):
                    if val[x] != " ":
                        expression.append(val[x])
                s[var] = mathematicalExpressions(expression)

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
    return


def main(filename):
    state = dict()
    with io.open(filename) as file:
        lines = file.readlines()
        interpret(state, lines)


main("testprogram.ez")
