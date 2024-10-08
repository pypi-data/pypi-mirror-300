import torch

from TorchImager import Window

tc = torch.rand(3, 256, 256)
tg = torch.rand(256, 256)

with Window(256, 256, "color", 4) as window:
	window.show(tc)