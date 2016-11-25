"""Script to """
from sys import argv
from sys import exit as sysexit

def isint(test):
    """Tests if test is an integer."""
    try:
        int(test)
        return True
    except ValueError:
        pass
    return False

def writer(outfile, lines, char_count=100):
    """Writes a slice to char_count."""
    toks = [y for x in lines for y in x.split(" ")]
    current_lin = []
    current_len = 0
    last_action_append = False
    for tok in toks:
        # if 0, we had a line with just newline.
        # won't get empty strings elsewhere since we strip before
        # passing to this function.
        if not len(tok):
            if len(current_lin):
                current_lin[-1] += '\n'
                outfile.write(" ".join(current_lin))
                current_lin, current_len = [], 0
                last_action_append = True
            outfile.write("\n")
        elif current_len + len(tok) > char_count:
            current_lin[-1] += '\n'
            outfile.write(" ".join(current_lin))
            current_lin, current_len = [tok], len(tok) + 1
            last_action_append = True
        else:
            current_lin.append(tok)
            current_len += len(tok) + 1
            last_action_append = False

    if not last_action_append:
        current_lin[-1] += '\n'
        outfile.write(" ".join(current_lin))

def strip(tok):
    """Strips, leaving the single newline character alone."""
    if tok != "\n":
        return tok.strip()
    return ""

def main():
    """Reads and writes from and to a test file."""
    if len(argv) > 3 or not isint(argv[2]):
        print("Usage: format.py file.txt 80")
        sysexit(1)
    if len(argv) == 3:
        max_len = int(argv[2])

    with open(argv[1], 'r') as infile:
        lines = infile.readlines()
    lines = [strip(x) for x in lines]

    try:
        start = lines.index(r"\begin{document}")
        end = lines.index(r"\end{document}")
    except ValueError:
        print("Document does not have matching begin/end document tags.")
        sysexit(1)

    with open(argv[1], 'w') as outfile:
        for i in range(0, start + 1):
            outfile.write(lines[i] + '\n')
        writer(outfile, lines[start + 1: end], char_count=max_len)
        for i in range(end, len(lines)):
            outfile.write(lines[i] + '\n')

if __name__ == "__main__":
    main()
