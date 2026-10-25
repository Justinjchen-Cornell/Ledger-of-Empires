# 数据字典

## dynasty_master

一行一个朝代/时期；`period_id` 唯一。`start_year` / `end_year` 为公元纪年，公元前用负数。

## fiscal_annual

一行一个年份。收入/支出单位在 `notes` 注明（万石 / 万贯 / 万两）。`deficit` = 总收入 - 总支出；空值表示史料未载。

## money_series

`weight_g` 克；`fineness` 0-1；`nominal_value` 名义面值；`issue_volume` 发行量；`price_index` 以某年为 100；`silver_copper_ratio` 银钱比价。

## price_series

`unit` 为石/斛/匹；`price_nominal` 为名义货币单位；`price_grams_silver` 折算为克银。

## modern_series

GDP 为现价美元；财政收支为人民币亿元；M2 为人民币亿元；土地出让金为人民币亿元；外储为美元。

## 空值规则

空值表示“史料未载”，不允许填 0。每个数据点必须在 `sources.md` 有 `source_id` 与 `evidence_grade`。
