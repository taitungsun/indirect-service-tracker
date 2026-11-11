"""IST 自動測試（Playwright + Chromium，以 file:// 開啟）。
用法：python -I tests/test_ist.py [IST_vX.Y.html]   （預設取 repo 裡版本號最大的主程式）
測試資料一律虛構。"""
import json, pathlib, re, sys, tempfile
sys.stdout.reconfigure(encoding="utf-8")  # Windows 主控台預設 cp950，印不出部分字元（python -I 不讀 PYTHONIOENCODING）
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
def newest():
    fs = [f for f in ROOT.glob('IST_v*.html')]
    ver = lambda f: tuple(int(x) for x in re.findall(r'\d+', f.stem))
    return max(fs, key=ver)
HTML = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else newest()
URL = HTML.as_uri()

results = []
def ok(name, cond, detail=''):
    results.append((bool(cond), name, detail))

def fill_record(pg, name, summary='測試摘要'):
    pg.evaluate("switchTab('record')")
    pg.fill('#date', '2026-11-03')
    pg.select_option('#sessions', '2')
    pg.fill('#studentName', name)
    pg.select_option('#target', '教師')
    pg.select_option('#mainCategory', index=1)
    pg.fill('#summary', summary)
    pg.click('#submitBtn')

def toast(pg):
    return pg.inner_text('#saveAlert').strip()

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(accept_downloads=True)
    external = []
    ctx.route(re.compile(r'^https?://'), lambda r: (external.append(r.request.url), r.abort()))
    pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    msgs = []
    def dlg(d):
        msgs.append(d.message); d.accept()
    pg.on('dialog', dlg)
    pg.goto(URL); pg.wait_for_load_state('load')

    ver = pg.evaluate('APP_VERSION')
    ok('版本號與檔名一致', ver in HTML.name.replace('_', ''), ver)
    tabs = pg.locator('.tab-btn').all_inner_texts()
    ok('頁籤：新增紀錄、歷史紀錄、成果報告、系統設定', tabs == ['新增紀錄', '歷史紀錄', '成果報告', '系統設定'], tabs)
    ok('沒有英文小標', pg.locator('.eyebrow').count() == 0)
    ok('分頁名稱「間接服務紀錄系統 IST」', pg.title() == '間接服務紀錄系統 IST', pg.title())
    t2 = pg.evaluate("(() => { window.dispatchEvent(new Event('beforeprint')); const a = document.title; window.dispatchEvent(new Event('afterprint')); return [a, document.title]; })()")
    ok('列印時換成報告標題、印完恢復', t2 == ['間接服務成果報告', '間接服務紀錄系統 IST'], t2)
    html = HTML.read_text(encoding='utf-8')
    ok('沒有 Google 字型', 'googleapis' not in html and 'gstatic' not in html)

    pg.evaluate("switchTab('settings')")
    ok('設定頁標題「系統設定」', pg.inner_text('#settings-tab h2') == '系統設定')
    heads = pg.locator('#settings-tab h3').all_inner_texts()
    ok('區塊：學校資訊、備份與還原、資料使用量', heads == ['學校資訊', '備份與還原', '資料使用量'], heads)
    btns = pg.locator('#settings-tab .backup-btns button').all_inner_texts()
    ok('備份區按鈕順序（v1.7 移除匯出 CSV）', btns == ['下載備份', '還原備份', '清除資料'], btns)
    cls = pg.locator('#settings-tab .backup-btns button').evaluate_all('bs => bs.map(b => b.className)')
    ok('按鈕樣式：主要、一般、危險', cls == ['', 'btn-sec', 'btn-danger'], cls)
    ok('備份區說明只有一行', pg.locator('#settings-tab .backup-btns + input + p.hint').inner_text() == '資料只存在這台電腦的瀏覽器，請定期下載備份。')

    # 新增、錯誤訊息
    pg.evaluate("switchTab('record')")
    pg.fill('#studentName', ''); pg.click('#submitBtn')
    ok('錯誤訊息不加「錯誤：」', not toast(pg).startswith('錯誤'), toast(pg))
    fill_record(pg, '王小明')
    ok('新增後提示「已新增紀錄」', toast(pg) == '已新增紀錄', toast(pg))
    fill_record(pg, '李小華、陳大同')
    ok('兩筆紀錄', pg.evaluate('records.length') == 2)

    # 歷史紀錄：筆數不與表格重疊
    pg.evaluate("switchTab('list')")
    cnt = pg.locator('#recordCount').bounding_box(); tbl = pg.locator('#dataTable').bounding_box()
    ok('「共 N 筆」在表格上方、不重疊', cnt['y'] + cnt['height'] <= tbl['y'] + 0.5, (cnt, tbl))
    ok('筆數文字', pg.inner_text('#recordCount') == '共 2 筆')

    # 下載備份
    pg.evaluate("switchTab('settings')")
    with pg.expect_download() as dl:
        pg.click('.backup-btns >> text=下載備份')
    path = dl.value.path(); data = json.loads(pathlib.Path(path).read_text(encoding='utf-8'))
    ok('備份檔名', re.fullmatch(r'IST_\d{10}\.json', dl.value.suggested_filename), dl.value.suggested_filename)
    ok('備份最外層 app/version/exportedAt', data.get('app') == 'IST' and data.get('version') == ver and 'exportedAt' in data)
    ok('下載後提示「已下載備份檔」', toast(pg) == '已下載備份檔', toast(pg))


    # 清除資料：問兩次
    pg.click('.backup-btns >> text=清除資料')
    ok('清除資料問兩次', msgs[-2:] == ['確定要清除資料嗎？此動作無法復原，請先下載備份。', '再確認一次：真的要清除所有資料嗎？'], msgs)
    ok('清除後沒有紀錄', pg.evaluate('records.length') == 0)

    # 還原備份
    pg.set_input_files('#restoreFile', path)
    pg.wait_for_function('records.length === 2')
    ok('還原確認文字', any(m.startswith('目前 0 筆，備份檔 2 筆。還原會取代目前所有資料') for m in msgs), msgs[-1])
    ok('還原後提示「已還原備份」', toast(pg) == '已還原備份', toast(pg))

    # 擋下其他系統的備份
    tmp = pathlib.Path(tempfile.mkdtemp())
    for app, body in [('SEAM', {'app': 'SEAM', 'version': 'v1.6', 'students': [], 'budgetTables': []}),
                      ('SEIA', {'app': 'SEIA', 'version': 'beta', 'v': 1, 'cases': []})]:
        f = tmp / f'{app}.json'; f.write_text(json.dumps(body), encoding='utf-8')
        pg.set_input_files('#restoreFile', str(f))
        pg.wait_for_timeout(300)
        ok(f'擋下 {app} 備份', toast(pg) == f'這是 {app} 的備份檔，請在 {app} 還原，目前資料未變動' and pg.evaluate('records.length') == 2, toast(pg))

    # 狀態列與 7 天備份提醒（規範 11.1、13.3）
    pill = lambda: pg.inner_text('#savepill')
    banner = lambda: pg.locator('#backupBanner').is_visible()
    ok('狀態列不加 role=status', pg.get_attribute('#savepill', 'role') is None)
    box = pg.locator('#savepill').bounding_box(); vp = pg.viewport_size
    ok('狀態列固定在畫面右下角', pg.evaluate("getComputedStyle(document.getElementById('savepill')).position") == 'fixed'
       and box and vp['width'] - (box['x'] + box['width']) < 40 and vp['height'] - (box['y'] + box['height']) < 40, box)
    ok('狀態列有「儲存」「備份」按鈕', pg.locator('#savepill button').all_inner_texts() == ['儲存', '備份'])
    ok('還原後顯示已自動儲存時間', re.search(r'✓ 已自動儲存 \d\d:\d\d:\d\d', pill()), pill())
    def set_backup(days_ago):
        pg.evaluate(f"localStorage.setItem('ist_last_backup', new Date(Date.now() - {days_ago} * 86400000).toISOString()); refreshStorageInfo()")
    set_backup(6)
    ok('6 天：不逾期、不顯示提醒', '已逾' not in pill() and not banner(), pill())
    roc = pg.evaluate("(() => { const d = new Date(Date.now() - 6 * 86400000); return `${d.getFullYear() - 1911}/${String(d.getMonth() + 1).padStart(2, '0')}/${String(d.getDate()).padStart(2, '0')}`; })()")
    ok('上次備份以民國年顯示', f'上次備份 {roc}' in pill(), pill())
    set_backup(8)
    ok('8 天：狀態列標示「已逾 7 天」', '（已逾 7 天）' in pill(), pill())
    ok('8 天：頁面上方提醒', banner() and '已 8 天未備份' in pg.inner_text('#backupBannerText'), pg.inner_text('#backupBannerText'))
    ok('逾期時備份文字為警示色', 'stale' in pg.get_attribute('#savepill .bk', 'class'))
    pg.evaluate("localStorage.removeItem('ist_last_backup'); refreshStorageInfo()")
    ok('從未備份：狀態列「尚未備份」、頁面上方提醒', '｜尚未備份' in pill() and banner(), pill())
    with pg.expect_download():
        pg.click('#savepill button:text-is("備份")')
    ok('按狀態列「備份」後提醒消失', not banner() and '已逾' not in pill(), pill())
    pg.click('#savepill button:text-is("儲存")')
    ok('按「儲存」的提示', toast(pg) == '已儲存到這台電腦的瀏覽器', toast(pg))
    # 午夜顯示 00 時（不可出現 24）
    hh = pg.evaluate("(() => { lastSaved = new Date(2026, 10, 4, 0, 5, 9); updateStatusBar(); return document.getElementById('savepill').textContent; })()")
    ok('午夜顯示 00:05:09', '已自動儲存 00:05:09' in hh, hh)
    # 無法儲存時紅字
    bad = pg.evaluate("""(() => { const o = Storage.prototype.setItem; Storage.prototype.setItem = () => { throw new Error('quota'); };
        saveData(); Storage.prototype.setItem = o; const p = document.getElementById('savepill'); return [p.className, p.textContent]; })()""")
    ok('無法儲存時狀態列為紅色並提示', bad[0] == 'bad' and '儲存失敗：請勿關閉頁面，並盡快下載備份' in bad[1], bad)
    pg.evaluate('saveData()')
    ok('恢復後狀態列回到正常', pg.get_attribute('#savepill', 'class') == '')

    # 夜間模式、列印
    pg.emulate_media(color_scheme='dark'); pg.reload(); pg.wait_for_load_state('load')
    ok('夜間模式跟隨電腦設定', pg.evaluate("document.documentElement.getAttribute('data-theme')") == 'dark')
    pg.emulate_media(media='print')
    ok('列印時隱藏頁籤', not pg.locator('.tab-btn').first.is_visible())
    ok('列印時隱藏狀態列', not pg.locator('#savepill').is_visible())
    # 成果報告明細表：長摘要、長網址不會把表格撐出紙張（V1.6 右側格線被裁掉）
    pg.emulate_media(media='screen')
    pg.evaluate("""records.push(normalizeRecord({ id: 1, date: '2026-11-01', sessions: 1, student: '測試甲', target: '教師', mainCategory: '其他',
        summary: 'https://example.org/averyveryverylongunbrokenstringwithoutspaces1234567890' + '很長的摘要'.repeat(40) })); saveData();
        switchTab('report'); generateReport();""")
    pg.set_viewport_size({'width': 718, 'height': 1000}); pg.emulate_media(media='print'); pg.wait_for_timeout(200)
    wid = pg.evaluate("(() => { const w = document.querySelector('#printRecordTable').parentElement; return [w.clientWidth, w.scrollWidth]; })()")
    ok('列印時明細表不超出紙張寬度', wid[1] <= wid[0], wid)

    ok('沒有對外請求', not external, external)
    ok('沒有 JS 錯誤', not errs, errs)
    b.close()

passed = sum(r[0] for r in results)
for good, name, detail in results:
    print(('PASS ' if good else 'FAIL ') + name + ('' if good or detail == '' else f'  ({detail})'))
print(f'\n{passed}/{len(results)} passed  ({HTML.name})')
sys.exit(0 if passed == len(results) else 1)
