"""
prints any string as a block with (n number) of words max per line 
"""
def print_str_as_blocks(str, char_limit=70) -> str:
    str_split = str.split(" ")
    line = ""
    block = ""
    lines = []
    for i, str in enumerate(str_split):
        line += str
        if len(line) > char_limit:
            line += "\n"
            block += line
            line = ""
        else:
            line += " "
        if i == len(str_split)-1:
            block+=line
        if "\n" in str:
            block += line
            line = ""
    print(block)

def remove_extra_lines(str):
    temp = ""
    repeat_nline = False
    for i in str:
        if i == "\n":
            if not repeat_nline:
                repeat_nline = True
                temp += i
            else:
                continue
        else:
            if i != " ":
                repeat_nline = False
            temp += i
            continue
    return temp