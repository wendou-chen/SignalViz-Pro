# 文件用途：采样定理与混叠效应可视化（模块B）
# 对应考点：奈奎斯特采样定理、混叠现象、信号重建

import numpy as np
from scipy.interpolate import CubicSpline
import plotly.graph_objects as go
import streamlit as st

from utils import PLOTLY_CONFIG, LAYOUT_DEFAULTS

# ── 页面标题与公式 ──
st.title("采样定理与混叠效应")
st.latex(r"f_s \geq 2\,f_{\max}")

# ── 侧边栏控件 ──
st.sidebar.markdown("### 采样参数")
f_sig = st.sidebar.slider("信号频率 f_sig (Hz)", 1.0, 20.0, 5.0, step=0.5)
f_s = st.sidebar.slider("采样频率 f_s (Hz)", 1.0, 100.0, 12.0, step=0.5)

# ── 混叠检测 ──
is_aliased = f_s < 2 * f_sig

if is_aliased:
    # 理论混叠频率：将 f_sig 折叠到 [0, f_s/2] 区间
    f_folded = f_sig % f_s
    f_alias = f_folded if f_folded <= f_s / 2 else f_s - f_folded
    st.sidebar.warning(f"混叠! 表观频率 ≈ {f_alias:.2f} Hz")
else:
    st.sidebar.success("满足奈奎斯特准则，无混叠")

# ── 信号生成（向量化计算） ──
T_max = 2.0

# 连续信号：2000 点密集网格
t = np.linspace(0, T_max, 2000)
x_cont = np.sin(2 * np.pi * f_sig * t)

# 采样点
t_s = np.arange(0, T_max, 1.0 / f_s)
x_s = np.sin(2 * np.pi * f_sig * t_s)

# 重建信号：CubicSpline 插值（边界保护）
if len(t_s) >= 2:
    cs = CubicSpline(t_s, x_s)
    x_recon = cs(t)
else:
    x_recon = np.zeros_like(t)

# ── 绘图：三层叠加 ──
fig = go.Figure()

# Layer 1：连续信号（灰色实线）
fig.add_trace(go.Scatter(
    x=t, y=x_cont,
    mode="lines",
    name="连续信号",
    line=dict(color="gray", width=2),
))

# Layer 2：采样点（红色散点）
fig.add_trace(go.Scatter(
    x=t_s, y=x_s,
    mode="markers",
    name="采样点",
    marker=dict(color="red", size=8),
))

# Layer 3：重建信号（蓝色虚线）
fig.add_trace(go.Scatter(
    x=t, y=x_recon,
    mode="lines",
    name="重建信号",
    line=dict(color="blue", width=2, dash="dash"),
))

fig.update_layout(
    **LAYOUT_DEFAULTS,
    height=500,
    xaxis_title="t (s)",
    yaxis_title="x(t)",
)

st.plotly_chart(fig, width="stretch", config=PLOTLY_CONFIG)

# ── 教学注释 ──
st.info(
    "当采样频率 $f_s < 2f_{sig}$ 时发生混叠：采样后的离散序列无法区分原始频率与其"
    "镜像折叠频率，导致重建信号呈现一个更低的「假象」频率。"
    "提高采样频率至奈奎斯特率以上即可消除混叠。"
)
