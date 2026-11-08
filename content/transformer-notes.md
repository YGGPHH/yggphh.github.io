---
title: Transformer 笔记
tags:
  - deep-learning
  - paper-notes
---

这是一篇演示笔记，展示数学公式、代码高亮与 Obsidian 双链的渲染效果。正式写作后可删除。

## 注意力机制

缩放点积注意力：

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V
$$

其中 $d_k$ 是键向量的维度，除以 $\sqrt{d_k}$ 用于防止点积过大导致 softmax 梯度消失。

## 代码示例

```python
import torch
import torch.nn as nn

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model: int, n_heads: int):
        super().__init__()
        self.attn = nn.MultiheadAttention(d_model, n_heads, batch_first=True)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out, _ = self.attn(x, x, x)
        return out
```

## 关联笔记

工程实践见 [[git-notes]]。
