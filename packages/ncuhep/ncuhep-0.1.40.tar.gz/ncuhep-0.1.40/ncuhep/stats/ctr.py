import numpy as np
import matplotlib.pyplot as plt
from .histogram import Histogram
from iminuit import Minuit
from iminuit.cost import LeastSquares
from ..utils.unit import unit, unit_uncertainty
from .histogram import bisection
from scipy.interpolate import PchipInterpolator
from tqdm import tqdm
from numba import njit, prange
import concurrent.futures
from uncertainties import ufloat, nominal_value, std_dev
from uncertainties.umath import sqrt
from scipy.signal import fftconvolve
from matplotlib.ticker import AutoLocator, AutoMinorLocator



@njit
def signal(t, risetime, decaytime, lightyield):
    return (np.exp(-t/decaytime) - np.exp(-t/risetime)) / (decaytime - risetime) * lightyield

# @njit
# def signal_int(t, risetime, decaytime, lightyield):
#     x = np.linspace(0, t, 2000)
#     y = - np.trapz(signal(x, risetime, decaytime, lightyield), x)
#     return np.exp(y)

@njit
def signal_int(t, risetime, decaytime, lightyield):
    y = lightyield / (decaytime - risetime) * (risetime * np.exp(-t/risetime) - decaytime * np.exp(-t/decaytime) + decaytime - risetime)
    return np.exp(-y)


@njit
def sCTR_jit(t, risetime, decaytime, lightyield):
    return signal(t, risetime, decaytime, lightyield) * signal_int(t, risetime, decaytime, lightyield)

@njit
def sCTR(t, risetime, decaytime, lightyield):
    result = np.zeros(len(t))
    for i in range(len(t)):
        result[i] = sCTR_jit(t[i], risetime, decaytime, lightyield)
    
    return result



def model(x, dt, risetime, decaytime, lightyield):
    n = 0
    while True:
        n += 1
        val = n * np.amax(x)
        if sCTR_jit(val, risetime, decaytime, lightyield) < 1E-5:
            break

    t = np.linspace(0, n * np.amax(x), 10000)
    sctr = sCTR(t, risetime, decaytime, lightyield)

    ctr = fftconvolve(sctr, np.flip(sctr), "same")
    ct = t - np.mean(t)
    area = np.trapz(ctr, ct)


    try:
        ctr = PchipInterpolator(ct, ctr / area)(x - dt)
        ctr /= np.trapz(ctr, x)
    except:
        ctr = np.zeros(len(x))

    return ctr



