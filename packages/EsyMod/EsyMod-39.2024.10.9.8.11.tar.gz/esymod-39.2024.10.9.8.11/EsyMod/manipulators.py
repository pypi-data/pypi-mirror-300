import torch
from torch.nn import Flatten, Unflatten, Identity
from . import Model


class View(torch.nn.Module):
    def __init__(self, *shape):
        super().__init__()
        self.shape = shape

    def forward(self, x):
        id = 0
        shape = []
        for s in self.shape:
            if s == -1:
                shape.append(x.size(id))
                id += 1
            else:
                shape.append(s)
        return x.view(*shape)

class PadUnflatten(Model):
    def __init__(self, dim, size):
        """
        unflatten a dim to size, pad if not match
        """
        super().__init__()
        self.dim = dim
        self.size = size
        self.ideal_size = torch.tensor(size).cumprod(0)[-1].item()
    
    def forward(self, x):
        if not x.size(self.dim) == self.ideal_size:
            pad_size = self.ideal_size - x.size(self.dim)
            if self.dim == -1:
                pad = torch.zeros(*x.size()[:self.dim], pad_size, device=x.device)
            else:
                pad = torch.zeros(*x.size()[:self.dim], pad_size, *x.size()[self.dim+1:], device=x.device)
            x = torch.cat([x, pad], dim=self.dim)
        return torch.unflatten(x, self.dim, self.size)

    
#region math
class SUM(Model):
    def __init__(self, *routes):
        super().__init__(*routes)
        self.routes = routes

    def manipulate(self, x1, x2):
        return x1 + x2

    def forward(self, x):
        rs = [route(x) for route in self.routes]
        result = rs[0]
        for r in rs[1:]:
            result = self.manipulate(result, r)
        self.output = result
        return result


class Multiply(SUM):
    def manipulate(self, x1, x2):
        return x1 * x2


class MatrixMultiply(Multiply):
    def manipulate(self, x1, x2):
        return x1 @ x2


class Exp(torch.nn.Module):
    def forward(self, x):
        return torch.exp(x)
#endregion
