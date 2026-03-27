import torch
import torch.nn as nn


class BCELossWithLogits(nn.Module):
	def __init__(self):
		super().__init__()
		self.loss = nn.BCEWithLogitsLoss()

	def forward(self, logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
		return self.loss(logits, targets)
















