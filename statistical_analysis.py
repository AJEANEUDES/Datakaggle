import powerlaw
from scipy import stats
import warnings
warnings.simplefilter(action='ignore', category=RuntimeWarning)

def fit_power_law(data):
    """Fit power law to data and return the fit object"""
    return powerlaw.Fit(data, discrete=True, estimate_discrete=False)

def test_distributions(data):
    """Test various distributions against the data using KS test"""
    cdfs = [
        "norm", "alpha", "anglit", "arcsine", "beta", "betaprime", "bradford", "burr",
        # ... (rest of distributions)
    ]
    
    results = []
    for cdf in cdfs:
        parameters = eval(f"stats.{cdf}.fit(data)")
        D, p = stats.kstest(data, cdf, args=parameters)
        results.append({'distribution': cdf, 'p_value': p, 'D_statistic': D})
    
    return results