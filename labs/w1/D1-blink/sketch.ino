/**
 * W1-D1 · ESP32 LED 闪烁（GPIO 基础）
 * ------------------------------------------------------------
 * 目标：唤醒嵌入式手感 —— GPIO 输出模式、数字电平、时序控制
 * 电路：GPIO2 ── 220Ω ── LED(阳极) ── LED(阴极) ── GND
 * 注：ESP32-DevKit-V1 板载蓝色 LED 也在 GPIO2，可直接观察
 *
 * 框架：Arduino（Wokwi 默认支持，setup/loop 结构）
 */

const int LED_PIN = 2;  // const 编译期常量，不占 RAM（比 #define 类型安全）

void setup() {
  // 把 GPIO2 配置为输出模式：芯片内部驱动电路接管引脚，可输出 3.3V/0V
  pinMode(LED_PIN, OUTPUT);
  // 串口 115200 波特率。D1 就养成调试习惯：跑起来先看 Serial Monitor
  Serial.begin(115200);
}

void loop() {
  // 输出高电平（3.3V）→ LED 两端有压差 → 点亮
  digitalWrite(LED_PIN, HIGH);
  Serial.println("LED ON");

  delay(500);  // 阻塞 500ms。注意：阻塞期间 CPU 空转，loop 干不了别的

  // 输出低电平（0V）→ 无压差 → 熄灭
  digitalWrite(LED_PIN, LOW);
  Serial.println("LED OFF");

  delay(500);
}

/**
 * 思考：
 * 1. delay() 是阻塞的。换成 millis() 非阻塞写法（记上次翻转时刻），
 *    LED 不闪的间隙 loop 还能做其他事 —— 这是所有状态机/多任务的地基。
 * 2. HIGH/LOW 只是 1/0 的宏。ESP32 GPIO 输出高电平 = 3.3V（非 5V）。
 */
