# 文件用途：DFT/FFT 频谱分析可视化（时域加窗 + 频域幅度谱）
# 对应考点：频谱泄漏、窗函数效果、零填充与频率分辨率

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

MIN_MAG = 1e-12


def discrete_sine_signal(n: np.ndarray, f_sig: float, f_s: float) -> np.ndarray:
    """离散正弦信号 x[n]，保持向量化实现。"""
    signal = np.sin(2.0 * np.pi * f_sig * n / f_s)
    return np.where(n >= 0, signal, 0.0)


def rectangular_window(n_points: int) -> np.ndarray:
    """矩形窗（全 1），使用 np.where 返回向量。"""
    idx = np.arange(n_points)
    return np.where(idx >= 0, 1.0, 1.0)


def get_window(window_type: str, n_points: int) -> np.ndarray:
    """窗函数映射。"""
    if window_type == "矩形窗":
        return rectangular_window(n_points)
    if window_type == "汉宁窗":
        return np.hanning(n_points)
    if window_type == "汉明窗":
        return np.hamming(n_points)
    return np.blackman(n_points)


@st.cache_data
def compute_dft_data(
    f_sig: float,
    f_s: float,
    n_points: int,
    window_type: str,
    zero_pad: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, int, float]:
    """缓存 DFT 计算，避免重复 FFT 开销。"""
    n = np.arange(n_points)
    x = discrete_sine_signal(n, f_sig, f_s)

    window = get_window(window_type, n_points)
    x_windowed = x * window

    n_fft = int(n_points * zero_pad)
    spectrum = np.fft.fft(x_windowed, n=n_fft)
    freqs = np.fft.fftfreq(n_fft, d=1.0 / f_s)

    mask = freqs >= 0.0
    freqs_pos = freqs[mask]

    mag = np.abs(spectrum[mask]) * 2.0 / n_points
    mag_db = 20.0 * np.log10(np.maximum(mag, MIN_MAG))

    delta_f = f_s / n_fft

    return n, x, x_windowed, freqs_pos, mag_db, n_fft, delta_f


# ──────────────────────────── 页面标题与公式 ────────────────────────────

st.title("DFT / FFT 频谱分析")

st.latex(r"X[k] = \sum_{n=0}^{N-1} x[n] \, w[n] \, e^{-j2\pi kn/N}")


# ──────────────────────────── 侧边栏控件 ────────────────────────────

f_sig = st.sidebar.slider("信号频率 (Hz)", 1.0, 50.0, 10.0, 0.5)
f_s = st.sidebar.slider("采样频率 (Hz)", 50.0, 500.0, 100.0, 10.0)
N_points = st.sidebar.slider("采样点数 N", 16, 512, 64, step=16)
window_type = st.sidebar.selectbox("窗函数", ["矩形窗", "汉宁窗", "汉明窗", "布莱克曼窗"])
zero_pad = st.sidebar.slider("零填充倍数", 1, 8, 1)


# ──────────────────────────── 核心计算 ────────────────────────────

n, x, x_windowed, freqs_pos, mag_db, N_fft, delta_f = compute_dft_data(
    f_sig, f_s, N_points, window_type, zero_pad
)


# ──────────────────────────── 侧边栏指标 ────────────────────────────

st.sidebar.metric("频率分辨率 Δf", f"{delta_f:.4f} Hz")
st.sidebar.metric("FFT 点数 N_fft", f"{N_fft}")


# ──────────────────────────── Plotly 图表（2 行 1 列） ────────────────────────────

fig = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=False,
    vertical_spacing=0.10,
    subplot_titles=["时域信号（加窗后）", "DFT 幅度谱"],
)

# 上图：原始离散信号（灰色虚线）
fig.add_trace(
    go.Scatter(
        x=n,
        y=x,
        mode="lines+markers",
        name="原始信号 x[n]",
        line=dict(color=COLOR_REF, width=1.5, dash="dash"),
        marker=dict(size=4, color=COLOR_REF),
    ),
    row=1,
    col=1,
)

# 上图：加窗后离散信号（蓝色实线）
fig.add_trace(
    go.Scatter(
        x=n,
        y=x_windowed,
        mode="lines+markers",
        name="加窗信号 x[n]w[n]",
        line=dict(color=COLOR_PRIMARY, width=2),
        marker=dict(size=4, color=COLOR_PRIMARY),
    ),
    row=1,
    col=1,
)

# 下图：单边幅度谱 dB
fig.add_trace(
    go.Bar(
        x=freqs_pos,
        y=mag_db,
        name="|X(f)| (dB)",
        marker_color=COLOR_PRIMARY,
        opacity=0.9,
    ),
    row=2,
    col=1,
)

# 下图：信号频率参考线
fig.add_vline(
    x=f_sig,
    line_dash="dash",
    line_color=COLOR_ACCENT,
    line_width=2,
    row=2,
    col=1,
)

fig.update_xaxes(title_text="n (采样点)", row=1, col=1)
fig.update_yaxes(title_text="幅度", row=1, col=1)
fig.update_xaxes(title_text="频率 (Hz)", row=2, col=1)
fig.update_yaxes(title_text="幅度 (dB)", row=2, col=1)

fig.update_layout(**LAYOUT_DEFAULTS, height=700)
st.plotly_chart(fig, width="stretch", config=PLOTLY_CONFIG)


# ──────────────────────────── 教学注释 ────────────────────────────

st.info(
    "考点提示：频谱泄漏源于有限长截断（等效矩形窗卷积）。"
    "加窗可降低旁瓣但展宽主瓣。"
    "零填充不提高真实分辨率，但使频谱更平滑（插值效果）。"
)
