# Sim Lab · 仿真实验室

> 定位：**测试与仿真工作台**（家用主机 · RTX 3060 ×2）
> 当前：BOM 场景匹配引擎 + 照明数字孪生（规划）
> 未来：自动驾驶仿真（CARLA）

---

## 双项目协作

本仓（`Forge`）与 [`Atlas`](D:\projects\Atlas)（方案馆）成对工作：

- **本仓**：引擎代码 / 仿真 / 测试（3060 主机运行）
- **方案馆**：场景定义 TOML / 方案文档 / 素材（公司电脑编辑）
- 依赖方向：**Forge 读 Atlas**，场景库不在本仓

协作细节见 `../Atlas/COLLAB.md`

---

## 目录结构

```
Forge/
├── engine/           # BOM 场景匹配引擎（bom-scene-engine）
│   ├── src/          #   解析/匹配/渲染/CLI
│   └── examples/     #   BOM 样本 + 报告样例
├── digital-twin/     # 照明数字孪生（规划中）
├── carla/            # 自动驾驶仿真（远期）
├── scripts/          # 测试/实验脚本
└── README.md
```

---

## 快速开始

```bash
# 跑引擎（场景库在 Atlas）
cd engine
pip install -e .        # 或: pip install pydantic click
python -m src.cli match examples/bom_sample.toml \
  --scene-dir ../Atlas/scene-library/scenes \
  --output-dir ../Atlas/reports
```

## 场景库路径

场景定义不在本仓，从方案馆引用：

```
../Atlas/scene-library/scenes/   ← 8 个场景 TOML
../Atlas/scene-library/schemas/  ← 品类 schema
```

新增/修改场景 → 到 Atlas 编辑 → 本仓 pull 后生效。

---

## 硬件

- 主机：RTX 3060 ×2（12GB 显存）
- 用途：CARLA 仿真（自动驾驶）/ 数字孪生可视化
- 显卡相关仿真脚本放 `carla/` 与 `digital-twin/`
