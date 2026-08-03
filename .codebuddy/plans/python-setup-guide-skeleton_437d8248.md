---
name: python-setup-guide-skeleton
overview: 为面向 HKU 新生的 Python 安装入门指南搭建纯静态 HTML 站点骨架（用于 GitHub Pages）：包含欢迎/目录落地页与覆盖 AGENTS.md 所有章节的占位 HTML 页面、共享样式、带说明的占位图，正文内容后续分批填充。
design:
  architecture:
    framework: html
    component: mui
  styleKeywords:
    - Documentation
    - Clean
    - Readable
    - Minimal
    - Responsive
  fontSystem:
    fontFamily: Open Sans
    heading:
      size: 28px
      weight: 700
    subheading:
      size: 20px
      weight: 600
    body:
      size: 16px
      weight: 400
  colorSystem:
    primary:
      - "#2563EB"
      - "#1E40AF"
    background:
      - "#FFFFFF"
      - "#F8FAFC"
    text:
      - "#1F2937"
      - "#6B7280"
    functional:
      - "#16A34A"
      - "#D97706"
      - "#DC2626"
      - "#2563EB"
todos:
  - id: setup-structure-style
    content: 创建目录结构与共享样式表 css/style.css（响应式、代码块、导航、占位图样式）
    status: completed
  - id: build-welcome-toc
    content: 编写 index.html 欢迎页：HKU 欢迎语、简介与带超链接的 TOC（标注可跳过章节）
    status: completed
    dependencies:
      - setup-structure-style
  - id: build-section-pages
    content: 编写五个章节骨架页并插入占位图与图注（unix/virtualenv/installation/ide/reading）
    status: completed
    dependencies:
      - setup-structure-style
  - id: update-readme-deploy
    content: 更新 readme.md 补充项目说明与 GitHub Pages 部署指引
    status: completed
    dependencies:
      - build-welcome-toc
      - build-section-pages
---

## 用户需求

基于 AGENTS.md，为 HKU 编程 bootcamp 新生（背景混合）制作一份 Python 环境安装入门教程，教程正文使用英文撰写，目标平台覆盖 arm64-macos、amd64-windows、x86_64-linux。

本轮已澄清的交付约束：

1. 本次只搭建**结构骨架与目录（TOC）**，各章节正文后续分批填充，不一次性写全。
2. 以**纯静态 HTML 文件**交付，直接用于 GitHub Pages 部署，不使用 Jekyll / MkDocs 等构建工具。
3. 内容范围仅为**结构 + 目录**，页面内用标题、占位段落与 TODO 注释预留正文位置。
4. 需要截图处使用**占位图 + 图注说明**（标注"此处放 XX 截图"），由用户后续补充真实图片。

## 产品概述

一个纯静态多页 HTML 教程站点：欢迎页提供 HKU 欢迎语、教程简介与带超链接的章节索引表（index table）；其余章节为各自独立的 HTML 页面，页面间通过相对路径互相跳转。部分章节标注"可跳过 / 非必读"。整体使用共享样式表，保持排版、配色、代码块与占位图风格统一。

## 核心功能

- 欢迎页（index.html）：HKU 欢迎语 + 教程简介 + 带超链接的 TOC（标注可跳过章节）
- 基础 Unix 类系统介绍骨架页（命令行、sudo、-h/--help、选项与参数、exe 差异、pwsh）
- 虚拟环境概念骨架页（uv / conda / anaconda / miniconda 差异，标注非必读）
- Python 安装骨架页（standalone / conda / uv 三种方式 × 三平台，含各平台下载 URL 占位）
- 编辑器 / IDE 配置骨架页（VSCode / Cursor / PyCharm / copilot 等）
- 推荐阅读骨架页（pep8 / lsp: ty,pyright / lint: ruff）
- 占位图组件：通用 SVG 占位图 + figure/figcaption 标注截图位置

## 技术栈

- 标记语言：纯 HTML5（无前端框架、无组件库）
- 样式：原生 CSS3，单一共享样式表 `css/style.css`
- 占位图：内联 / 独立 SVG 文件，不引入图片处理依赖
- 部署：GitHub Pages 直接托管仓库根目录静态文件，无需构建步骤
- 内容语言：教程正文英文；代码注释与 TODO 标记可用英文

## 实现方案

采用"静态多页站点 + 共享样式表"策略：根目录 `index.html` 作为欢迎页与导航中枢，各章节独立 HTML 置于 `pages/`，通过相对路径（如 `pages/unix-basics.html`）互链；共享 `css/style.css` 统一排版、配色、代码块与响应式布局。每个页面仅搭建语义化骨架（`<header>` 标题、`<nav>` 章节内导航、`<main>` 带 `id` 的小节标题、占位 `<p>`/`<pre>` 与 TODO 注释），不填充完整正文。截图位置用 `<figure><img src="assets/img/placeholder.svg"><figcaption>此处放 XX 截图</figcaption></figure>` 标注。

