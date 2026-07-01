# 網站更新流程 (Update Workflow)

當使用者更新了 `品飲紀錄.md` 後，請 AI 助手嚴格依照以下順序執行後續作業，完成資料同步與網站發布：

## 1. 表格排序 (Sorting Tables)
* **執行命令**：`python sort_tables.py`
* **目的**：讀取 `品飲紀錄.md` 中的酒款表格，自動進行重新排序。
* **排序規則**：「有圖片的酒款」放置於上方，「無圖片的酒款」移至該表格的最下方。而在兩組內部，會再根據「酒名」自動以字母/筆畫進行遞增排序。

## 2. 重新編譯網頁資料與圖片 (Build Data)
* **執行命令**：`python build_data.py`
* **目的**：讀取剛排序好的 `品飲紀錄.md`，將內容轉為網站需要的 JSON 格式，並寫入到 `public/data.js` 中。
* **處理細節**：這個腳本會自動檢查 `酒/` 目錄下的圖片大小寫，確保複製到 `public/images/` 裡面的檔名，以及寫入 `data.js` 裡的路徑**大小寫完全一致**，避免未來部署在 Linux 或 GitHub Pages 上發生圖片無法顯示的問題。

## 3. 版本控制與上傳 (Git Commit & Push)
* **執行命令**：
  ```bash
  git add .
  git commit -m "Update tasting notes, rebuild data, and sort tables"
  git push
  ```
* **目的**：將更新後的 `品飲紀錄.md`、生成的 `data.js`、與新複製的圖片等所有變更，一次性提交並上傳到使用者的 GitHub 儲存庫 (`r850727/TastingNote`)，以觸發後續的發布流程。

---

> **對 AI 助手的特別指示**：
> 以後只要使用者說「更新網頁」、「我更新了品飲紀錄」，或者是「幫我上傳」，請直接讀取此 `update.md`，並循序漸進幫使用者執行上述 3 個步驟，即可自動完成所有工作！
