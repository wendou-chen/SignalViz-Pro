# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SignalViz-Pro — 考研信号与系统交互式可视化复习平台。Streamlit 多页面应用，6 个独立可视化模块分三组导航。

## Run & Deploy

```bash
pip install -r requirements.txt
streamlit run app.py
# 部署目标：Streamlit Cloud（仅需 requirements.txt）
```

## Architecture

- `app.py` — 唯一入口，`st.set_page_config` 全局唯一调用，`st.navigation` dict 分组路由
- `utils.py` — 导出 `PLOTLY_CONFIG` 和 `LAYOUT_DEFAULTS`，所有页面共享
- `pages/*.py` — 6 个独立子页面，零耦合，通过 `from utils import` 引入共享配置

导航分组：基础理论（fourier/sampling/convolution）| 系统与控制（laplace）| 通信原理（modulation/ofdm）

## Page Module Pattern

每个页面严格遵循骨架顺序：
```
文件头注释（用途 + 考点）→ imports → [信号函数/常量] → st.title → st.latex → st.sidebar 控件 → 核心计算 → st.sidebar.metric → Plotly 图表 → st.info 教学注释
```

图表收尾统一写法：
```python
fig.update_layout(**LAYOUT_DEFAULTS, height=N)
st.plotly_chart(fig, width="stretch", config=PLOTLY_CONFIG)
```

## Key Conventions

- 子页面禁止调用 `st.set_page_config`
- 信号函数用 `np.where` 向量化，参数/返回类型 `np.ndarray`
- 数值计算全部 NumPy 向量化，禁止 Python for 循环做数值运算
- 耗时计算用 `@st.cache_data` 缓存
- 所有交互控件放 `st.sidebar`
- 配色：`#636EFA`(主蓝) `#EF553B`(强调红) `#00CC96`(绿) `gray`(参考)
- Import 顺序：numpy → streamlit → scipy(按需) → plotly → from utils import
- 依赖锁定在 requirements.txt 四个库，禁止引入额外第三方库

## Module Algorithms Quick Reference

| Module | Core Math | Key scipy/numpy |
|--------|-----------|-----------------|
| fourier | 方波奇次谐波求和，广播矩阵 (2000,N) | `scipy.signal.square` |
| sampling | CubicSpline 插值重建，混叠频率折叠 | `scipy.interpolate.CubicSpline` |
| convolution | `np.trapezoid` 梯形积分，翻转平移 | `@st.cache_data` 预计算 300 点 |
| laplace | `2*exp(σt)*cos(ωt)*u(t)`，`np.clip(-50,50)` 防溢出 | — |
| modulation | AWGN 复高斯噪声，眼图 None 断点单 trace | `np.random.default_rng(42)` |
| ofdm | sinc 频谱 `sin(x)/x`，奇点 `np.where` 保护 | — |
