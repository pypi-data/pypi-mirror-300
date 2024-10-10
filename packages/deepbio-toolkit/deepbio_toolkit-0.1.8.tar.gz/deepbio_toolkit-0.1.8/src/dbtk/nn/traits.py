import abc
import torch
from typing import Optional

class AttentionAttributionTransformerEncoderTrait(abc.ABC):
    """
    A computationally-efficient trait for transformer-based models
    to compute attention attribution.

    forward:
      1. pre-forward: input process before passing through transformer
      2. transformer-forward: transformer pass through
      3. post-forward: processing transformer output

    """

    def forward(self, *args, **kwargs):

        # pre-forward
        # transformer-forward
        # post-forward
        kwargs = self.pre_forward(*args, **kwargs)
        kwargs.update(self.transformer_forward(**kwargs))
        return self.post_forward(**kwargs)

    @abc.abstractmethod
    def pre_forward(
        self,
        src: torch.Tensor,
        src_mask: torch.Tensor,
        src_key_padding_mask: Optional[torch.Tensor] = None,
        attention_head_mask: Optional[torch.Tensor] = None,
        average_attention_weights: bool = True,
        return_attention_weights: bool = False
    ) -> dict:
        raise NotImplementedError()

    def transformer_forward(
        self,
        src,
        src_key_padding_mask: Optional[torch.Tensor]
    ):
        pass

    @abc.abstractmethod
    def post_forward(self, output):
        raise NotImplementedError()