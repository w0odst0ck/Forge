# Forge · 项目规划

> 仿真实验室：从 BOM 引擎 → 数字孪生 → 自动驾驶仿真

## 阶段规划

### Phase 1：引擎稳定（当前）
- [x] BOM 场景匹配引擎迁入（engine/）
- [ ] 品类扩展（工矿灯/三防灯 schema）
- [ ] 场景嵌套/继承
- [ ] 匹配结果可视化（HTML 仪表盘）
- [ ] 单元测试（pytest）

### Phase 2：数字孪生（4 周唤醒后）
- [ ] 灯节点模拟器（pymodbus 从站 × N）
- [ ] 网关桥接（Modbus → MQTT）
- [ ] FastAPI 平台 + 时序库
- [ ] Web 面板（平面图 + 状态 + 能耗曲线）
- [ ] 课表联动/场景调度仿真

### Phase 3：自动驾驶仿真（远期）
- [ ] CARLA + ROS 2 环境搭建（3060 双卡）
- [ ] 车辆/传感器/规划 demo
- [ ] SUMO 多车协同
- [ ] CAN 总线基础

## 工作流

```
公司电脑编辑场景 → Atlas push → 本机 pull
本机跑引擎/仿真 → 报告 → Atlas/reports/ 回传
```

详见 `../Atlas/COLLAB.md`
