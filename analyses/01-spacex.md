# SpaceX — SaaS Valuation Compression Analysis

- **分析日**: 2026-05-23
- **ステータス**: Draft v1 (要 finance-skills 実値リフレッシュ)
- **担当**: Katomasa (x402 Inc.)
- **使用 Skill**: `saas-valuation-compression` / `startup-analysis` / `estimate-analysis` / `stock-correlation` / `finance-sentiment`
- **依存 Phase 1 ベースライン**: `reports/phase-1-comparable-psr-baseline.md`
- **採用 basket**: Tier A (ハイパースケール) + 通信/航空 (`IRDM`, `VSAT`, `LMT`, `BA`) を補助 basket として併用

---

## ⚠️ 免責事項

本分析は2026年5月23日時点の公開情報・報道に基づく **推定** であり、投資助言ではない。SpaceX は未上場で財務開示義務がないため、Starlink ARR・打ち上げ事業売上は二次情報・リーク報道・契約公開情報からの再構成である。training cutoff (2026年1月) 以降の動きは未反映であり、IPO 観測・$1.75T の評価については報道ソースの一次確認が必須。各数値には Low / Mid / High のレンジを併記する。

---

## 1. 基本情報

| 項目 | Mid | レンジ (Low–High) | 出典 / 更新日 |
|------|-----|------------------|---------------|
| 現状バリュエーション (推定) | **$400 B** | $350 – $1,750 B | 私募市場 (~$350–400 B, 2025年 tender)/IPO 観測 (~$1.75 T, 2026年5月報道) |
| 直近調達 (年月) | 2025-Q4 (tender offer) | — | Bloomberg / Reuters report (要確認) |
| 直近調達 (金額) | $1.5 B (tender) | — | 〃 |
| Lead 投資家 | Founders Fund / Sequoia 等の既存 LP | — | — |
| 推定 ARR (連結) | **$15 B** | $13 – $20 B | Payload Space / Bloomberg 報道 (2025年通期) |
| 推定 ARR 成長率 (YoY) | **50 %** | 40 – 60 % | Starlink 加入者 +50%/年・Falcon 9 打ち上げ件数 +20%/年 |
| 主要事業セグメント | Starlink (≈61%) / Falcon 9 commercial launches (≈25%) / NASA + DoD (≈14%) | — | CLAUDE.md 言及 + Payload Space estimate |
| 主要競合 (上場) | `IRDM` (Iridium), `VSAT` (Viasat), `LMT`/`BA` (打ち上げ), `KTOS` (国防) | — | — |
| 主要競合 (未上場) | Blue Origin / Rocket Lab (`RKLB`は上場) / Amazon Kuiper / OneWeb (Eutelsat 統合) | — | — |

**重要な注意**: SpaceX は純粋な SaaS ではなく、ハードウェア + サービス + 政府契約の hybrid。Starlink 部分のみが SaaS 的 (subscription revenue, gross margin 改善中) であり、saas-valuation-compression Skill の適用には **Starlink 単体 / 連結** の2軸で出す必要がある。

---

## 2. SaaS Valuation Compression 計算

### 2.1 連結ベース (SpaceX 全体)

- 公開 SaaS Tier A 中央値 PSR (Phase 1 baseline): **TBD 倍** (placeholder: ~8 倍と仮定)
- 連結 PSR: $400 B ÷ $15 B = **26.7 倍**
- **Compression 係数 = 26.7 / 8 ≈ 3.3** → **顕著なプレミアム**

### 2.2 SOTP (Sum-of-the-Parts) 試算

| セグメント | 推定売上 | 適用倍率 | セグメント価値 |
|-----------|---------|---------|---------------|
| Starlink (SaaS 的) | $9.2 B | SaaS Tier A 中央値 × 1.5 (高成長プレミアム) = 12 倍 | **$110 B** |
| 商業打ち上げ | $3.8 B | 航空宇宙 PSR ~3–5 倍 = 4 倍 | **$15 B** |
| 政府契約 (NASA/DoD) | $2.0 B | 防衛系 PSR ~2–3 倍 = 2.5 倍 | **$5 B** |
| Starship オプション価値 (R&D 先行) | n/a | 実物オプション法で別途加算 | **$30–100 B** |
| **SOTP 合計 (Base)** | **$15 B** | — | **$160 – $230 B** |

→ SOTP Base は連結報道の $350–400 B より **明確に低い**。差分 ($120–240 B) は:
- 私募市場の流動性プレミアム / 期待先行
- Starship 商業化の実物オプション過大評価
- Musk 経営者プレミアム
- 政府との特殊関係による参入障壁プレミアム

### 2.3 IPO 観測 $1.75 T シナリオの検証

$1.75 T ÷ $15 B = **117 倍 PSR**。これは SaaS Tier A 中央値の **約 15 倍**。連結ベースでは合理的に説明不可能。説明仮説:

1. **Starlink スピンオフ IPO 説**: Starlink 単体で $1 T 級として評価 (subscriber ~10M, ARPU ~$1,200/年 → ARR $12 B、PSR 80倍超で説明)。
2. **Starship 完全成功シナリオ**: Mars / 月開発の実物オプション過剰評価。
3. **AI / 通信統合ストーリー**: xAI (Grok) との垂直統合プレミアム。
4. **報道側のセンセーション**: $1.75 T は記者の試算であって市場合意ではない可能性が高い。

→ Base シナリオでは IPO 観測値は **過大** と評価する。

