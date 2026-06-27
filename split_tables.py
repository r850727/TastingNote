import os
from collections import defaultdict

md_file = "品飲紀錄.md"
with open(md_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

header_lines = []
for line in lines:
    if "## 詳細清單" in line:
        header_lines.append(line)
        break
    header_lines.append(line)

tables = defaultdict(list)
for line in lines:
    if line.strip().startswith("|") and "---|---|---" not in line and "圖片 | 酒名" not in line:
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) >= 5:
            cat = cells[3]
            tables[cat].append(line)

new_content = "".join(header_lines) + "\n"

order = ["威士忌", "果實酒", "清酒", "烈酒", "葡萄酒", "其他"]
# add any other categories just in case
for cat in list(tables.keys()):
    if cat not in order:
        order.append(cat)

for cat in order:
    if cat in tables and len(tables[cat]) > 0:
        new_content += f"### {cat}\n\n"
        new_content += "| 圖片 | 酒名 | 價錢 | 酒種 | 標籤 |\n"
        new_content += "|---|---|---|---|---|\n"
        # sort alphabetically by name for neatness? The prompt doesn't ask, I'll keep original order.
        for row in tables[cat]:
            new_content += row
        new_content += "\n"

with open("品飲紀錄.md", "w", encoding="utf-8") as f:
    f.write(new_content)

with open("images_table.md", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Tables split successfully!")
