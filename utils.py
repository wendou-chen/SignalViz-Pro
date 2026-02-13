# Plotly 共享样式配置

# 工具栏按钮配置
PLOTLY_CONFIG = {
    "displayModeBar": True,
    "displaylogo": False,
    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
}

# 统一布局默认值 — 中文字体回退链
LAYOUT_DEFAULTS = dict(
    template="plotly_white",
    font=dict(
        family="SimHei, Microsoft YaHei, Noto Sans SC, sans-serif",
        size=14,
    ),
    hovermode="x unified",
    margin=dict(l=60, r=30, t=50, b=50),
)
