---
name: index-hide-toc-list
overview: "修改 css/style.css 隐藏 index 页面由 render.js buildToc 生成的「1. python version / 2. Why learn this...」有序列表（位于 #toc），同时保留 markdown 渲染出的 ## 标题（如「Why learn this when AI agents can code for you?」）显示。"
todos:
  - id: hide-toc-list
    content: "在 css/style.css 追加 body[data-md=\"index.md\"] #toc { display:none; } 隐藏首页 ol 列表"
    status: completed
  - id: 0204ae65
    content: 颜色样式不变的情况下配色主题改成港大主题色#005A33
    status: completed
---

## 用户需求

保留 index 首页 markdown 渲染出的 ## 标题（如「Why learn this when AI agents can code for you?」「python version」），同时隐藏下方由 render.js buildToc 注入的「1. python version / 2. Why learn this...」有序列表。

## 产品概述

index 首页由 hero 区 + #content（index.md 正文）+ #toc（被 buildToc 替换为 ol）+ #tochome（章节卡片网格）组成。当前 #toc 元素视觉上呈现为「1. python version / 2. Why learn this...」的有序列表，需通过 CSS 在首页作用域内隐藏。

## 核心功能

- 首页隐藏 #toc（即 buildToc 生成的 ol 列表）。
- 首页 markdown 渲染的 ## 标题（h2）保留显示，正文段落保留显示。
- #tochome 章节卡片网格不受影响。
- 章节页 pages/*.html 内部 sidebar TOC 不受影响（其结构不通过 #toc 渲染）。

## Tech Stack

- 纯静态站点：HTML + CSS + 原生 JS（marked + DOMPurify CDN）
- 样式表：css/style.css（已含完整设计令牌与暗色主题）

## 实现方案

通过 CSS 属性选择器精确命中首页，隐藏 #toc 元素：

```css
body[data-md="index.md"] #toc { display: none; }
```

关键决策：

- 选择 `body[data-md="index.md"] #toc` 而非通用 .markdown h2：#toc 是被 buildToc 替换的 ol 容器，与 markdown 渲染的 h2 是两个独立 DOM 路径。隐藏 #toc 不会影响 #content 内的 ## 标题。
- 使用 display:none 而非 visibility:hidden：彻底从布局流中移除，避免占位空白。
- 复用 render.js 已写入的 body[data-md] 属性，零侵入、不改 HTML/JS/MD。
- 暗色主题下 display:none 同样生效，无需重复声明。

## 实现注意

- 仅在 style.css 末尾追加一条规则，位置独立、互不影响。
- 不修改 index.md、index.html、render.js、site.js。
- 改动完全可逆：删除该规则即可恢复。
- 不会影响 render.js 中 postProcess 对 h1/h2/h3 的 id 生成与侧栏 TOC 构建逻辑。