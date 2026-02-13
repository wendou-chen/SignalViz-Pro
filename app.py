import streamlit as st

st.set_page_config(
    page_title="SignalViz-Pro",
    page_icon="📡",
    layout="wide",
)

pages = {
    "基础理论": [
        st.Page("pages/fourier.py", title="傅里叶级数与吉布斯现象", icon="🔊"),
        st.Page("pages/sampling.py", title="采样定理与混叠", icon="📊"),
        st.Page("pages/convolution.py", title="卷积演示（翻转滑动）", icon="🔄"),
    ],
    "系统与控制": [
        st.Page("pages/laplace.py", title="拉普拉斯变换与系统稳定性", icon="🎛️"),
    ],
    "通信原理": [
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
