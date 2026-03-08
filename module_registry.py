from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class PageMeta:
    group: str
    page_path: str
    title: str
    icon: str
    slug: str
    core_concepts: tuple[str, ...]
    question_types: tuple[str, ...]
    prerequisites: tuple[str, ...]
    status: str
    kind: str = "module"
    summary: str = ""


GROUP_ORDER = ["项目总览", "基础理论", "变换域分析", "系统与通信"]

GROUP_DESCRIPTIONS = {
    "基础理论": "先用时域与频域的基础直觉打牢信号分析能力。",
    "变换域分析": "从 s 域、z 域与频域工具出发，建立系统分析框架。",
    "系统与通信": "把系统性质与通信链路联系起来，形成工程视角。",
}

LEARNING_PATH_SLUGS = [
    "signal-ops",
    "fourier-series",
    "ctft",
    "sampling-aliasing",
    "convolution-sliding",
    "laplace-stability",
    "z-transform",
    "dft-fft",
    "bode-response",
    "lti-properties",
    "digital-modulation",
    "ofdm-orthogonality",
]

PAGE_REGISTRY: tuple[PageMeta, ...] = (
    PageMeta(
        group="项目总览",
        page_path="pages/project_overview.py",
        title="平台总览与知识地图",
        icon="🧭",
        slug="project-overview",
        core_concepts=("项目定位", "知识地图", "扩展准入"),
        question_types=("学习路径规划", "模块导航"),
        prerequisites=("无",),
        status="active",
        kind="overview",
        summary="以作品集视角展示平台结构、能力亮点与知识地图。",
    ),
    PageMeta(
        group="基础理论",
        page_path="pages/signal_ops.py",
        title="信号基本运算",
        icon="✏️",
        slug="signal-ops",
        core_concepts=("时移", "尺度变换", "信号叠加"),
        question_types=("波形变换题", "图像读图题"),
        prerequisites=("连续时间信号",),
        status="active",
        summary="把时移、翻转、尺度变换的图像规律可视化。",
    ),
    PageMeta(
        group="基础理论",
        page_path="pages/fourier.py",
        title="傅里叶级数与吉布斯现象",
        icon="🔊",
        slug="fourier-series",
        core_concepts=("谐波叠加", "奇次谐波", "吉布斯现象"),
        question_types=("周期信号展开题", "频谱理解题"),
        prerequisites=("三角函数", "周期信号"),
        status="active",
        summary="用谐波叠加解释方波逼近与约 9% 过冲。",
    ),
    PageMeta(
        group="基础理论",
        page_path="pages/ctft.py",
        title="连续时间傅里叶变换",
        icon="🌊",
        slug="ctft",
        core_concepts=("时频对偶", "带宽", "窗函数"),
        question_types=("傅里叶变换题", "时频对应题"),
        prerequisites=("积分", "复指数"),
        status="active",
        summary="观察典型连续信号在时域与频域之间的对应关系。",
    ),
    PageMeta(
        group="基础理论",
        page_path="pages/sampling.py",
        title="采样定理与混叠效应",
        icon="📊",
        slug="sampling-aliasing",
        core_concepts=("奈奎斯特准则", "混叠", "重建"),
        question_types=("采样判据题", "混叠分析题"),
        prerequisites=("正弦信号", "频率概念"),
        status="active",
        summary="比较连续信号、采样点与重建波形，直观看到混叠。",
    ),
    PageMeta(
        group="基础理论",
        page_path="pages/convolution.py",
        title="卷积演示 — 翻转滑动法",
        icon="🔄",
        slug="convolution-sliding",
        core_concepts=("卷积积分", "翻转平移", "重叠面积"),
        question_types=("卷积几何题", "系统响应题"),
        prerequisites=("积分", "LTI 基础"),
        status="active",
        summary="通过翻转滑动演示卷积积分的几何意义。",
    ),
    PageMeta(
        group="变换域分析",
        page_path="pages/laplace.py",
        title="拉普拉斯变换与系统稳定性",
        icon="🎛️",
        slug="laplace-stability",
        core_concepts=("极点位置", "冲激响应", "稳定性"),
        question_types=("拉普拉斯分析题", "稳定性判断题"),
        prerequisites=("复频域", "微分方程"),
        status="active",
        summary="把 s 平面极点位置和时域稳定性直接对应起来。",
    ),
    PageMeta(
        group="变换域分析",
        page_path="pages/z_transform.py",
        title="Z 变换与离散系统稳定性",
        icon="🔢",
        slug="z-transform",
        core_concepts=("单位圆", "极点模", "离散稳定性"),
        question_types=("Z 变换题", "离散稳定性题"),
        prerequisites=("离散时间信号", "复平面"),
        status="active",
        summary="通过单位圆与冲激响应包络理解离散系统稳定性。",
    ),
    PageMeta(
        group="变换域分析",
        page_path="pages/dft.py",
        title="DFT / FFT 频谱分析",
        icon="📈",
        slug="dft-fft",
        core_concepts=("窗函数", "频谱泄漏", "离散频谱"),
        question_types=("DFT 计算题", "频谱泄漏题"),
        prerequisites=("复数", "离散信号"),
        status="active",
        summary="对比时域采样参数与离散频谱分辨率之间的关系。",
    ),
    PageMeta(
        group="变换域分析",
        page_path="pages/bode.py",
        title="频率响应与 Bode 图",
        icon="📉",
        slug="bode-response",
        core_concepts=("幅频特性", "相频特性", "转折频率"),
        question_types=("Bode 图题", "频率响应题"),
        prerequisites=("拉普拉斯变换", "传递函数"),
        status="active",
        summary="统一展示极点零点、转折频率与幅相特性的联系。",
    ),
    PageMeta(
        group="系统与通信",
        page_path="pages/lti_properties.py",
        title="LTI 系统四大性质",
        icon="⚖️",
        slug="lti-properties",
        core_concepts=("线性性", "时不变性", "因果性", "BIBO 稳定性"),
        question_types=("系统判定题", "性质证明题"),
        prerequisites=("卷积", "系统定义"),
        status="active",
        summary="把 LTI 系统的四大性质拆成可交互验证的实验。",
    ),
    PageMeta(
        group="系统与通信",
        page_path="pages/modulation.py",
        title="数字调制与噪声",
        icon="📶",
        slug="digital-modulation",
        core_concepts=("星座图", "AWGN", "眼图"),
        question_types=("数字调制题", "误码分析题"),
        prerequisites=("概率基础", "复数表示"),
        status="active",
        summary="观察不同调制方式在噪声下的星座扩散与眼图开口。",
    ),
    PageMeta(
        group="系统与通信",
        page_path="pages/ofdm.py",
        title="OFDM 子载波正交性",
        icon="📡",
        slug="ofdm-orthogonality",
        core_concepts=("子载波间隔", "sinc 频谱", "ICI"),
        question_types=("OFDM 原理题", "正交条件题"),
        prerequisites=("傅里叶变换", "通信系统基础"),
        status="active",
        summary="通过 sinc 频谱重叠展示 OFDM 正交条件与载波间干扰。",
    ),
)


