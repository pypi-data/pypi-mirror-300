def register_pandas_handler():
    def is_dataframe(obj):
        try:
            import pandas as pd

            return isinstance(obj, pd.DataFrame)
        except ImportError:
            return False

    from .pandas_handler import DataFrameHandler
    from .snapshot_handler import SnapshotHandlerRegistry

    SnapshotHandlerRegistry.add_handler(is_dataframe, DataFrameHandler)


def register_numpy_handler():
    def is_numpy(obj):
        try:
            import numpy as np

            return isinstance(obj, np.ndarray)
        except ImportError:
            return False

    from .numpy_handler import NumpyHandler
    from .snapshot_handler import SnapshotHandlerRegistry

    SnapshotHandlerRegistry.add_handler(is_numpy, NumpyHandler)
