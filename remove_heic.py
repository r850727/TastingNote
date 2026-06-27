import os

def remove_converted_heic():
    # 尋找所有 HEIC 檔案 (不區分大小寫)
    heic_files = [f for f in os.listdir(".") if f.lower().endswith(".heic")]
    count = 0
    not_converted = 0
    
    for f in heic_files:
        # 取得對應的 jpg 檔名
        jpg_name = os.path.splitext(f)[0] + ".jpg"
        
        # 檢查 jpg 檔案是否存在
        if os.path.exists(jpg_name):
            print(f"✅ 確認已存在 {jpg_name}，安全移除: {f}")
            os.remove(f)
            count += 1
        else:
            print(f"⚠️ 找不到對應的 {jpg_name}，保留原始檔: {f}")
            not_converted += 1
            
    print("-" * 30)
    print(f"🎉 成功移除 {count} 個已轉換的 HEIC 檔案。")
    if not_converted > 0:
        print(f"有 {not_converted} 個 HEIC 檔案因為尚未轉換而被保留。")

if __name__ == "__main__":
    print("開始檢查並清理 HEIC 檔案...")
    remove_converted_heic()
