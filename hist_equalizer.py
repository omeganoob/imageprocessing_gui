import numpy as np

def hist_equalize(img):
    hist, _ = np.histogram(img, 256, [0, 255])

    cdf = np.cumsum(hist)

    cdf_m = np.ma.masked_equal(cdf, 0)
    num_cdf_m = (cdf_m - cdf_m.min()) * 255
    den_cdf_m = (cdf_m.max() - cdf_m.min())
    cdf_m = num_cdf_m / den_cdf_m

    return np.ma.filled(cdf_m, 0).astype(np.uint8)