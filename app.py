import streamlit as st

from module_registry import GROUP_ORDER, count_pages_by_group, get_grouped_pages, get_teaching_modules

st.set_page_config(
    page_title="SignalViz-Pro",
    page_icon="📡",
    layout="wide",
)

grouped_pages = get_grouped_pages()
pages = {
    group: [
        st.Page(page.page_path, title=page.title, icon=page.icon)
        for page in grouped_pages[group]
    ]
    for group in GROUP_ORDER
}

page_counts = count_pages_by_group()

pg = st.navigation(pages)

# 侧边栏共享品牌信息
st.sidebar.markdown("### 📡 SignalViz-Pro")
st.sidebar.markdown("复试作品集型信号与系统交互式可视化平台")
st.sidebar.metric("教学模块", len(get_teaching_modules()))
st.sidebar.metric("导航分组", len(GROUP_ORDER))
for group in GROUP_ORDER:
    st.sidebar.caption(f"{group}：{page_counts[group]} 页")
st.sidebar.divider()

pg.run()
