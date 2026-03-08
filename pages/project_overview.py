# 文件用途：SignalViz-Pro 项目总览与知识地图页面
# 对应考点：项目定位、模块导航、题型映射、学习路径与扩展策略

import streamlit as st
import plotly.graph_objects as go

from module_registry import (
    GROUP_DESCRIPTIONS,
    build_module_rows,
    filter_teaching_modules,
    get_learning_path,
    get_question_types,
    get_teaching_groups,
)
from utils import LAYOUT_DEFAULTS, PLOTLY_CONFIG


NODE_COLORS = [
    "#636EFA",
    "#EF553B",
    "#00CC96",
    "#AB63FA",
    "#FFA15A",
    "#19D3F3",
    "#FF6692",
    "#B6E880",
]


def build_sankey_figure(selected_modules: tuple) -> go.Figure:
    domain_labels = list(dict.fromkeys(module.group for module in selected_modules))
    question_labels = get_question_types(selected_modules)
    module_labels = [module.title for module in selected_modules]
    labels = domain_labels + question_labels + module_labels
    label_index = {label: index for index, label in enumerate(labels)}

    domain_links: dict[tuple[str, str], int] = {}
    module_sources: list[int] = []
    module_targets: list[int] = []
    module_values: list[int] = []

    for module in selected_modules:
        for question_type in module.question_types:
            domain_links[(module.group, question_type)] = (
                domain_links.get((module.group, question_type), 0) + 1
            )
            module_sources.append(label_index[question_type])
            module_targets.append(label_index[module.title])
            module_values.append(1)

    sources = [label_index[source] for source, _ in domain_links] + module_sources
    targets = [label_index[target] for _, target in domain_links] + module_targets
    values = list(domain_links.values()) + module_values

    node_colors = [
        NODE_COLORS[index % len(NODE_COLORS)]
        for index in range(len(labels))
    ]

    fig = go.Figure(
        data=[
            go.Sankey(
                arrangement="snap",
                node=dict(
                    pad=18,
                    thickness=18,
                    line=dict(color="rgba(0,0,0,0.15)", width=0.5),
                    label=labels,
                    color=node_colors,
                ),
                link=dict(
                    source=sources,
                    target=targets,
                    value=values,
                    color="rgba(99,110,250,0.20)",
                ),
            )
        ]
    )
    fig.update_layout(**LAYOUT_DEFAULTS, height=560, title="知识域 → 题型 → 模块")
    return fig


def build_module_table(selected_modules: tuple) -> go.Figure:
    rows = build_module_rows(selected_modules)
    headers = ["模块", "分组", "核心考点", "典型题型", "先修知识"]
    cells = [[row[header] for row in rows] for header in headers]

    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=headers,
                    fill_color="#636EFA",
                    font=dict(color="white", size=13),
                    align="left",
                ),
                cells=dict(
                    values=cells,
                    fill_color="white",
                    align="left",
                    height=32,
                ),
            )
        ]
    )
    fig.update_layout(
        **LAYOUT_DEFAULTS,
        height=max(380, 120 + 34 * len(rows)),
        title="模块摘要表",
    )
    return fig


st.title("SignalViz-Pro 平台总览")
st.latex(r"\text{题型抽象} \rightarrow \text{可视化建模} \rightarrow \text{系统化平台}")

available_groups = get_teaching_groups()
selected_groups = st.sidebar.multiselect(
    "按知识域查看",
    available_groups,
    default=available_groups,
)
available_question_types = ["全部", *get_question_types()]
selected_question_type = st.sidebar.selectbox("按题型查看", available_question_types)

filtered_modules = filter_teaching_modules(selected_groups, selected_question_type)

st.sidebar.metric("教学模块数", len(filtered_modules))
st.sidebar.metric("覆盖题型数", len(get_question_types(filtered_modules)))
st.sidebar.metric("覆盖知识域", len({module.group for module in filtered_modules}))

col1, col2, col3 = st.columns(3)
col1.metric("当前教学模块", len(filtered_modules))
col2.metric("平台总分组", len(available_groups))
col3.metric("推荐学习阶段", len(get_learning_path()))

st.markdown(
    "SignalViz-Pro 现在定位为**复试作品集型教育可视化平台**："
    "既展示你对信号与系统、通信原理核心考点的抽象能力，"
    "也展示你把多个独立实验整理成可扩展系统的工程能力。"
)

st.markdown("### 能力亮点")
st.markdown(
    "- **系统能力**：统一入口、多分组导航、共享 Plotly 配置与模块注册表。\n"
    "- **建模能力**：把公式、参数、现象转化为可操作的交互实验。\n"
    "- **扩展能力**：后续新增内容按题型抽象，不再盲目按单题堆页面。"
)

st.markdown("### 三大知识域")
for group, description in GROUP_DESCRIPTIONS.items():
    st.markdown(f"- **{group}**：{description}")

if filtered_modules:
    sankey_fig = build_sankey_figure(filtered_modules)
    st.plotly_chart(sankey_fig, width="stretch", config=PLOTLY_CONFIG)

    table_fig = build_module_table(filtered_modules)
    st.plotly_chart(table_fig, width="stretch", config=PLOTLY_CONFIG)
else:
    st.warning("当前筛选条件下没有模块，请调整知识域或题型筛选。")

st.markdown("### 推荐学习顺序")
learning_path = get_learning_path()
for index, module in enumerate(learning_path, start=1):
    st.markdown(f"{index}. **{module.title}** — {module.summary}")

st.markdown("### 后续扩展规则（简版）")
st.markdown(
    "- 只有当一个主题能覆盖**至少 3 类题型**时，才考虑升级为独立模块。\n"
    "- 必须具备**1 个核心公式**、**2 个以上有效交互参数**、**1 个以上可观察现象**。\n"
    "- 若只是某道题的特殊技巧，先记入题型笔记，不直接新建页面。"
)

st.info(
    "这页不是新增教学模块，而是平台首页：它把模块分布、题型覆盖、学习顺序和扩展机制集中展示，"
    "帮助你把项目从多个 demo 升级为可持续迭代的教育系统。"
)
