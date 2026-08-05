/**
 * W1-D4 · UART 通信（loopback 自发自收）
 * ------------------------------------------------------------
 * 目标：理解 UART 帧结构/波特率/收发流程 —— W2 Modbus 的直接地基
 * 电路：TX2 ── RX2 短接（loopback：自己发给自己）
 *
 * 玩法升级（字符串帧）：
 * 发 "ping\n"，收端 readStringUntil('\n') 拼帧 —— 体会"帧边界"概念
 */

void setup() {
  Serial.begin(115200);     // USB 串口：给 PC 看调试信息
  Serial2.begin(9600);      // UART2：硬件串口（TX2=D17, RX2=D16）
  Serial.println("UART loopback test @9600");
}

void loop() {
  // 发送字符串帧（带 \n 结尾 = 帧边界）
  Serial2.println("ping");

  // 等待回显（loopback 线 200ms 内应该回来）
  unsigned long start = millis();
  while (!Serial2.available() && millis() - start < 200) {
    // 忙等超时保护
  }

  if (Serial2.available()) {
    // 按帧读取：直到 \n
    String rx = Serial2.readStringUntil('\n');
    rx.trim();
    if (rx == "ping") {
      Serial.println("RX: \"ping\"  MATCH ✓");
    } else {
      Serial.printf("RX: \"%s\"  MISMATCH ✗\n", rx.c_str());
    }
  } else {
    Serial.println("RX: timeout (检查 loopback 线 TX2↔RX2)");
  }

  delay(1000);
}

/**
 * 思考（对应面试题 4）：
 * 把 "esp:TX2" 和 "esp:RX2" 的连接线删掉，再运行 ——
 * 看 timeout 分支。这就是"设备没接线/对方没回"的真实表现，
 * W2 的掉线容错（D6）就是围绕这个场景设计的。
 */
