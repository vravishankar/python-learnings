import json

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
            row[cell_num] = pad_to(cell, col_sizes[cell_num])
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


data = """
{
    "data": [
        {
            "incidents": [
                {
                    "incident_no": "INCH00009101",
                    "incident_date": "30/06/2019 10:00:00",
                    "status": "open",
                    "description": "CTL-M job failed. Service restarted"
                },
                {
                    "incident_no": "INCH00009102",
                    "incident_date": "30/06/2019 10:00:00",
                    "status": "closed",
                    "description": "Main job failed. Service restarted"
                }
            ]
        }
    ]
}
"""

json_data = json.loads(data)
print(data)
x = len(json_data['data'][0]['incidents'])

if x > 1:
    header = list(json_data['data'][0]['incidents'][0].keys())
    header = list(k.replace("_"," ").title() for k in header)
    body = []
    for i in range(x):
        vals = list(json_data['data'][0]['incidents'][i].values())
        body.append(vals)
   
    table = [header]
    table.extend(body)
    table = normalize_cols(table)
    table = pad_cells(table)
    col_widths = [len(cell) for cell in header]
    horiz = horiz_div(col_widths, '-','|',1)

    header = add_dividers(header,'|',1)
    body = [add_dividers(row,'|',1) for row in body]
    table = [header, horiz]
    table.extend(body)
    table = [row.rstrip() for row in table]
    print('\n'.join(table))

elif x == 1:
    row = json_data['data'][0]['incidents'][0]
    cols = list(row.keys())
    header = ['Attribute', 'Value']
    body = []
    for col in cols:
        cell = [col.replace('_','').title(),row[col]]
        body.append(cell)

    table = [header]
    print(table)
    table.extend(body)
    print(table)
    table = normalize_cols(table)
    table = pad_cells(table)
    col_widths = [len(cell) for cell in header]
    horiz = horiz_div(col_widths, '-','|',1)

    header = add_dividers(header,'|',1)
    body = [add_dividers(row,'|',1) for row in body]
    table = [header, horiz]
    table.extend(body)
    table = [row.rstrip() for row in table]
    print('\n'.join(table))
else:
    print('|\n|---|\n|No Data Found|')

