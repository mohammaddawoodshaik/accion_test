__author__ = "Dawood"

import sys


def parse_the_contents():
    """
    Read the data from STDIN and parse the contents and write back them in to STDOUT.
    :return: There is no return.
    """
    index = 0
    sub_index = 0
    previous_line = ""
    for line in sys.stdin:
        if line.strip():
            line_meta = line.split()[0]
            if line_meta == "*":
                # If there are any old entries from previous section, this make sure those are handled
                if previous_line:
                    indentation_collapse(previous_line)
                    previous_line = ""
                index += 1
                # Re-initialize the sub index data for next section
                sub_index = 0
                sys.stdout.write(str(index) + line.lstrip("*"))
            elif line_meta.startswith("*"):
                # If there are any old entries from previous section, this make sure those are handled
                if previous_line:
                    indentation_collapse(previous_line)
                    previous_line = ""
                # In our input we have only upto two level index handling. There is no criteria defined for 3.1.1->3.1.2
                if len(line_meta) == 2:
                    sub_index = sub_index + 1
                data = str(index) + "." + str(sub_index)
                for i in range(len(line_meta)-2):
                    data = data + "."+"1"
                sys.stdout.write(data + " " + line.lstrip("*"))
            else:
                if not previous_line:
                    previous_line = line
                    continue
                previous_line = indentation_collapse(previous_line, line)
    if previous_line:
        indentation_collapse(previous_line)


def indentation_collapse(previous_line, current_line=""):
    """
    Will Compare the indentation of the current line and the previous line.
    According to the indentation this will collapse the rows.
    :param previous_line: Line prior to the current line
    :param current_line: Line read from teh stdin
    :return: Will return the current line
    """
    previous_line_meta = len(previous_line.split()[0])
    if current_line.split():
        current_line_meta = len(current_line.split()[0])
    else:
        current_line_meta = 0
    if current_line:
        if not current_line.startswith("."):
            return previous_line + "$MERGE$" + current_line
    data = ""
    for i in range(previous_line_meta):
        data = data + " "
    if current_line_meta == 0:
        sys.stdout.write(data + "-" + previous_line.lstrip("."))
    elif current_line_meta > previous_line_meta:
        previous_line_slpit = previous_line.split("$MERGE$")
        sys.stdout.write(data + "+" + previous_line_slpit[0].lstrip("."))
        for line in previous_line_slpit[1:]:
            sys.stdout.write(data + line)
    else:
        previous_line_slpit = previous_line.split("$MERGE$")
        sys.stdout.write(data + "-" + previous_line_slpit[0].lstrip("."))
        for line in previous_line_slpit[1:]:
            sys.stdout.write(data + line)
    return current_line


#The main parser method where STDIN will get read and data will get transformed and written back to STDOUT
parse_the_contents()

