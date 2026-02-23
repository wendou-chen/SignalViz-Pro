# 文件用途：LTI 系统四大性质交互式验证（线性性、时不变性、因果性、BIBO 稳定性）
# 对应考点：LTI 系统定义与判定、叠加原理、时移性质、因果系统条件、BIBO 稳定判据

import numpy as np
import streamlit as st
from scipy.integrate import cumulative_trapezoid
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from utils import PLOTLY_CONFIG, LAYOUT_DEFAULTS


def h_causal(t: np.ndarray) -> np.ndarray:
    """因果冲激响应 h(t) = e^{-t}u(t)"""
    return np.where(t >= 0, np.exp(-t), 0.0)


def h_noncausal(t: np.ndarray) -> np.ndarray:
    """非因果冲激响应 h(t) = e^{-|t|}"""
    return np.exp(-np.abs(t))


def rect_pulse(t: np.ndarray) -> np.ndarray:
    """矩形脉冲 [0,1] 区间为 1"""
    return np.where((t >= 0) & (t <= 1), 1.0, 0.0)


def tri_pulse(t: np.ndarray) -> np.ndarray:
    """三角脉冲 [0,1] 区间线性下降"""
    return np.where((t >= 0) & (t <= 1), 1.0 - t, 0.0)


TAU = np.linspace(-3, 10, 1000)
T_OUT = np.linspace(-2, 8, 400)
COLOR_BLUE = "#636EFA"
COLOR_RED = "#EF553B"
COLOR_GREEN = "#00CC96"
COLOR_REF = "gray"


def _conv_from_samples(x_vals: np.ndarray, h_key: str) -> np.ndarray:
    h_map = {"causal": h_causal, "noncausal": h_noncausal}
    h_matrix = h_map[h_key](T_OUT[:, None] - TAU[None, :])
    return np.trapezoid(x_vals[None, :] * h_matrix, TAU, axis=1)


@st.cache_data
def _conv(x_key: str, h_key: str, delay: float = 0.0) -> np.ndarray:
    x_map = {"rect": rect_pulse, "tri": tri_pulse}
    x_vals = x_map[x_key](TAU - delay)
    return _conv_from_samples(x_vals, h_key)


st.title("LTI 系统四大性质")
st.latex(r"h(t) = e^{-t}u(t) \quad \text{（示例 LTI 系统）}")

prop = st.sidebar.selectbox(
    "选择性质",
    ["线性性（叠加原理）", "时不变性", "因果性", "BIBO 稳定性"],
)

if prop == "线性性（叠加原理）":
    st.latex(r"\mathcal{T}\{a x_1(t) + b x_2(t)\} = a\mathcal{T}\{x_1(t)\} + b\mathcal{T}\{x_2(t)\}")

    a = st.sidebar.slider("系数 a", -2.0, 2.0, 1.0, step=0.1)
    b = st.sidebar.slider("系数 b", -2.0, 2.0, 0.5, step=0.1)

    x1 = rect_pulse(TAU)
    x2 = tri_pulse(TAU)
    x_mix = a * x1 + b * x2

    y1 = _conv("rect", "causal")
    y2 = _conv("tri", "causal")
    y_left = _conv_from_samples(x_mix, "causal")
    y_right = a * y1 + b * y2
    max_diff = float(np.max(np.abs(y_left - y_right)))
    st.sidebar.metric("最大误差", f"{max_diff:.2e}")

    fig = make_subplots(
        rows=2,
        cols=1,
        row_heights=[0.4, 0.6],
        subplot_titles=["输入信号", "输出对比"],
        vertical_spacing=0.12,
    )

    fig.add_trace(
        go.Scatter(
            x=TAU,
            y=x1,
            mode="lines",
            name="x1(t)=rect(t)",
            line=dict(color=COLOR_BLUE, width=2),
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=TAU,
            y=x2,
            mode="lines",
            name="x2(t)=tri(t)",
            line=dict(color=COLOR_RED, width=2),
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=TAU,
            y=x_mix,
            mode="lines",
            name="a x1 + b x2",
            line=dict(color=COLOR_GREEN, width=2),
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=T_OUT,
            y=y_left,
            mode="lines",
            name="T{a x1 + b x2}",
            line=dict(color=COLOR_BLUE, width=3),
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=T_OUT,
            y=y_right,
            mode="lines",
            name="aT{x1}+bT{x2}",
            line=dict(color=COLOR_RED, width=2, dash="dash"),
        ),
        row=2,
        col=1,
    )

    fig.update_xaxes(title_text="t", row=1, col=1)
    fig.update_xaxes(title_text="t", row=2, col=1)
    fig.update_yaxes(title_text="幅值", row=1, col=1)
    fig.update_yaxes(title_text="幅值", row=2, col=1)
    fig.update_layout(**LAYOUT_DEFAULTS, height=720)
    st.plotly_chart(fig, width="stretch", config=PLOTLY_CONFIG)

    st.info("蓝色实线与红色虚线完全重合，验证了线性系统满足叠加原理。")