def get_grouped_pages() -> dict[str, list[PageMeta]]:
    grouped = {group: [] for group in GROUP_ORDER}
    for page in PAGE_REGISTRY:
        grouped[page.group].append(page)
    return grouped


def get_teaching_modules() -> tuple[PageMeta, ...]:
    return tuple(page for page in PAGE_REGISTRY if page.kind == "module")


def get_teaching_groups() -> list[str]:
    return [group for group in GROUP_ORDER if group != "项目总览"]


def get_question_types(modules: Iterable[PageMeta] | None = None) -> list[str]:
    selected_modules = modules if modules is not None else get_teaching_modules()
    seen: dict[str, None] = {}
    for module in selected_modules:
        for question_type in module.question_types:
            seen.setdefault(question_type, None)
    return list(seen.keys())


def filter_teaching_modules(
    groups: Iterable[str] | None = None,
    question_type: str | None = None,
) -> tuple[PageMeta, ...]:
    modules = get_teaching_modules()
    if groups:
        allowed_groups = set(groups)
        modules = tuple(module for module in modules if module.group in allowed_groups)
    if question_type and question_type != "全部":
        modules = tuple(
            module for module in modules if question_type in module.question_types
        )
    return modules


def build_module_rows(modules: Iterable[PageMeta] | None = None) -> list[dict[str, str]]:
    selected_modules = modules if modules is not None else get_teaching_modules()
    return [
        {
            "模块": module.title,
            "分组": module.group,
            "核心考点": " / ".join(module.core_concepts),
            "典型题型": " / ".join(module.question_types),
            "先修知识": " / ".join(module.prerequisites),
        }
        for module in selected_modules
    ]


def count_pages_by_group() -> dict[str, int]:
    grouped = get_grouped_pages()
    return {group: len(grouped[group]) for group in GROUP_ORDER}


def get_learning_path() -> tuple[PageMeta, ...]:
    page_by_slug = {page.slug: page for page in PAGE_REGISTRY}
    return tuple(page_by_slug[slug] for slug in LEARNING_PATH_SLUGS)
