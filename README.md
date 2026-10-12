# 分散式資源班間接服務紀錄系統 IST

**Indirect Service Tracker for Resource Room · v1.4**

[![Version](https://img.shields.io/badge/version-1.4-blue)](../../releases/latest)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey)](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hant)
[![Platform](https://img.shields.io/badge/Platform-Browser%20(Offline)-blue)](#技術說明)
[![Ko-fi](https://img.shields.io/badge/Support-Ko--fi-FF5E5B?logo=ko-fi)](https://ko-fi.com/izensun)

高中職資源班教師專用的輕量化間接服務紀錄工具，協助簡化登錄、統計與報表產出流程。系統採用單一 HTML 檔案架構，免安裝、跨平台、完全離線可用，資料落地儲存在使用者自己的瀏覽器中。

---

## 主要功能

- **單一檔案架構**：純 HTML 技術構建，不需安裝任何軟體、帳號、伺服器或網路連線，下載後雙擊即可在瀏覽器中開啟使用。
- **紀錄管理與成果統計**：提供新增、編輯、刪除介面；成果報告頁可依日期、學生、服務對象篩選，並提供「本學期／本學年」快速期間，自動統計各服務項目節數、服務對象人次，並以長條圖與圓餅圖呈現各類型佔比。
- **報表輸出**：以 A4 直式列印成果報告與統計圖表，報告標題下方自動帶入學校、學年度學期、資源班教師與統計期間；另提供標準 CSV 格式匯出，方便轉入一般試算表軟體做後續處理。
- **學生名單（與 SEAM 整合）**：可從 [SEAM 特殊教育行政管理系統](https://github.com/taitungsun/seam) 匯入在學學生名單，登錄時直接選取學生，避免同一學生出現不同寫法。
- **資料安全與個人化**：JSON 備份與還原、超過 30 天未備份自動提醒、儲存用量顯示；支援深色模式切換。

---

## 快速開始

1. 到 [Releases](../../releases) 下載最新版的 `IndirectServiceTracker_v1_4.html`。
2. 用瀏覽器（建議 Chrome / Edge）開啟該檔案即可使用。
3. 首次使用時，到「設定與備份」頁填寫學校名稱與資源班教師，這些資料會顯示在成果報告上。
4. （選用）若有使用 SEAM，可在「設定與備份 → 學生名單」匯入學生名單。

---

## 資料備份與還原

所有資料存放在瀏覽器的 `localStorage`，不會上傳到任何伺服器。**清除瀏覽器資料或更換電腦都會讓資料消失**，請養成定期備份的習慣；超過 30 天未備份時，系統會在頁面上方提醒。

| 操作 | 方式 |
| --- | --- |
| 備份 | 「設定與備份」頁 →「下載備份 (JSON)」，檔名如 `IST_2610121630.json`（西元年末兩碼＋月日時分），內含紀錄、報告基本資料與學生名單 |
| 還原 | 「設定與備份」頁 → 還原，選取備份的 `.json` 檔（可還原 V1.0 以後所有版本的備份） |
| 匯出 Excel | 「設定與備份」頁 →「匯出 Excel (CSV)」，用於行政繳交或外部編輯 |
| 清除資料 | 「歷史紀錄」頁 →「清除所有資料」（無法復原，請先備份） |

### 從舊版升級

- 用**同一個瀏覽器**開啟新版檔案，即可直接看到原有資料。V1.4 起資料改存於 `ist_` 開頭的鍵名，首次開啟時會自動複製舊資料，舊資料保留不刪除。
- 部分瀏覽器會依檔案存放位置分開儲存，若新版中看不到資料，請用舊版匯出 JSON 備份，再於新版還原即可。
- 若要換瀏覽器或換電腦，請先匯出 JSON 備份，再於新環境還原。

---

## 學生名單與 SEAM 整合

| 方式 | 說明 |
| --- | --- |
| 匯入 SEAM 備份檔 | 選取 SEAM 匯出的 `SEAM_*.json` 備份檔 |
| 讀取本瀏覽器的 SEAM 名單 | 若 SEAM 與 IST 在同一個瀏覽器中開啟過，會出現此按鈕，可直接讀取、不必匯出檔案 |

- 只匯入「在學」學生的**姓名、班級、座號**，不會複製 SEAM 中的其他個人資料。
- 若 IST 尚未設定學校名稱，會一併帶入 SEAM 的學校名稱。
- 登錄紀錄時，輸入名單外的姓名會先確認一次；過去紀錄中已出現的姓名（如已畢業學生）不再詢問。

---

## 技術說明

- **架構**：單一 HTML 檔，原生 JavaScript，不依賴任何框架
- **內嵌套件**：Chart.js 4.5.1、chartjs-plugin-datalabels 2.2.0（皆為 MIT 授權），已內建於檔案中，離線可用
- **圖示**：使用系統內建 emoji，不需載入外部圖示庫
- **儲存**：瀏覽器 `localStorage`（約 5 MB；設定頁可查看目前用量）
- **隱私**：資料只存在使用者本機，不會傳送到任何伺服器

---

## 版本資訊

- 目前版本：**V1.4**
- 參考依據：教育部國民及學前教育署《分散式資源班間接服務參考手冊》(第二版)
- 詳細版本更新內容請見 [CHANGELOG.md](CHANGELOG.md)

---

## 授權

本系統採用 [創用 CC 姓名標示-非商業性-相同方式分享 4.0 國際授權條款（CC BY-NC-SA 4.0）](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hant)。

- **姓名標示**：使用或改作時，須標示原作者。
- **非商業性**：不得用於商業目的。
- **相同方式分享**：改作後再散布，須採用相同授權條款。

完整條款請見 [LICENSE](LICENSE)。

---

## 支持開發

如果這個工具對您有幫助，歡迎透過 Ko-fi 請我喝杯咖啡 ☕

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/izensun)

---

## 作者

Designed by [@izensun](https://mastodon.social/@izensun)
Built with [Claude](https://claude.ai) (Anthropic)
