from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from typing import Dict, List, Optional, Union

class Chart(ABC):
    """Wrapper for general charts"""

    @abstractmethod
    def __init__(
        self,
        data: np.ndarray,
        data_vmin: Optional[Union[int, float, None]] = None,
        data_vmax: Optional[Union[int, float, None]] = None,
        colors: Optional[Union[List, Dict, None]] = None,
    ):

        if not data_vmin:
            data_vmin = data.min()
        if not data_vmax:
            data_vmax = data.max()
        norm = plt.Normalize(vmin=data_vmin, vmax=data_vmax)

        # create color map, one for each chart
        if colors:
            if isinstance(colors, dict):
                self.cmap = LinearSegmentedColormap('cmap', colors, N=256)
            elif isinstance(colors, list):
                self.cmap = LinearSegmentedColormap.from_list('cmap', colors, N=256)
            self.__sm = plt.cm.ScalarMappable(cmap=self.cmap, norm=norm)
        else:
            self.cmap = None

        # create chart figure and axis
        self.fig, self.ax = plt.subplot()

class PieChart(Chart):

    def __init__(self):
        super().__init__()
