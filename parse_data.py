import os
import re
import json
import shutil

MD_FILE = r"酒\喝過的酒.md"
OUTPUT_JS = r"public\data.js"
IMAGE_DEST_DIR = r"public\images"
IMAGE_SEARCH_DIR = r"酒"

def parse_markdown():
    if not os.path.exists(MD_FILE):
        print(f"Error: {MD_FILE} not found.")
        return

    with open(MD_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_category = None
    wines = []
    
    # regex for markdown table row
    row_regex = re.compile(r'^\|(.*)\|$')
    img_regex = re.compile(r'<img.*?src="([^"]+)".*?>')

    in_table = False
    headers = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith("## "):
            current_category = line[3:].strip()
            in_table = False
            continue
            
        if line.startswith("|") and "---" in line:
            continue # separator line
            
        if line.startswith("|"):
            cells = [cell.strip() for cell in line.split("|")[1:-1]]
            
            if not in_table or cells[0] == "圖片" or "名稱" in cells[1]:
                headers = cells
                in_table = True
                continue
            
            if len(cells) < 2:
                continue

            # Parse image
            img_html = cells[0]
            img_match = img_regex.search(img_html)
            img_src = img_match.group(1) if img_match else ""
            
            # Copy image to public/images if it exists
            new_img_src = ""
            if img_src:
                filename = os.path.basename(img_src)
                # Some files might have .jpeg in markdown but .jpg on disk
                filename_jpg = filename.replace('.jpeg', '.jpg')
                
                img_path_exact = os.path.join(os.path.dirname(MD_FILE), img_src)
                img_path_search1 = os.path.join(IMAGE_SEARCH_DIR, filename)
                img_path_search2 = os.path.join(IMAGE_SEARCH_DIR, filename_jpg)
                
                actual_path = None
                if os.path.exists(img_path_exact):
                    actual_path = img_path_exact
                elif os.path.exists(img_path_search1):
                    actual_path = img_path_search1
                elif os.path.exists(img_path_search2):
                    actual_path = img_path_search2
                
                if actual_path:
                    dest_path = os.path.join(IMAGE_DEST_DIR, os.path.basename(actual_path))
                    shutil.copy2(actual_path, dest_path)
                    new_img_src = f"./images/{os.path.basename(actual_path)}"
                else:
                    new_img_src = img_src # keep original if not found
                    print(f"Warning: Image not found for {filename}")

            name = cells[1] if len(cells) > 1 else ""
            if not name:
                continue
                
            item = {
                "id": len(wines) + 1,
                "main_category": current_category,
                "name": name,
                "image": new_img_src,
                "saketime_rank": None, # Default to None
            }
            
            if len(cells) >= 6: # Sake format
                item["category"] = cells[2]
                item["method"] = cells[3]
                item["price"] = cells[4]
                item["note"] = cells[5]
            elif len(cells) >= 4: # Other format
                item["price"] = cells[2]
                item["note"] = cells[3]
                item["category"] = "-"
                item["method"] = "-"
                
            wines.append(item)

    # Write to data.js
    js_content = "const wineData = " + json.dumps(wines, ensure_ascii=False, indent=2) + ";\n"
    
    with open(OUTPUT_JS, 'w', encoding='utf-8') as f:
        f.write(js_content)
        
    print(f"Successfully parsed {len(wines)} wines and wrote to {OUTPUT_JS}")

if __name__ == "__main__":
    parse_markdown()
