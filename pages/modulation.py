# 文件用途: 数字调制（BPSK/QPSK/16QAM）星座图与眼图可视化
# 对应考点: 数字调制原理、加性高斯白噪声信道、星座图判决区域、眼图分析

import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils import PLOTLY_CONFIG, LAYOUT_DEFAULTS

# ── 星座点生成（纯函数，归一化平均功率为 1） ──────────────────────


def bpsk_constellation() -> np.ndarray:
    """BPSK: 两个实轴对称点"""
    return np.array([-1.0 + 0j, 1.0 + 0j])


def qpsk_constellation() -> np.ndarray:
    """QPSK: 四个等间隔相位点，归一化"""
    return np.array([1 + 1j, -1 + 1j, -1 - 1j, 1 - 1j]) / np.sqrt(2)


def qam16_constellation() -> np.ndarray:
    """16QAM: 4x4 矩形网格，归一化平均功率为 1"""
    levels = np.array([-3, -1, 1, 3])
    grid = levels[:, np.newaxis] + 1j * levels[np.newaxis, :]
    return grid.flatten() / np.sqrt(10)


CONSTELLATION_MAP = {
    "BPSK": bpsk_constellation,
    "QPSK": qpsk_constellation,
    "16QAM": qam16_constellation,
}

# ── 页面标题与公式 ────────────────────────────────────────────────

st.title("数字调制与噪声")
st.latex(r"r(t) = s(t) + n(t), \quad n \sim \mathcal{N}(0, \sigma_n^2)")

# ── 侧边栏控件 ───────────────────────────────────────────────────

st.sidebar.markdown("### 调制参数")
mod_type = st.sidebar.selectbox("调制方式", list(CONSTELLATION_MAP.keys()))
snr_db = st.sidebar.slider("SNR (dB)", -5.0, 30.0, 10.0, step=1.0)
num_symbols = st.sidebar.slider("符号数", 100, 2000, 500, step=100)

# ── 核心计算：发射 → 加噪 → 接收 ─────────────────────────────────

constellation = CONSTELLATION_MAP[mod_type]()
snr_lin = 10.0 ** (snr_db / 10.0)
noise_std = 1.0 / np.sqrt(2.0 * snr_lin)  # AWGN 标准差

st.sidebar.metric("噪声标准差 σ_n", f"{noise_std:.4f}")

# 固定种子确保相同参数产生相同图形
rng = np.random.default_rng(42)
symbol_idx = rng.integers(0, len(constellation), size=num_symbols)
tx_symbols = constellation[symbol_idx]  # 发射符号（向量化索引）
# 复高斯噪声 = 实部噪声 + j*虚部噪声
noise = noise_std * (rng.standard_normal(num_symbols) + 1j * rng.standard_normal(num_symbols))
rx_symbols = tx_symbols + noise  # 接收符号

# ── 眼图数据构建（单条 trace + None 分隔，避免性能瓶颈） ──────────

samples_per_symbol = 20
eye_span = 2  # 每段覆盖 2 个符号周期
eye_len = eye_span * samples_per_symbol
baseband = np.repeat(rx_symbols.real, samples_per_symbol)  # I 分量上采样
t_eye = np.linspace(0, eye_span, eye_len)
num_segments = min(num_symbols // eye_span, 200)

eye_x: list = []
eye_y: list = []
for i in range(num_segments):
    start = i * samples_per_symbol
    if start + eye_len > len(baseband):
        break
    eye_x.extend(t_eye.tolist())
    eye_x.append(None)  # None 断开线段
    eye_y.extend(baseband[start:start + eye_len].tolist())
    eye_y.append(None)

# ── 图表：上星座图 + 下眼图 ──────────────────────────────────────

fig = make_subplots(
    rows=2, cols=1,
    row_heights=[0.55, 0.45],
    subplot_titles=["星座图 (I/Q)", "眼图 (I 分量)"],
    vertical_spacing=0.12,
)

# 上图 — 接收符号散点
fig.add_trace(go.Scatter(
    x=rx_symbols.real, y=rx_symbols.imag,
    mode="markers", name="接收符号",
    marker=dict(color="#636EFA", size=3, opacity=0.4),
), row=1, col=1)

# 上图 — 理想星座点（置于上层）
fig.add_trace(go.Scatter(
    x=constellation.real, y=constellation.imag,
    mode="markers", name="理想星座点",
    marker=dict(color="#EF553B", size=12, symbol="cross"),
), row=1, col=1)

fig.update_xaxes(title_text="I (同相)", row=1, col=1)
fig.update_yaxes(title_text="Q (正交)", scaleanchor="x", scaleratio=1, row=1, col=1)

# 下图 — 眼图
fig.add_trace(go.Scatter(
    x=eye_x, y=eye_y,
    mode="lines", name="眼图",
    line=dict(color="#636EFA", width=0.5),
    opacity=0.4,
), row=2, col=1)

fig.update_xaxes(title_text="符号周期", row=2, col=1)
fig.update_yaxes(title_text="幅值", row=2, col=1)

fig.update_layout(**LAYOUT_DEFAULTS, height=700, showlegend=True)
st.plotly_chart(fig, width="stretch", config=PLOTLY_CONFIG)

# ── 教学注释 ─────────────────────────────────────────────────────

st.info(
    "**星座图**展示 I/Q 平面上的符号分布，SNR 越高点越集中于理想位置；"
    "SNR 降低时噪声使符号扩散，判决区域重叠导致误码率上升。\n\n"
    "**眼图**将基带信号按符号周期叠加显示，「眼睛」张开越大说明抗噪声能力越强。"
)
