from torch import nn

from jcopdl.layers.base import BaseBlock


class LinearBlock(BaseBlock):
    """
    available activation {relu, lrelu, sigmoid, tanh, elu, selu, lsoftmax, None}
    """
    def __init__(self, n_input, n_output, activation="relu", batchnorm=False, dropout=0):
        super().__init__()
        self.block = nn.Sequential()
        self.block.add_module("linear", nn.Linear(n_input, n_output))

        if batchnorm:
            self.append_batchnorm(n_output)

        self.append_activation(activation)

        if dropout > 0:
            self.append_dropout(dropout)

    def forward(self, x):
        return self.block(x)


class ConvBlock(BaseBlock):
    """
    available activation {relu, lrelu, sigmoid, tanh, elu, selu, lsoftmax, None}
    available pool_type {maxpool, avgpool, None}
    """
    def __init__(self, in_channel, out_channel, kernel=3, stride=1, pad=1, bias=True, activation="relu",
                 batchnorm=False, dropout=0, pool=None, pool_kernel=2, pool_stride=2):
        super().__init__()
        self.block = nn.Sequential()
        self.block.add_module("conv2d", nn.Conv2d(in_channel, out_channel, kernel, stride, pad, bias=bias))

        if batchnorm:
            self.append_batchnorm2d(out_channel)

        self.append_activation(activation)

        if dropout > 0:
            self.append_dropout2d(dropout)

        self.append_pooling2d(pool, pool_kernel, pool_stride)

    def forward(self, x):
        return self.block(x)


class TConvBlock(BaseBlock):
    def __init__(self, in_channel, out_channel, kernel=3, stride=1, pad=1, bias=True, activation="relu",
                 batchnorm=False, dropout=0, pool=None, pool_kernel=2, pool_stride=2):
        super().__init__()
        self.block = nn.Sequential()
        self.block.add_module("tconv2d", nn.ConvTranspose2d(in_channel, out_channel, kernel, stride, pad, bias=bias))

        if batchnorm:
            self.append_batchnorm2d(out_channel)

        self.append_activation(activation)

        if dropout > 0:
            self.append_dropout2d(dropout)

        self.append_pooling2d(pool, pool_kernel, pool_stride)

    def forward(self, x):
        return self.block(x)


def linear_block(n_in, n_out, activation='relu', batch_norm=False, dropout=0.):
    """
    Linear + Act
    """    
    return LinearBlock(n_in, n_out, activation, batch_norm, dropout)


def conv_block(c_in, c_out, kernel=3, stride=1, pad=1, bias=True, activation='relu', batch_norm=False, dropout=0,
               pool_type='maxpool', pool_kernel=2, pool_stride=2):
    """
    Conv + Act + Pool
    """
    return ConvBlock(c_in, c_out, kernel, stride, pad, bias, activation, batch_norm, dropout, pool_type, pool_kernel,
                     pool_stride)


def tconv_block(c_in, c_out, kernel=4, stride=2, pad=1, bias=True, activation='relu', batch_norm=False, dropout=0,
                pool_type=None, pool_kernel=2, pool_stride=2):
    """
    TConv + Act + Pool
    """    
    return TConvBlock(c_in, c_out, kernel, stride, pad, bias, activation, batch_norm, dropout, pool_type, pool_kernel,
                      pool_stride)


def conv_relu_block(c_in, c_out, kernel=3, stride=1, pad=1, bias=True, activation='relu', batch_norm=False, dropout=0):
    """
    Conv + Act
    """
    return ConvBlock(c_in, c_out, kernel, stride, pad, bias, activation, batch_norm, dropout, pool=None)