关键决策：

- 选纯静态 HTML 而非 Markdown/Jekyll：符合用户明确选择，零构建、易预览、易部署，且章节可独立成页便于分批写作。
- 欢迎页与章节分离而非单页长文档：TOC 超链接跳转体验更好，单个文件更短、易维护，符合 AGENTS.md "index table with hyperlink" 描述。
- 占位图用单一通用 SVG：避免引入二进制资源，用户后续替换为真实截图时只需改 `src`，图注已说明内容。

性能与可靠性：纯静态文件，无运行时依赖，首屏仅加载一个 CSS 与少量 SVG，体积可忽略；相对路径保证本地双击预览与 GitHub Pages 托管行为一致。

## 实现说明

- 正文撰写前先用 `<!-- TODO: ... -->` 注释与占位段落预留内容，保证后续填充不破坏结构。
- 可跳过 / 非必读章节在 TOC 与该页标题处加 `（Skippable）`/`（Optional）` 标注，沿用 AGENTS.md 标记。
- 各平台差异（macos/windows/linux）在 installation 页用带 `id` 的子标题分区，正文阶段再补表格式对比。
- 链接统一使用相对路径，避免本地预览失效；TOC 与各页底部"上一篇/下一篇"导航保持一致。
- 占位图统一引用 `assets/img/placeholder.svg`，`figcaption` 明确描述应补充的截图类型，避免后期歧义。
- 不改动 `azure-api-key.py` 与既有无关文件；`readme.md` 仅补充说明与部署指引。

## 架构设计

静态多页文档站点，无后端、无构建。导航关系：`index.html`（欢迎页 + TOC）为入口，链接到 `pages/` 下五个章节页；每个章节页含返回首页与相邻章节的相对链接。共享样式表被所有页面引用，保证视觉一致。结构层级简单，无需 Mermaid 图。

## 目录结构

```
python-setup-moodle/
├── index.html                  # [NEW] 欢迎页：HKU 欢迎语、教程简介、带超链接的 TOC（标注可跳过章节），底部部署/说明入口
├── css/
│   └── style.css               # [NEW] 共享样式表：基础排版、配色变量、响应式布局、代码块/表格样式、导航与占位图样式
├── pages/
│   ├── unix-basics.html        # [NEW] 基础 Unix 类系统介绍骨架：命令行/终端入口、sudo、-h/--help、选项与参数、exe 差异、pwsh 别名；含占位代码块与截图占位
│   ├── virtual-environment.html # [NEW] 虚拟环境概念骨架（标注 Optional）：uv/conda/anaconda/miniconda 差异、全局 vs 本地；占位对比表
│   ├── installation.html       # [NEW] Python 安装骨架：standalone/conda/uv 三法 × macos/windows/linux 三平台子章节，含官方下载 URL 占位与截图占位
│   ├── ide-setup.html          # [NEW] 编辑器/IDE 配置骨架：VSCode/Cursor/CodeBuddy/PyCharm + copilot 学生订阅；含配置截图占位
│   └── recommended-reading.html # [NEW] 推荐阅读骨架：pep8、lsp(ty/pyright)、lint(ruff)；占位链接列表
├── assets/
│   └── img/
│       └── placeholder.svg     # [NEW] 通用占位图（灰底 + "Screenshot Placeholder" 文字），供各页 figure 引用
└── readme.md                   # [MODIFY] 补充项目说明、目录结构、GitHub Pages 部署步骤（当前为空）
```

## 设计风格

采用现代、清爽的"技术文档（Documentation）"风格，以可读性为核心，兼顾教育场景的友好度。欢迎页与章节页统一视觉语言：顶部 sticky 导航栏显示站点名与章节入口，桌面端左侧固定章节内 TOC、右侧正文，移动端折叠为单栏；内容区使用卡片化小节块、充足留白与清晰层级。代码块采用深色背景+等宽字体并保留复制友好排版；占位图以圆角灰底块呈现，配浅色图注。整体交互克制：导航 hover 微高亮、章节锚点平滑滚动，避免花哨动效，确保初学者专注内容。

## 页面规划（仅结构骨架，正文占位）

- 欢迎页（index.html）：顶部品牌栏 → 欢迎语与简介块 → 带超链接的 TOC 索引表（标注 Skippable/Optional）→ 底部说明。
- 章节页（pages/*.html）：顶部返回首页导航 → 页面标题与"可跳过"标识 → 左侧/顶部章节内 TOC → 多个带 id 的小节块（标题+占位段落+占位代码块/截图）→ 底部上一篇/下一篇导航。每页至少含 4 个关键功能块。