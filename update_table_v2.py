import os

MD_FILE = "images_table.md"

def determine_category_and_tag(name):
    name_lower = name.lower()
    
    # 威士忌
    if any(k in name_lower for k in ["whisky", "威士忌", "大摩", "格蘭傑", "高原騎士"]):
        if any(k in name_lower for k in ["single malt", "單一麥芽", "大摩", "格蘭傑", "高原騎士", "琉歌"]):
            return "威士忌", "單一麥芽威士忌"
        elif "調和" in name_lower:
            return "威士忌", "調和威士忌"
        return "威士忌", "威士忌"
        
    # 琴酒
    if any(k in name_lower for k in ["gin", "琴酒"]):
        return "琴酒", "琴酒"
        
    # 葡萄酒
    if any(k in name_lower for k in ["champagne", "wine", "葡萄酒", "spumante", "紅酒", "白酒", "blanc", "riesling", "domaine", "cru"]):
        if "champagne" in name_lower:
            return "葡萄酒", "香檳"
        if "spumante" in name_lower or ("氣泡" in name_lower and "清酒" not in name) or "sparkling" in name_lower:
            return "葡萄酒", "氣泡酒"
        if "白" in name_lower or "blanc" in name_lower or "riesling" in name_lower:
            return "葡萄酒", "白酒"
        return "葡萄酒", "紅酒"
        
    # 果實酒
    if "梅酒" in name_lower:
        return "果實酒", "梅酒"
    if "柚子酒" in name_lower:
        return "果實酒", "柚子酒"
        
    # 烈酒
    if "高粱" in name_lower:
        return "烈酒", "高粱"
    if "rum" in name_lower or "蘭姆酒" in name_lower:
        return "烈酒", "蘭姆酒"

    # 清酒
    sake_tags = ["純米大吟釀", "純米大吟醸", "大吟釀", "大吟醸", "純米吟釀", "純米吟醸", "吟釀", "吟醸", "特別純米", "特別本釀造", "特別本醸造", "純米", "本釀造", "本醸造"]
    for tag in sake_tags:
        if tag in name:
            clean_tag = tag.replace("醸", "釀")
            return "清酒", clean_tag
            
    if "氣泡清酒" in name_lower or "スパークリング" in name_lower or "微発泡" in name_lower:
        return "清酒", "氣泡清酒"
        
    if any(k in name_lower for k in ["生原酒", "清酒", "直汲み", "おりがらみ"]):
        return "清酒", "清酒 (其他)"
        
    # Known sake brands without explicit grades in name
    if any(k in name_lower for k in ["あべ", "産土", "日日", "亀の海", "十四代", "大嶺"]):
        return "清酒", "清酒 (無標示)"

    return "其他", "其他"

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
            # Check if this is the header of the main table
            # It could be | 圖片 | 酒名 | 價錢 | or | 圖片 | 酒名 | 價錢 | 標籤 |
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

    # We will track tags grouped by main category
    category_tags = {}
    processed_table = []
    
    for line in table_lines:
        if "---|---|---" in line:
            processed_table.append("| 圖片 | 酒名 | 價錢 | 酒種 | 標籤 |")
            processed_table.append("|---|---|---|---|---|")
            continue
        if "圖片" in line and "酒名" in line:
            continue # Header is handled above
            
        # cells: [img, name, price, tag (optional)]
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) >= 3:
            img = cells[0]
            name = cells[1]
            price = cells[2]
            
            main_cat, sub_tag = determine_category_and_tag(name)
            
            if main_cat not in category_tags:
                category_tags[main_cat] = set()
            category_tags[main_cat].add(sub_tag)
            
            processed_table.append(f"| {img} | {name} | {price} | {main_cat} | {sub_tag} |")

    # Generate summary table
    summary = [
        "## 酒類標籤總覽",
        "",
        "| 酒種 | 細緻分類標籤 |",
        "|---|---|"
    ]
    for cat in sorted(category_tags.keys()):
        tags_str = "、".join(sorted(list(category_tags[cat])))
        summary.append(f"| {cat} | {tags_str} |")
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
