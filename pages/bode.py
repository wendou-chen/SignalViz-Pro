# 文件用途：频率响应与 Bode 图可视化（幅频 + 相频）
# 对应考点：幅频特性、相频特性、转折频率识别、Bode 渐近线理解

import numpy as np
import streamlit as st
from scipy import signal
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils import PLOTLY_CONFIG, LAYOUT_DEFAULTS

# ──────────────────────────── 常量与计算函数 ────────────────────────────

COLOR_PRIMARY = "#636EFA"
COLOR_ACCENT = "#EF553B"
COLOR_SUCCESS = "#00CC96"
COLOR_REF = "gray"

OMEGA_MIN = 1e-2
OMEGA_MAX = 1e4
OMEGA_POINTS = 2000
EPS = 1e-12


def to_transfer_function_coefficients(
    K: float, z1: float, p1: float, p2: float
) -> tuple[np.ndarray, np.ndarray]:
    """将零极点增益形式转换为传递函数多项式系数。"""
    zpk_system = signal.ZerosPolesGain([z1], [p1, p2], K)
    tf_system = zpk_system.to_tf()

    num = np.atleast_1d(np.asarray(tf_system.num, dtype=float))
    den = np.atleast_1d(np.asarray(tf_system.den, dtype=float))

    return num, den


def unwrap_phase_degrees(H: np.ndarray) -> np.ndarray:
    """对相位进行展开，避免 ±180° 跳变。"""
    phase_rad = np.unwrap(np.angle(H))
    return np.rad2deg(phase_rad)


@st.cache_data
def compute_bode_data(
    K: float,
    z1: float,
    p1: float,
    p2: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float, float, float, float]:
    """缓存 Bode 计算结果。"""
    num, den = to_transfer_function_coefficients(K, z1, p1, p2)

    w = np.logspace(np.log10(OMEGA_MIN), np.log10(OMEGA_MAX), OMEGA_POINTS)
    w, H = signal.freqs(num, den, worN=w)

    mag_db = 20.0 * np.log10(np.maximum(np.abs(H), EPS))
    phase_deg = unwrap_phase_degrees(H)

    wz = abs(z1)
    wp1 = abs(p1)
    wp2 = abs(p2)

    dc_gain_linear = np.abs(K * z1 / (p1 * p2))
    dc_gain_db = 20.0 * np.log10(np.maximum(dc_gain_linear, EPS))

    return w, mag_db, phase_deg, wz, wp1, wp2, dc_gain_db


# ──────────────────────────── 页面标题与公式 ────────────────────────────

st.title("频率响应与 Bode 图")

st.latex(r"H(s)=K\cdot\frac{s-z_1}{(s-p_1)(s-p_2)}")


# ──────────────────────────── 侧边栏控件 ────────────────────────────

K = st.sidebar.slider("增益 K", 0.1, 20.0, 1.0, 0.1)
z1 = st.sidebar.slider("零点 z₁ (实部)", -50.0, -0.1, -10.0, 0.1)
p1 = st.sidebar.slider("极点 p₁ (实部)", -50.0, -0.1, -1.0, 0.1)
p2 = st.sidebar.slider("极点 p₂ (实部)", -50.0, -0.1, -5.0, 0.1)


# ──────────────────────────── 核心计算 ────────────────────────────

w, mag_db, phase_deg, wz, wp1, wp2, dc_gain_db = compute_bode_data(K, z1, p1, p2)


# ──────────────────────────── 侧边栏指标 ────────────────────────────

st.sidebar.metric("转折频率 |z₁|", f"{wz:.2f} rad/s")
st.sidebar.metric("转折频率 |p₁|", f"{wp1:.2f} rad/s")
st.sidebar.metric("转折频率 |p₂|", f"{wp2:.2f} rad/s")
st.sidebar.metric("DC 增益", f"{dc_gain_db:.2f} dB")


# ──────────────────────────── Plotly 图表（2 行 1 列） ────────────────────────────

fig = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.08,
    subplot_titles=["幅频特性", "相频特性"],
)

# 上图：精确幅频曲线
fig.add_trace(
    go.Scatter(
        x=w,
        y=mag_db,
        mode="lines",
        line=dict(color=COLOR_PRIMARY, width=2),
        name="|H(jω)| (dB)",
    ),
    row=1,
    col=1,
)

# 上图：0 dB 参考线
fig.add_hline(y=0.0, line_dash="dash", line_color=COLOR_REF, row=1, col=1)

# 上图：转折频率标记
fig.add_vline(x=wz, line_dash="dot", line_color=COLOR_ACCENT, row=1, col=1)
fig.add_vline(x=wp1, line_dash="dot", line_color=COLOR_ACCENT, row=1, col=1)
fig.add_vline(x=wp2, line_dash="dot", line_color=COLOR_ACCENT, row=1, col=1)

# 下图：相频曲线（展开后）
fig.add_trace(
    go.Scatter(
        x=w,
        y=phase_deg,
        mode="lines",
        line=dict(color=COLOR_PRIMARY, width=2),
        name="∠H(jω)",
    ),
    row=2,
    col=1,
)

# 下图：相位参考线
fig.add_hline(y=-90.0, line_dash="dash", line_color=COLOR_REF, row=2, col=1)
fig.add_hline(y=-180.0, line_dash="dash", line_color=COLOR_REF, row=2, col=1)

fig.update_xaxes(type="log", title_text="频率 ω (rad/s)", row=1, col=1)
fig.update_xaxes(type="log", title_text="频率 ω (rad/s)", row=2, col=1)
fig.update_yaxes(title_text="幅度 (dB)", row=1, col=1)
fig.update_yaxes(title_text="相位 (°)", row=2, col=1)

fig.update_layout(**LAYOUT_DEFAULTS, height=680)
st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)


# ──────────────────────────── 教学注释 ────────────────────────────

st.info(
    "考点提示：Bode 图渐近线画法 — 每个实数极点在转折频率处贡献 -20 dB/dec "
    "斜率变化，每个实数零点贡献 +20 dB/dec。"
    "相位在转折频率前后一个十倍频程内变化 ±90°。"
)
