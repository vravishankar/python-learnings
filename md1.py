import sys
import json

DEFAULT_PADDING = 2


def pad_to(unpadded, target_len):
    """
    Pad a string to the target length in characters, or return the original
    string if it's longer than the target length.
    """
    under = target_len - len(unpadded)
    if under <= 0:
        return unpadded
    return unpadded + (' ' * under)


def normalize_cols(table):
    """
    Pad short rows to the length of the longest row to help render "jagged"
    CSV files
    """
    longest_row_len = max([len(row) for row in table])
    for row in table:
        while len(row) < longest_row_len:
            row.append('')
    return table


def pad_cells(table):
    """Pad each cell to the size of the largest cell in its column."""
    col_sizes = [max(map(len, col)) for col in zip(*table)]
    for row in table:
        for cell_num, cell in enumerate(row):
            row[cell] = pad_to(cell, col_sizes[cell_num])
    return table


def horiz_div(col_widths, horiz, vert, padding):
    """
    Create the column dividers for a table with given column widths.
    col_widths: list of column widths
    horiz: the character to use for a horizontal divider
    vert: the character to use for a vertical divider
    padding: amount of padding to add to each side of a column
    """
    horizs = [horiz * w for w in col_widths]
    div = ''.join([padding * horiz, vert, padding * horiz])
    return div.join(horizs)


def add_dividers(row, divider, padding):
    """Add dividers and padding to a row of cells and return a string."""
    div = ''.join([padding * ' ', divider, padding * ' '])
    return div.join(row)


def md_table(table, padding=DEFAULT_PADDING, divider='|', header_div='-'):
    """
    Convert a 2D array of items into a Markdown table.
    padding: the number of padding spaces on either side of each divider
    divider: the vertical divider to place between columns
    header_div: the horizontal divider to place between the header row and
        body cells
    """
    table = normalize_cols(table)
    print(table)
    table = pad_cells(table)
    header = table[0]
    body = table[1:]

    col_widths = [len(cell) for cell in header]
    horiz = horiz_div(col_widths, header_div, divider, padding)

    header = add_dividers(header, divider, padding)
    body = [add_dividers(row, divider, padding) for row in body]

    table = [header, horiz]
    table.extend(body)
    table = [row.rstrip() for row in table]
    return '\n'.join(table)


def main():
        data = """
        {
            "data": [
                {
                    "incidents": [
                        {
                            "incident_no": "INCH00009101",
                            "incident_date": "30/06/2019 10:00:00"
                        },
                        {
                            "incident_no": "INCH00009102",
                            "incident_date": "30/06/2019 10:00:01"
                        }
                    ]
                }
            ]
        }
        """
        json_data = json.loads(data)
        table = json_data['data'][0]['incidents']
        # Generate and print Markdown table
        print(md_table(table, padding=4))


if __name__ == '__main__':
    main()