# BOM 场景匹配报告

**产品**: 智能IoT雷达感应灯管
**生成时间**: 2026-07-31 08:32

---

## 📊 摘要

| 指标 | 值 |
|------|-----|
| 评估场景数 | 7 |
| 通过硬约束 | 7 |
| 平均匹配分 | 95.71% |

## 🏆 最佳匹配

**冷库/冷链** — 100.0%
> ✅ 强烈推荐用于此场景

## 📋 场景匹配详情

### 1. 冷库/冷链

**✅ 推荐** — 匹配分: **100.0%**

**维度评分:**

| 维度 | 得分 | 权重 | 加权分 |
|------|------|------|--------|
| temp_margin | 100.00% | 30% | 30.00% |
| ip_match | 100.00% | 25% | 25.00% |
| sensor_match | 100.00% | 20% | 20.00% |
| communication_match | 100.00% | 15% | 15.00% |
| power_match | 100.00% | 10% | 10.00% |

- **temp_margin**: -40.0 在理想区间 [-999, -30]
- **ip_match**: IP ['IP30', 'IP40', 'IP67'] ≥ IP66, 得分 1.00
- **sensor_match**: 值 'radar_5.8G' → 映射得分 1.0
- **communication_match**: 交集得分 1.0 (值: ['rs-485', 'rs-232', 'lora', 'zigbee', 'ethernet'], 理想: ['lora', 'rs-485', 'ethernet'])
- **power_match**: 12.0 在理想区间 [10, 15]

---

### 2. 长走廊/通道

**✅ 推荐** — 匹配分: **100.0%**

**维度评分:**

| 维度 | 得分 | 权重 | 加权分 |
|------|------|------|--------|
| neighbor_notify_match | 100.00% | 30% | 30.00% |
| fade_match | 100.00% | 25% | 25.00% |
| sensor_match | 100.00% | 20% | 20.00% |
| hold_time_match | 100.00% | 15% | 15.00% |
| power_match | 100.00% | 10% | 10.00% |

- **neighbor_notify_match**: 全部特性匹配 1/1
- **fade_match**: 全部特性匹配 2/2
- **sensor_match**: 值 'radar_5.8G' → 映射得分 1.0
- **hold_time_match**: 全部特性匹配 1/1
- **power_match**: 12.0 在理想区间 [8, 16]

---

### 3. 工业厂房/车间

**✅ 推荐** — 匹配分: **100.0%**

**维度评分:**

| 维度 | 得分 | 权重 | 加权分 |
|------|------|------|--------|
| protocol_match | 100.00% | 25% | 25.00% |
| efficacy_match | 100.00% | 20% | 20.00% |
| communication_match | 100.00% | 20% | 20.00% |
| sensor_match | 100.00% | 15% | 15.00% |
| zone_control_match | 100.00% | 10% | 10.00% |
| environment_match | 100.00% | 10% | 10.00% |

- **protocol_match**: 多协议匹配得分 1.00
- **efficacy_match**: 180.0 在理想区间 [160, 999]
- **communication_match**: 交集得分 1.0 (值: ['rs-485', 'rs-232', 'lora', 'zigbee', 'ethernet'], 理想: ['rs-485', 'ethernet'])
- **sensor_match**: 值 'radar_5.8G' → 映射得分 1.0
- **zone_control_match**: 全部特性匹配 2/2
- **environment_match**: IP ['IP30', 'IP40', 'IP67'] ≥ IP54, 得分 1.00

---

### 4. 物流仓储

**✅ 推荐** — 匹配分: **100.0%**

**维度评分:**

| 维度 | 得分 | 权重 | 加权分 |
|------|------|------|--------|
| communication_range_match | 100.00% | 25% | 25.00% |
| efficacy_match | 100.00% | 20% | 20.00% |
| environment_match | 100.00% | 20% | 20.00% |
| sensor_match | 100.00% | 15% | 15.00% |
| communication_downlink | 100.00% | 10% | 10.00% |
| protocol_match | 100.00% | 10% | 10.00% |

