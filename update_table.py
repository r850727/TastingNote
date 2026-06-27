import os
import re

MD_FILE = "images_table.md"

def determine_category(name):
    # check for specific sake types first
    if "純米大吟釀" in name or "純米大吟醸" in name:
        return "純米大吟釀"
    if "大吟釀" in name or "大吟醸" in name:
        return "大吟釀"
    if "純米吟釀" in name or "純米吟醸" in name:
        return "純米吟釀"
    if "吟釀" in name or "吟醸" in name:
        return "吟釀"
    if "特別純米" in name:
        return "特別純米"
    if "特別本釀造" in name or "特別本醸造" in name:
        return "特別本釀造"
    if "純米" in name:
        return "純米"
    if "本釀造" in name or "本醸造" in name:
        return "本釀造"
    
    name_lower = name.lower()
    if any(k in name_lower for k in ["gin", "琴酒"]):
        return "Gin (琴酒)"
    if any(k in name_lower for k in ["whisky", "威士忌"]):
        return "Whisky (威士忌)"
    if any(k in name_lower for k in ["champagne", "wine", "葡萄酒", "spumante", "紅酒", "白酒"]):
        return "Wine (葡萄酒)"
    if any(k in name_lower for k in ["梅酒", "柚子酒"]):
        return "Liqueur (果實酒)"
    if any(k in name_lower for k in ["高粱", "rum", "蘭姆酒"]):
        return "Spirits (烈酒)"
    
    # Fallback for other sake or unknown
    if any(k in name_lower for k in ["生原酒", "清酒", "直汲み", "おりがらみ"]):
        return "清酒 (其他)"

    return "其他"

def process_file():
    if not os.path.exists(MD_FILE):
        print(f"{MD_FILE} not found.")
        return

    with open(MD_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find the main table (starts with | 圖片 | 酒名 |)
    table_lines = []
    in_main_table = False
    
    for line in lines:
        line_s = line.strip()
        if not in_main_table:
            if line_s.startswith("|") and "圖片" in line_s and "酒名" in line_s:
                in_main_table = True
                table_lines.append(line_s)
        else:
            if not line_s.startswith("|"):
                in_main_table = False
            else:
                table_lines.append(line_s)
                
    if not table_lines:
        print("No main table found")
        return

    category_counts = {}
    processed_table = []
    
    for line in table_lines:
        if "---|---|---" in line:
            processed_table.append("| 圖片 | 酒名 | 價錢 | 標籤 |")
            processed_table.append("|---|---|---|---|")
            continue
        if "圖片" in line and "酒名" in line:
            continue # Header is handled above
            
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) >= 3:
            img = cells[0]
            name = cells[1]
            price = cells[2]
            
            cat = determine_category(name)
            category_counts[cat] = category_counts.get(cat, 0) + 1
            
            processed_table.append(f"| {img} | {name} | {price} | {cat} |")

    # Generate summary table
    summary = [
        "## 酒款分類統計",
        "",
        "| 分類標籤 | 數量 |",
        "|---|---|"
    ]
    for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        summary.append(f"| {cat} | {count} |")
    summary.append("")
    summary.append("## 詳細清單")
    summary.append("")

    # Write back
    with open(MD_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(summary) + "\n")
        f.write("\n".join(processed_table) + "\n")
        
    print("Done processing.")

if __name__ == "__main__":
    process_file()
