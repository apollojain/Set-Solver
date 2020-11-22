import os
from os import listdir
from os.path import isfile, join
from card_utils import (
    num_shapes,
    get_color,
    get_image_filepaths,
    contains_horizontal_lines,
)
import card
import cv2
import numpy as np

TEMPLATE_DIR = "./images/templates"


def get_template_category(img_path):
    base = os.path.basename(img_path)
    shading, shape = os.path.splitext(base)[0].split("_")
    return card.Shading[shading.upper()], card.Shape[shape.upper()]


templates = {
    get_template_category(img_path): cv2.cvtColor(
        cv2.imread(img_path), cv2.COLOR_BGR2GRAY
    )
    for img_path in get_image_filepaths(TEMPLATE_DIR)
}


def get_shading_shape(img_rgb, templates=templates):
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    scores = [
        (
            template_identity,
            np.max(cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)),
        )
        for (template_identity, template) in templates.items()
    ]
    return max(scores, key=lambda pair: pair[1])[0]


def get_img_identity(img_rgb, templates=templates, threshold_per=15):
    shading, shape = get_shading_shape(img_rgb)
    color = get_color(img_rgb)
    number, _ = num_shapes(img_rgb)
    if contains_horizontal_lines(
        img_rgb, num_shapes=number.value, threshold_per=threshold_per
    ):
        shading = card.Shading.STRIPED
    return card.Card(number=number, shape=shape, shading=shading, color=color)
