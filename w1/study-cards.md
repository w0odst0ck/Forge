# W1 概念卡收集箱（study-vault 格式）

> 用法：每完成一个 D，把该 D `understand.md` 第 5 节的概念卡复制到对应小节（渐进沉淀，非一次性）
> 归属：W1 完成后整篇导入 study-vault（按节拆卡入库复习体系）
> 复习：Obsidian 内直接浏览（同 vault）

---

## D1 · GPIO 输出

```yaml
---
tags: [w1, gpio, digital-write, register]
domain: embedded-basics
---
# GPIO 输出
- **定义**：芯片引脚配置为输出后，digitalWrite 控制内部推挽开关，输出 3.3V/0V
- **本质**：写寄存器位（GPIO_OUT_REG），硬件纳秒级响应
- **类比**：受代码控制的开关面板
- **易错点**：① 必须 pinMode 先行 ② 3.3V 逻辑 vs 5V 逻辑混接 ③ LED 必须串电阻（限流）
- **架构位置**：控制层——调光/开关的执行单元
```

---

## D2 · 按键中断与防抖

```yaml
---
tags: [w1, interrupt, isr, volatile, debounce]
domain: embedded-basics
---
# 按键中断与防抖
- **定义**：硬件事件（下降沿）打断主循环执行 ISR；防抖用时间戳过滤机械抖动
- **本质**：事件驱动 vs 轮询；ISR=生产者、loop=消费者
- **易错点**：① ISR 必须短（禁 delay/print，会卡死+看门狗复位）② ISR 共享变量必须 volatile（防编译器缓存优化）③ 防抖用时间戳非阻塞，不用 delay ④ ESP32 ISR 加 IRAM_ATTR（防 Flash 访问冲突）
- **架构位置**：感知层输入 + 事件驱动处理
```

---

<!-- 每完成一个 D，把 understand.md 第 5 节概念卡复制到下面 -->

## D3 · PWM 调光（待完成）

## D4 · UART 通信（待完成）

## D5 · I2C 传感器（待完成）

## D6 · 主线串讲（待完成）

## D7 · 复盘（待完成）
