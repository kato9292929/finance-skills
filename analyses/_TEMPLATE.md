# [企業名] — SaaS Valuation Compression Analysis

- **分析日**: YYYY-MM-DD
- **ステータス**: Draft / In Progress / Complete
- **担当**: Katomasa (x402 Inc.)
- **使用 Skill**: saas-valuation-compression / startup-analysis / estimate-analysis / stock-correlation
- **依存 Phase 1 ベースライン**: `reports/phase-1-comparable-psr-baseline.md`

---

## ⚠️ 免責事項

本分析は公開情報に基づく推定であり、投資助言ではない。未上場企業のバリュエーション・ARR は二次情報・リーク報道・推測を含むため、必ず一次情報で再検証すること。各数値には Low / Mid / High の推定レンジを併記する。

---

## 1. 基本情報

| 項目 | 値 (Mid) | レンジ (Low–High) | 出典 / 更新日 |
|------|---------|------------------|---------------|
| 現状バリュエーション (推定) | $XX B | $XX – $XX B | TBD |
| 直近調達 (年月) | YYYY-MM | — | TBD |
| 直近調達 (金額) | $XX M | — | TBD |
| Lead 投資家 | TBD | — | TBD |
| 推定 ARR | $XX B | $XX – $XX B | TBD |
| 推定 ARR 成長率 (YoY) | XX % | XX – XX % | TBD |
| 主要事業セグメント | TBD | — | — |
| 主要競合 (上場) | TBD | — | — |
| 主要競合 (未上場) | TBD | — | — |

---

## 2. SaaS Valuation Compression 計算

- 公開 SaaS 中央値 PSR (Phase 1 baseline): **X.X 倍** (2026-05 時点)
- 対象企業 PSR: Mid バリュエーション ÷ Mid ARR = **Y.Y 倍**
- **Compression 係数 (Y / X) = Z.Z**

判定基準:
- `> 1.5` → 顕著なプレミアム (未上場プレミアム / 期待先行)
- `1.0 – 1.5` → 軽度プレミアム
- `0.7 – 1.0` → 概ね適正
- `< 0.7` → ディスカウント (ガバナンス・流動性懸念で説明されている可能性)

---

## 3. Bull / Base / Bear シナリオ

| シナリオ | 想定 ARR 成長率 (3yr CAGR) | 想定 PSR | 3年後 ARR | 想定時価総額 | 確率 |
|---------|---------------------------|---------|-----------|--------------|------|
| Bull | XX % | X.X 倍 | $XX B | $XXX B | XX % |
| Base | XX % | X.X 倍 | $XX B | $XXX B | XX % |
| Bear | XX % | X.X 倍 | $XX B | $XX B | XX % |

**確率加重期待値**: `$XXX B`

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
- ADR / 関連上場銘柄: TBD
- 親会社経由 (例: Microsoft 経由で OpenAI 間接): TBD

---

## 6. 参照 Skill ログ

実行した finance-skills プラグイン:
- [ ] `saas-valuation-compression` — 主要 compression 計算
- [ ] `startup-analysis` — VC 視点評価
- [ ] `estimate-analysis` — ARR / 成長率推定
- [ ] `stock-correlation` — comparable 相関
- [ ] `finance-sentiment` — ソーシャル sentiment
- [ ] `funda-data` — (有料・x402 観測対象)

---

## 出典

1. TBD
2. TBD

---

## 更新履歴

- YYYY-MM-DD: Draft 作成
