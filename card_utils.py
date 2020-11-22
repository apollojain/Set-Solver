import cv2
import numpy as np
from scipy import ndimage
from card import Number, Shape, Shading, Color
from os import listdir
from os.path import isfile, join
import os
import math

POSSIBLE_CARDS = [12, 15]

get_image_filepaths = lambda dirpath: [
    os.path.join(dirpath, f)
    for f in listdir(dirpath)
    if isfile(join(dirpath, f)) and f.endswith(".jpg") or f.endswith(".png")
]


def contains_horizontal_lines(img_rgb, num_shapes=2, threshold_per=15):
    modified_sample_image = cv2.addWeighted(
        img_rgb, 4, cv2.blur(img_rgb, (30, 30)), -4, 128
    )
    gray = cv2.cvtColor(modified_sample_image, cv2.COLOR_BGR2GRAY)

    # Smoothing without removing edges.
    gray_filtered = cv2.bilateralFilter(gray, 7, 50, 50)

    # Applying the canny filter
    edges_filtered = cv2.Canny(gray_filtered, 60, 120)
    lines = cv2.HoughLinesP(edges_filtered, 1, math.pi / 2, 2, None, 30, 1)
    try:
        return len(lines) > threshold_per * num_shapes
    except TypeError as e:
        return False


def get_label_image_pairs(img_directory):
    def get_enum_labels(img_filepath):
        base = os.path.basename(img_filepath)
        (number, shape, shading, color) = os.path.splitext(base)[0].split("_")
        return (
            Number[number.upper()],
            Shape[shape.upper()],
            Shading[shading.upper()],
            Color[color.upper()],
        )

    image_filepaths = get_image_filepaths(img_directory)
    return {
        get_enum_labels(image_filepath): cv2.imread(image_filepath)
        for image_filepath in image_filepaths
    }


def get_median_area(sorted_contours, numcards):
    return np.mean([cv2.contourArea(contour) for contour in sorted_contours[:numcards]])


def filter_contours(contours, median_area, tolerance=2.0):
    n = len(contours)
    areas = [cv2.contourArea(contour) for contour in contours]
    return [
        contours[i]
        for i in range(n)
        if median_area / tolerance < areas[i] and areas[i] < median_area * tolerance
    ]


def filled_shape(img):
    kernel = np.ones((5, 5), np.uint8)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Smoothing without removing edges.
    gray_filtered = cv2.bilateralFilter(gray, 7, 50, 50)

    # Applying the canny filter
    edges_filtered = cv2.Canny(gray_filtered, 60, 120)
    mask = cv2.inRange(edges_filtered, 100, 255)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    filled = np.array(ndimage.binary_fill_holes(mask).astype(int), np.uint8)
    return filled


def num_shapes(img, get_crops=False):
    filled = filled_shape(img)
    contours, _ = cv2.findContours(filled, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = [
        contour
        for contour in sorted(contours, key=cv2.contourArea, reverse=True)
        if cv2.contourArea(contour) < 400 ** 2
    ]
    contours = filter_contours(contours, cv2.contourArea(contours[0]), 2.0)
    crops = []
    if get_crops:
        for c in contours:
            # get the bounding rect
            x, y, w, h = cv2.boundingRect(c)
            # get crop
            crops.append(img[y : y + h, x : x + w])
    n = len(contours)
    number = None
    if n == 1:
        number = Number.ONE
    elif n == 2:
        number = Number.TWO
    elif n == 3:
        number = Number.THREE
    return number, crops


def get_color(image):
    color_masks = {
        Color.RED: [(40, 40, 150), (120, 120, 255)],
        Color.GREEN: [(34, 93, 0), (94, 153, 40)],
        Color.PURPLE: [(59, 30, 46), (170, 80, 160)],
    }
    color_sums = []
    for color in color_masks.keys():
        lower, upper = color_masks[color]

        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        mask = cv2.inRange(image, lower, upper)
        color_sums.append((color, np.sum(mask)))
    return max(color_sums, key=lambda pair: pair[1])[0]


def rectify(h):
    h = h.reshape((4, 2))
    hnew = np.zeros((4, 2), dtype=np.float32)

    add = h.sum(1)
    hnew[0] = h[np.argmin(add)]
    hnew[2] = h[np.argmax(add)]

    diff = np.diff(h, axis=1)
    hnew[1] = h[np.argmin(diff)]
    hnew[3] = h[np.argmax(diff)]

    return hnew


def filter_contours(contours, median_area, tolerance=2.0):
    n = len(contours)
    areas = [cv2.contourArea(contour) for contour in contours]
    return [
        contours[i]
        for i in range(n)
        if median_area / tolerance < areas[i] and areas[i] < median_area * tolerance
    ]


def get_cards(im, numcards=15):
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (1, 1), 1000)
    flag, thresh = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    median_area = get_median_area(contours, numcards)
    contours = filter_contours(contours, median_area)

    n = len(contours)
    if n >= max(POSSIBLE_CARDS):
        contours = contours[: max(POSSIBLE_CARDS)]
    elif n >= min(POSSIBLE_CARDS):
        contours = contours[: min(POSSIBLE_CARDS)]
    else:
        raise ValueError(
            "This image doesn't seem to have enough cards to play a game of set."
        )

    warped_list = []
    for card in contours:
        peri = cv2.arcLength(card, True)
        approx = rectify(cv2.approxPolyDP(card, 0.02 * peri, True))

        h = np.array([[0, 0], [449, 0], [449, 449], [0, 449]], np.float32)

        transform = cv2.getPerspectiveTransform(approx, h)
        warp = cv2.warpPerspective(im, transform, (450, 450))
        warped_list.append(warp)
    return warped_list, contours
