import numpy as np
from babyyoda.util import loc, overflow, rebin, underflow


class HISTO2D_V2:
    def __init__(self, target):
        """
        target is either a yoda or grogu HISTO2D_V2
        """
        # Store the target object where calls and attributes will be forwarded
        super().__setattr__('target', target)

    ########################################################
    # Relay all attribute access to the target object
    ########################################################

    def __getattr__(self, name):
        # First, check if the Forwarder object itself has the attribute
        if name in self.__dict__ or hasattr(type(self), name):
            return object.__getattribute__(self, name)
        # If not, forward attribute access to the target
        elif hasattr(self.target, name):
            return getattr(self.target, name)
        raise AttributeError(f"'{type(self).__name__}' object and target have no attribute '{name}'")

    def __setattr__(self, name, value):
        # First, check if the attribute belongs to the Forwarder itself
        if name in self.__dict__ or hasattr(type(self), name):
            object.__setattr__(self, name, value)
        # If not, forward attribute setting to the target
        elif hasattr(self.target, name):
            setattr(self.target, name, value)
        else:
            raise AttributeError(f"Cannot set attribute '{name}'; it does not exist in target or Forwarder.")

    def __call__(self, *args, **kwargs):
        # If the target is callable, forward the call, otherwise raise an error
        if callable(self.target):
            return self.target(*args, **kwargs)
        raise TypeError(f"'{type(self.target).__name__}' object is not callable")


    ########################################################
    # YODA compatibility code (dropped legacy code?)
    ########################################################

    def xMins(self):
        return np.array(sorted(list(set([b.xMin() for b in self.bins()]))))
    
    def xMaxs(self):
        return np.array(sorted(list(set([b.xMax() for b in self.bins()])))) 

    def yMins(self):
        return np.array(sorted(list(set([b.yMin() for b in self.bins()]))))
    
    def yMaxs(self):
        return np.array(sorted(list(set([b.yMax() for b in self.bins()]))))

    def sumWs(self):
        return np.array([b.sumW() for b in self.bins()])

    ########################################################
    # Generic UHI code
    ########################################################

    @property
    def axes(self):
        return [
            list(zip(self.xMins(), self.xMaxs())),
            list(zip(self.yMins(), self.yMaxs())),
        ]

    @property
    def kind(self):
        return "COUNT"

    def values(self):
        return self.sumWs().reshape((len(self.axes[0]), len(self.axes[1])))

    def variances(self):
        return np.array([b.sumW2() for b in self.bins()]).reshape(
            (len(self.axes[0]), len(self.axes[1]))
        )

    def counts(self):
        return np.array([b.numEntries() for b in self.bins()]).reshape(
            (len(self.axes[0]), len(self.axes[1]))
        )

    
    def __single_index(self, ix, iy):
        return ix * len(self.axes[1]) + iy

    def __get_by_indices(self, ix, iy):
        return self.bin(self.__single_index(ix, iy))

    def __get_index_by_loc(self, loc, bins):
        # find the index in bin where loc is
        for a, b in bins:
            if a <= loc.value and loc.value < b:
                return bins.index((a, b))
        raise ValueError(f"loc {loc.value} is not in the range of {bins}")

    def __get_indices(self, slices):
        ix, iy = None, None
        if isinstance(slices[0], int):
            ix = slices[0]
        if isinstance(slices[0], loc):
            ix = self.__get_index_by_loc(slices[0], self.axes[0]) + slices[0].offset
        if isinstance(slices[1], int):
            iy = slices[1]
        if isinstance(slices[1], loc):
            iy = self.__get_index_by_loc(slices[1], self.axes[1]) + slices[1].offset
        return ix, iy

    def __getitem__(self, slices):
        # integer index
        if slices is underflow:
            raise TypeError("No underflow bin in 2D histogram")
        if slices is overflow:
            raise TypeError("No overflow bin in 2D histogram")
        if isinstance(slices, tuple):
            if len(slices) == 2:
                ix, iy = self.__get_indices(slices)
                return self.__get_by_indices(ix, iy)
        # TODO implement slice
        raise TypeError("Invalid argument type")

    def plot(self, *args, **kwargs):
        import mplhep as hep

        hep.hist2dplot(self, *args, **kwargs)

    def _ipython_display_(self):
        try:
            self.plot()
        except ImportError:
            pass
        return self