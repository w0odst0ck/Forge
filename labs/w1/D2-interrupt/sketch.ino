/**
 * W1-D2 · 按键中断 + 防抖
 * ------------------------------------------------------------
 * 目标：理解中断机制（vs 轮询）、ISR 编写规则、防抖原理
 * 电路：D4 ── 按键 ── GND（INPUT_PULLUP：不按 = HIGH，按下 = LOW）
 *
 * 关键设计：
 * 1. ISR 里只"置标志位"，主循环里"消费"——ISR 必须短
 * 2. volatile：ISR 写、主循环读的变量必须声明，防编译器优化
 * 3. 防抖用时间戳过滤（非阻塞），不用 delay（阻塞会丢中断）
 */

const int BTN_PIN = 4;

volatile bool btnPressed = false;        // ISR 置位，主循环消费
volatile unsigned long lastTrigger = 0;  // 上次有效触发时刻

const unsigned long DEBOUNCE_MS = 50;    // 机械抖动 ~10ms，取 50ms 保险

// IRAM_ATTR：ESP32 的 ISR 放 IRAM，避免 Flash 访问与中断冲突
void IRAM_ATTR onButtonPress() {
  unsigned long now = millis();          // ESP32 的 millis 在 ISR 里安全
  if (now - lastTrigger > DEBOUNCE_MS) { // 距上次触发 <50ms 视为抖动，忽略
    lastTrigger = now;
    btnPressed = true;                   // 只置标志，绝不在这里 Serial.print
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(BTN_PIN, INPUT_PULLUP);        // 内部上拉，省外部电阻
  attachInterrupt(digitalPinToInterrupt(BTN_PIN), onButtonPress, FALLING);
  // FALLING：按下瞬间 HIGH→LOW 的下降沿触发
  Serial.println("Ready. Press the button!");
}

void loop() {
  if (btnPressed) {                      // 主循环消费标志
    btnPressed = false;
    Serial.println("Button pressed! (debounced)");
  }
  // 主循环很空 → 中断的优势：不按的时候 CPU 可以干别的
}
