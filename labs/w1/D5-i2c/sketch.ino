/**
 * W1-D5 · I2C 读 MPU6050 六轴传感器
 * ------------------------------------------------------------
 * 目标：理解 I2C 总线（SDA/SCL/设备地址/寄存器），会用库读传感器
 * 电路：D21(SDA) ── MPU6050 SDA；D22(SCL) ── MPU6050 SCL；3V3/GND 供电
 *
 * 业务关联：智能照明里传感器无处不在 —— 人感（存在型雷达）、
 * 恒照度（光照传感器）、能耗（电表）。"读传感器"是设备智能化的第一步。
 */

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_MPU6050.h>

Adafruit_MPU6050 mpu;   // 库对象：封装了寄存器读写

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);                // SDA=D21, SCL=D22（ESP32 默认 I2C）

  if (!mpu.begin()) {                // 内部用默认地址 0x68
    Serial.println("MPU6050 not found! 检查接线 / 地址（AD0 接高 = 0x69）");
    while (1) delay(100);            // 找不到就停在这
  }

  // 配置量程与滤波（熟悉"寄存器配置"的入口，库里封装了寄存器写）
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  Serial.println("MPU6050 OK");
}

void loop() {
  sensors_event_t accel, gyro, temp;
  mpu.getEvent(&accel, &gyro, &temp);   // 一次读全部数据（库内部读多个寄存器）

  Serial.printf("A X=%6.1f Y=%6.1f Z=%6.1f m/s2 | G X=%6.1f Y=%6.1f Z=%6.1f rad/s | T=%5.1f C\n",
                accel.acceleration.x, accel.acceleration.y, accel.acceleration.z,
                gyro.gyro.x, gyro.gyro.y, gyro.gyro.z,
                temp.temperature);
  delay(500);
}

/**
 * 试玩：
 * 1. 点 Wokwi 里的 MPU6050 部件 → 右侧面板直接改 accelX / rotationX / temperature
 *    → 串口读数跟随变化（体会"寄存器值 → 物理量"的链路）
 * 2. 把 mpu.begin() 的地址改成 0x69（需要 AD0 接 3V3）→ 模拟地址接错场景
 * 3. 挑战：翻 Adafruit_MPU6050.cpp，看 getEvent() 读了哪些寄存器
 *    （这是 W3 读驱动芯片 datasheet 的预演：读寄存器 → 查表/公式 → 得物理量）
 */
