# 文件用途：Z 变换与离散系统稳定性可视化（z 平面极零点 + 冲激响应）
# 对应考点：z 平面极零点分布、单位圆稳定判据、ROC 与因果性/稳定性关系

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

UNIT_CIRCLE_POINTS = 200


def causal_impulse_response(n: np.ndarray, r: float, theta: float) -> np.ndarray:
    """因果序列 h[n] = r^n cos(theta*n) u[n]。"""
    return np.where(n >= 0, (r ** n) * np.cos(theta * n), 0.0)


def classify_stability(r: float) -> str:
    """按照极点模长分类稳定性。"""
    if np.isclose(r, 1.0):
        return "critical"
    return "stable" if r < 1.0 else "unstable"


@st.cache_data
def compute_z_domain_data(r: float, theta: float, length: int) -> tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    float,
    float,
]:
    """缓存离散冲激响应和 z 平面绘图所需数据。"""
    n = np.arange(0, length)
    h_n = causal_impulse_response(n, r, theta)

    theta_circle = np.linspace(0.0, 2.0 * np.pi, UNIT_CIRCLE_POINTS)
    unit_circle_x = np.cos(theta_circle)
    unit_circle_y = np.sin(theta_circle)

    pole_real = r * np.cos(theta)
    pole_imag = r * np.sin(theta)

    envelope = np.power(r, n)

    return n, h_n, unit_circle_x, unit_circle_y, envelope, pole_real, pole_imag


# ──────────────────────────── 页面标题与公式 ────────────────────────────

st.title("Z 变换与离散系统稳定性")

st.latex(r"H(z)=\frac{z}{z^2 - 2r\cos\theta\cdot z + r^2}")


# ──────────────────────────── 侧边栏控件 ────────────────────────────

r = st.sidebar.slider("极点模 r", 0.1, 2.0, 0.8, 0.05)
theta = st.sidebar.slider("极点角 θ (rad)", 0.0, float(np.pi), float(np.pi / 4), 0.05)
N = st.sidebar.slider("序列长度 N", 10, 100, 50)


# ──────────────────────────── 核心计算 ────────────────────────────

n, h_n, unit_circle_x, unit_circle_y, envelope, pole_real, pole_imag = compute_z_domain_data(
    r, theta, N
)

stability_state = classify_stability(r)
axis_limit = max(1.3, r + 0.4)


# ──────────────────────────── 侧边栏指标 ────────────────────────────

st.sidebar.metric("极点模 |r|", f"{r:.3f}")

if stability_state == "stable":
    st.sidebar.success("稳定")
elif stability_state == "unstable":
    st.sidebar.error("不稳定")
else:
    st.sidebar.warning("临界")


# ──────────────────────────── Plotly 图表（1 行 2 列） ────────────────────────────

fig = make_subplots(
    rows=1,
    cols=2,
    subplot_titles=["z 平面极零点图", "离散冲激响应 h[n]"],
    horizontal_spacing=0.12,
)

# 左图：稳定区域（单位圆内，浅绿色）
fig.add_shape(
    type="circle",
    x0=-1.0,
    y0=-1.0,
    x1=1.0,
    y1=1.0,
    fillcolor="rgba(0, 204, 150, 0.16)",
    line_width=0,
    row=1,
    col=1,
)

# 左图：单位圆边界（灰色虚线）
fig.add_trace(
    go.Scatter(
        x=unit_circle_x,
        y=unit_circle_y,
        mode="lines",
        name="单位圆",
        line=dict(color=COLOR_REF, width=2, dash="dash"),
    ),
    row=1,
    col=1,
)

# 左图：共轭极点（红色 ×）
fig.add_trace(
    go.Scatter(
        x=[pole_real, pole_real],
        y=[pole_imag, -pole_imag],
        mode="markers",
        name="极点",
        marker=dict(symbol="x", size=14, color=COLOR_ACCENT, line=dict(width=2)),
    ),
    row=1,
    col=1,
)

# 左图：零点（原点蓝色 ○）
fig.add_trace(
    go.Scatter(
        x=[0.0],
        y=[0.0],
        mode="markers",
        name="零点",
        marker=dict(symbol="circle-open", size=13, color=COLOR_PRIMARY, line=dict(width=2)),
    ),
    row=1,
    col=1,
)

fig.update_xaxes(
    title_text="Re(z)",
    range=[-axis_limit, axis_limit],
    zeroline=True,
    zerolinecolor=COLOR_REF,
    scaleanchor="y",
    scaleratio=1,
    row=1,
    col=1,
)
fig.update_yaxes(
    title_text="Im(z)",
    range=[-axis_limit, axis_limit],
    zeroline=True,
    zerolinecolor=COLOR_REF,
    row=1,
    col=1,
)

# 右图：离散冲激响应柱状茎叶图
fig.add_trace(
    go.Bar(
        x=n,
        y=h_n,
        width=0.3,
        name="h[n]",
        marker_color=COLOR_PRIMARY,
        opacity=0.9,
    ),
    row=1,
    col=2,
)

# r < 1 时叠加指数包络 ±r^n
if stability_state == "stable":
    fig.add_trace(
        go.Scatter(
            x=n,
            y=envelope,
            mode="lines",
            name="+r^n 包络",
            line=dict(color=COLOR_REF, width=1.5, dash="dash"),
        ),
        row=1,
        col=2,
    )
    fig.add_trace(
        go.Scatter(
            x=n,
            y=-envelope,
            mode="lines",
            name="-r^n 包络",
            line=dict(color=COLOR_REF, width=1.5, dash="dash"),
            showlegend=False,
        ),
        row=1,
        col=2,
    )

fig.update_xaxes(title_text="n", row=1, col=2)
fig.update_yaxes(title_text="h[n]", row=1, col=2)

fig.update_layout(**LAYOUT_DEFAULTS, height=520)
st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)


# ──────────────────────────── 教学注释 ────────────────────────────

st.info("考点提示：因果 LTI 系统稳定的充要条件是所有极点位于单位圆内（|z| < 1），即 ROC 包含单位圆。")
