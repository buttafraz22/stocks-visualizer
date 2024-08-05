import numpy as np

def generate_bell_curve_data(mean, std_dev):
    """ Generates the data for the bell distribution according to 
        the Gaussian Distribution Formula.

        f(x | μ, σ²) = (1 / √(2πσ²)) * e^(-(x - μ)² / (2σ²))

        where:
        x   : the random variable
        μ   : mean of the distribution
        σ²  : variance of the distribution
    """
    if std_dev <= 0:
        std_dev = 1e-5  # Avoid division by zero or very small std_dev issues
    
    step = std_dev / 10
    if step <= 0:
        step = 1e-5  # Prevent step size from being zero or negative

    # Generate data using the corrected mean and std_dev
    x_values = np.arange(mean - 3 * std_dev, mean + 3 * std_dev, step)
    gaussian_values = (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-((x_values - mean) ** 2) / (2 * std_dev ** 2))

    return list(zip(x_values, gaussian_values))

def create_custom_tooltip(symbol_name, metric, value):
    return f"""<div style="width: 8rem; height: 4rem; display: flex; align-items: center; justify-content: center; box-shadow: 5px 5px 5px; font-family: 'Montserrat';">
        {symbol_name} <br/>
        {metric} deviation: {value:.2f}
        </div>""" # Placeholder for actual tooltip creation logic