---

## 3. Bull / Base / Bear シナリオ

| シナリオ | 想定 ARR 成長率 (3yr CAGR) | 想定 PSR (連結) | 3年後 ARR | 3年後想定時価総額 | 確率 |
|---------|---------------------------|----------------|-----------|------------------|------|
| **Bull** | 60 % (Starlink 加入者 30M 突破・Starship 商業化成功) | 25 倍 | $61 B | **$1,500 B** | 20 % |
| **Base** | 45 % (Starlink 加入者 18M・Starship 試験段階) | 15 倍 | $46 B | **$690 B** | 55 % |
| **Bear** | 30 % (Starlink 競合激化・Starship 遅延・規制) | 8 倍 | $33 B | **$265 B** | 25 % |

**確率加重期待値 (3年後)**:
`0.20 × 1,500 + 0.55 × 690 + 0.25 × 265 = 300 + 380 + 66 ≈ $746 B`

→ 現状報道の私募バリュエーション $400 B はやや安、IPO 観測 $1.75 T は過大。

---

## 4. リスク要因

| カテゴリ | 内容 | 重要度 |
|---------|------|--------|
| **収益集中** | Starlink が連結売上の ~61%。Starlink の規制・競合悪化が全社直撃 | **High** |
| **ガバナンス** | Musk 個人による事実上の支配 (株式・voting 構造)。xAI/Tesla との利益相反 | **High** |
| **規制** | スペクトラム規制 (FCC) / 各国市場参入 / 衛星デブリ規制強化の動き | **High** |
| **競合 (LEO)** | Amazon Kuiper の商業化開始 (~2026)、中国 GuoWang・千帆 constellation 加速 | **Mid–High** |
| **打ち上げ事業** | 商業価格戦争 (Blue Origin / 中国国営)、Falcon 9 老朽化リスク | **Mid** |
| **Starship 開発遅延** | 商業化遅延が IPO ストーリーを直撃 | **Mid–High** |
| **政治リスク** | Musk の政治関与による国防契約変動 / 同盟国市場での反発 | **Mid** |
| **為替・地政学** | 中国市場アクセス不可 / 欧州での反 Musk センチメント | **Mid** |

---

## 5. 結論

### 5.1 もし今日上場したら (推定レンジ)

- **Bull**: `$1,500 B` (Starship 成功 + Starlink ハイパー成長)
- **Base**: `$690 B` (確率加重 ~$746 B に近い)
- **Bear**: `$265 B`

### 5.2 現状バリュエーションへの評価

**判定**: 私募 $400 B = **やや割安**、IPO 観測 $1.75 T = **明確にプレミアム (過大)**。

**根拠**:
- SOTP base 試算 ($160–230 B) に Starship オプション ($50 B 程度) を上乗せして $250 B 前後が「保守的 fair value」。
- 私募 $400 B は私募プレミアム込みでギリギリ正当化可能 (Compression 係数 ~3.3 はハイパースケール SaaS の高成長企業群とほぼ同水準)。
- $1.75 T は確率加重期待値の 2.3 倍に相当し、Bull 達成 (確率 20%) 後の 3 年先想定値ですら 1,500 B。Bull が前倒し or 過小評価されている特殊シナリオ以外では正当化困難。

### 5.3 個人投資家がアクセスする手段

- **セカンダリーマーケット**: Forge Global / EquityZen / Hiive で SpaceX 株は流通あり (最低ロット数万ドル)。
- **関連 ETF**: ARKX (ARK Space Exploration ETF) は SpaceX を間接保有していない場合あり要確認。`UFO` (Procure Space ETF) なども同様。
- **間接アクセス**: Alphabet (Google) は2015年に SpaceX へ ~$900M 出資、現在も保有を継続している可能性 (要確認)。最も大きな間接エクスポージャーかも。
- **公開関連銘柄**: `RKLB` (Rocket Lab, 競合だがロケット銘柄として連動傾向), `IRDM` (衛星通信), `VSAT` (Viasat)。
- **IPO 待機**: Starlink スピンオフが先行する可能性が高い (Musk 過去発言)。

---

## 6. 参照 Skill ログ

実行した finance-skills プラグイン:
- [ ] `saas-valuation-compression` — SOTP 計算は手動。Skill リフレッシュで再算出予定
- [ ] `startup-analysis` — VC 視点評価 (Founders Fund / Sequoia 視点)
- [ ] `estimate-analysis` — ARR / 成長率 (Payload Space + Bloomberg)
- [ ] `stock-correlation` — `RKLB` / `IRDM` / `VSAT` との相関
- [ ] `finance-sentiment` — Twitter/X (Musk 投稿) + HackerNews 言及量
- [ ] `funda-data` — 未呼び出し (x402 観測対象)

---

## 出典 (要再検証)

1. Bloomberg "SpaceX Tender Offer Valuation" (2025年, 要 URL 確認)
2. Payload Space industry estimates (2025年通期)
3. The Information "Starlink Subscriber Growth" (2025年, 要 URL 確認)
4. Reuters "SpaceX IPO Speculation $1.75T" (2026年5月, 要 URL 確認)
5. FCC filings (Starlink スペクトラム関連)
6. NASA / DoD 契約公開情報

---

## 更新履歴

- 2026-05-23: Draft v1 作成。Phase 1 ベースライン PSR 確定後に compression 係数を再計算、WebSearch で IPO 観測報道の一次ソース確認が必要。