elif prop == "时不变性":
    st.latex(r"x(t)\xrightarrow{\mathcal{T}}y(t), \quad x(t-t_0)\xrightarrow{\mathcal{T}}y(t-t_0)")

    t0 = st.sidebar.slider("延迟 t0", 0.0, 4.0, 2.0, step=0.1)

    x_orig = rect_pulse(TAU)
    x_delayed = rect_pulse(TAU - t0)
    y_orig = _conv("rect", "causal", delay=0.0)
    y_delayed = _conv("rect", "causal", delay=t0)
    y_shifted = np.interp(T_OUT - t0, T_OUT, y_orig, left=0.0, right=0.0)
    max_diff = float(np.max(np.abs(y_delayed - y_shifted)))
    st.sidebar.metric("最大误差", f"{max_diff:.2e}")

    fig = make_subplots(
        rows=2,
        cols=1,
        row_heights=[0.4, 0.6],
        subplot_titles=["输入信号", "输出信号"],
        vertical_spacing=0.12,
    )

    fig.add_trace(
        go.Scatter(
            x=TAU,
            y=x_orig,
            mode="lines",
            name="x(t)",
            line=dict(color=COLOR_BLUE, width=2),
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=TAU,
            y=x_delayed,
            mode="lines",
            name="x(t-t0)",
            line=dict(color=COLOR_RED, width=2, dash="dash"),
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=T_OUT,
            y=y_orig,
            mode="lines",
            name="y(t)",
            line=dict(color=COLOR_REF, width=2, dash="dash"),
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=T_OUT,
            y=y_delayed,
            mode="lines",
            name="T{x(t-t0)}",
            line=dict(color=COLOR_BLUE, width=3),
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=T_OUT,
            y=y_shifted,
            mode="lines",
            name="y(t-t0)",
            line=dict(color=COLOR_RED, width=2, dash="dash"),
        ),
        row=2,
        col=1,
    )

    fig.update_xaxes(title_text="t", row=1, col=1)
    fig.update_xaxes(title_text="t", row=2, col=1)
    fig.update_yaxes(title_text="幅值", row=1, col=1)
    fig.update_yaxes(title_text="幅值", row=2, col=1)
    fig.update_layout(**LAYOUT_DEFAULTS, height=720)
    st.plotly_chart(fig, width="stretch", config=PLOTLY_CONFIG)

    st.info("输入延迟 t0 后，输出也恰好延迟 t0 且波形不变，验证了系统时不变。")

