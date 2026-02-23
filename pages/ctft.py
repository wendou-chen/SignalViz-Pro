# 文件用途：连续时间傅里叶变换（CTFT）可视化（时域信号 + 频域谱）
# 对应考点：常见变换对、时频对偶性、脉宽与带宽反比关系

import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils import PLOTLY_CONFIG, LAYOUT_DEFAULTS

# ──────────────────────────── 常量与信号函数 ────────────────────────────

COLOR_PRIMARY = "#636EFA"
COLOR_ACCENT = "#EF553B"
COLOR_SUCCESS = "#00CC96"
COLOR_REF = "gray"

SAMPLE_POINTS = 2000


# 矩形脉冲 x(t) 与解析频谱 X(f)
def rect_time_signal(t: np.ndarray, tau: float) -> np.ndarray:
    return np.where(np.abs(t) <= tau / 2.0, 1.0, 0.0)


def rect_frequency_response(f: np.ndarray, tau: float) -> np.ndarray:
    return tau * np.sinc(f * tau)


# 高斯脉冲 x(t) 与解析频谱 X(f)
def gaussian_time_signal(t: np.ndarray, tau: float) -> np.ndarray:
    return np.exp(-np.pi * (t / tau) ** 2)


def gaussian_frequency_response(f: np.ndarray, tau: float) -> np.ndarray:
    return tau * np.exp(-np.pi * (f * tau) ** 2)


# 双边指数 x(t) 与解析频谱 X(f)
def bilateral_exponential_time_signal(t: np.ndarray, tau: float) -> np.ndarray:
    return np.exp(-np.abs(t) / tau)


def bilateral_exponential_frequency_response(f: np.ndarray, tau: float) -> np.ndarray:
    return 2.0 * tau / (1.0 + (2.0 * np.pi * f * tau) ** 2)


# sinc 信号 x(t) 与理想低通矩形谱 X(f)
def sinc_time_signal(t: np.ndarray, tau: float) -> np.ndarray:
    return np.sinc(t / tau)


def sinc_frequency_response(f: np.ndarray, tau: float) -> np.ndarray:
    cutoff = 1.0 / (2.0 * tau)
    return tau * np.where(np.abs(f) <= cutoff, 1.0, 0.0)


@st.cache_data
def compute_ctft_data(
    signal_type: str,
    tau: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, float]:
    """缓存时域与频域解析结果。"""
    tau_max = max(tau, 1.0)

    t = np.linspace(-5.0 * tau_max, 5.0 * tau_max, SAMPLE_POINTS)

    freq_limit = 3.0 / tau if tau > 0.3 else 10.0
    f = np.linspace(-freq_limit, freq_limit, SAMPLE_POINTS)

    if signal_type == "矩形脉冲":
        x_t = rect_time_signal(t, tau)
        X_f = rect_frequency_response(f, tau)
    elif signal_type == "高斯脉冲":
        x_t = gaussian_time_signal(t, tau)
        X_f = gaussian_frequency_response(f, tau)
    elif signal_type == "双边指数":
        x_t = bilateral_exponential_time_signal(t, tau)
        X_f = bilateral_exponential_frequency_response(f, tau)
    else:
        x_t = sinc_time_signal(t, tau)
        X_f = sinc_frequency_response(f, tau)

    main_lobe_bandwidth = 2.0 / tau

    return t, x_t, f, X_f, main_lobe_bandwidth


# ──────────────────────────── 页面标题与公式 ────────────────────────────

st.title("连续时间傅里叶变换")

st.latex(r"X(f)=\int_{-\infty}^{\infty}x(t)e^{-j2\pi ft}\,dt")


# ──────────────────────────── 侧边栏控件 ────────────────────────────

signal_type = st.sidebar.selectbox(
    "信号类型",
    ["矩形脉冲", "高斯脉冲", "双边指数", "sinc 信号"],
)

tau = st.sidebar.slider("脉宽参数 τ", 0.1, 5.0, 1.0, 0.1)


# ──────────────────────────── 核心计算 ────────────────────────────

t, x_t, f, X_f, main_lobe_bandwidth = compute_ctft_data(signal_type, tau)

spectrum_magnitude = np.abs(X_f)


# ──────────────────────────── 侧边栏指标 ────────────────────────────

st.sidebar.metric("脉宽 τ", f"{tau:.1f} s")

if signal_type == "矩形脉冲":
    st.sidebar.metric("主瓣带宽", f"{main_lobe_bandwidth:.2f} Hz")


# ──────────────────────────── Plotly 图表（1 行 2 列） ────────────────────────────

fig = make_subplots(
    rows=1,
    cols=2,
    subplot_titles=["时域信号 x(t)", "频谱 |X(f)|"],
    horizontal_spacing=0.12,
)

# 左图：时域波形
fig.add_trace(
    go.Scatter(
        x=t,
        y=x_t,
        mode="lines",
        name="x(t)",
        line=dict(color=COLOR_PRIMARY, width=2),
        fill="tozeroy",
        fillcolor="rgba(99, 110, 250, 0.30)",
    ),
    row=1,
    col=1,
)

# 右图：频域幅度谱
fig.add_trace(
    go.Scatter(
        x=f,
        y=spectrum_magnitude,
        mode="lines",
        name="|X(f)|",
        line=dict(color=COLOR_ACCENT, width=2),
        fill="tozeroy",
        fillcolor="rgba(239, 85, 59, 0.30)",
    ),
    row=1,
    col=2,
)

fig.update_xaxes(title_text="t (s)", row=1, col=1)
fig.update_yaxes(title_text="x(t)", row=1, col=1)
fig.update_xaxes(title_text="f (Hz)", row=1, col=2)
fig.update_yaxes(title_text="|X(f)|", row=1, col=2)

fig.update_layout(**LAYOUT_DEFAULTS, height=520)
st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)


# ──────────────────────────── 教学注释 ────────────────────────────

st.info(
    "考点提示：时域压缩 τ 倍 → 频域展宽 1/τ 倍（时频对偶性）。"
    "矩形脉冲 ↔ sinc 函数是最经典的傅里叶变换对。"
)
