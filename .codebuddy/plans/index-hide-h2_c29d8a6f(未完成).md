---
name: index-hide-h2
overview: "修改 css/style.css，使 index 页面（body[data-md=\"index.md\"]）不再单独展示 markdown 渲染出的 ## 标题列表，正文段落保留。"
todos:
  - id: hide-index-h2
    content: "在 css/style.css 追加 body[data-md=\"index.md\"] .markdown h2 { display:none; } 隐藏首页 ## 标题"
    status: pending
---

## 用户需求

修改 CSS，使 index 首页不再单独展示由 Markdown 渲染出的 `##` 标题列表。

## 产品概述

index 首页由 `index.html` + `index.md` 渲染：顶部 hero 区、中间 `#content`（渲染 index.md 正文）、下方 `#tochome` 章节卡片网格（由 render.js 自动生成）。当前 index.md 含两个 `##` 标题，被渲染为 `<h2>` 单独显示在正文区，与下方自动生成的章节卡片视觉重复。

## 核心功能

- 在 index 页面隐藏 markdown 渲染出的 `##`（`<h2>`）标题，仅保留其下方正文段落。
- 不影响 pages/*.html 各章节页的正常 `##` 标题展示。
- 不影响 `#tochome` 章节卡片网格的生成与显示。

## 技术栈

- 纯静态站点：HTML + CSS + 原生 JS（marked + DOMPurify CDN）
- 样式表：`css/style.css`（已有完整设计令牌与暗色主题）

## 实现方案

通过 CSS 选择器精确命中 index 页面（`body[data-md="index.md"]`），隐藏其 `#content` 内由 markdown `##` 生成的 `<h2>` 元素。正文 `<p>` 段落保留显示，章节卡片 `#tochome` 由 JS 独立生成不受此规则影响。

关键决策：

- 使用属性选择器 `body[data-md="index.md"]` 而非额外 class，复用 render.js 已写入的 `data-md` 属性，零侵入、不改动 HTML/JS/MD。
- 仅隐藏 `h2` 而非整个 `#content`，正文说明文字（CPython 说明、Why learn this、How to use this guide）仍可见，符合历史"留下正文，不要标题"约定。
- 暗色主题通过 `@media` 与 `html[data-theme="dark"]` 两套选择器实现，新增的隐藏规则与主题无关（display:none 不受变量影响），无需在暗色块重复声明。

## 实现注意

- 该规则应加在 `.markdown h2` 通用样式（第 110 行附近）之后，确保特异性足够覆盖。
- 不影响 `.sidebar`、`.toc-grid`、`.pager` 等其它组件。
- 改动仅一处 CSS 规则，完全可逆。

## 架构设计

无架构变动。仅为样式层追加一条页面级作用域规则，符合现有"按 body[data-md] 区分页面"的既有模式（render.js 已用此属性区分首页/章节页）。

## 目录结构

```
css/
└── style.css   # [MODIFY] 在 .markdown h2 规则后新增：body[data-md="index.md"] .markdown h2 { display: none; }
```

仅修改此一个文件，不触及 index.md / index.html / render.js / site.js。

## 关键代码结构

无需新增类型或接口。新增 CSS 规则：

```css
/* Hide markdown ## headings on the index/home page (content shown as plain intro,
   chapter list is rendered separately by #tochome). */
body[data-md="index.md"] .markdown h2 { display: none; }
```