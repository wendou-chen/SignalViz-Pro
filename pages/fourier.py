# 文件用途：傅里叶级数与吉布斯现象可视化页面
# 对应考点：方波的傅里叶级数展开、奇次谐波叠加、吉布斯现象（~9% 过冲）
# 作为 Streamlit 子页面由 app.py 通过 st.navigation 路由加载，不调用 st.set_page_config

import numpy as np
import streamlit as st
from scipy import signal
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from utils import PLOTLY_CONFIG, LAYOUT_DEFAULTS

# ──────────────────────────── 页面标题与公式 ────────────────────────────

st.title("傅里叶级数与吉布斯现象")

st.latex(
    r"x_N(t) = \frac{4}{\pi} \sum_{k=0}^{N-1} "
    r"\frac{\sin\!\bigl((2k+1)\,\omega_0\, t\bigr)}{2k+1}"
)

# ──────────────────────────── 侧边栏控件 ────────────────────────────

# 谐波数 N：只取奇数项，滑块步长 2
N = st.sidebar.slider("谐波数 N（奇次项数）", min_value=1, max_value=101, value=5, step=2)

# 周期 T
T = st.sidebar.slider("周期 T (s)", min_value=1.0, max_value=5.0, value=2.0, step=0.1)

# ──────────────────────────── 核心计算 ────────────────────────────

# 基频
omega_0 = 2.0 * np.pi / T

# 时间轴：覆盖 4 个周期，2000 个采样点
t = np.linspace(-2 * T, 2 * T, 2000)

# 原始方波（scipy 生成，幅值 -1/+1）
square_wave = signal.square(omega_0 * t)

# 奇次谐波序号：1, 3, 5, ..., 2*(N-1)+1
ns = 2 * np.arange(N) + 1  # shape (N,)

# NumPy 广播构建 (len_t, N) 矩阵 —— 每列是一个谐波分量
# t[:, None] → (2000, 1)，ns[None, :] → (1, N)
harmonics = np.sin(ns[np.newaxis, :] * omega_0 * t[:, np.newaxis]) / ns[np.newaxis, :]

# 合成波形：对所有谐波求和
x_synth = (4.0 / np.pi) * harmonics.sum(axis=1)

# 吉布斯过冲百分比（相对于方波幅值 1.0）
overshoot = (float(x_synth.max()) - 1.0) * 100.0

# 频谱数据：频率与幅度
freqs = ns / T                       # 各谐波频率 f = n / T
magnitudes = 2.0 / (ns * np.pi)     # 傅里叶系数幅度 |c_n|

# ──────────────────────────── 侧边栏指标 ────────────────────────────

st.sidebar.metric("吉布斯过冲", f"{overshoot:.2f} %")

# ──────────────────────────── Plotly 图表（1 行 2 列） ────────────────────────────

fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=("时域波形", "频域谱线"),
    horizontal_spacing=0.12,
)

# 左图 —— 原始方波（灰色虚线）
fig.add_trace(
    go.Scatter(
        x=t, y=square_wave,
        mode="lines",
        line=dict(color="gray", dash="dash"),
        name="原始方波",
    ),
    row=1, col=1,
)

# 左图 —— 合成波形（蓝色实线）
fig.add_trace(
    go.Scatter(
        x=t, y=x_synth,
        mode="lines",
        line=dict(color="#636EFA", width=2),
        name=f"N={N} 合成",
    ),
    row=1, col=1,
)

# 右图 —— 频谱柱状图（红色）
fig.add_trace(
    go.Bar(
        x=freqs, y=magnitudes,
        marker_color="#EF553B",
        width=0.05,
        name="频谱 |cₙ|",
    ),
    row=1, col=2,
)

# 坐标轴标签
fig.update_xaxes(title_text="t", row=1, col=1)
fig.update_yaxes(title_text="x(t)", row=1, col=1)
fig.update_xaxes(title_text="f (Hz)", row=1, col=2)
fig.update_yaxes(title_text="|cₙ|", row=1, col=2)

# 应用共享布局
fig.update_layout(**LAYOUT_DEFAULTS, height=500)

st.plotly_chart(fig, width="stretch", config=PLOTLY_CONFIG)

# ──────────────────────────── 教学注释 ────────────────────────────

st.info("💡 观察：当 N→∞ 时，不连续点处的过冲始终约为 9%，这就是吉布斯现象。")
