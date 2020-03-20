# The MIT License (MIT)
#
# Copyright (c) 2018 Computer Assisted Medical Interventions Group, DKFZ
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import numpy as np
import matplotlib.pylab as plt


class AbsorptionSpectrum(object):
    """
    An instance of this class represents the absorption spectrum over wavelength for a particular
    """

    def __init__(self, spectrum_name: str, wavelengths: np.ndarray, absorption_per_centimeter: np.ndarray):
        """
        @param spectrum_name:
        @param wavelengths:
        @param absorption_per_centimeter:
        """
        self.spectrum_name = spectrum_name
        self.wavelengths = wavelengths
        self.absorption_per_centimeter = absorption_per_centimeter

        if np.shape(wavelengths) != np.shape(absorption_per_centimeter):
            raise ValueError("The shape of the wavelengths and the absorption coefficients did not match: " +
                             str(np.shape(wavelengths)) + " vs " + str(np.shape(absorption_per_centimeter)))

    def get_absorption_over_wavelength(self):
        return np.asarray([self.wavelengths, self.absorption_per_centimeter])

    def get_absorption_for_wavelength(self, wavelength: float) -> float:
        """
        @param wavelength: the wavelength to retrieve a optical absorption value for [cm^{-1}].
        @return: the best matching linearly interpolated absorption value for the given wavelength.
        """
        # TODO: behavior outside of the available wavelength range?
        if wavelength > max(self.wavelengths):
            raise ValueError("Given wavelength is larger than the maximum available wavelength")
        if wavelength < min(self.wavelengths):
            raise ValueError("Given wavelength is smaller than the minimum available wavelength")

        return np.interp(wavelength, self.wavelengths, self.absorption_per_centimeter)


