# Sim Lab · 仿真实验室

> 定位：**测试与仿真工作台**（家用主机）
> 当前：BOM 场景匹配引擎 + W1 嵌入式唤醒（学习进行中）
> 未来：数字孪生 → 自动驾驶仿真（CARLA）

## 双仓协作（单机）

本仓（`Forge`）与 [`Atlas`](../Atlas)（方案馆）成对工作，同在 Obsidian vault `D:\ZZZ\NOTES`：

- **本仓**：引擎代码 / 训练包 / 仿真 / 学习进度（动态）
- **Atlas**：计划 / 课纲 / 场景定义 / 方案（设计基线，轻文档）
- 依赖方向：**Forge 读 Atlas**（场景库/计划）；技术决策变更回流 Atlas（纠错）
- 同步协议见 `../Atlas/COLLAB.md`

## 文档导航

| 类别 | 位置 | 说明 |
|------|------|------|
| 🧰 工程代码 | `engine/` `scripts/` | BOM 引擎 + 工具脚本 |
| 📚 学习材料 | `w1/` | W1 训练包（D1-D7 + 架构 + 概念卡） |
| 📝 项目记录 | `memory/` | 项目日志 |

## 目录结构

```
Forge/
├── engine/           # BOM 场景匹配引擎（解析/匹配/渲染/CLI）
├── w1/               # W1 嵌入式唤醒训练包（任务表/进度看板：w1/README.md）
├── scripts/          # 工具脚本（run_match / verify_engine / verify-links / wokwi-lint）
├── memory/           # 项目日志
└── README.md
```

> 技术路线图（三年规划）在 `../Atlas/tech-plans/ROADMAP.md`，本仓不复制。

## 快速开始

```bash
# 跑引擎（场景库在 Atlas）
cd engine
python -m src.cli match examples/bom_sample.toml \
  --scene-dir ../Atlas/scene-library/scenes \
  --output-dir ../Atlas/reports

# 双仓互链自检
./scripts/verify-links.sh
```

## 场景库路径

场景定义不在本仓，从方案馆引用：

```
../Atlas/scene-library/scenes/   ← 8 个场景 TOML
../Atlas/scene-library/schemas/  ← 品类 schema
```

新增/修改场景 → 到 Atlas 编辑 → 本仓 pull 后生效。

## 硬件

- 主机：RTX 3060 12GB（WSL2 CUDA 可用）
- 用途：CARLA 仿真（自动驾驶）/ 数字孪生可视化（远期）
