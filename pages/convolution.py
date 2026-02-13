# 文件用途：卷积翻转滑动法可视化演示（Streamlit 子页面）
# 对应考点：连续时间卷积积分、翻转平移法、卷积的几何意义

import numpy as np
import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from utils import PLOTLY_CONFIG, LAYOUT_DEFAULTS

# ── 信号定义（纯函数，不可变） ──────────────────────────────

def rect_pulse(t_arr: np.ndarray) -> np.ndarray:
    """单位矩形脉冲 p(t): [0,1] 区间为 1"""
    return np.where((t_arr >= 0) & (t_arr <= 1), 1.0, 0.0)

def exp_decay(t_arr: np.ndarray) -> np.ndarray:
    """单边指数衰减 e^{-2t}u(t)"""
    return np.where(t_arr >= 0, np.exp(-2 * t_arr), 0.0)

def triangle_pulse(t_arr: np.ndarray) -> np.ndarray:
    """三角脉冲: [0,1] 区间线性下降"""
    return np.where((t_arr >= 0) & (t_arr <= 1), 1.0 - t_arr, 0.0)

# ── 共享积分网格 ────────────────────────────────────────────
TAU = np.linspace(-2, 6, 1000)

# ── 完整卷积曲线（缓存，避免重复计算） ──────────────────────
@st.cache_data
def full_conv(choice: str) -> tuple:
    """预计算 300 点完整卷积 y(t)，返回 (t_range, y_arr)"""
    t_range = np.linspace(-2, 5, 300)
    x_vals = rect_pulse(TAU) if choice == "矩形脉冲" else triangle_pulse(TAU)
    # 逐点梯形积分（对应公式 y(t)=∫x(τ)h(t-τ)dτ）
    y_arr = np.array([np.trapezoid(x_vals * exp_decay(tv - TAU), TAU) for tv in t_range])
    return t_range, y_arr

# ── 信号选择映射 ────────────────────────────────────────────
SIGNAL_MAP = {"矩形脉冲": rect_pulse, "三角脉冲": triangle_pulse}

# ── 页面内容 ────────────────────────────────────────────────
st.title("卷积演示 — 翻转滑动法")
st.latex(r"y(t) = \int_{-\infty}^{+\infty} x(\tau)\, h(t - \tau)\, d\tau")

# ── 侧边栏控件 ──────────────────────────────────────────────
choice = st.sidebar.selectbox("选择 x(t)", list(SIGNAL_MAP.keys()))
t_val = st.sidebar.slider("t 位置", -2.0, 5.0, 0.0, step=0.02)

# ── 当前帧计算 ──────────────────────────────────────────────
x_func = SIGNAL_MAP[choice]
x_tau = x_func(TAU)                    # x(τ)
h_flipped = exp_decay(t_val - TAU)     # h(t-τ): 翻转后平移到 t
product = x_tau * h_flipped            # 被积函数（重叠区域）
y_current = float(np.trapezoid(product, TAU))  # 当前 y(t) 值

st.sidebar.metric("y(t) 当前值", f"{y_current:.4f}")

# ── 预计算完整卷积曲线 ──────────────────────────────────────
t_full, y_full = full_conv(choice)

# ── 构建双行子图 ────────────────────────────────────────────
fig = make_subplots(
    rows=2, cols=1,
    row_heights=[0.6, 0.4],
    subplot_titles=["翻转滑动过程", "卷积结果 y(t)"],
    vertical_spacing=0.12,
)

# 上图：x(τ) 蓝色填充
fig.add_trace(go.Scatter(
    x=TAU, y=x_tau, name="x(τ)",
    line=dict(color="#636EFA", width=2),
    fill="tozeroy", fillcolor="rgba(99,110,250,0.2)",
), row=1, col=1)

# 上图：h(t-τ) 红色
fig.add_trace(go.Scatter(
    x=TAU, y=h_flipped, name="h(t−τ)",
    line=dict(color="#EF553B", width=2),
), row=1, col=1)

# 上图：重叠乘积区域 绿色填充
fig.add_trace(go.Scatter(
    x=TAU, y=product, name="x(τ)·h(t−τ)",
    line=dict(color="#00CC96", width=1),
    fill="tozeroy", fillcolor="rgba(0,204,150,0.4)",
), row=1, col=1)
# 下图：完整卷积曲线（灰色）
fig.add_trace(go.Scatter(
    x=t_full, y=y_full, name="y(t)",
    line=dict(color="gray", width=2),
    showlegend=True,
), row=2, col=1)

# 下图：当前点红色标记
fig.add_trace(go.Scatter(
    x=[t_val], y=[y_current], name="当前点",
    mode="markers",
    marker=dict(color="red", size=10),
), row=2, col=1)

# 下图：竖直虚线标记当前 t
fig.add_vline(
    x=t_val, line_dash="dash", line_color="red",
    opacity=0.5, row=2, col=1,
)

# ── 坐标轴标题 ──────────────────────────────────────────────
fig.update_xaxes(title_text="τ", row=1, col=1)
fig.update_xaxes(title_text="t", row=2, col=1)
fig.update_yaxes(title_text="幅值", row=1, col=1)
fig.update_yaxes(title_text="y(t)", row=2, col=1)

# ── 应用统一布局 ────────────────────────────────────────────
fig.update_layout(**LAYOUT_DEFAULTS, height=700, showlegend=True)
st.plotly_chart(fig, width="stretch", config=PLOTLY_CONFIG)

# ── 教学注释 ────────────────────────────────────────────────
st.info(
    "**卷积的几何意义：** 将 h(τ) 翻转得到 h(−τ)，"
    "再平移 t 得到 h(t−τ)。h(t−τ) 与 x(τ) 的重叠面积"
    "（绿色区域）就是输出 y(t) 在该时刻的值。"
    "拖动滑块观察绿色区域面积如何随 t 变化。"
)