- **communication_range_match**: 200.0 在理想区间 [150, 999]
- **efficacy_match**: 180.0 在理想区间 [170, 999]
- **environment_match**: IP ['IP30', 'IP40', 'IP67'] ≥ IP54, 得分 1.00
- **sensor_match**: 值 'radar_5.8G' → 映射得分 1.0
- **communication_downlink**: 交集得分 1.0 (值: ['rs-485', 'rs-232', 'lora', 'zigbee', 'ethernet'], 理想: ['lora', 'zigbee'])
- **protocol_match**: 交集得分 1.0 (值: ['modbus', 'opc_ua', 'siemens_plc', 'mitsubishi_plc'], 理想: ['modbus'])

---

### 5. 隧道照明

**✅ 推荐** — 匹配分: **100.0%**

**维度评分:**

| 维度 | 得分 | 权重 | 加权分 |
|------|------|------|--------|
| efficacy_match | 100.00% | 25% | 25.00% |
| ip_match | 100.00% | 20% | 20.00% |
| communication_match | 100.00% | 20% | 20.00% |
| protocol_match | 100.00% | 15% | 15.00% |
| sensor_match | 100.00% | 10% | 10.00% |
| temp_margin | 100.00% | 10% | 10.00% |

- **efficacy_match**: 180.0 在理想区间 [170, 999]
- **ip_match**: IP ['IP30', 'IP40', 'IP67'] ≥ IP65, 得分 1.00
- **communication_match**: 交集得分 1.0 (值: ['rs-485', 'rs-232', 'lora', 'zigbee', 'ethernet'], 理想: ['lora', 'rs-485', 'ethernet'])
- **protocol_match**: 交集得分 1.0 (值: ['modbus', 'opc_ua', 'siemens_plc', 'mitsubishi_plc'], 理想: ['modbus', 'opc_ua'])
- **sensor_match**: 值 'radar_5.8G' → 映射得分 1.0
- **temp_margin**: -40.0 在理想区间 [-999, -25]

---

### 6. 地下车库

**✅ 推荐** — 匹配分: **100.0%**

**维度评分:**

| 维度 | 得分 | 权重 | 加权分 |
|------|------|------|--------|
| sensor_match | 100.00% | 25% | 25.00% |
| communication_match | 100.00% | 20% | 20.00% |
| power_match | 100.00% | 15% | 15.00% |
| installation_match | 100.00% | 15% | 15.00% |
| environment_match | 100.00% | 15% | 15.00% |
| protocol_match | 100.00% | 10% | 10.00% |

- **sensor_match**: 值 'radar_5.8G' → 映射得分 1.0
- **communication_match**: 交集得分 1.0 (值: ['rs-485', 'rs-232', 'lora', 'zigbee', 'ethernet'], 理想: ['lora', 'zigbee'])
- **power_match**: 12.0 在理想区间 [10, 20]
- **installation_match**: 布尔字段匹配 1/1
- **environment_match**: IP ['IP30', 'IP40', 'IP67'] ≥ IP40, 得分 1.00
- **protocol_match**: 交集得分 1.0 (值: ['modbus', 'opc_ua', 'siemens_plc', 'mitsubishi_plc'], 理想: ['modbus'])

---

### 7. 洁净车间/洁净室

**⚠️ 条件适配** — 匹配分: **70.0%**

**维度评分:**

| 维度 | 得分 | 权重 | 加权分 |
|------|------|------|--------|
| ra_match | 0.00% | 30% | 0.00% |
| ip_match | 100.00% | 20% | 20.00% |
| efficacy_match | 100.00% | 15% | 15.00% |
| sensor_match | 100.00% | 15% | 15.00% |
| communication_match | 100.00% | 10% | 10.00% |
| installation_match | 100.00% | 10% | 10.00% |

- **ra_match**: 0 < 80, 偏差 80, 得分 0.00
- **ip_match**: IP ['IP30', 'IP40', 'IP67'] ≥ IP54, 得分 1.00
- **efficacy_match**: 180.0 在理想区间 [150, 999]
- **sensor_match**: 值 'radar_5.8G' → 映射得分 1.0
- **communication_match**: 交集得分 1.0 (值: ['rs-485', 'rs-232', 'lora', 'zigbee', 'ethernet'], 理想: ['rs-485', 'ethernet'])
- **installation_match**: 布尔字段匹配 1/1

**Gap 分析:**

  - 🟡 **ra_match**: 值 0 低于理想最小值 80，偏差 80
    当前: `0` | 需求: `≥80`

---