class CTR(Histogram):
    def __init__(self, sample, bin_width, confidence_level=0.95, offset=True, bins=None, range=None):
        super().__init__(sample, bin_width, confidence_level, bins, range)
        self.sample_size = len(self.sample)
        
    def fit_FWHM(self, resolution):
        if not np.all(np.isfinite(self.y_fit)):
            self.fwhm = 0
            self.fwhm_error = 0
            self.fwhm_ufloat = ufloat(0, 0)
            return 0
        
        y = PchipInterpolator(self.x, self.y_fit)

        max_value = np.amax(self.y)
        half_max = max_value / 2

        peak_x = self.x[np.argmax(self.y)]

        min_x = np.amin(self.x)
        max_x = np.amax(self.x)

        left = bisection(self.x, y, half_max, resolution, min_x, peak_x)
        right = bisection(self.x, y, half_max, resolution, peak_x, max_x)

        self.risetime_ufloat = ufloat(self.risetime, self.risetime_error)
        self.decaytime_ufloat = ufloat(self.decaytime, self.decaytime_error)
        self.lightyield_ufloat = ufloat(self.lightyield, self.lightyield_error)

        factor = np.abs(right - left) / np.sqrt(self.risetime * self.decaytime / self.lightyield)
        
        
        self.fwhm_ufloat = factor * sqrt(self.risetime_ufloat * self.decaytime_ufloat / self.lightyield_ufloat)

        self.fwhm = nominal_value(self.fwhm_ufloat)
        self.fwhm_error = std_dev(self.fwhm_ufloat)

        return np.abs(right - left)

    def fit_worker(self):
        lsq = LeastSquares(self.x, self.y, self.e, model)
        m = Minuit(lsq,
                   dt=self.x[np.argmax(self.y)] * np.random.uniform(0.9, 1.1),
                   risetime=self.risetime,
                   decaytime=self.decaytime,
                   lightyield=self.lightyield * np.random.uniform(0.5, 1.5))

        m.strategy = 2
        m.limits["risetime"] = (1E-12, 10E-9)
        m.limits["decaytime"] = (20E-9, 300E-9)
        # m.limits['lightyield'] = (100, 100000)

        m.fixed['risetime'] = False
        m.fixed['decaytime'] = True
        m.fixed['lightyield'] = False

        m.simplex()
        m.migrad(iterate=100)
        try:
            m.minos()
        except:
            pass
        
        m.fixed['risetime'] = False
        m.fixed['decaytime'] = True
        m.fixed['lightyield'] = True

        m.simplex()
        m.migrad(iterate=100)
        try:
            m.minos()
        except:
            pass

        m.fixed['risetime'] = True
        m.fixed['decaytime'] = True
        m.fixed['lightyield'] = False

        m.simplex()
        m.migrad(iterate=100)

        try:
            m.minos()
        except:
            pass
        
        return m

    def fit(self, risetime, decaytime, lightyield, iterations=1, fwhm_resolution=1E-12):
        self.risetime = risetime
        self.decaytime = decaytime
        self.lightyield = lightyield


        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = []
            futures = [executor.submit(self.fit_worker) for _ in range(iterations)]

            for future in tqdm(concurrent.futures.as_completed(futures), total=iterations):
                results.append(future.result())
        
        results = np.array(results)
        mask = np.array([minuit.valid for minuit in results])
        m = results[mask]
        
        chi2 = [m.fval / (len(self.x) - len(m.values)) for m in results]
        m = results[np.argmin(chi2)]

        self.dt = m.values['dt']
        self.risetime = m.values['risetime']
        self.decaytime = m.values['decaytime']
        self.lightyield = m.values['lightyield']
        self.dt_error = m.errors['dt']
        self.risetime_error = m.errors['risetime']
        self.decaytime_error = m.errors['decaytime']
        self.lightyield_error = m.errors['lightyield']

        self.chi2 = m.fval / (len(self.x) - len(m.values))
        self.ndof = len(self.x) - len(m.values)

        self.y_fit = model(self.x, self.dt, self.risetime, self.decaytime, self.lightyield)
        self.fit_FWHM(fwhm_resolution)

    def fit_plot(self, resolution=160E-12, fill=False):
        plt.rcParams["font.family"] = "monospace"
        # plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Liberation Sans"]
        
        fit_info = [
            f'$\chi^2$\t      ${self.chi2:.3f}$\n',
            f'$\Delta t$ \t\t{unit_uncertainty(self.dt, self.dt_error, "s")}',
            f'Rise Time \t{unit_uncertainty(self.risetime, self.risetime_error, "s")}',
            f'Decay Time \t{unit_uncertainty(self.decaytime, self.decaytime_error, "s")}',
            f'Light Yield \t{unit_uncertainty(self.lightyield, self.lightyield_error, "ph")}\n',
            f'Model FWHM \t{unit_uncertainty(self.fwhm, self.fwhm_error, "s")}',
            f'Data FWHM \t{unit_uncertainty(self.dataFWHM, self.dataFWHMError, "s")}\n',
            f'Sample Size \t{int(self.sample_size)} $[Events]$',
            f"Time Scale \t{unit(resolution, 's/pt')}\n",
            f"Bin Width \t{unit(self.bin_width, 's')}",
            f"Poisson C.I. \t{self.confidence_level*100:.1f} [$\%$]\n",
        ]
      

        plt.errorbar(self.x, self.y, yerr=self.error_bound, fmt='o', label='Data', zorder=1, color='#2b2b2b')
        x = np.linspace(np.amin(self.x), np.amax(self.x), 1000)
        plt.plot(x, model(x, self.dt, self.risetime, self.decaytime, self.lightyield), label='Fit', zorder=2, color='#2b2b2b', linestyle='--',
                 linewidth=2)
        
        data_area = np.trapezoid(self.x, self.y)
        fit_area = np.trapezoid(x, model(x, self.dt, self.risetime, self.decaytime, self.lightyield))
        
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
            plt.fill_between(t, y_lower_bound, y_upper_bound, color='#a0a0a0', alpha=0.25)

        ax = plt.gca()
        ax.xaxis.set_major_locator(AutoLocator())
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_major_locator(AutoLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.tick_params(direction = 'in', length = 7, top = True, right = True)
        ax.tick_params(direction = 'in', length = 4, which = 'minor', top = True, right = True)
        plt.legend(title='\n'.join(fit_info), bbox_to_anchor=(1.11, 1.14), loc='upper right', borderaxespad=0.)
        plt.xlabel('Time Difference [s]')
        plt.ylabel('Probability Density')
        plt.grid(True)








