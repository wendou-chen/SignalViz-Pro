# 文件用途: 拉普拉斯变换与系统稳定性可视化（s平面极零图 + 冲激响应）
# 对应考点: 拉普拉斯变换、传递函数极点与系统稳定性关系、冲激响应包络

import numpy as np
import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from utils import PLOTLY_CONFIG, LAYOUT_DEFAULTS

# ── 页面标题与公式 ──
st.title("拉普拉斯变换与系统稳定性")
st.latex(r"H(s) = \frac{\omega_n^2}{s^2 - 2\sigma s + (\sigma^2 + \omega^2)}")

# ── 侧边栏控件 ──
st.sidebar.markdown("### 极点参数")
sigma = st.sidebar.slider("σ（实部）", -5.0, 5.0, -1.0, step=0.1)
omega = st.sidebar.slider("ω（虚部）", 0.0, 20.0, 5.0, step=0.1)

# 稳定性判断
if sigma < 0:
    st.sidebar.success("稳定系统")
elif sigma > 0:
    st.sidebar.error("不稳定系统")
else:
    st.sidebar.warning("临界稳定")

st.sidebar.metric("极点位置", f"{sigma:.1f} ± j{omega:.1f}")

# ── 核心计算 ──
t = np.linspace(0, 5, 1000)

# h(t) = 2·exp(σt)·cos(ωt)·u(t)，阶跃函数用 np.where 向量化
h_t = np.where(t >= 0, 2.0 * np.exp(sigma * t) * np.cos(omega * t), 0.0)
# 包络线 ±2·exp(σt)
envelope = 2.0 * np.exp(sigma * t)

# 防止 σ>0 时指数爆炸导致绘图异常
h_t = np.clip(h_t, -50, 50)
envelope = np.clip(envelope, -50, 50)

# ── 图表：1行2列 ──
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=["s 平面极零图", "冲激响应 h(t)"],
    horizontal_spacing=0.12,
)

# ── 左图：s平面极零图 ──
# 左半平面稳定区域（浅绿色背景）
fig.add_shape(
    type="rect", x0=-6, x1=0, y0=-22, y1=22,
    fillcolor="rgba(144,238,144,0.15)", line_width=0,
    row=1, col=1,
)
# 虚轴参考线
fig.add_vline(x=0, line_dash="dash", line_color="gray", opacity=0.5, row=1, col=1)

# 共轭极点标记（×符号，红色）
fig.add_trace(
    go.Scatter(
        x=[sigma, sigma], y=[omega, -omega],
        mode="markers", name="极点",
        marker=dict(symbol="x", color="#EF553B", size=15, line_width=3),
    ),
    row=1, col=1,
)
# 固定坐标范围
fig.update_xaxes(title_text="σ (Real)", range=[-6, 6], row=1, col=1)
fig.update_yaxes(title_text="jω (Imaginary)", range=[-22, 22], row=1, col=1)

# ── 右图：冲激响应 h(t) ──
# 主曲线
fig.add_trace(
    go.Scatter(x=t, y=h_t, mode="lines", name="h(t)",
               line=dict(color="#636EFA", width=2)),
    row=1, col=2,
)
# 正包络线
fig.add_trace(
    go.Scatter(x=t, y=envelope, mode="lines", name="包络线",
               line=dict(color="gray", width=1, dash="dash")),
    row=1, col=2,
)
# 负包络线
fig.add_trace(
    go.Scatter(x=t, y=-envelope, mode="lines", name="负包络线",
               line=dict(color="gray", width=1, dash="dash"), showlegend=False),
    row=1, col=2,
)
fig.update_xaxes(title_text="t (s)", row=1, col=2)
fig.update_yaxes(title_text="h(t)", row=1, col=2)

# ── 统一布局 ──
fig.update_layout(**LAYOUT_DEFAULTS, height=500)
st.plotly_chart(fig, width="stretch", config=PLOTLY_CONFIG)

# ── 教学注释 ──
st.info(
    "极点在左半平面（σ < 0）时系统稳定，h(t) 衰减趋零；"
    "右半平面（σ > 0）时系统不稳定，h(t) 指数发散；"
    "虚轴上（σ = 0）时临界稳定，h(t) 等幅振荡。"
)
