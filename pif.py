def read_pif():
    symbol_table = {
        "INT": [],
        "STRING": [],
        "ID": []
    }

    with open("pif.out", "r") as file:
        lines = file.readlines()

    idx = lines.index("Symbol table:\n")
    st_lines = lines[idx+2:]

    section = "ID"
    for line in st_lines:
        if line.strip() == "INT:":
            section = "INT"
            continue
        if line.strip() == "STRING:":
            section = "STRING"
            continue

        line_list = eval(line)
        symbol_table[section].append(line_list)

    pif_lines = lines[1:idx]
    pif_data = []
    for line in pif_lines:
        line = line.strip()
        if line:
            index, value = eval(line)

            if index != -1:
                token = tokens[index]
                pif_data.append(token)
            else:
                if value[0] == ""

    return pif_data