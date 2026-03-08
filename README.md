# SignalViz-Pro

信号与系统 / 通信原理交互式可视化复试作品集。

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.36+-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?logo=plotly&logoColor=white)
![Target](https://img.shields.io/badge/Portfolio-Postgrad%20Interview-blue)

## 项目定位

SignalViz-Pro 不再只是若干独立 demo，而是一个面向复试展示的教育可视化平台：

- 展示你对信号与系统核心考点的**抽象能力**
- 展示你把数学模型变成交互实验的**建模能力**
- 展示你把多个模块组织成可扩展产品的**系统能力**

当前版本包含 **12 个教学模块 + 1 个平台总览页**，覆盖基础理论、变换域分析、系统与通信三大知识域。

## 现在有什么

### 项目总览

- `平台总览与知识地图`：项目定位、模块统计、知识域 → 题型 → 模块映射、推荐学习顺序、扩展准入规则

### 基础理论

| 模块 | 核心考点 | 典型题型 |
|---|---|---|
| 信号基本运算 | 时移、尺度变换、信号叠加 | 波形变换题、图像读图题 |
| 傅里叶级数与吉布斯现象 | 谐波叠加、奇次谐波、吉布斯现象 | 周期信号展开题、频谱理解题 |
| 连续时间傅里叶变换 | 时频对偶、带宽、窗函数 | 傅里叶变换题、时频对应题 |
| 采样定理与混叠效应 | 奈奎斯特准则、混叠、重建 | 采样判据题、混叠分析题 |
| 卷积演示 — 翻转滑动法 | 卷积积分、翻转平移、重叠面积 | 卷积几何题、系统响应题 |

### 变换域分析

| 模块 | 核心考点 | 典型题型 |
|---|---|---|
| 拉普拉斯变换与系统稳定性 | 极点位置、冲激响应、稳定性 | 拉普拉斯分析题、稳定性判断题 |
| Z 变换与离散系统稳定性 | 单位圆、极点模、离散稳定性 | Z 变换题、离散稳定性题 |
| DFT / FFT 频谱分析 | 窗函数、频谱泄漏、离散频谱 | DFT 计算题、频谱泄漏题 |
| 频率响应与 Bode 图 | 幅频特性、相频特性、转折频率 | Bode 图题、频率响应题 |

### 系统与通信

| 模块 | 核心考点 | 典型题型 |
|---|---|---|
| LTI 系统四大性质 | 线性性、时不变性、因果性、BIBO 稳定性 | 系统判定题、性质证明题 |
| 数字调制与噪声 | 星座图、AWGN、眼图 | 数字调制题、误码分析题 |
| OFDM 子载波正交性 | 子载波间隔、sinc 频谱、ICI | OFDM 原理题、正交条件题 |

## 平台结构

### 单一信息源

- `module_registry.py` 统一维护所有页面元数据：分组、路由、标题、图标、题型、先修知识、状态
- `app.py` 从注册表动态生成导航，避免页面清单和文档长期漂移
- `pages/project_overview.py` 作为平台首页，负责知识地图和作品集叙事

### 共享约束

- 唯一入口：`app.py`
- 唯一全局 `st.set_page_config`
- 全部子页面共享 `utils.py` 中的 `PLOTLY_CONFIG` 和 `LAYOUT_DEFAULTS`
- 数值计算保持 NumPy 向量化；不新增第三方依赖

### 性能策略

- 高频计算使用 `@st.cache_data`
- 卷积、Bode、CTFT、Z 变换等模块缓存关键结果
- Plotly 图表统一配置，避免模块间交互体验割裂

## 知识地图与扩展机制

项目已经从“想到一个题就加一个页面”切换为“按题型抽象再扩展”：

- 先判断一个新主题能否覆盖**至少 3 类题型**
- 必须具备**1 个核心公式**
- 必须具备**2 个以上有效交互参数**
- 必须具备**1 个以上可观察现象**

如果只是单题技巧，优先进入题型笔记或扩展文档，而不是直接新建页面。

详细规则见：

- `docs/KNOWLEDGE_MAP.md`
- `docs/ROADMAP.md`
- `docs/MODULE_BLUEPRINT.md`

## 本地运行

```bash
pip install -r requirements.txt
python scripts/validate_registry.py
streamlit run app.py
```

## 部署

- 目标部署平台：Streamlit Cloud
- 依赖文件：`requirements.txt`
- 启动入口：`app.py`

## 验证命令

```bash
python scripts/validate_registry.py
python -m unittest discover -s tests -v
python -m compileall app.py utils.py pages module_registry.py scripts
streamlit run app.py --server.headless true --server.port 8510
```

## 项目结构

```text
app.py
module_registry.py
utils.py
requirements.txt
pages/
  project_overview.py
  signal_ops.py
  fourier.py
  ctft.py
  sampling.py
  convolution.py
  laplace.py
  z_transform.py
  dft.py
  bode.py
  lti_properties.py
  modulation.py
  ofdm.py
scripts/
  validate_registry.py
docs/
  KNOWLEDGE_MAP.md
  ROADMAP.md
  MODULE_BLUEPRINT.md
tests/
  test_module_registry.py
```

## 下一阶段方向

优先补强高复用主题，而不是盲目加页：

1. ROC / 因果 / 稳定性统一视图
2. 微分方程到零输入 / 零状态响应
3. 相关、匹配滤波与检测
4. 采样 - 重建 - 量化链路
5. 滤波器与带宽 / 截止频率

这些内容会优先进入路线图，再决定是扩展现有页面还是新增独立模块。