class AbsorptionSpectrumLibrary(object):

    def __init__(self):
        self.spectra = [
            AbsorptionSpectrum("Deoxyhemoglobin", np.arange(450, 1001, 1), np.asarray([553.0, 444.0, 335.0, 265.0, 194.0, 179.0, 164.0, 152.0, 139.0, 132.0, 125.0, 119.0, 112.0, 108.0, 103.0, 100.0, 97.1, 94.2, 91.2, 88.8, 86.5, 84.2, 82.0, 81.3, 80.6, 79.9, 79.2, 78.9, 78.5, 78.2, 77.9, 78.8, 79.7, 80.6, 81.5, 82.3, 83.2, 84.2, 85.1, 87.2, 89.3, 91.4, 93.5, 95.7, 97.8, 99.9, 102.0, 104.0, 107.0, 109.0, 112.0, 114.0, 117.0, 120.0, 122.0, 125.0, 127.0, 130.0, 133.0, 135.0, 138.0, 141.0, 144.0, 147.0, 150.0, 154.0, 157.0, 160.0, 163.0, 166.0, 169.0, 173.0, 176.0, 180.0, 184.0, 188.0, 192.0, 197.0, 201.0, 205.0, 209.0, 213.0, 217.0, 221.0, 225.0, 229.0, 233.0, 237.0, 241.0, 245.0, 249.0, 254.0, 258.0, 262.0, 266.0, 270.0, 275.0, 278.0, 281.0, 284.0, 286.0, 288.0, 290.0, 291.0, 292.0, 292.0, 292.0, 291.0, 290.0, 289.0, 288.0, 284.0, 280.0, 275.0, 271.0, 266.0, 261.0, 256.0, 251.0, 246.0, 241.0, 237.0, 232.0, 228.0, 223.0, 219.0, 215.0, 210.0, 206.0, 202.0, 198.0, 195.0, 191.0, 187.0, 184.0, 180.0, 176.0, 171.0, 166.0, 159.0, 152.0, 144.0, 136.0, 129.0, 121.0, 113.0, 106.0, 98.7, 91.3, 85.0, 78.6, 75.8, 72.9, 70.1, 67.3, 64.5, 61.7, 58.9, 56.1, 53.3, 50.6, 48.3, 46.0, 43.8, 41.6, 40.4, 39.3, 38.2, 37.1, 36.0, 34.9, 34.0, 33.2, 32.4, 31.6, 30.9, 30.1, 29.4, 28.7, 28.2, 27.6, 27.0, 26.4, 25.9, 25.3, 25.0, 24.6, 24.3, 24.0, 23.6, 23.3, 22.9, 22.6, 22.2, 21.9, 21.6, 21.2, 20.9, 20.7, 20.4, 20.1, 19.8, 19.5, 19.2, 18.9, 18.6, 18.4, 18.1, 17.8, 17.5, 17.3, 17.0, 16.8, 16.6, 16.4, 16.1, 15.9, 15.7, 15.4, 15.2, 15.0, 14.7, 14.5, 14.3, 14.1, 13.9, 13.7, 13.5, 13.3, 13.1, 12.9, 12.7, 12.5, 12.3, 12.1, 11.9, 11.7, 11.5, 11.3, 11.2, 11.0, 10.9, 10.7, 10.6, 10.4, 10.3, 10.2, 10.0, 9.89, 9.75, 9.61, 9.47, 9.32, 9.18, 9.04, 8.9, 8.75, 8.62, 8.48, 8.36, 8.25, 8.13, 8.02, 7.9, 7.79, 7.67, 7.56, 7.44, 7.33, 7.21, 7.1, 6.99, 6.88, 6.77, 6.66, 6.55, 6.45, 6.31, 6.17, 6.04, 5.9, 5.9, 5.9, 5.9, 5.9, 5.9, 5.9, 5.9, 5.89, 5.93, 5.98, 6.1, 6.22, 6.34, 6.47, 6.62, 6.78, 6.96, 7.14, 7.33, 7.52, 7.82, 8.11, 8.19, 8.26, 8.31, 8.36, 8.36, 8.36, 8.32, 8.29, 8.18, 8.08, 7.95, 7.82, 7.68, 7.55, 7.42, 7.29, 7.16, 7.02, 6.89, 6.76, 6.63, 6.5, 6.36, 6.23, 6.1, 5.97, 5.86, 5.76, 5.65, 5.55, 5.44, 5.34, 5.23, 5.13, 5.03, 4.94, 4.85, 4.77, 4.69, 4.6, 4.52, 4.44, 4.37, 4.3, 4.24, 4.19, 4.13, 4.08, 4.03, 3.98, 3.97, 3.95, 3.93, 3.91, 3.89, 3.87, 3.86, 3.84, 3.83, 3.81, 3.8, 3.78, 3.77, 3.76, 3.74, 3.73, 3.72, 3.71, 3.71, 3.71, 3.71, 3.71, 3.71, 3.71, 3.71, 3.71, 3.71, 3.71, 3.71, 3.71, 3.71, 3.71, 3.71, 3.71, 3.71, 3.71, 3.71, 3.71, 3.71, 3.71, 3.71, 3.71, 3.7, 3.7, 3.7, 3.7, 3.7, 3.7, 3.7, 3.7, 3.7, 3.7, 3.7, 3.7, 3.7, 3.71, 3.71, 3.72, 3.72, 3.73, 3.73, 3.74, 3.74, 3.75, 3.75, 3.76, 3.77, 3.78, 3.79, 3.8, 3.81, 3.82, 3.83, 3.85, 3.86, 3.87, 3.88, 3.89, 3.9, 3.91, 3.92, 3.93, 3.94, 3.94, 3.95, 3.96, 3.97, 3.98, 3.99, 4.0, 4.01, 4.02, 4.03, 4.04, 4.05, 4.06, 4.07, 4.08, 4.09, 4.1, 4.1, 4.11, 4.12, 4.12, 4.13, 4.13, 4.14, 4.15, 4.15, 4.16, 4.16, 4.17, 4.17, 4.17, 4.17, 4.16, 4.16, 4.16, 4.16, 4.16, 4.16, 4.16, 4.15, 4.14, 4.12, 4.11, 4.1, 4.09, 4.06, 4.03, 3.99, 3.95, 3.91, 3.87, 3.83, 3.79, 3.75, 3.71, 3.67, 3.63, 3.59, 3.54, 3.48, 3.43, 3.38, 3.33, 3.28, 3.22, 3.17, 3.12, 3.09, 3.05, 3.01, 2.97, 2.93, 2.89, 2.85, 2.81, 2.78, 2.74, 2.69, 2.65, 2.59, 2.53, 2.48, 2.42, 2.36, 2.3, 2.26, 2.22, 2.19, 2.15, 2.12, 2.08, 2.05, 2.01, 1.97, 1.93, 1.88, 1.84, 1.8, 1.76, 1.72, 1.68, 1.64, 1.6, 1.56, 1.52, 1.48, 1.43, 1.39, 1.35, 1.31, 1.27, 1.23, 1.19, 1.15, 1.11])),
            AbsorptionSpectrum("Oxyhemoglobin", np.arange(450, 1001, 1), np.asarray([336.0, 326.0, 315.0, 301.0, 287.0, 276.0, 265.0, 260.0, 254.0, 246.0, 238.0, 230.0, 221.0, 217.0, 213.0, 206.0, 199.0, 193.0, 187.0, 182.0, 178.0, 174.0, 169.0, 165.0, 161.0, 158.0, 154.0, 151.0, 148.0, 146.0, 143.0, 140.0, 138.0, 136.0, 135.0, 133.0, 132.0, 131.0, 129.0, 128.0, 127.0, 125.0, 124.0, 122.0, 120.0, 119.0, 117.0, 115.0, 114.0, 113.0, 112.0, 111.0, 110.0, 110.0, 109.0, 108.0, 107.0, 107.0, 107.0, 107.0, 107.0, 108.0, 108.0, 109.0, 109.0, 111.0, 112.0, 116.0, 121.0, 125.0, 130.0, 136.0, 142.0, 149.0, 157.0, 165.0, 174.0, 183.0, 193.0, 203.0, 214.0, 224.0, 235.0, 243.0, 251.0, 259.0, 266.0, 272.0, 277.0, 281.0, 285.0, 285.0, 285.0, 282.0, 279.0, 273.0, 267.0, 258.0, 250.0, 240.0, 230.0, 221.0, 212.0, 205.0, 197.0, 191.0, 185.0, 182.0, 179.0, 177.0, 175.0, 175.0, 175.0, 178.0, 182.0, 189.0, 195.0, 205.0, 215.0, 227.0, 238.0, 251.0, 263.0, 274.0, 285.0, 291.0, 297.0, 295.0, 293.0, 281.0, 268.0, 250.0, 232.0, 209.0, 185.0, 164.0, 142.0, 124.0, 106.0, 91.5, 77.1, 66.6, 56.1, 48.6, 41.1, 35.8, 30.4, 27.3, 24.1, 20.6, 17.1, 15.7, 14.3, 12.8, 11.4, 10.5, 9.58, 9.2, 8.82, 8.44, 8.06, 7.69, 7.31, 6.93, 6.55, 6.25, 5.94, 5.72, 5.49, 5.27, 5.04, 4.82, 4.59, 4.37, 4.14, 3.97, 3.79, 3.66, 3.53, 3.4, 3.27, 3.14, 3.01, 2.87, 2.74, 2.65, 2.56, 2.51, 2.47, 2.42, 2.37, 2.32, 2.27, 2.22, 2.17, 2.13, 2.09, 2.06, 2.03, 2.0, 1.97, 1.94, 1.91, 1.88, 1.85, 1.82, 1.79, 1.77, 1.74, 1.73, 1.71, 1.7, 1.68, 1.67, 1.65, 1.64, 1.62, 1.61, 1.6, 1.59, 1.57, 1.56, 1.55, 1.54, 1.53, 1.52, 1.51, 1.5, 1.5, 1.49, 1.49, 1.48, 1.48, 1.47, 1.47, 1.47, 1.46, 1.47, 1.47, 1.47, 1.48, 1.48, 1.49, 1.49, 1.5, 1.5, 1.51, 1.52, 1.53, 1.54, 1.55, 1.56, 1.57, 1.59, 1.6, 1.61, 1.62, 1.64, 1.65, 1.67, 1.68, 1.7, 1.71, 1.73, 1.74, 1.76, 1.78, 1.8, 1.82, 1.84, 1.86, 1.88, 1.91, 1.93, 1.95, 1.97, 1.99, 2.02, 2.04, 2.06, 2.09, 2.11, 2.14, 2.16, 2.18, 2.21, 2.24, 2.28, 2.32, 2.35, 2.39, 2.42, 2.46, 2.5, 2.53, 2.57, 2.61, 2.65, 2.69, 2.73, 2.77, 2.81, 2.86, 2.9, 2.94, 2.97, 3.01, 3.04, 3.07, 3.11, 3.14, 3.17, 3.2, 3.23, 3.27, 3.3, 3.33, 3.37, 3.41, 3.44, 3.48, 3.52, 3.55, 3.59, 3.63, 3.66, 3.69, 3.72, 3.75, 3.77, 3.8, 3.83, 3.86, 3.89, 3.91, 3.94, 3.96, 3.98, 4.01, 4.03, 4.05, 4.07, 4.09, 4.11, 4.13, 4.17, 4.21, 4.27, 4.32, 4.35, 4.37, 4.4, 4.43, 4.46, 4.48, 4.5, 4.52, 4.55, 4.58, 4.61, 4.63, 4.65, 4.67, 4.69, 4.71, 4.73, 4.75, 4.79, 4.83, 4.87, 4.91, 4.94, 4.98, 5.02, 5.06, 5.09, 5.12, 5.14, 5.17, 5.19, 5.22, 5.24, 5.26, 5.29, 5.31, 5.34, 5.36, 5.39, 5.42, 5.44, 5.47, 5.5, 5.53, 5.56, 5.58, 5.6, 5.62, 5.63, 5.64, 5.65, 5.67, 5.68, 5.69, 5.7, 5.71, 5.73, 5.74, 5.77, 5.8, 5.82, 5.85, 5.87, 5.9, 5.92, 5.95, 5.97, 5.99, 6.0, 6.01, 6.03, 6.04, 6.05, 6.07, 6.08, 6.09, 6.11, 6.12, 6.13, 6.15, 6.16, 6.18, 6.19, 6.21, 6.22, 6.24, 6.25, 6.27, 6.28, 6.29, 6.3, 6.31, 6.32, 6.33, 6.34, 6.35, 6.36, 6.37, 6.38, 6.39, 6.4, 6.42, 6.43, 6.44, 6.45, 6.46, 6.47, 6.48, 6.48, 6.49, 6.49, 6.5, 6.51, 6.51, 6.52, 6.53, 6.53, 6.54, 6.54, 6.55, 6.55, 6.55, 6.56, 6.56, 6.57, 6.57, 6.57, 6.57, 6.56, 6.56, 6.55, 6.54, 6.54, 6.53, 6.52, 6.52, 6.51, 6.51, 6.51, 6.51, 6.5, 6.5, 6.5, 6.5, 6.49, 6.49, 6.49, 6.48, 6.47, 6.46, 6.46, 6.45, 6.44, 6.43, 6.42, 6.41, 6.4, 6.39, 6.38, 6.37, 6.36, 6.35, 6.34, 6.33, 6.32, 6.31, 6.3, 6.28, 6.27, 6.25, 6.24, 6.22, 6.21, 6.19, 6.18, 6.16, 6.14, 6.13, 6.1, 6.08, 6.06, 6.04, 6.02, 6.0, 5.98, 5.95, 5.93, 5.9, 5.87, 5.84, 5.81, 5.78, 5.75, 5.72, 5.69, 5.66, 5.63, 5.6, 5.57, 5.54, 5.51, 5.48])),
            AbsorptionSpectrum("Water", np.arange(450, 1001, 1), np.asarray([0.00028, 0.000279, 0.000277, 0.000276, 0.000275, 0.000273, 0.000272, 0.000271, 0.000269, 0.000268, 0.000267, 0.000265, 0.000264, 0.000263, 0.000262, 0.00026000000000000003, 0.000259, 0.000258, 0.000256, 0.00025499999999999996, 0.000254, 0.000252, 0.000251, 0.00025, 0.000248, 0.00024700000000000004, 0.00024700000000000004, 0.00024700000000000004, 0.00024700000000000004, 0.00024700000000000004, 0.000248, 0.000248, 0.000248, 0.000248, 0.000248, 0.000248, 0.000248, 0.000248, 0.00024900000000000004, 0.00024900000000000004, 0.00024900000000000004, 0.00024900000000000004, 0.00024900000000000004, 0.00024900000000000004, 0.00024900000000000004, 0.00024900000000000004, 0.00025, 0.00025, 0.00025, 0.00025, 0.00025, 0.00025299999999999997, 0.000256, 0.000258, 0.000261, 0.000264, 0.000267, 0.00027, 0.000272, 0.000275, 0.000278, 0.000281, 0.00028399999999999996, 0.000286, 0.00028900000000000003, 0.000292, 0.000295, 0.000298, 0.0003, 0.000303, 0.000306, 0.000309, 0.000312, 0.000314, 0.000317, 0.00032, 0.000325, 0.00033, 0.000336, 0.000341, 0.000346, 0.00035099999999999997, 0.000356, 0.000362, 0.000367, 0.00037200000000000004, 0.000377, 0.00038199999999999996, 0.000388, 0.000393, 0.000398, 0.00040300000000000004, 0.000408, 0.000414, 0.00041900000000000005, 0.000424, 0.000429, 0.000434, 0.00044, 0.00044500000000000003, 0.00045, 0.00046399999999999995, 0.00047699999999999994, 0.000491, 0.000504, 0.000518, 0.000532, 0.000545, 0.000559, 0.000572, 0.000586, 0.0006, 0.0006129999999999999, 0.000627, 0.00064, 0.000654, 0.000668, 0.000681, 0.000695, 0.000708, 0.000722, 0.000736, 0.000749, 0.000763, 0.000776, 0.00079, 0.00085, 0.0009109999999999999, 0.0009710000000000001, 0.00103, 0.00109, 0.00115, 0.00121, 0.0012699999999999999, 0.00133, 0.00139, 0.00145, 0.00151, 0.00158, 0.00164, 0.0017, 0.00176, 0.00182, 0.0018800000000000002, 0.0019399999999999999, 0.002, 0.00206, 0.00212, 0.00218, 0.00224, 0.0023, 0.00232, 0.00234, 0.00236, 0.00238, 0.0024, 0.00242, 0.00244, 0.00246, 0.00248, 0.0025, 0.00252, 0.0025399999999999997, 0.00256, 0.0025800000000000003, 0.0026, 0.00262, 0.00264, 0.00266, 0.00268, 0.0027, 0.0027199999999999998, 0.00274, 0.0027600000000000003, 0.00278, 0.0028, 0.00282, 0.00283, 0.00285, 0.00286, 0.00288, 0.0029, 0.0029100000000000003, 0.00293, 0.00294, 0.00296, 0.00298, 0.00299, 0.00301, 0.00302, 0.0030399999999999997, 0.0030600000000000002, 0.00307, 0.00309, 0.0031, 0.00312, 0.00314, 0.00315, 0.00317, 0.00318, 0.0032, 0.00324, 0.00328, 0.00331, 0.00335, 0.00339, 0.00343, 0.0034700000000000004, 0.0035, 0.0035399999999999997, 0.00358, 0.0036200000000000004, 0.00366, 0.0036899999999999997, 0.00373, 0.0037700000000000003, 0.00381, 0.00385, 0.0038799999999999998, 0.00392, 0.00396, 0.004, 0.00404, 0.004070000000000001, 0.00411, 0.00415, 0.004220000000000001, 0.0043, 0.004370000000000001, 0.00445, 0.004520000000000001, 0.0045899999999999995, 0.0046700000000000005, 0.00474, 0.0048200000000000005, 0.00489, 0.00496, 0.00504, 0.00511, 0.00519, 0.00526, 0.00533, 0.00541, 0.00548, 0.00556, 0.00563, 0.0057, 0.0057799999999999995, 0.00585, 0.0059299999999999995, 0.006, 0.0064, 0.006790000000000001, 0.00719, 0.00758, 0.00798, 0.00838, 0.00877, 0.009170000000000001, 0.009559999999999999, 0.00996, 0.0104, 0.0108, 0.0111, 0.0115, 0.0119, 0.0123, 0.0127, 0.0131, 0.0135, 0.0139, 0.0143, 0.0147, 0.0151, 0.0155, 0.0159, 0.0163, 0.0167, 0.0171, 0.0175, 0.0179, 0.0183, 0.0187, 0.0191, 0.0195, 0.0199, 0.0203, 0.0207, 0.0212, 0.0216, 0.022000000000000002, 0.0224, 0.0228, 0.0232, 0.0236, 0.024, 0.0244, 0.0248, 0.0252, 0.0256, 0.026000000000000002, 0.0259, 0.0258, 0.0258, 0.0257, 0.0256, 0.0255, 0.0254, 0.0254, 0.0253, 0.0252, 0.0251, 0.025, 0.025, 0.0249, 0.0248, 0.0247, 0.0246, 0.0246, 0.0245, 0.0244, 0.0243, 0.0242, 0.0242, 0.0241, 0.024, 0.0238, 0.0237, 0.0235, 0.0234, 0.0232, 0.023, 0.0229, 0.0227, 0.0226, 0.0224, 0.0222, 0.0221, 0.0219, 0.0218, 0.0216, 0.0214, 0.0213, 0.0211, 0.021, 0.0208, 0.0206, 0.0205, 0.0203, 0.0202, 0.02, 0.02, 0.02, 0.02, 0.0199, 0.0199, 0.0199, 0.0199, 0.0199, 0.0199, 0.0199, 0.0203, 0.0207, 0.0211, 0.0215, 0.0219, 0.0223, 0.0227, 0.0231, 0.0235, 0.0239, 0.0247, 0.0255, 0.0264, 0.0272, 0.027999999999999997, 0.0282, 0.0284, 0.0286, 0.0289, 0.0291, 0.0296, 0.0302, 0.0308, 0.0313, 0.0319, 0.0325, 0.033, 0.0336, 0.0341, 0.0347, 0.0355, 0.0364, 0.0372, 0.038, 0.0389, 0.0397, 0.0405, 0.0413, 0.0422, 0.043, 0.0434, 0.0438, 0.0441, 0.0445, 0.0449, 0.0453, 0.0456, 0.046, 0.0464, 0.0468, 0.0473, 0.0478, 0.0483, 0.0489, 0.0494, 0.0499, 0.0504, 0.051, 0.0515, 0.052000000000000005, 0.0528, 0.0536, 0.0544, 0.0552, 0.055999999999999994, 0.055999999999999994, 0.055999999999999994, 0.055999999999999994, 0.055999999999999994, 0.055999999999999994, 0.0564, 0.0569, 0.0573, 0.0578, 0.0582, 0.0587, 0.0591, 0.0595, 0.06, 0.0604, 0.0612, 0.0619, 0.0627, 0.0635, 0.0642, 0.065, 0.0657, 0.0665, 0.0672, 0.068, 0.0685, 0.069, 0.0695, 0.07, 0.0705, 0.0709, 0.0714, 0.0719, 0.0724, 0.0729, 0.0765, 0.0802, 0.0838, 0.0875, 0.0911, 0.0947, 0.0984, 0.102, 0.106, 0.109, 0.11599999999999999, 0.12300000000000001, 0.13, 0.13699999999999998, 0.14400000000000002, 0.15, 0.156, 0.161, 0.16699999999999998, 0.17300000000000001, 0.182, 0.192, 0.201, 0.21100000000000002, 0.22, 0.23, 0.239, 0.248, 0.258, 0.267, 0.28, 0.292, 0.304, 0.316, 0.32899999999999996, 0.341, 0.353, 0.365, 0.37799999999999995, 0.39, 0.39299999999999996, 0.396, 0.39899999999999997, 0.402, 0.405, 0.408, 0.41100000000000003, 0.414, 0.41700000000000004, 0.42, 0.423, 0.426, 0.429, 0.43200000000000005, 0.435, 0.43799999999999994, 0.441, 0.444, 0.447, 0.45, 0.45, 0.45, 0.45, 0.45, 0.45, 0.446, 0.442, 0.43799999999999994, 0.434, 0.43, 0.428, 0.426, 0.424, 0.42200000000000004, 0.42, 0.418, 0.41600000000000004, 0.414, 0.41200000000000003, 0.41, 0.405, 0.4, 0.395, 0.39, 0.385, 0.38, 0.375, 0.37, 0.365, 0.36])),
            AbsorptionSpectrum("Fat", np.arange(450, 1001, 1), np.asarray([6.375, 6.291, 6.21, 6.135, 6.0489999999999995, 5.95, 5.837000000000001, 5.751, 5.662999999999999, 5.593, 5.523, 5.412999999999999, 5.287999999999999, 5.144, 4.985, 4.846, 4.72, 4.593999999999999, 4.513, 4.434, 4.327, 4.208, 4.084, 3.9610000000000003, 3.843, 3.7319999999999998, 3.635, 3.534, 3.452, 3.386, 3.315, 3.261, 3.1919999999999997, 3.109, 3.013, 2.9189999999999996, 2.832, 2.75, 2.676, 2.597, 2.515, 2.437, 2.3680000000000003, 2.298, 2.25, 2.193, 2.124, 2.06, 1.9980000000000002, 1.942, 1.906, 1.875, 1.828, 1.776, 1.724, 1.683, 1.6480000000000001, 1.62, 1.5759999999999998, 1.534, 1.501, 1.475, 1.4569999999999999, 1.432, 1.403, 1.368, 1.33, 1.298, 1.27, 1.246, 1.2309999999999999, 1.2109999999999999, 1.189, 1.165, 1.145, 1.1320000000000001, 1.113, 1.091, 1.064, 1.042, 1.031, 1.0170000000000001, 1.002, 0.991, 0.9840000000000001, 0.978, 0.97, 0.951, 0.929, 0.9129999999999999, 0.8959999999999999, 0.88, 0.8640000000000001, 0.8490000000000001, 0.84, 0.833, 0.828, 0.8220000000000001, 0.805, 0.785, 0.773, 0.763, 0.76, 0.757, 0.746, 0.733, 0.7240000000000001, 0.718, 0.71, 0.7040000000000001, 0.698, 0.69, 0.682, 0.6729999999999999, 0.662, 0.653, 0.647, 0.6409999999999999, 0.636, 0.63, 0.629, 0.633, 0.639, 0.632, 0.613, 0.589, 0.573, 0.562, 0.563, 0.5660000000000001, 0.5660000000000001, 0.564, 0.562, 0.562, 0.557, 0.5479999999999999, 0.541, 0.53, 0.52, 0.512, 0.502, 0.493, 0.488, 0.485, 0.486, 0.48700000000000004, 0.479, 0.47200000000000003, 0.467, 0.462, 0.466, 0.47100000000000003, 0.479, 0.48700000000000004, 0.48700000000000004, 0.484, 0.48, 0.475, 0.47, 0.469, 0.46399999999999997, 0.45799999999999996, 0.45399999999999996, 0.442, 0.42700000000000005, 0.42200000000000004, 0.423, 0.43, 0.43700000000000006, 0.435, 0.43, 0.425, 0.433, 0.44, 0.43799999999999994, 0.43200000000000005, 0.426, 0.424, 0.426, 0.428, 0.428, 0.429, 0.43700000000000006, 0.444, 0.44, 0.431, 0.42, 0.42200000000000004, 0.433, 0.446, 0.452, 0.45, 0.449, 0.45299999999999996, 0.46, 0.465, 0.46399999999999997, 0.46399999999999997, 0.46399999999999997, 0.465, 0.47100000000000003, 0.47200000000000003, 0.467, 0.46399999999999997, 0.457, 0.44799999999999995, 0.43799999999999994, 0.428, 0.424, 0.42200000000000004, 0.418, 0.414, 0.413, 0.414, 0.419, 0.428, 0.439, 0.447, 0.452, 0.45299999999999996, 0.45, 0.452, 0.457, 0.462, 0.46299999999999997, 0.457, 0.446, 0.433, 0.42200000000000004, 0.413, 0.406, 0.39799999999999996, 0.387, 0.375, 0.37, 0.369, 0.366, 0.361, 0.354, 0.348, 0.342, 0.33799999999999997, 0.335, 0.331, 0.32799999999999996, 0.324, 0.321, 0.324, 0.327, 0.325, 0.32299999999999995, 0.32, 0.319, 0.322, 0.326, 0.32299999999999995, 0.318, 0.313, 0.31, 0.311, 0.315, 0.32, 0.321, 0.32, 0.321, 0.326, 0.33399999999999996, 0.34299999999999997, 0.35100000000000003, 0.358, 0.36700000000000005, 0.376, 0.38299999999999995, 0.39, 0.401, 0.415, 0.43, 0.447, 0.46299999999999997, 0.48, 0.499, 0.516, 0.535, 0.552, 0.564, 0.5760000000000001, 0.589, 0.6, 0.616, 0.636, 0.654, 0.68, 0.7070000000000001, 0.735, 0.768, 0.8009999999999999, 0.8370000000000001, 0.8740000000000001, 0.9079999999999999, 0.941, 0.972, 1.001, 1.03, 1.0590000000000002, 1.089, 1.12, 1.155, 1.19, 1.227, 1.258, 1.278, 1.2890000000000001, 1.29, 1.273, 1.249, 1.206, 1.153, 1.089, 1.021, 0.948, 0.871, 0.7929999999999999, 0.7190000000000001, 0.653, 0.596, 0.5529999999999999, 0.515, 0.48100000000000004, 0.451, 0.426, 0.409, 0.391, 0.37799999999999995, 0.366, 0.36, 0.35700000000000004, 0.355, 0.353, 0.349, 0.34600000000000003, 0.34600000000000003, 0.34700000000000003, 0.34700000000000003, 0.34700000000000003, 0.35200000000000004, 0.359, 0.369, 0.379, 0.387, 0.39299999999999996, 0.40299999999999997, 0.413, 0.424, 0.434, 0.442, 0.45399999999999996, 0.467, 0.48200000000000004, 0.49700000000000005, 0.511, 0.527, 0.547, 0.5670000000000001, 0.583, 0.594, 0.603, 0.615, 0.633, 0.654, 0.674, 0.691, 0.708, 0.7240000000000001, 0.74, 0.758, 0.775, 0.7859999999999999, 0.7959999999999999, 0.799, 0.802, 0.8029999999999999, 0.8029999999999999, 0.8009999999999999, 0.794, 0.785, 0.775, 0.764, 0.757, 0.7509999999999999, 0.7390000000000001, 0.726, 0.715, 0.703, 0.6920000000000001, 0.685, 0.6779999999999999, 0.669, 0.6609999999999999, 0.6509999999999999, 0.643, 0.637, 0.633, 0.632, 0.631, 0.633, 0.639, 0.647, 0.6559999999999999, 0.662, 0.6659999999999999, 0.674, 0.68, 0.69, 0.705, 0.7240000000000001, 0.7509999999999999, 0.7859999999999999, 0.8220000000000001, 0.86, 0.899, 0.938, 0.9790000000000001, 1.022, 1.074, 1.133, 1.198, 1.264, 1.345, 1.43, 1.527, 1.636, 1.7519999999999998, 1.867, 1.992, 2.121, 2.262, 2.414, 2.5810000000000004, 2.7539999999999996, 2.932, 3.116, 3.305, 3.491, 3.674, 3.833, 3.983, 4.121, 4.256, 4.3839999999999995, 4.506, 4.633, 4.766, 4.915, 5.078, 5.267, 5.472, 5.721, 5.994, 6.316, 6.662999999999999, 7.046, 7.438, 7.837000000000001, 8.234, 8.621, 8.994, 9.354, 9.683, 10.0, 10.32, 10.65, 10.99, 11.33, 11.67, 12.0, 12.31, 12.6, 12.82, 12.99, 13.07, 13.1, 12.99, 12.83, 12.53, 12.18, 11.75, 11.26, 10.7, 10.08, 9.433, 8.754, 8.088, 7.446000000000001, 6.822, 6.25, 5.704, 5.234, 4.802, 4.445, 4.109, 3.799, 3.5189999999999997, 3.2739999999999996, 3.0460000000000003, 2.852, 2.6660000000000004, 2.504, 2.358, 2.242, 2.133, 2.0469999999999997, 1.975, 1.9169999999999998, 1.86, 1.808, 1.7530000000000001, 1.693, 1.639, 1.589, 1.554, 1.528, 1.51, 1.4909999999999999, 1.463, 1.431, 1.413, 1.4080000000000001, 1.4140000000000001, 1.421, 1.423, 1.4169999999999998, 1.4069999999999998, 1.406, 1.42, 1.4409999999999998, 1.4809999999999999, 1.524, 1.564, 1.607, 1.652, 1.716, 1.7930000000000001, 1.891, 1.994, 2.0869999999999997, 2.178, 2.272, 2.366, 2.464, 2.56, 2.654])/100),
            AbsorptionSpectrum("Melanin", np.arange(450, 1001, 1), np.asarray([965.0, 957.0, 950.0, 943.0, 937.0, 930.0, 923.0, 916.0, 910.0, 903.0, 897.0, 890.0, 884.0, 877.0, 871.0, 865.0, 859.0, 853.0, 846.0, 840.0, 835.0, 829.0, 823.0, 817.0, 811.0, 806.0, 800.0, 794.0, 789.0, 783.0, 778.0, 773.0, 767.0, 762.0, 757.0, 752.0, 747.0, 741.0, 736.0, 731.0, 726.0, 722.0, 717.0, 712.0, 707.0, 702.0, 698.0, 693.0, 688.0, 684.0, 679.0, 675.0, 670.0, 666.0, 661.0, 657.0, 653.0, 648.0, 644.0, 640.0, 636.0, 632.0, 628.0, 624.0, 619.0, 615.0, 612.0, 608.0, 604.0, 600.0, 596.0, 592.0, 588.0, 585.0, 581.0, 577.0, 574.0, 570.0, 566.0, 563.0, 559.0, 556.0, 552.0, 549.0, 546.0, 542.0, 539.0, 535.0, 532.0, 529.0, 526.0, 522.0, 519.0, 516.0, 513.0, 510.0, 507.0, 504.0, 500.0, 497.0, 494.0, 491.0, 489.0, 486.0, 483.0, 480.0, 477.0, 474.0, 471.0, 468.0, 466.0, 463.0, 460.0, 457.0, 455.0, 452.0, 449.0, 447.0, 444.0, 442.0, 439.0, 436.0, 434.0, 431.0, 429.0, 426.0, 424.0, 422.0, 419.0, 417.0, 414.0, 412.0, 410.0, 407.0, 405.0, 403.0, 400.0, 398.0, 396.0, 394.0, 391.0, 389.0, 387.0, 385.0, 383.0, 381.0, 378.0, 376.0, 374.0, 372.0, 370.0, 368.0, 366.0, 364.0, 362.0, 360.0, 358.0, 356.0, 354.0, 352.0, 350.0, 348.0, 346.0, 345.0, 343.0, 341.0, 339.0, 337.0, 335.0, 334.0, 332.0, 330.0, 328.0, 327.0, 325.0, 323.0, 321.0, 320.0, 318.0, 316.0, 315.0, 313.0, 311.0, 310.0, 308.0, 306.0, 305.0, 303.0, 302.0, 300.0, 299.0, 297.0, 295.0, 294.0, 292.0, 291.0, 289.0, 288.0, 286.0, 285.0, 283.0, 282.0, 281.0, 279.0, 278.0, 276.0, 275.0, 274.0, 272.0, 271.0, 269.0, 268.0, 267.0, 265.0, 264.0, 263.0, 261.0, 260.0, 259.0, 258.0, 256.0, 255.0, 254.0, 252.0, 251.0, 250.0, 249.0, 248.0, 246.0, 245.0, 244.0, 243.0, 242.0, 240.0, 239.0, 238.0, 237.0, 236.0, 235.0, 233.0, 232.0, 231.0, 230.0, 229.0, 228.0, 227.0, 226.0, 225.0, 224.0, 223.0, 221.0, 220.0, 219.0, 218.0, 217.0, 216.0, 215.0, 214.0, 213.0, 212.0, 211.0, 210.0, 209.0, 208.0, 207.0, 206.0, 205.0, 204.0, 204.0, 203.0, 202.0, 201.0, 200.0, 199.0, 198.0, 197.0, 196.0, 195.0, 194.0, 193.0, 193.0, 192.0, 191.0, 190.0, 189.0, 188.0, 187.0, 187.0, 186.0, 185.0, 184.0, 183.0, 182.0, 182.0, 181.0, 180.0, 179.0, 178.0, 178.0, 177.0, 176.0, 175.0, 174.0, 174.0, 173.0, 172.0, 171.0, 171.0, 170.0, 169.0, 168.0, 168.0, 167.0, 166.0, 166.0, 165.0, 164.0, 163.0, 163.0, 162.0, 161.0, 161.0, 160.0, 159.0, 159.0, 158.0, 157.0, 156.0, 156.0, 155.0, 154.0, 154.0, 153.0, 153.0, 152.0, 151.0, 151.0, 150.0, 149.0, 149.0, 148.0, 147.0, 147.0, 146.0, 146.0, 145.0, 144.0, 144.0, 143.0, 143.0, 142.0, 141.0, 141.0, 140.0, 140.0, 139.0, 138.0, 138.0, 137.0, 137.0, 136.0, 136.0, 135.0, 135.0, 134.0, 133.0, 133.0, 132.0, 132.0, 131.0, 131.0, 130.0, 130.0, 129.0, 129.0, 128.0, 128.0, 127.0, 127.0, 126.0, 126.0, 125.0, 125.0, 124.0, 124.0, 123.0, 123.0, 122.0, 122.0, 121.0, 121.0, 120.0, 120.0, 119.0, 119.0, 118.0, 118.0, 117.0, 117.0, 116.0, 116.0, 116.0, 115.0, 115.0, 114.0, 114.0, 113.0, 113.0, 112.0, 112.0, 112.0, 111.0, 111.0, 110.0, 110.0, 109.0, 109.0, 109.0, 108.0, 108.0, 107.0, 107.0, 107.0, 106.0, 106.0, 105.0, 105.0, 105.0, 104.0, 104.0, 103.0, 103.0, 103.0, 102.0, 102.0, 101.0, 101.0, 101.0, 100.0, 99.9, 99.6, 99.2, 98.8, 98.4, 98.1, 97.7, 97.4, 97.0, 96.6, 96.3, 95.9, 95.6, 95.2, 94.9, 94.5, 94.2, 93.8, 93.5, 93.1, 92.8, 92.5, 92.1, 91.8, 91.4, 91.1, 90.8, 90.5, 90.1, 89.8, 89.5, 89.2, 88.8, 88.5, 88.2, 87.9, 87.6, 87.2, 86.9, 86.6, 86.3, 86.0, 85.7, 85.4, 85.1, 84.8, 84.5, 84.2, 83.9, 83.6, 83.3, 83.0, 82.7, 82.4, 82.1, 81.8, 81.5, 81.3, 81.0, 80.7, 80.4, 80.1, 79.8, 79.6, 79.3, 79.0, 78.7, 78.5, 78.2, 77.9, 77.6, 77.4, 77.1, 76.8, 76.6, 76.3, 76.0, 75.8, 75.5, 75.3, 75.0, 74.7, 74.5, 74.2, 74.0, 73.7, 73.5, 73.2, 73.0, 72.7, 72.5, 72.2, 72.0, 71.7, 71.5, 71.3, 71.0, 70.8, 70.5, 70.3, 70.1, 69.8, 69.6, 69.4, 69.1, 68.9, 68.7, 68.4, 68.2, 68.0, 67.8, 67.5]))
        ]
        self.i = len(self.spectra)

    def __next__(self):
        if self.i > 0:
            self.i -= 1
            return self.spectra[self.i]
        raise StopIteration()

    def __iter__(self):
        return self

    def get_spectra_names(self):
        return [spectrum.spectrum_name for spectrum in self]

    def get_spectrum_by_name(self, spectrum_name: str) -> AbsorptionSpectrum:
        for spectrum in self:
            if spectrum.spectrum_name == spectrum_name:
                return spectrum

        raise LookupError("No spectrum for the given name exists")


SPECTRAL_LIBRARY = AbsorptionSpectrumLibrary()


def view_absorption_spectra(save_path=None):
    """
    Opens a matplotlib plot and visualizes the available absorption spectra.

    @param save_path: If not None, then the figure will be saved as a png file to the destination.
    """
    plt.figure()
    for spectrum in SPECTRAL_LIBRARY:
        plt.semilogy(spectrum.wavelengths,
                     spectrum.absorption_per_centimeter,
                     label=spectrum.spectrum_name)
    plt.legend(loc='best')
    plt.ylabel("Optical absorption [cm$^{-1}$]")
    plt.xlabel("Wavelength [nm]")
    plt.hlines([0.001, 0.01, 0.1, 1, 10, 100, 1000], 450, 1000, linestyles="dashed", colors=["#EEEEEE"])
    if save_path is not None:
        plt.savefig(save_path + "absorption_spectra.png")
    plt.show()
    plt.close()
