# 分散式資源班間接服務紀錄系統

Indirect Service Tracker for Resource Room

[![Version](https://img.shields.io/badge/version-1.1-blue)]()
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey)](http://creativecommons.org/licenses/by-nc-sa/4.0/)

高中職資源班教師專用的輕量化間接服務紀錄工具，協助簡化登錄、統計與報表產出流程。系統採用單一 HTML 檔案架構，免安裝、跨平台、資料落地儲存在使用者自己的瀏覽器中。

## 主要功能

- **單一檔案架構**：純 HTML 技術構建，不需安裝任何軟體或資料庫伺服器，下載後雙擊即可在瀏覽器中開啟使用。
- **紀錄管理與儀表板**：提供新增、編輯、刪除介面，並內建數據儀表板即時運算總服務時數、服務人次及各類型佔比。
- **報表輸出**：列印模式支援日期範圍篩選、紙張方向(直式/橫式)選擇，自動生成統計圖表與詳細紀錄表；另提供標準 CSV 格式匯出，方便轉入一般試算表軟體做後續處理。
- **資料安全與個人化**：內建 JSON 格式的備份與還原功能；支援深色模式切換。

## 使用方式

1. 下載 `IndirectServiceTracker_v1_1.html`。
2. 用瀏覽器（建議 Chrome / Edge）開啟該檔案即可使用，所有資料儲存在瀏覽器的 `localStorage`，不會上傳到任何伺服器。
3. 建議定期使用「資料備份」頁籤匯出 JSON 備份檔，避免清除瀏覽器資料時遺失紀錄。

## 版本資訊

- 目前版本：**V1.1**
- 授權：[CC BY-NC-SA 4.0](http://creativecommons.org/licenses/by-nc-sa/4.0/)（創用 CC 姓名標示-非商業性-相同方式分享 4.0 國際）
- 參考依據：教育部國民及學前教育署《分散式資源班間接服務參考手冊》(第二版)
- 詳細版本更新內容請見 [CHANGELOG.md](./CHANGELOG.md)
