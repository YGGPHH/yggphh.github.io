---
title: Git 工作流笔记
tags:
  - software-engineering
  - tools
---

这是一篇演示笔记，展示标签、代码高亮与 Obsidian 双链的渲染效果。正式写作后可删除。

## 常用命令

```bash
git switch -c feature/my-change   # 开新分支
git add -p                        # 按块暂存
git commit --amend                # 修正最近一次提交
```

## 小贴士

- 提交信息写清"为什么改"，而不是"改了什么"（diff 里能看到）
- rebase 个人分支保持线性历史，合并进主干用 merge commit 留痕

## 关联笔记

深度学习相关见 [[transformer-notes]]。