elif prop == "因果性":
    st.latex(r"h(t)=0,\ t<0 \quad \Rightarrow \quad \text{因果系统}")

    input_delay = st.sidebar.slider("输入起始时刻", 1.0, 5.0, 2.0, step=0.1)

    y_causal = _conv("rect", "causal", delay=input_delay)
    y_noncausal = _conv("rect", "noncausal", delay=input_delay)
    x_delayed = rect_pulse(T_OUT - input_delay)

    t_h = np.linspace(-3, 5, 600)
    h_c = h_causal(t_h)
    h_nc = h_noncausal(t_h)

    fig = make_subplots(
        rows=2,
        cols=1,
        row_heights=[0.4, 0.6],
        subplot_titles=["冲激响应 h(t)", "系统输出"],
        vertical_spacing=0.12,
    )

    fig.add_trace(
        go.Scatter(
            x=t_h,
            y=h_c,
            mode="lines",
            name="因果 h(t)=e^{-t}u(t)",
            line=dict(color=COLOR_BLUE, width=2),
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=t_h,
            y=h_nc,
            mode="lines",
            name="非因果 h(t)=e^{-|t|}",
            line=dict(color=COLOR_RED, width=2),
        ),
        row=1,
        col=1,
    )
    fig.add_vline(x=0.0, line_dash="dash", line_color=COLOR_REF, row=1, col=1)

    fig.add_trace(
        go.Scatter(
            x=T_OUT,
            y=x_delayed,
            mode="lines",
            name="输入 x(t)",
            line=dict(color=COLOR_REF, width=1),
            fill="tozeroy",
            fillcolor="rgba(128,128,128,0.2)",
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=T_OUT,
            y=y_causal,
            mode="lines",
            name="因果系统输出",
            line=dict(color=COLOR_BLUE, width=3),
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=T_OUT,
            y=y_noncausal,
            mode="lines",
            name="非因果系统输出",
            line=dict(color=COLOR_RED, width=2),
        ),
        row=2,
        col=1,
    )
    fig.add_vline(x=input_delay, line_dash="dash", line_color=COLOR_REF, row=2, col=1)

    fig.update_xaxes(title_text="t", row=1, col=1)
    fig.update_xaxes(title_text="t", row=2, col=1)
    fig.update_yaxes(title_text="幅值", row=1, col=1)
    fig.update_yaxes(title_text="幅值", row=2, col=1)
    fig.update_layout(**LAYOUT_DEFAULTS, height=720)
    st.plotly_chart(fig, width="stretch", config=PLOTLY_CONFIG)

    st.info("非因果系统（红色）在输入到达前已有输出，表现为“预知未来”；因果系统不会出现该现象。")

else:
    st.latex(r"\int_{0}^{\infty}\lvert h(t)\rvert dt < \infty \Rightarrow \text{BIBO 稳定}")

    alpha = st.sidebar.slider("指数参数 α", 0.1, 3.0, 1.0, step=0.1)

    t = np.linspace(0, 6, 600)
    h_stable = np.exp(-alpha * t)
    h_unstable = np.clip(np.exp(alpha * t), 0.0, 50.0)
    int_stable = cumulative_trapezoid(h_stable, t, initial=0.0)
    int_unstable = cumulative_trapezoid(h_unstable, t, initial=0.0)

    st.sidebar.metric(r"∫|h_stable|dt", f"{int_stable[-1]:.3f}")
    st.sidebar.metric("理论极限 1/α", f"{1 / alpha:.3f}")

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=["冲激响应", "累积积分 ∫₀ᵗ|h(τ)|dτ"],
        horizontal_spacing=0.12,
    )

    fig.add_trace(
        go.Scatter(
            x=t,
            y=h_stable,
            mode="lines",
            name="稳定 h(t)=e^{-αt}",
            line=dict(color=COLOR_BLUE, width=2),
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=t,
            y=h_unstable,
            mode="lines",
            name="不稳定 h(t)=e^{αt}",
            line=dict(color=COLOR_RED, width=2),
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=t,
            y=int_stable,
            mode="lines",
            name="稳定积分（收敛）",
            line=dict(color=COLOR_BLUE, width=3),
        ),
        row=1,
        col=2,
    )
    fig.add_trace(
        go.Scatter(
            x=t,
            y=int_unstable,
            mode="lines",
            name="不稳定积分（发散）",
            line=dict(color=COLOR_RED, width=2),
        ),
        row=1,
        col=2,
    )
    fig.add_hline(
        y=1.0 / alpha,
        line_dash="dash",
        line_color=COLOR_REF,
        annotation_text="1/α",
        annotation_position="top right",
        row=1,
        col=2,
    )

    fig.update_xaxes(title_text="t", row=1, col=1)
    fig.update_xaxes(title_text="t", row=1, col=2)
    fig.update_yaxes(title_text="h(t)", row=1, col=1)
    fig.update_yaxes(title_text="累积积分", row=1, col=2)
    fig.update_layout(**LAYOUT_DEFAULTS, height=520)
    st.plotly_chart(fig, width="stretch", config=PLOTLY_CONFIG)

    st.info("衰减指数的积分收敛到 1/α（稳定）；增长指数积分持续发散（不稳定）。")
