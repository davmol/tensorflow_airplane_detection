import cv2
import numpy as np
from skimage import io
import matplotlib.pyplot as plt


def save_cv(image, url):
    cv2.imwrite(url, image)


def save_pil(image, url):
    return None


def mean_color_brightness(img_path):
    img = io.imread(img_path)

    average = img.mean(axis=0).mean(axis=0)
    brightness = sum(average) / 3
    print(average)
    print(brightness)

def img_luminance(img_path):
    img = io.imread(img_path)

    sR, sG, sB = img.mean(axis=0).mean(axis=0)
    vR = sR / 255
    vG = sG / 255
    vB = sB / 255
    color_channel = [vR, vG, vB]
    print(sR, sG, sB)
    print(color_channel)

    color_channel_lin = []
    for c in color_channel:
        if (c <= 0.04045):
            c / 12.92;
            color_channel_lin.append(c)
        else:
            c = pow(((c + 0.055) / 1.055), 2.4)
            color_channel_lin.append(c)

    print(color_channel_lin)

    luminance = [0.2126 * color_channel_lin[0] + 0.7152 * color_channel_lin[1] + 0.0722 * color_channel_lin[2]]
    print(luminance)






    #brightness = sum(average) / 3


    #print(average)
    #print(brightness)


    255



def mean_dominant_color(img_path):


    img = io.imread(img_path)

    average = img.mean(axis=0).mean(axis=0)

    pixels = np.float32(img.reshape(-1, 3))

    n_colors = 5
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)

    dominant = palette[np.argmax(counts)]

    print(average)
    print(dominant)

    avg_patch = np.ones(shape=img.shape, dtype=np.uint8) * np.uint8(average)

    indices = np.argsort(counts)[::-1]
    freqs = np.cumsum(np.hstack([[0], counts[indices] / counts.sum()]))
    rows = np.int_(img.shape[0] * freqs)

    dom_patch = np.zeros(shape=img.shape, dtype=np.uint8)
    for i in range(len(rows) - 1):
        dom_patch[rows[i]:rows[i + 1], :, :] += np.uint8(palette[indices[i]])

    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(12, 6))
    ax0.imshow(avg_patch)
    ax0.set_title('Average color')
    ax0.axis('off')
    ax1.imshow(dom_patch)
    ax1.set_title('Dominant colors')
    ax1.axis('off')
    plt.show(fig)

