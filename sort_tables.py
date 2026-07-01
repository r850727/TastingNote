import re

MD_FILE = "品飲紀錄.md"

def sort_tables():
    with open(MD_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    output_lines = []
    in_data_table = False
    table_header = []
    table_rows = []

    def flush_table():
        if not table_rows:
            return
        
        # Sort table_rows
        # row is a list of columns. row[0] is image, row[1] is name
        def sort_key(row_tuple):
            row_str = row_tuple[1]
            cells = [c.strip() for c in row_str.split('|')[1:-1]]
            if len(cells) < 2:
                return (0, "")
            
            img_col = cells[0]
            name_col = cells[1]
            
            has_img = "<img" in img_col
            return (1 if not has_img else 0, name_col)

        table_rows.sort(key=sort_key)
        
        output_lines.extend(table_header)
        for row in table_rows:
            output_lines.append(row[1])
        
        table_header.clear()
        table_rows.clear()

    i = 0
    while i < len(lines):
        line = lines[i]
        
        if line.strip().startswith("| 圖片 | 酒名 |"):
            flush_table()
            in_data_table = True
            table_header.append(line)
            # Next line should be separator
            if i + 1 < len(lines) and lines[i+1].strip().startswith("|---|"):
                table_header.append(lines[i+1])
                i += 1
        elif in_data_table:
            if line.strip().startswith("|"):
                table_rows.append((i, line))
            else:
                flush_table()
                in_data_table = False
                output_lines.append(line)
        else:
            output_lines.append(line)
            
        i += 1

    flush_table() # in case file ends with table

    with open(MD_FILE, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)

    print("Tables sorted successfully!")

if __name__ == "__main__":
    sort_tables()
