# 文件用途：信号基本运算可视化（时移、尺度、翻转、微分、积分）
# 对应考点：时移、尺度变换、翻转、微分、积分的图形变换关系

import numpy as np
import streamlit as st
from scipy.integrate import cumulative_trapezoid
import plotly.graph_objects as go

from utils import PLOTLY_CONFIG, LAYOUT_DEFAULTS

# ──────────────────────────── 常量与信号函数 ────────────────────────────

COLOR_PRIMARY = "#636EFA"
COLOR_ACCENT = "#EF553B"
COLOR_SUCCESS = "#00CC96"
COLOR_REF = "gray"

T_MIN = -5.0
T_MAX = 5.0
T_POINTS = 2000


def triangle_pulse(t: np.ndarray) -> np.ndarray:
    """三角脉冲 x(t)=1-|t|, |t|<=1。"""
    return np.where(np.abs(t) <= 1.0, 1.0 - np.abs(t), 0.0)


def shifted_triangle(t: np.ndarray, t0: float) -> np.ndarray:
    """时移 y(t)=x(t-t0)。"""
    shifted = t - t0
    return np.where(np.abs(shifted) <= 1.0, 1.0 - np.abs(shifted), 0.0)


def scaled_triangle(t: np.ndarray, a: float) -> np.ndarray:
    """尺度变换 y(t)=x(at)。"""
    scaled = a * t
    return np.where(np.abs(scaled) <= 1.0, 1.0 - np.abs(scaled), 0.0)


def flipped_triangle(t: np.ndarray) -> np.ndarray:
    """翻转 y(t)=x(-t)。"""
    flipped = -t
    return np.where(np.abs(flipped) <= 1.0, 1.0 - np.abs(flipped), 0.0)


@st.cache_data
def compute_signal_operation(
    op_type: str,
    t0: float,
    a: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, str, str]:
    """缓存不同运算下的 y(t)、表达式和提示文本。"""
    t = np.linspace(T_MIN, T_MAX, T_POINTS)
    x_t = triangle_pulse(t)

    if op_type == "时移":
        y_t = shifted_triangle(t, t0)
        expression = f"y(t) = x(t - {t0:.2f})"
        info_text = "考点提示：x(t-t₀) 表示信号右移 t₀（t₀>0），左移用 x(t+|t₀|)。注意符号方向。"
    elif op_type == "尺度变换":
        y_t = scaled_triangle(t, a)
        expression = f"y(t) = x({a:.2f}t)"
        info_text = "考点提示：x(at) 中 |a|>1 时信号压缩，0<|a|<1 时信号展宽。压缩使频带展宽（时频对偶）。"
    elif op_type == "翻转":
        y_t = flipped_triangle(t)
        expression = "y(t) = x(-t)"
        info_text = "考点提示：x(-t) 是信号关于 t=0 的镜像翻转，是卷积运算的基础步骤。"
    elif op_type == "微分":
        y_t = np.gradient(x_t, t)
        expression = "y(t) = d x(t) / d t"
        info_text = "考点提示：信号微分对应频域乘以 jω，增强高频分量。不连续点产生冲激。"
    else:
        integral = cumulative_trapezoid(x_t, t)
        y_t = np.concatenate(([0.0], integral))
        expression = r"y(t) = \int_{-\infty}^{t} x(\tau) d\tau"
        info_text = "考点提示：信号积分对应频域除以 jω，平滑信号并增强低频分量。"

    return t, x_t, y_t, expression, info_text


# ──────────────────────────── 页面标题与公式 ────────────────────────────

st.title("信号基本运算")

st.latex(r"y(t) = x(at - b) \quad \text{（尺度变换 + 时移）}")


# ──────────────────────────── 侧边栏控件 ────────────────────────────

op_type = st.sidebar.selectbox("运算类型", ["时移", "尺度变换", "翻转", "微分", "积分"])

t0 = 1.0
a = 2.0

if op_type == "时移":
    t0 = st.sidebar.slider("时移量 t₀", -3.0, 3.0, 1.0, 0.1)
elif op_type == "尺度变换":
    a = st.sidebar.slider("尺度因子 a", 0.2, 5.0, 2.0, 0.1)


# ──────────────────────────── 核心计算 ────────────────────────────

t, x_t, y_t, expression, info_text = compute_signal_operation(op_type, t0, a)


# ──────────────────────────── 侧边栏指标 ────────────────────────────

st.sidebar.metric("当前表达式", expression)


# ──────────────────────────── Plotly 图表（单图叠加） ────────────────────────────

fig = go.Figure()

# 原始信号：灰色虚线 + 浅灰填充
fig.add_trace(
    go.Scatter(
        x=t,
        y=x_t,
        mode="lines",
        name="原始信号 x(t)",
        line=dict(color=COLOR_REF, width=2, dash="dash"),
        fill="tozeroy",
        fillcolor="rgba(128,128,128,0.15)",
    )
)

# 运算后信号：蓝色实线
fig.add_trace(
    go.Scatter(
        x=t,
        y=y_t,
        mode="lines",
        name=f"{op_type}后信号 y(t)",
        line=dict(color=COLOR_PRIMARY, width=2.5),
    )
)

# 时移边界标注
if op_type == "时移":
    fig.add_vline(x=t0, line_color=COLOR_ACCENT, line_dash="dash", line_width=2)

# 尺度边界标注
if op_type == "尺度变换":
    boundary = 1.0 / a
    fig.add_vline(x=boundary, line_color=COLOR_ACCENT, line_dash="dash", line_width=2)
    fig.add_vline(x=-boundary, line_color=COLOR_ACCENT, line_dash="dash", line_width=2)

fig.update_layout(title=f"{op_type}：原始信号与运算结果对比")
fig.update_xaxes(title_text="t (s)")
fig.update_yaxes(title_text="幅度")

fig.update_layout(**LAYOUT_DEFAULTS, height=560)
st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)


# ──────────────────────────── 教学注释 ────────────────────────────

st.info(info_text)
