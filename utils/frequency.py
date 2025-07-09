import numpy as np
import cv2

def analyze_frequency(image_path):
    try:
        img = cv2.imread(image_path, 0)  # grayscale
        if img is None:
            return 50, ["Image could not be loaded for frequency analysis."]

        f = np.fft.fft2(img)
        fshift = np.fft.fftshift(f)
        magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)

        high_freq = magnitude_spectrum > 150
        ratio = np.sum(high_freq) / high_freq.size

        score = int(min(max(ratio * 300, 0), 100))

        return score, [f"High-frequency pixel ratio: {round(ratio, 4)}"]

    except Exception as e:
        return 70, [f"Frequency analysis error: {str(e)}"]
