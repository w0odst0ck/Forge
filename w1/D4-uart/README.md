---
tags: [w1, esp32, uart, serial, communication]
domain: embedded-basics
depends-on: D1-blink
---

# W1-D4 · UART 通信（loopback 自发自收）

> 验证标准：串口监视器看到 TX 发送与 RX 回显字节一致（MATCH）

## 操作步骤

1. `sketch.ino` 粘贴到 Wokwi 代码编辑器
2. `diagram.json` 粘贴生成电路：一根线把 **TX2 接到 RX2**（loopback）
3. 点 ▶ 运行：Serial Monitor 每秒打印一对 `TX: 0x..` / `RX: 0x.. MATCH ✓`
4. 把 `Serial2.begin(9600)` 改成 `4800`（只改接收端预期不变）→ 观察波特率不匹配时收到乱码
   - 等等：loopback 是同一条线，两端都是同一个 Serial2，波特率一定一致。
   - **要制造波特率错误**：把 `Serial2.write(cnt)` 和 `Serial2.read()` 拆成两个不同波特率的串口？不行。
   - 正确玩法：**改 TX 侧协议**（比如发送两个字节、接收端读一个）或者观察 `MATCH/MISMATCH` 逻辑。
   - 实操推荐：把发送改成字符串 `"ping"`，用 `readStringUntil('\n')` 接收回显，体验"帧"的边界概念。

## 电路

```
ESP32 TX2 ──────── RX2（loopback 短接）
```

- UART 全双工：TX（发送）与 RX（接收）独立走线。loopback 是串口调试第一课——先确认"自己能收到自己发的"，再谈和其他设备通信
- ESP32 三组硬件 UART：Serial（USB，调试用）、Serial1、Serial2。这里用 **Serial2**，默认引脚 **TX2=D17 / RX2=D16**

## 概念速记

| 概念 | 要点 |
|------|------|
| UART | 异步串行通信：一根 TX 一根 RX，靠**波特率**对齐时序，无时钟线 |
| 帧结构 | 1 起始位(低) + 5~8 数据位 + 可选校验 + 1~2 停止位(高)。收发双方必须完全一致 |
| 波特率 | 每秒符号数（bit/s）。9600/115200 常见。**两端不一致 = 乱码**（异步无参考时钟）|
| 环形缓冲 | 硬件 FIFO：收到的字节先进缓冲区，主循环 `available()` 轮询读取，不丢数据 |
| TX2/RX2 | ESP32 的 UART2 引脚（D17/D16），与 USB 串口 Serial 独立 |

## 面试式验证问题

1. **UART 为什么需要"波特率一致"？**（异步通信没有时钟线，接收端按约定速率采样电平；速率不同 → 采样点错位 → 乱码）
2. **`Serial` 和 `Serial2` 什么区别？**（Serial 走 USB 转串口芯片，PC 能看到；Serial2 是芯片内部 UART，连真实外部设备用）
3. **`available()` 返回什么？为什么循环里要先查它再 `read()`？**（缓冲区可读字节数；直接 read 空缓冲返回 -1，业务上易误判）
4. **如果 TX 接错到另一个设备的 TX（而不是 RX），会发生什么？**（两个发送端对顶——信号冲突，无数据或乱码；接线的 TX↔RX 交叉是 UART 联调最常见错误）

## 组合挑战（D4+D5 合体，W2 预演）

- **把 D5 的传感器数据用 Serial2 发出来**：BME280 读数 → `Serial2.printf("T=%.1f\n", t)` → 用任意串口助手（或第二个 ESP32）接收
- 这就是 **Modbus 从站的雏形**：设备"说话"的字节流，W2 会用 pymodbus 让 PC 读懂它

## 完成确认

- [ ] 编译通过，MATCH 循环输出
- [ ] 能说出 UART 帧结构（起始位/数据位/停止位）
- [ ] 面试题 ≥3 题能答出
- [ ] （进阶）用 readStringUntil 收发字符串帧
