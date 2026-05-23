# [企業名] — SaaS Valuation Compression Analysis

- **分析日**: YYYY-MM-DD
- **ステータス**: Draft / In Progress / Complete
- **担当**: Katomasa (x402 Inc.)
- **依存 Phase 1 ベースライン**: `reports/phase-1-comparable-psr-baseline.md`
- **データ取得**: WebSearch (バリュエーション・ARR・調達ラウンド) + `yfinance-data` (comparable 上場銘柄) + `twitter` (sentiment・CEO 発言)
- **分析実装**: Claude 自身 (PSR 計算 / SOTP / Bull/Base/Bear / 確率加重 / Compression 係数)

---

## ⚠️ 免責事項

本分析は公開情報に基づく推定であり、投資助言ではない。未上場企業のバリュエーション・ARR は二次情報・リーク報道・推測を含むため、必ず一次情報で再検証すること。各数値には Low / Mid / High の推定レンジを併記する。

---

## 1. 基本情報

| 項目 | 値 (Mid) | レンジ (Low–High) | 出典 / 更新日 |
|------|---------|------------------|---------------|
| 現状バリュエーション (推定) | $XX B | $XX – $XX B | TBD URL |
| 直近調達 (年月) | YYYY-MM | — | TBD URL |
| 直近調達 (金額) | $XX M | — | TBD URL |
| Lead 投資家 | TBD | — | TBD URL |
| 推定 ARR | $XX B | $XX – $XX B | TBD URL |
| 推定 ARR 成長率 (YoY) | XX % | XX – XX % | TBD URL |
| 主要事業セグメント | TBD | — | — |
| 主要競合 (上場) | TBD | — | — |
| 主要競合 (未上場) | TBD | — | — |

---

## 2. SaaS Valuation Compression 計算 (Claude 手計算)

### 2.1 入力値
- 公開 SaaS 中央値 PSR (Phase 1 baseline, 採用 basket): **X.X 倍** (2026-05 時点)
- 対象企業の推定バリュエーション (Mid): $XX B
- 対象企業の推定 ARR (Mid): $XX B

### 2.2 計算
- 対象 PSR = バリュエーション ÷ ARR = **Y.Y 倍**
- **Compression 係数 (Y / X) = Z.Z**

### 2.3 判定
- `> 1.5` → 顕著なプレミアム (未上場プレミアム / 期待先行)
- `1.0 – 1.5` → 軽度プレミアム
- `0.7 – 1.0` → 概ね適正
- `< 0.7` → ディスカウント (ガバナンス・流動性懸念で説明されている可能性)

---

## 3. Bull / Base / Bear シナリオ (Claude 手計算)

| シナリオ | 想定 ARR 成長率 (3yr CAGR) | 想定 PSR | 3年後 ARR | 想定時価総額 | 確率 |
|---------|---------------------------|---------|-----------|--------------|------|
| Bull | XX % | X.X 倍 | $XX B | $XXX B | XX % |
| Base | XX % | X.X 倍 | $XX B | $XXX B | XX % |
| Bear | XX % | X.X 倍 | $XX B | $XX B | XX % |

**確率加重期待値**: `$XXX B` (= Σ 確率 × 時価総額)

---

## 4. リスク要因

| カテゴリ | 内容 | 重要度 |
|---------|------|--------|
| 規制 | TBD | High / Mid / Low |
| 競合 | TBD | — |
| 収益集中 | TBD | — |
| ガバナンス | TBD | — |
| 為替・地政学 | TBD | — |
| その他固有 | TBD | — |

---

## 5. 結論

### 5.1 もし今日上場したら (推定レンジ)

- Bull: `$XXX B`
- Base: `$XXX B`
- Bear: `$XX B`

### 5.2 現状バリュエーションへの評価

**判定**: [適正 / プレミアム / ディスカウント]

根拠: 1–2 段落で簡潔に。

### 5.3 個人投資家がアクセスする手段

- セカンダリーマーケット (Forge Global / EquityZen / Hiive): TBD
- 関連 ETF: TBD
- ADR / 関連上場銘柄 / 親会社経由: TBD

---

## 6. データ収集ログ

### 6.1 WebSearch クエリ (Claude が実行)
- [ ] "[企業名] valuation 2025 2026 site:bloomberg.com"
- [ ] "[企業名] ARR site:theinformation.com"
- [ ] "[企業名] tender offer secondary"
- [ ] "[企業名] IPO filing rumor"
- [ ] (その他)

### 6.2 Skill 呼び出しログ
- [ ] `yfinance-data` — Phase 1 ベースライン PSR 取得 (`reports/phase-1-comparable-psr-baseline.md` 参照)
- [ ] `twitter` — `from:@[企業CEO]` / `[企業名]` で直近 sentiment 取得
- [ ] `telegram-news` — アジア圏 / 中国語報道があれば取得
- [ ] `generative-ui` — Phase 4 で図表生成 (個別分析では未使用)
- [ ] `options-payoff` — 代理上場銘柄でのヘッジ pay-off (任意)

### 6.3 取得できなかった情報 (x402 候補)
- TBD (有料 / 限定アクセスで取れなかった一次情報)

---

## 7. 出典

(WebSearch で確認した URL を時系列で列挙)

1. TBD
2. TBD

---

## 更新履歴

- YYYY-MM-DD: Draft 作成
