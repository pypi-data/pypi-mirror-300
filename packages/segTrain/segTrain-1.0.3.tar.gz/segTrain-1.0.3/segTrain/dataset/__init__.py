from .dataset import Single_View, Single_View_HDF5
from torch.utils.data import DataLoader


def build_dataloader(data_path, isSingleClass, batch_size, num_workers=0):
    print(f"Loading data from : {data_path}")
    print(f"batch_size = {batch_size}")
    if data_path[-2:] == "h5":
        data = Single_View_HDF5(HDF5path=data_path)
        loader = DataLoader(data,
                            batch_size=batch_size,
                            num_workers=num_workers,
                            shuffle=True,
                            drop_last=True)
    else:
        data = Single_View(root_path=data_path, isSingleClass=isSingleClass)
        loader = DataLoader(data,
                            batch_size=batch_size,
                            num_workers=num_workers,
                            shuffle=True,
                            drop_last=True)
    print(f"data sizes : {len(data)}")
    print(f"data items : {len(loader)}")

    return loader
