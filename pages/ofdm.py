# 文件用途: OFDM 子载波正交性可视化 — sinc 频谱重叠与正交条件演示
# 对应考点: OFDM 子载波间隔 Δf=1/T 的正交性原理、载波间干扰(ICI)

import numpy as np
import streamlit as st
import plotly.graph_objects as go

from utils import PLOTLY_CONFIG, LAYOUT_DEFAULTS

# 8 色循环，依次分配给各子载波
CARRIER_COLORS = [
    "#636EFA", "#EF553B", "#00CC96", "#AB63FA",
    "#FFA15A", "#19D3F3", "#FF6692", "#B6E880",
]

# ── 页面标题与公式 ──
st.title("OFDM 子载波正交性")
st.latex(r"\Delta f = \frac{1}{T} \quad \text{（正交条件）}")

# ── 侧边栏控件 ──
st.sidebar.markdown("### OFDM 参数")
num_carriers = st.sidebar.slider("子载波数 K", 2, 8, 4, step=1)
T = st.sidebar.slider("符号周期 T (ms)", 0.5, 5.0, 1.0, step=0.1)
delta_f = st.sidebar.slider("子载波间隔 Δf (kHz)", 0.2, 3.0, 1.0, step=0.05)

# 正交检测：理想间隔 = 1/T
ideal_delta_f = 1.0 / T
is_orthogonal = abs(delta_f - ideal_delta_f) < 0.05

if is_orthogonal:
    st.sidebar.success(f"✔ 满足正交条件 Δf ≈ 1/T = {ideal_delta_f:.2f} kHz")
else:
    st.sidebar.warning(f"⚠ 偏离正交条件，理想 Δf = {ideal_delta_f:.2f} kHz")

st.sidebar.metric("理想 Δf", f"{ideal_delta_f:.2f} kHz")

# ── 核心计算：各子载波 sinc 频谱 ──
f_max = (num_carriers - 1) * delta_f + 2.0  # 频率轴上界留余量
f = np.linspace(-2, f_max, 2000)             # 2000 点密集频率网格

fig = go.Figure()

for k in range(num_carriers):
    f_center = k * delta_f                    # 第 k 个子载波中心频率
    arg = np.pi * (f - f_center) * T          # sinc 参数
    # 处理 sinc(0)=1 奇点，避免 0/0 产生 NaN
    sinc_k = np.where(np.abs(arg) < 1e-10, 1.0, np.sin(arg) / arg)

    # 绘制 sinc 曲线
    fig.add_trace(go.Scatter(
        x=f, y=sinc_k,
        mode="lines",
        name=f"子载波 {k}  (f₀={f_center:.2f} kHz)",
        line=dict(width=2, color=CARRIER_COLORS[k % len(CARRIER_COLORS)]),
    ))

    # 子载波中心频率虚线标记
    fig.add_vline(x=f_center, line_dash="dot", line_color="gray", opacity=0.3)

# ── 图表布局 ──
fig.update_layout(
    **LAYOUT_DEFAULTS,
    height=500,
    xaxis_title="f (kHz)",
    yaxis_title="幅度",
    title="子载波 sinc 频谱",
)
st.plotly_chart(fig, width="stretch", config=PLOTLY_CONFIG)

# ── 教学注释 ──
st.info(
    "当 Δf = 1/T 时，每个子载波的 sinc 峰值恰好对齐其他子载波的零点，"
    "实现频谱重叠但互不干扰（正交）。偏离该条件时将产生载波间干扰 (ICI)。"
)
