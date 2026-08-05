/**
 * W1-D3 · PWM 调光（呼吸灯）
 * ------------------------------------------------------------
 * 目标：理解 PWM 占空比/频率/分辨率，会用 ESP32 LEDC 硬件外设
 * 电路：D2 ── 220Ω ── LED ── GND；逻辑分析仪 CH0 观察 D2
 *
 * 业务关联：这是"调光"的底层机制。真实智能照明里，
 * 0-10V / DALI / 可控硅 只是"怎么告诉驱动调多少"，
 * 驱动最终大多是 PWM 或恒流方式控制灯珠 —— W3 深挖。
 */

const int LED_PIN = 2;
const int PWM_CH  = 0;        // LEDC 通道号（0-15）
const int PWM_FREQ = 5000;    // 5kHz：高于人眼闪烁阈值（≥3kHz）
const int PWM_RES  = 8;       // 8bit 分辨率：占空比 0-255

void setup() {
  ledcSetup(PWM_CH, PWM_FREQ, PWM_RES);  // 配置通道：频率 + 分辨率
  ledcAttachPin(LED_PIN, PWM_CH);        // 把物理引脚绑定到通道
}

void loop() {
  // 渐亮：占空比 0 → 255
  for (int duty = 0; duty <= 255; duty++) {
    ledcWrite(PWM_CH, duty);             // 占空比 = duty / 255
    delay(5);                            // 每级停留 5ms → 全程 ~1.3s
  }
  // 渐暗：255 → 0
  for (int duty = 255; duty >= 0; duty--) {
    ledcWrite(PWM_CH, duty);
    delay(5);
  }
}

/**
 * 试玩：
 * 1. PWM_FREQ 改 1000 → 逻辑分析仪波形变疏（还能看到闪烁吗？）
 * 2. PWM_RES 改 10 → 亮度级数变 1024，渐变更细腻
 * 3. duty 跳变（直接 0↔255）→ 不是渐变，是开关 —— 对比"调光"与"开关"的本质
 */
