import streamlit as st

st.set_page_config(
    page_title="SignalViz-Pro",
    page_icon="📡",
    layout="wide",
)

pages = {
    "基础理论": [
        st.Page("pages/signal_ops.py", title="信号基本运算", icon="✏️"),
        st.Page("pages/fourier.py", title="傅里叶级数与吉布斯现象", icon="🔊"),
        st.Page("pages/ctft.py", title="连续时间傅里叶变换", icon="🌊"),
        st.Page("pages/sampling.py", title="采样定理与混叠", icon="📊"),
        st.Page("pages/convolution.py", title="卷积演示（翻转滑动）", icon="🔄"),
    ],
    "变换域分析": [
        st.Page("pages/laplace.py", title="拉普拉斯变换与系统稳定性", icon="🎛️"),
        st.Page("pages/z_transform.py", title="Z 变换与离散系统稳定性", icon="🔢"),
        st.Page("pages/dft.py", title="DFT / FFT 频谱分析", icon="📈"),
        st.Page("pages/bode.py", title="频率响应与 Bode 图", icon="📉"),
    ],
    "系统与通信": [
        st.Page("pages/lti_properties.py", title="LTI 系统四大性质", icon="⚖️"),
        st.Page("pages/modulation.py", title="数字调制与噪声", icon="📶"),
        st.Page("pages/ofdm.py", title="OFDM 正交性", icon="📡"),
    ],
}

pg = st.navigation(pages)

# 侧边栏共享品牌信息
st.sidebar.markdown("### 📡 SignalViz-Pro")
st.sidebar.markdown("考研信号与系统交互式可视化复习台")
st.sidebar.divider()

pg.run()
