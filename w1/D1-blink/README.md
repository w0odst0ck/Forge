# W1-D1 · ESP32 LED 闪烁（GPIO 基础）

> 验证标准：编译通过，仿真运行（LED 闪烁）

## 操作步骤（约 10 分钟）

1. 打开 <https://wokwi.com/projects/new/esp32>（免费，无需注册即可跑，登录可保存）
2. 左侧文件树：`sketch.ino` 全部替换为本目录代码
3. 左侧文件树：新建 `diagram.json`，粘贴本目录 `diagram.json` 内容 → 电路图自动生成
4. 点 ▶ 运行：LED 每 500ms 闪烁；右侧 Serial Monitor 滚动 `LED ON / LED OFF`
5. 改 `delay(500)` 数值 → 看闪烁频率变化（手感第一步）

## 电路

```
GPIO2 ── 220Ω ── LED(阳极) ── LED(阴极) ── GND
```

- 220Ω 限流：LED 工作电流 ≈ (3.3V - 2V 压降) / 220Ω ≈ 6mA，安全
- ESP32 GPIO 最大灌/拉电流 40mA，**电阻必须加**，否则烧 LED

## 概念速记

| 概念 | 要点 |
|------|------|
| GPIO | 通用输入输出引脚，可配输入/输出/复用功能 |
| 输出模式 | 引脚由芯片内部驱动，输出高(3.3V)/低(0V) |
| digitalWrite | 写数字电平：HIGH=1 / LOW=0 |
| pinMode | 引脚模式配置，必须先于读写 |
| delay | 阻塞延时，CPU 空转（简单但浪费） |
| millis() | 上电以来的毫秒计数，非阻塞计时的地基 |

## 思考题

1. 改成 1s 亮 / 200ms 灭
2. 用 `millis()` 写非阻塞版（LED 不闪的间隙，loop 还能干别的）
3. 为什么电阻必须加？把 220Ω 换成 10Ω 会怎样？（提示：LED 正向压降约 2V，算算电流）
4. 试试把引脚换成 GPIO4 并同步改 diagram.json —— 为 D3 PWM 调光预热（PWM 引脚在 GPIO2/4/5/15...）

## 完成确认

- [ ] 编译通过
- [ ] 仿真运行，LED 闪烁
- [ ] Serial Monitor 有输出
- [ ] 能向别人讲清：为什么需要 pinMode、HIGH 是多少伏
