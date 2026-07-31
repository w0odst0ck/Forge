# BOM 场景匹配报告

**产品**: 智能LED教室灯（600×600）
**生成时间**: 2026-07-31 11:46

---

## 📊 摘要

| 指标 | 值 |
|------|-----|
| 评估场景数 | 8 |
| 通过硬约束 | 1 |
| 平均匹配分 | 12.50% |

## 🏆 最佳匹配

**学校教室** — 100.0%
> ✅ 强烈推荐用于此场景

## 📋 场景匹配详情

### 1. 学校教室

**✅ 推荐** — 匹配分: **100.0%**

**维度评分:**

| 维度 | 得分 | 权重 | 加权分 |
|------|------|------|--------|
| efficacy_match | 100.00% | 15% | 15.00% |
| power_match | 100.00% | 10% | 10.00% |
| ra_match | 100.00% | 10% | 10.00% |
| dimming_match | 100.00% | 15% | 15.00% |
| schedule_match | 100.00% | 10% | 10.00% |
| presence_sensor_match | 100.00% | 10% | 10.00% |
| light_sensor_match | 100.00% | 10% | 10.00% |
| anti_glare_match | 100.00% | 5% | 5.00% |
| integrated_match | 100.00% | 5% | 5.00% |
| communication_match | 100.00% | 10% | 10.00% |

- **efficacy_match**: 95.0 在理想区间 [90, 130]
- **power_match**: 36.0 在理想区间 [34, 38]
- **ra_match**: 95.0 在理想区间 [93, 100]
- **dimming_match**: 全部特性匹配 2/2
- **schedule_match**: 全部特性匹配 1/1
- **presence_sensor_match**: 布尔字段匹配 1/1
- **light_sensor_match**: 布尔字段匹配 1/1
- **anti_glare_match**: 布尔字段匹配 1/1
- **integrated_match**: 布尔字段匹配 1/1
- **communication_match**: 交集得分 1.0 (值: ['rs-485', 'lora', 'zigbee'], 理想: ['rs-485', 'lora', 'zigbee'])

---

### 2. 洁净车间/洁净室

**❌ 未通过硬约束** — 此场景不推荐
- `product_specs.efficacy.value` 要求 `gte 120`，BOM 不满足
  - 洁净间基础光效要求
- `environment.ip_ratings` 要求 `contains_any ['IP54', 'IP65', 'IP66', 'IP67']`，BOM 不满足
  - 洁净间需 ≥IP54
- `control_module.no_neutral_wire` 要求 `eq True`，BOM 不满足
  - 洁净间改造方案需免布线

### 3. 冷库/冷链

**❌ 未通过硬约束** — 此场景不推荐
- `environment.temp_range.min` 要求 `lte -20`，BOM 不满足
  - 冷库工作温度需 ≤-20℃
- `environment.ip_ratings` 要求 `contains_any ['IP65', 'IP66', 'IP67']`，BOM 不满足
  - 冷库凝露环境，防护等级需 IP65+

### 4. 长走廊/通道

**❌ 未通过硬约束** — 此场景不推荐
- `control_module.features` 要求 `contains neighbor_notification`，BOM 不满足
  - 邻组通知实现'人未到灯先亮'

### 5. 工业厂房/车间

**❌ 未通过硬约束** — 此场景不推荐
- `product_specs.efficacy.value` 要求 `gte 150`，BOM 不满足
  - 工业车间要求高光效 ≥150LM/W

### 6. 物流仓储

**❌ 未通过硬约束** — 此场景不推荐
- `product_specs.efficacy.value` 要求 `gte 160`，BOM 不满足
  - 仓储要求高光效 ≥160LM/W
- `communication_module.protocols.distance.max` 要求 `gte 100`，BOM 不满足
  - 仓储大面积，通信距离需 ≥100m
- `control_module.no_neutral_wire` 要求 `eq True`，BOM 不满足
  - 改造场景必须免布线

### 7. 隧道照明

**❌ 未通过硬约束** — 此场景不推荐
- `product_specs.efficacy.value` 要求 `gte 150`，BOM 不满足
  - 隧道需高光效
- `environment.temp_range.min` 要求 `lte -20`，BOM 不满足
  - 隧道可能存在低温
- `environment.ip_ratings` 要求 `contains_any ['IP65', 'IP66', 'IP67']`，BOM 不满足
  - 隧道潮湿、粉尘，需 IP65+

### 8. 地下车库

**❌ 未通过硬约束** — 此场景不推荐
- `control_module.no_neutral_wire` 要求 `eq True`，BOM 不满足
  - 改造项目必须免布线
