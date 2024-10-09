import torch
class Model(torch.nn.Sequential):
    """
    1. model with device param for device automatic adaptation.
    2. model with save and load method for model persistence.
    3. model with param_num property for model parameter count.
    4. model with output property for forward output.
    """
    
    def __init__(self, *layers):
        """
        init model with layers.
        """
        super().__init__()
        for idx, module in enumerate(layers):
            self.add_module(f'layer{idx}', module)
        
    def forward(self, x):
        """
        forward pass

        Args:
            x (Tensor): input tensor

        Returns:
            Tensor: output tensor
        """
        self.output = super().forward(x)
        return self.output

    #region device
    @ property
    def device(self):
        return next(self.parameters()).device
    #endregion

    #region param count
    @ property
    def param_num(self):
        params = list(self.parameters())
        k = 0
        for i in params:
            l = 1
            for j in i.size():
                l *= j
            k = k + l
        return k
    #endregion

class Dataset(torch.utils.data.Dataset):

    #region iterable
    def __iter__(self):
        self.iter_count = -1
        return self

    def __next__(self):
        self.iter_count += 1
        if self.iter_count >= len(self):
            raise StopIteration
        return self[self.iter_count]
    #endregion

    def get_loader(self, batch_size=4, shuffle=True):
        return torch.utils.data.DataLoader(self, batch_size=batch_size, shuffle=shuffle)