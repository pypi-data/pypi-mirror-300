from xsigmamodules.Util import datetimeHelper
from xsigmamodules.util.numpy_support import xsigmaToNumpy, numpyToXsigma

# Attempt to import numpy and handle the case where it's not installed
try:
    import numpy as np
except ImportError:
    print("Numpy (http://numpy.scipy.org) not found.")
    print("This test requires numpy!")
    Testing.skip()

# Attempt to import matplotlib and handle the case where it's not installed
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Matplotlib (http://matplotlib.org) not found.")
    print("This test requires matplotlib!")
    Testing.skip()


def convert_dates_to_fraction(valuation_date, dates, convention):
    """
    Convert a list of dates to fractional years based on a given day count convention.

    Parameters:
    - valuation_date: The base date for the conversion.
    - dates: List of dates to be converted.
    - convention: The day count convention to be used for the conversion.

    Returns:
    - np_array: Numpy array of fractional years.
    """
    np_array = np.zeros(len(dates))
    for i in range(len(dates)):
        np_array[i] = convention.fraction(valuation_date, dates[i])
    return np_array


def plot_params(
    x, np_array1, np_array2, title, xlabel, ylabel, legend, legend_2, num_factor
):
    """
    Plot parameters with the given data and labels.

    Parameters:
    - x: X-axis data.
    - np_array1: First set of Y-axis data arrays.
    - np_array2: Second set of Y-axis data arrays.
    - title: Title of the plot.
    - xlabel: Label for the X-axis.
    - ylabel: Label for the Y-axis.
    - legend: List of legends for the first set of data.
    - legend_2: List of legends for the second set of data.
    - num_factor: Number of factors (subplots).
    """
    for i in range(num_factor):
        if np_array1.size == 0:
            print("No data available for np_array1")
        else:
            plt.plot(x, np_array1[i], ".-", label=legend[i])
        if np_array2.size == 0:
            print("No data available for np_array2")
        else:
            plt.plot(x, np_array2[i], ".-", label=legend_2[i], dashes=[6, 2])
        plt.legend(loc="lower right")
        plt.title(title)
        plt.grid(True, which="both")
        plt.axhline(y=0, color="k")
        plt.axvline(x=0, color="k")
        plt.xlim(np.min(x), np.max(x))
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.show()
    return 0


def markov_test(a, b):
    """
    Perform Markov test on the given inputs.

    Parameters:
    - a: First input array.
    - b: Second input array.

    Returns:
    - Average of the product of the inputs, with b exponentiated.
    """
    z = xsigmaToNumpy(a) * np.exp(xsigmaToNumpy(b))
    return np.average(z)


def mm_test(a):
    """
    Calculate the average of the given input array.

    Parameters:
    - a: Input array.

    Returns:
    - Average of the input array.
    """
    return np.average(xsigmaToNumpy(a))


def average(a):
    """
    Calculate the average of the given input array.

    Parameters:
    - a: Input array.

    Returns:
    - Average of the input array.
    """
    return np.average(xsigmaToNumpy(a))


def average_product(a, b):
    """
    Calculate the average of the product of two input arrays.

    Parameters:
    - a: First input array.
    - b: Second input array.

    Returns:
    - Average of the product of the input arrays.
    """
    return np.average(xsigmaToNumpy(a) * xsigmaToNumpy(b))


def simulation_dates(start_date, tenor, size):
    """
    Generate a list of simulation dates starting from a given date with a specific tenor.

    Parameters:
    - start_date: The starting date.
    - tenor: The tenor to add for each subsequent date.
    - size: The number of dates to generate.

    Returns:
    - sim_dates: List of generated simulation dates.
    """
    sim_dates = [start_date]
    date_0 = start_date
    for _ in range(size):
        date_0 = datetimeHelper.add_tenor(date_0, tenor)
        sim_dates.append(date_0)
    return sim_dates


def simulation_dates_from_tenors(start_date, tenors):
    """
    Generate a list of simulation dates starting from a given date based on a list of tenors.

    Parameters:
    - start_date: The starting date.
    - tenors: List of tenors to add for each subsequent date.

    Returns:
    - sim_dates: List of generated simulation dates.
    """
    sim_dates = [start_date]
    for tenor in tenors:
        date_0 = datetimeHelper.add_tenor(start_date, tenor)
        sim_dates.append(date_0)
    return sim_dates
