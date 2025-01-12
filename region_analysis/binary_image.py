from dip import *

class BinaryImage:
    def __init__(self):
        pass

    def compute_histogram(self, image):
        """Computes the histogram of the input image.
        Takes as input:
        image: a grayscale image
        Returns a histogram as a list."""

        hist = [0] * 256
        height, width = shape(image)

        for i in range(height):
            for j in range(width):
                intensity = image[i, j]
                hist[intensity] += 1

        return hist

    def find_otsu_threshold(self, hist):
        """Analyzes a histogram to find Otsu's threshold assuming that the input histogram is bimodal.
        Takes as input:
        hist: a bimodal histogram
        Returns: an optimal threshold value (Otsu's threshold)"""

        total_pixels = sum(hist)
        max_variance = 0
        optimal_threshold = 0

        for t in range(1, 255):
            w0 = sum(hist[:t]) / total_pixels
            w1 = 1 - w0

            if w0 == 0 or w1 == 0:
                continue

            mu0 = sum([i * hist[i] for i in range(t)]) / (w0 * total_pixels)
            mu1 = sum([i * hist[i] for i in range(t, 256)]) / (w1 * total_pixels)

            variance = w0 * w1 * (mu0 - mu1) ** 2

            if variance > max_variance:
                max_variance = variance
                optimal_threshold = t

        return optimal_threshold

    def binarize(self, image):
        """Computes the binary image of the input image based on histogram analysis and thresholding.
        Takes as input:
        image: a grayscale image
        Returns: a binary image"""

        bin_img = zeros(shape(image), dtype=uint8)
        threshold = self.find_otsu_threshold(self.compute_histogram(image))

        # Invert the binarization to make objects white on a black background
        bin_img[image <= threshold] = 255

        return bin_img
    