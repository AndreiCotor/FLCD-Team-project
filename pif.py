def read_pif():

    with open("token.in", "r") as file:
        tokens = file.readlines()

    with open("pif.out", "r") as file:
        lines = file.readlines()

    idx = lines.index("Symbol table:\n")

    pif_lines = lines[1:idx]
    pif_data = []
    for line in pif_lines:
        line = line.strip()
        if line:
            index, value = eval(line)

            if index != -1:
                token = tokens[index].strip()
                pif_data.append(token)
            else:
                if value[0] == "ID":
                    pif_data.append("Identifier")
                elif value[0] == "INT":
                    pif_data.append("IntConstant")
                else:
                    pif_data.append("StringConstant")

    return pif_data
