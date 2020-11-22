import argparse
from shape_match import get_img_identity
from card_utils import get_cards
from solver import all_solutions, choose_set_combo
import cv2
import numpy as np
import itertools


def solve_set_board(board_img_rgb, numcards=15):
    # segment the image into images (with the limits)
    card_images, card_contours = get_cards(board_img_rgb, numcards=numcards)
    # loop through the images and get the card classes
    cards = [get_img_identity(card_img) for card_img in card_images]
    print(all_solutions(cards))
    # pass that list of cards into the solver
    valid_triplets = [valid_set[0] for valid_set in all_solutions(cards)]
    print(valid_triplets)
    # get the bounding boxes
    if len(valid_triplets):
        print(choose_set_combo(valid_triplets))
        # remaining triplets
        remaining_cards = set(itertools.chain(*[valid_triplets[i] for i in choose_set_combo(valid_triplets)]))
        print(remaining_cards)
        # get first triplet
        remaining_contours = [
            card_contours[i] for i in remaining_cards
        ]
        # draw them onto the original images
        cv2.drawContours(board_img_rgb, remaining_contours, -1, (0, 255, 0), 3)
    # show image
    cv2.imshow("board", board_img_rgb)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
        help="path to the image you would like to process")
    ap.add_argument("-n", "--number",
        help="number of cards on board", default=15)
    args = vars(ap.parse_args())

    solve_set_board(cv2.imread(args["image"]), args["number"])


