import numpy as np
import scipy.stats as stats
from scipy.interpolate import PchipInterpolator
import matplotlib.pyplot as plt


class Histogram:
    def __init__(self, sample, bin_width=None, confidence_level=0.95, bins=None, range=None):

        assert len(sample) > 0
        assert confidence_level > 0
        assert confidence_level < 1
        if range is not None:
            assert type(range) == tuple
            assert len(range) == 2
            assert range[0] < range[1]

        if bin_width is None and bins is None:
            raise ValueError("Either bin_width or bins must be specified")
        elif bin_width is not None and bins is not None:
            raise ValueError("Only one of bin_width or bins must be specified")
        elif bin_width is not None:
            pass
        else:
            bin_width = (np.amax(sample) - np.amin(sample)) / bins

        if range is not None:
            sample = sample[(sample > range[0]) & (sample < range[1])]

        self.sample = sample
        self.range = range
        self.bin_width = bin_width
        self.confidence_level = confidence_level
        if range is not None:
            self.bins = int((range[1] - range[0]) // bin_width + 1)
        else:
            self.bins = int((np.amax(sample) - np.amin(sample)) // bin_width + 1)

        if self.range is not None:
            self.__min = self.range[0] // bin_width - 1
        else:
            self.__min = np.amin(sample) // bin_width - 1

        self.__shift = self.__min * bin_width + bin_width / 2
        self.__shifted_sample = sample - self.__shift
        self.__center_adjustment = bin_width/2 - np.mean(self.__shifted_sample) % bin_width
        self.__shifted_sample += self.__center_adjustment
        self.__shift -= self.__center_adjustment

        self._x, self._y = self.__bin(self.__shifted_sample, bin_width, self.bins)
        
        self.FWHM((self.x[1] - self.x[0]) / 1E4)

    def __bin(self, sample, bin_width, bins):
        assert bin_width > 0
        assert bins > 0
        assert type(bins) == int
        assert type(bin_width) in [int, float, np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64, np.float16, np.float32, np.float64]

        x = np.linspace(0, bins * bin_width, bins + 1, endpoint=True)
        y = np.zeros(bins + 1)

        for s in sample:
            index = int((s // bin_width))
            if index >= bins:  # Ensure index is within bounds
                index = bins - 1
            y[index] += 1

        return x, y

    @property
    def x(self):
        return self._x + self.__shift + self.bin_width / 2

    @x.setter
    def x(self, value):
        self._x = value - self.__shift - self.bin_width / 2

    @property
    def y(self):
        area = -np.trapezoid(self.x, self._y)

        return self._y / area
    
    @y.setter
    def y(self, value):
        self._y = value

    @property
    def e(self):
        area = -np.trapezoid(self.x, self._y)
        return self.error_estimate(self._y) / area
    
    @property
    def error_bound(self):
        lower_bound = []
        upper_bound = []
        for i in range(len(self._y)):
            lower, upper = self.poisson_confidence_interval(self._y[i])
            if not np.isfinite(lower):
                lower = 0
            if not np.isfinite(upper):
                upper = 0
            lower_bound.append(self._y[i] - lower)
            upper_bound.append(upper - self._y[i])
        return np.array([lower_bound, upper_bound]) / (np.sum(self._y) * self.bin_width)
    
    @property
    def counts(self):
        return self._y

    @property
    def counts_error(self):
        return self.error_estimate(self._y)

    def poisson_confidence_interval(self, k):
        alpha = 1 - self.confidence_level
        lower_bound = 0.5 * stats.chi2.ppf(alpha / 2, 2 * k)
        upper_bound = 0.5 * stats.chi2.ppf(1 - alpha / 2, 2 * (k + 1))

        if type(k) == np.ndarray:
            lower_bound[k == 0] = 0
        return lower_bound, upper_bound
    
    def error_estimate(self, k):
        lower_bound, upper_bound = self.poisson_confidence_interval(k)
        return (upper_bound - lower_bound) / 2

    
    def FWHM(self, resolution):
        y = PchipInterpolator(self.x, self.y)
        e_lower = PchipInterpolator(self.x, self.y - self.error_bound[0])
        e_upper = PchipInterpolator(self.x, self.y + self.error_bound[1])
        
        max_value = np.amax(self.y)
        half_max = max_value / 2

        peak_x = self.x[np.argmax(self.y)]

        min_x = np.amin(self.x)
        max_x = np.amax(self.x)

        left = bisection(self.x, y, half_max, resolution, min_x, peak_x)
        right = bisection(self.x, y, half_max, resolution, peak_x, max_x)
        
        left_gradient = (y(left + resolution) - y(left - resolution)) / (2 * resolution)
        right_gradient = (y(right + resolution) - y(right - resolution)) / (2 * resolution)
        
        left_error = e_upper(left) - e_lower(left)
        right_error = e_upper(right) - e_lower(right)
        
        left_uncertainty = left_error / left_gradient
        right_uncertainty = right_error / right_gradient
        
        uncertainty = np.sqrt(left_uncertainty ** 2 + right_uncertainty ** 2)
        
        self.dataFWHM = np.abs(right - left)
        self.dataFWHMError = uncertainty
        
        return np.abs(right - left)
    
    def plot(self, **kwargs):
        
        x = self.x if 'x' not in kwargs else kwargs.pop('x')
        
        plt.rcParams["font.family"] = "monospace"
        
        plt.errorbar(x=self.x, 
                     y=self.y,
                     yerr=self.error_bound,
                     fmt="s" if "fmt" not in kwargs else kwargs.pop("fmt"),
                     color='black' if "color" not in kwargs else kwargs.pop("color"), 
                     zorder=1 if "zorder" not in kwargs else kwargs.pop("zorder"),
                     markerfacecolor='none' if "markerfacecolor" not in kwargs else kwargs.pop("markerfacecolor"),
                     label="Data" if "label" not in kwargs else kwargs.pop("label"),
                     linestyle='none' if "linestyle" not in kwargs else kwargs.pop("linestyle"),
                     markersize=2 if "markersize" not in kwargs else kwargs.pop("markersize"))


        fill = False if "fill" not in kwargs else kwargs.pop("fill")
        
        t = np.linspace(np.amin(self.x), np.amax(self.x), 1000)

        try:
            y_lower_bound = PchipInterpolator(self.x, self.y - self.error_bound[0])(t)
        except:
            y_lower_bound = np.zeros(len(t))

        try:
            y_upper_bound = PchipInterpolator(self.x, self.y + self.error_bound[1])(t)
        except:
            y_upper_bound = np.zeros(len(t))


        if fill:
            plt.fill_between(t, y_lower_bound, y_upper_bound, color='#808080', alpha=0.25)


        plt.grid(True)
    
    def plot_unnormalized(self, **kwargs):
            
            x = self.x if 'x' not in kwargs else kwargs.pop('x')
            
            plt.rcParams["font.family"] = "monospace"
            
            plt.errorbar(x=self.x, 
                        y=self._y,
                        yerr=self.error_estimate(self._y),
                        fmt="s" if "fmt" not in kwargs else kwargs.pop("fmt"),
                        color='black' if "color" not in kwargs else kwargs.pop("color"), 
                        zorder=1 if "zorder" not in kwargs else kwargs.pop("zorder"),
                        markerfacecolor='none' if "markerfacecolor" not in kwargs else kwargs.pop("markerfacecolor"),
                        label="Data" if "label" not in kwargs else kwargs.pop("label"),
                        linestyle='none' if "linestyle" not in kwargs else kwargs.pop("linestyle"),
                        markersize=2 if "markersize" not in kwargs else kwargs.pop("markersize"))
            
            fill = False if "fill" not in kwargs else kwargs.pop("fill")
            
            t = np.linspace(np.amin(self.x), np.amax(self.x), 1000)
    
            try:
                y_lower_bound = PchipInterpolator(self.x, self._y - self.error_estimate(self._y)[0])(t)
            except:
                y_lower_bound = np.zeros(len(t))
    
            try:
                y_upper_bound = PchipInterpolator(self.x, self._y + self.error_estimate(self._y)[1])(t)
            except:
                y_upper_bound = np.zeros(len(t))
    
    
            if fill:
                plt.fill_between(t, y_lower_bound, y_upper_bound, color='#808080', alpha=0.25)
    
    
            plt.grid(True)
        
        
    def show(self):
        plt.legend()
        plt.show()
        
        
def bisection(x, y, value, tolerance, left, right):
    assert len(x) > 1
    assert tolerance > 0

    if right - left <= tolerance:
        return (left + right) / 2

    mid = (left + right) / 2

    if y(mid) < value < y(right) or y(mid) > value > y(right):
        return bisection(x, y, value, tolerance, mid, right)
    else:
        return bisection(x, y, value, tolerance, left, mid)


if __name__ == '__main__':
    sample = np.random.normal(0, 1, 10000)
    hist = Histogram(sample, 1)
    hist.plot(label='Data 1')
    hist.show()
    print(hist.FWHM(1e-5))
