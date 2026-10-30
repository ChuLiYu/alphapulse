# AlphaPulse 繁體中文導讀

英文權威來源：[產品方向](../product/strategy.md)、[領域規格](../domain/investment-operations.md)、[交付計畫](../ROADMAP.md)、[開發指南](../DEVELOPMENT.md)、[Context Router](../INDEX.md)。
類型：閱讀摘要；涵蓋定位、主要規則、技術責任、操作入口，不是完整翻譯。
來源版本：`refactor/asset-management-platform` 分支的未提交草稿，2026-10-30。
同步狀態：草稿；以英文完整規格確認例外、數值限制與驗收條件。

## 專案要證明什麼

AlphaPulse 的定位是資產管理投資作業平台。目標是讓面試官看見：你理解持倉、現金、匯率、估值、風險、交易覆核與對帳之間的關係，也能把它們實作成可靠、可追溯的軟體。

第一階段採用合成的股票／ETF 資料，支援美元與加幣、美元報表、只做多與日終估值。這是投資帳簿的教學模型，不等於基金會計 NAV，也不連接真實券商。

## 現在做到哪裡

原有 FastAPI、React、PostgreSQL、容器化開發環境與 Ollama 受限工具呼叫仍保留。本次新增的是獨立的持倉估值核心與離線示範；尚未建立新的投資組合網頁、持倉資料庫、風險引擎或交易覆核服務。舊網頁仍有加密資產與模擬資料，不能當成新產品已完成的證據。

估值核心要求 Decimal、明確的「一單位當地貨幣等於多少美元」匯率，以及完全相同的業務日期。缺少或過期價格／匯率時，整體估值會被阻擋，不回傳看起來完整的部分總額。合成示範有明確標記；金額先加總，再依規格捨入。

## 技術與業務怎麼連起來

- Python／FastAPI：投資資料、估值、分析與 AI 整合，沿用可用基礎。
- PostgreSQL：交易一致性、版本、對帳與稽核；新持久化功能必須先建立 migration。
- React／TypeScript：呈現業務流程、資料來源與異常狀態。
- Java／Spring：後續用交易提案與獨立覆核服務展現 JVM 能力，尚未實作。
- Kafka／outbox：有實際跨服務事件需求後再加入，處理重試、去重與重播。
- 雲端／Terraform／觀測：用部署、負載測試與復原演練證明能力，不以設定檔存在宣稱上線。

AI 的工作是解釋已計算的風險／異常與整理有來源的研究；不能計算權威金額、批准交易、修改限制或繞過權限。現有 Ollama PoC 尚未接上投資資料，相關設計見 [英文 AI 規格](../ai/governance.md)。

## AI Flywheel Core 如何落地

從 [Context Router](../INDEX.md) 選任務，找到唯一權威來源，再讀相關實作與測試。產品目的、業務規則、架構取捨、工作進度各有來源，不複製個人角色與登入設定進專案。

例如修改匯率規則：先讀 `VAL-02`，再看估值核心與測試；若幣別或日期政策不清楚，只等待該決定，其他工作繼續。修改後同步規格、黃金案例與驗證結果。文件檢查只能證明結構與連結，不能批准業務語意。

[架構中文導讀](architecture.md) · [英文開發入口](../DEVELOPMENT.md) · [英文驗證紀錄](../engineering/refactor-verification.md)

## 如何開始

先執行不需要安裝套件的檢查與合成示範：

```sh
python3 scripts/verify_context.py
PYTHONPATH=src python3 -m unittest discover -s tests/portfolio -v
PYTHONPATH=src python3 -m alphapulse.portfolio.demo
```

完整本機服務需要啟動 OrbStack，接著依序執行 `./alphapulse setup`、`./alphapulse up`、`./alphapulse test`。結束用 `./alphapulse down`，資料卷會保留。詳細前提、設定與限制請讀英文開發指南；本摘要不取代操作規格。
