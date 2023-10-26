from dataclasses import dataclass

from colours import colours

@dataclass(repr=False)
class Table:
    table_head: str
    heading_strings: list[str]
    vertedge: str
    table_middle: str
    value_strings: list[str]
    table_foot: str

    def __repr__(self) -> str:
        s = ""
        s += self.table_head + "\n"
        for heading_string in self.heading_strings:
            s += heading_string
        s += self.vertedge + "\n"
        s += self.table_middle + "\n"
        for row_num, row in enumerate(self.value_strings):
            for value in row:
                s += value
            s += self.vertedge + "\n"
            if row_num != len(self.value_strings) - 1:
                s += self.table_middle + "\n"
        s += self.table_foot + "\n"
        return s


def to_table(border_chars: str, lpadding: int, rpadding: int, headings: list[str], values: list[list[any]]) -> Table:

    # makes sure the correct number of border chars are provided
    assert (len(border_chars) == 11)

    ldcorner = border_chars[0]
    rdcorner = border_chars[1]
    lucorner = border_chars[2]
    rucorner = border_chars[3]
    lrdedge  = border_chars[4]
    lduedge  = border_chars[5]
    lruedge  = border_chars[6]
    rduedge  = border_chars[7]
    vertedge = border_chars[8]
    horzedge = border_chars[9]
    cross    = border_chars[10]

    value_strings = [ # converts all values to string to easily size
        [str(value) for value in row]
        for row in values
    ]

    heading_strings = headings[:]

    # finds the width and height of the table which are used in formatting
    height = len(values)
    width  = len(values[0])

    # cant have the wrong number of headings
    assert (len(heading_strings) == width)

    # gathering how many characters each column will be in width
    column_widths = []
    for x in range(width):
        max_string_length = 0

        for y in range(height):
            temp_string = value_strings[y][x]

            for colour in colours.values():
                temp_string = temp_string.replace(colour, "")

            new_string_length = len(temp_string)
            max_string_length = max([max_string_length, new_string_length])

        column_widths.append(max_string_length)

    for i, (column_width, heading_string) in enumerate(zip(column_widths, heading_strings)):
        heading_length = len(heading_string)
        column_widths[i] = max([heading_length, column_width])

    # makes sure padding isn't less than zero
    assert (lpadding >= 0)
    assert (rpadding >= 0)

    # adding buffer spaces to format table content and vertical borders
    for x, column_width in enumerate(column_widths):
        buffer = column_width - len(heading_strings[x])
        lpadding_space = " " * lpadding
        rpadding_space = " " * rpadding
        buffer_space = " " * buffer
        heading_strings[x] = vertedge + lpadding_space + heading_strings[x] + buffer_space + rpadding_space

        for y in range(len(value_strings)):
            temp_string = value_strings[y][x]
            for colour in colours.values():
                temp_string = temp_string.replace(colour, "")

            buffer = column_width - len(temp_string)
            lpadding_space = " " * lpadding
            rpadding_space = " " * rpadding
            buffer_space = " " * buffer
            value_strings[y][x] = vertedge +  lpadding_space + value_strings[y][x] + buffer_space + rpadding_space

    # updates the widths for border characters
    column_widths = [
        column_width + lpadding + rpadding
        for column_width in column_widths
    ]

    # create lines
    table_head = rdcorner + lrdedge.join([horzedge * column_width for column_width in column_widths]) + ldcorner
    table_foot = rucorner + lruedge.join([horzedge * column_width for column_width in column_widths]) + lucorner
    table_middle = rduedge + cross.join([horzedge * column_width for column_width in column_widths]) + lduedge

    return Table (table_head, heading_strings, vertedge, table_middle, value_strings, table_foot)

    # print table



def ascii_table(headings: list[str], values: list[list[any]]) -> Table:
    return to_table("++++++++|-+", 1, 1, headings, values)


def unicode_table(headings: list[str], values: list[list[any]]) -> Table:
    return to_table("┐┌┘└┬┤┴├│─┼", 1, 1, headings, values)


# t = unicode_table(["Fruit", "Weight"], [["Apple", 200], ["Pear", 300]])
# print(repr(t))