import numpy as np
import matplotlib.pyplot as plt 
from .histogram import Histogram
from iminuit import Minuit
from iminuit.cost import LeastSquares
from ..utils.unit import unit, unit_uncertainty
from .histogram import bisection
from scipy.interpolate import PchipInterpolator
from tqdm import tqdm
import concurrent.futures
from numba import njit


@njit
def model(x, dt, risetime, decaytime, A, c):
    return A * (np.exp(-(x - dt) / decaytime) - np.exp(-(x - dt) / risetime)) + c


class Signal(Histogram):
    def __init__(self, sample, bin_width=None, confidence_level=0.95, bins=None):
        super().__init__(sample, bin_width, confidence_level, bins)
        self.sample_size = len(self.sample)
    
    def fit_worker(self):
        lsq = LeastSquares(self.x, self.y, 0.1 * np.amax(self.y), model)
        m = Minuit(lsq, 
                   dt=np.random.uniform(np.min(self.x), 0.01 * np.max(self.x)),
                   risetime=self.risetime * np.random.normal(1, 0.1),
                   decaytime=self.decaytime * np.random.normal(1, 0.1),
                   A=np.random.normal(1, 0.1) * np.max(self.sample),
                   c=np.random.normal(1, 0.1) * np.min(self.sample))
        
        m.limits["dt"] = (0, None)
        m.limits["risetime"] = (0, None)
        m.limits["decaytime"] = (0, None)
        m.limits["A"] = (0, None)

        m.migrad()
        m.hesse()
        
        return m
    
    def fit(self, risetime, decaytime):
        self.risetime = risetime
        self.decaytime = decaytime
            
        num_tasks = 100
        
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = []
            futures = [executor.submit(self.fit_worker) for _ in range(num_tasks)]

            for future in tqdm(concurrent.futures.as_completed(futures), total=num_tasks):
                results.append(future.result())
                
        chi2 = [m.fval / (len(self.x) - len(m.values)) for m in results]
        
        m = results[np.argmin(chi2)]
        
        self.dt = m.values['dt']
        self.risetime = m.values['risetime']
        self.decaytime = m.values['decaytime']
        self.A = m.values['A']
        self.c = m.values['c']
        self.dt_error = m.errors['dt']
        self.risetime_error = m.errors['risetime']
        self.decaytime_error = m.errors['decaytime']
        self.A_error = m.errors['A']
        self.c_error = m.errors['c']
        
        lsq = LeastSquares(self.x, self.y, self.e, model)
        m = Minuit(lsq, dt=self.dt, risetime=self.risetime, decaytime=self.decaytime, A=self.A, c=self.c)
        m.hesse()
        self.chi2 = m.fval / (len(self.x) - len(m.values))
        self.ndof = len(self.x) - len(m.values)

        self.y_fit = model(self.x, self.dt, self.risetime, self.decaytime, self.A, self.c)
        
        pass
    
    def fit_plot(self, units="", xlabel=""):
        plt.rcParams["font.family"] = "monospace"
        plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Liberation Sans"]


        fit_info = [
            f'$\chi^2$\t      ${self.chi2:.3f}$\n',
            f'Drift Time \t{unit_uncertainty(self.dt, self.dt_error, units)}',
            f'Rise Time \t{unit_uncertainty(self.risetime, self.risetime_error, units)}',
            f'Decay Time \t{unit_uncertainty(self.decaytime, self.decaytime_error, units)}',
            f'Amplitude \t{unit_uncertainty(self.A, self.A_error, units)}',
            f'Constant \t{unit_uncertainty(self.c, self.c_error, units)}\n',
            f'FWHM \t\t{unit(self.fit_FWHM(1E-12), units)}',
            f'Sample Size \t{int(self.sample_size)} $[Events]$\n',
        ]
        
        plt.errorbar(self.x, self.y, yerr=self.e, fmt='o', label='Data', zorder=1, color='black')
        x = np.linspace(np.amin(self.x), np.amax(self.x), 1000)
        plt.plot(x, model(x, self.dt, self.risetime, self.decaytime, self.A, self.c), label='Fit', zorder=2, color='black', linestyle='--', linewidth=2)
        plt.legend(title='\n'.join(fit_info), bbox_to_anchor=(1.11, 1.14), loc='upper right', borderaxespad=0.)
        plt.ylabel('Probability Density')
        plt.xlabel(xlabel)
        plt.grid(True)


    def fit_FWHM(self, resolution):
        y = PchipInterpolator(self.x, self.y_fit)

        max_value = np.amax(self.y)
        half_max = max_value / 2

        peak_x = self.x[np.argmax(self.y)]

        min_x = np.amin(self.x)
        max_x = np.amax(self.x)

        left = bisection(self.x, y, half_max, resolution, min_x, peak_x)
        right = bisection(self.x, y, half_max, resolution, peak_x, max_x)

        return np.abs(right - left)
   


