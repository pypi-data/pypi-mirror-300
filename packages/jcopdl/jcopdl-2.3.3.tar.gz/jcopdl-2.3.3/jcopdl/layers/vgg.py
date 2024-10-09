from torch import nn
from jcopdl.layers.block import conv_relu_block


class VGGEncoder(nn.Module):
    """
    Create a bottleneck style encoder like the one in VGG model family.
    - vgg11
    model = VGGEncoder([3, 64, 128, 256, 512, 512], [1, 1, 2, 2, 2])
    - vgg13
    model = VGGEncoder([3, 64, 128, 256, 512, 512], 2)
    - vgg16 
    model = VGGEncoder([3, 64, 128, 256, 512, 512], [2, 2, 3, 3, 3])
    - vgg19
    model = VGGEncoder([3, 64, 128, 256, 512, 512], [2, 2, 4, 4, 4])

    set batch_norm=True to use batch normalization
    model = VGGEncoder([3, 64, 128, 256, 512, 512], [2, 2, 4, 4, 4], batch_norm=True)
    """
    def __init__(self, channels, n_convs=2, batch_norm=True, adaptive_avg_pool=True, avg_pool_size=(7, 7)):
        super().__init__()
        if isinstance(n_convs, int):
            n_convs = [n_convs] * (len(channels) - 1)
        assert len(channels) == len(n_convs) + 1

        blocks = []
        for c_in, c_out, n_repeat in zip(channels[:-1], channels[1:], n_convs):
            blocks.extend([
                conv_relu_block(c_in, c_out, batch_norm=batch_norm),
                *[conv_relu_block(c_out, c_out, batch_norm=batch_norm) for _ in range(n_repeat - 1)],
                 nn.MaxPool2d(2, 2)
            ])
        self.features = nn.Sequential(*blocks)
        self.avg_pool = nn.AdaptiveAvgPool2d(avg_pool_size)
        self.adaptive_avg_pool = adaptive_avg_pool

    def forward(self, x):
        x = self.features(x) 
        if self.adaptive_avg_pool:
            x = self.avg_pool(x)
        return x
