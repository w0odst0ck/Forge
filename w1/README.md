# W1 · 嵌入式手感唤醒（Wokwi 仿真）

> 来源：`Atlas/tech-plans/4week-awakening.md` 周计划 · 优化版（2026-08-03）
> 方式：纯仿真，零硬件（Wokwi 浏览器）
> 目标：唤醒嵌入式手感（GPIO/中断/PWM/UART/I2C），5 个 demo 拼装 = 智能灯具雏形

## 🗺️ 学习地图（知识依赖）

```mermaid
graph LR
    D1[D1 GPIO 点灯] --> D2[D2 按键中断+防抖]
    D1 --> D3[D3 PWM 调光]
    D3 --> D6[D6 主线串讲<br/>5 demo = 智能灯具]
    D2 --> D6
    D4[D4 UART 通信] --> D6
    D5[D5 I2C 传感器] --> D6
    D6 --> D7[D7 复盘 + W2 衔接]
```

- **主线**：D1 → D2/D3（输入/输出控制）→ D4/D5（通信）→ D6 串讲 → D7 复盘
- D4/D5 可并行；D2 之前先过 D1（GPIO 基础）

## 任务表

| 天 | 任务 | 目录 | 验证标准 | 状态 |
|----|------|------|----------|------|
| D1 | ESP32 LED 闪烁 | `D1-blink/` | 编译通过，仿真运行 | ✅ 材料就绪（lint 验证过） |
| D2 | 按键中断 + 防抖 | `D2-interrupt/` | 串口打印正确，无抖动误触发 | ✅ 材料就绪 |
| D3 | PWM 调光（呼吸灯） | `D3-pwm/` | 逻辑分析仪看到占空比变化 | ✅ 材料就绪 |
| D4 | UART 双实例互发（loopback） | `D4-uart/` | 串口 MATCH 循环 | ✅ 材料就绪 |
| D5 | I2C 读 MPU6050 | `D5-i2c/` | 读到加速度/温度实时值 | ✅ 材料就绪 |
| D6 | 主线串讲（智能灯具雏形） | `D6-review/` | 能讲 3 分钟 + 15 题自测 | ✅ 材料就绪 |
| D7 | 复盘 + W2 衔接 | `D7-review/` | 复盘笔记 + W2 前置清单 | ✅ 材料就绪 |

## 每日节奏

1. 打开对应 D 目录的 `README.md`（目标 + 步骤 + 概念速记 + 面试题 + 组合挑战）
2. Wokwi 粘贴 `sketch.ino` + `diagram.json`（+ `libraries.txt`），点 ▶ 跑通
3. 验证标准打勾；面试题口头答一遍
4. 完成状态告诉 Agent → 更新本表

## 质量保障

- 所有 `diagram.json` 交付前经官方 linter 验证（`Forge/scripts/wokwi-lint/`），0 error
- 已抓并修复 2 处引脚名错误（esp:2→D2、逻辑分析仪 0→D0、按钮 1/2→1.l/2.l）

## 产出约定

- 代码 + 电路 + 说明 → 各 D 目录
- 每天收获 → `notes/YYYY-MM-DD-Dn.md`
- 复盘 → `notes/W1-review.md`
- W1 完成后：概念卡批量入库 study-vault 复习体系

## 里程碑

- [ ] W1 完成：GPIO/PWM/UART/I2C 手感恢复（→ W2 Modbus 主从）
