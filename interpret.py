import io


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
                i += 1
                forBody = []
                while "}" not in lines[i]:
                    forBody.append(lines[i])
                    i += 1
                varInMap = inVarMap(s, variable)
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

                i += 1
                whileBody = []
                while "}" not in lines[i]:
                    whileBody.append(lines[i].strip())
                    i += 1
                if result:
                    while lessThan(
                        s[value1] if value1Exist else value1,
                        s[value2] if value2Exist else value2,
                    ):
                        interpret(s, whileBody)

                i += 1
        elif line.startswith("if "):
            if "==" in line:
                if "+" in line:
                    expression = line.split("if ")[1].strip()[:-2]
                    value1 = expression.split("+")[0].strip()
                    value2 = expression.split("+")[1].strip()[:1]
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
                    value2 = expression.split("%")[1].strip()[:1]
                    equivalenceRelation = expression.split("==")[1].strip()
                    result = None
                    value1Exist, value2Exist = inVarMap(s, value1, value2)
                    binResult = modulo(
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
                elif "-" in line:
                    expression = line.split("if ")[1].strip()[:-2]
                    value1 = expression.split("-")[0].strip()
                    value2 = expression.split("-")[1].strip()[:1]
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
            if "+" in line:
                definition = line.split("let ")[1]
                var, val = definition.split("=")
                var = var.strip()
                value1 = val.split("+")[0].strip()
                value2 = val.split("+")[1].strip()
                value1Exist, value2Exist = inVarMap(s, value1, value2)
                s[var] = addition(
                    s[value1] if value1Exist else value1,
                    s[value2] if value2Exist else value2,
                )
                i += 1
            elif "-" in line:
                definition = line.split("let ")[1]
                var, val = definition.split("=")
                var = var.strip()
                value1 = val.split("-")[0].strip()
                value2 = val.split("-")[1].strip()

                value1Exist, value2Exist = inVarMap(s, value1, value2)
                s[var] = subtraction(
                    s[value1] if value1Exist else value1,
                    s[value2] if value2Exist else value2,
                )
                i += 1
            elif "*" in line:
                definition = line.split("let ")[1]
                var, val = definition.split("=")
                var = var.strip()
                value1 = val.split("*")[0].strip()
                value2 = val.split("*")[1].strip()
                value1Exist, value2Exist = inVarMap(s, value1, value2)
                s[var] = multiplecation(
                    s[value1] if value1Exist else value1,
                    s[value2] if value2Exist else value2,
                )
                i += 1
            elif "/" in line:
                definition = line.split("let ")[1]
                var, val = definition.split("=")
                var = var.strip()
                value1 = val.split("/")[0].strip()
                value2 = val.split("/")[1].strip()

                value1Exist, value2Exist = inVarMap(s, value1, value2)
                s[var] = division(
                    s[value1] if value1Exist else value1,
                    s[value2] if value2Exist else value2,
                )
                i += 1
            elif "%" in line:
                definition = line.split("let ")[1]
                var, val = definition.split("=")
                var = var.strip()
                value1 = val.split("%")[0].strip()
                value2 = val.split("%")[1].strip()

                value1Exist, value2Exist = inVarMap(s, value1, value2)
                s[var] = modulo(
                    s[value1] if value1Exist else value1,
                    s[value2] if value2Exist else value2,
                )
                i += 1
            else:
                definition = line.split("let ")[1]
                var, val = definition.split("=")
                var = var.strip()
                val = val.strip()
                if val not in s.keys():
                    s[var] = val
                else:
                    s[var] = s[val]
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


main("program1.ez")
