import os
import glob
import sys

def rename_jpg():
    count = 0
    # Windows 對大小寫不敏感，所以用 listdir 來精確匹配
    for f in os.listdir("."):
        if f.endswith(".JPG"):
            new_name = f[:-4] + ".jpg"
            temp_name = f + ".tmp"
            print(f"重新命名: {f} -> {new_name}")
            # 先改名成暫存檔，再改成小寫檔名，避免 Windows 大小寫判定衝突
            os.rename(f, temp_name)
            os.rename(temp_name, new_name)
            count += 1
    print(f"已完成 {count} 個 .JPG 重新命名為 .jpg")

def convert_heic():
    # Windows 的 listdir 大小寫都要檢查
    heic_files = [f for f in os.listdir(".") if f.lower().endswith(".heic")]
    if not heic_files:
        print("沒有找到需要轉換的 HEIC 圖片。")
        return
    
    try:
        from PIL import Image
        from pillow_heif import register_heif_opener
        register_heif_opener()
        
        count = 0
        for f in heic_files:
            new_name = os.path.splitext(f)[0] + ".jpg"
            if not os.path.exists(new_name):
                print(f"正在轉換: {f} -> {new_name}")
                img = Image.open(f)
                img.save(new_name, "JPEG")
                count += 1
            else:
                print(f"檔案已存在，跳過轉換: {new_name}")
        print(f"已成功轉換 {count} 個 HEIC 檔案為 .jpg！")
    except ImportError:
        print("缺少必要的 Python 套件！請先執行: pip install pillow pillow-heif")
        sys.exit(1)

if __name__ == "__main__":
    print("開始處理圖片...")
    rename_jpg()
    convert_heic()
    print("圖片處理完成！")
