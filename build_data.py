import os
import re
import json
import shutil

MD_FILE = "品飲紀錄.md"
OUTPUT_JS = os.path.join("public", "data.js")
IMAGE_DEST_DIR = os.path.join("public", "images")
IMAGE_SEARCH_DIR = "酒"

def parse_markdown():
    if not os.path.exists(MD_FILE):
        print(f"Error: {MD_FILE} not found in {os.getcwd()}")
        return

    os.makedirs(IMAGE_DEST_DIR, exist_ok=True)

    with open(MD_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    wines = []
    
    img_regex = re.compile(r'src="([^"]+)"')

    in_table = False
    
    for line in lines:
        line = line.strip()
        if not line.startswith("|") or "---|---|---" in line:
            continue
            
        cells = [c.strip() for c in line.split('|')[1:-1]]
        # We expect 5 columns: 圖片 | 酒名 | 價錢 | 酒種 | 標籤
        if len(cells) >= 5:
            img_html = cells[0]
            name = cells[1]
            price_str = cells[2]
            category = cells[3]
            tag = cells[4]
            
            if name == "酒名" or "圖片" in img_html:
                continue # Header
                
            img_src = ""
            img_match = img_regex.search(img_html)
            if img_match:
                img_src = img_match.group(1)
            
            new_img_src = ""
            if img_src:
                filename = os.path.basename(img_src)
                filename_jpg = filename.replace('.jpeg', '.jpg')
                
                # Check paths
                paths_to_try = [
                    img_src, # exact
                    os.path.join(IMAGE_SEARCH_DIR, filename),
                    os.path.join(IMAGE_SEARCH_DIR, filename_jpg)
                ]
                
                actual_path = None
                for p in paths_to_try:
                    if os.path.exists(p):
                        actual_path = p
                        break
                        
                if actual_path:
                    dest_path = os.path.join(IMAGE_DEST_DIR, filename)
                    shutil.copy2(actual_path, dest_path)
                    new_img_src = f"./images/{filename}"
                else:
                    print(f"Warning: Image not found for {filename}")
                    new_img_src = f"./images/{filename}" # fallback
                    
            # parse price
            price_val = 0
            currency = "JPY"
            if "NT$" in price_str:
                currency = "TWD"
                price_val = "".join(filter(str.isdigit, price_str))
            else:
                price_val = "".join(filter(str.isdigit, price_str))
                
            price_val = int(price_val) if price_val else 0

            # Parse rank from tag
            rank = "-"
            tag_clean = []
            for t in [x.strip() for x in tag.split('、')]:
                if t in ["Top10", "Top 10"]:
                    rank = "S+"
                elif t in ["Top20", "Top 20"]:
                    rank = "S"
                elif t in ["Top50", "Top 50"]:
                    rank = "A"
                elif t in ["Top100", "Top 100"]:
                    rank = "B"
                elif t == "知名銘柄":
                    rank = "C"
                else:
                    tag_clean.append(t)
            
            clean_tag = "、".join(tag_clean)

            item = {
                "id": len(wines) + 1,
                "category": category,
                "tag": clean_tag,
                "name": name,
                "image": new_img_src,
                "price": price_val,
                "currency": currency,
                "saketime_rank": rank, 
                "note": ""
            }
            wines.append(item)

    # Write to data.js
    js_content = "const wineData = " + json.dumps(wines, ensure_ascii=False, indent=2) + ";\n"
    
    with open(OUTPUT_JS, 'w', encoding='utf-8') as f:
        f.write(js_content)
        
    print(f"Successfully parsed {len(wines)} wines and wrote to {OUTPUT_JS}")

if __name__ == "__main__":
    parse_markdown()
