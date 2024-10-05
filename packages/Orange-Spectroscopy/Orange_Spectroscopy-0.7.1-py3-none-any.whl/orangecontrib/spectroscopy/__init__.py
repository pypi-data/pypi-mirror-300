import Orange.data
import os.path


# Remove this when we require Orange 3.34
if not hasattr(Orange.data.Table, "get_column"):
    def get_column(self, column):
        col, _ = self.get_column_view(column)
        if self.domain[column].is_primitive():
            col = col.astype(float)
        return col

    Orange.data.Table.get_column = get_column

from . import io  # register file formats


def get_sample_datasets_dir():
    thispath = os.path.dirname(__file__)
    dataset_dir = os.path.join(thispath, 'datasets')
    return os.path.realpath(dataset_dir)


Orange.data.table.dataset_dirs.append(get_sample_datasets_dir())


try:
    import dask
    import dask.distributed
    dask_client = dask.distributed.Client(processes=False, n_workers=2,
                                          set_as_default=False,
                                          dashboard_address=None)
except ImportError:
    dask = None
    dask_client = None