import unittest
from solver import solve_three, all_solutions, choose_set_combo
from card import Number, Shape, Shading, Color, Card
from shape_match import get_img_identity
from card_utils import get_label_image_pairs


class TestSetGame(unittest.TestCase):
    true_combo_1 = [
        Card(
            number=Number.TWO,
            shape=Shape.OVAL,
            shading=Shading.SOLID,
            color=Color.GREEN,
        ),
        Card(
            number=Number.ONE,
            shape=Shape.DIAMOND,
            shading=Shading.SOLID,
            color=Color.GREEN,
        ),
        Card(
            number=Number.THREE,
            shape=Shape.SQUIGGLE,
            shading=Shading.SOLID,
            color=Color.GREEN,
        ),
    ]
    true_combo_2 = [
        Card(
            number=Number.TWO,
            shape=Shape.OVAL,
            shading=Shading.SOLID,
            color=Color.GREEN,
        ),
        Card(
            number=Number.THREE,
            shape=Shape.DIAMOND,
            shading=Shading.SOLID,
            color=Color.GREEN,
        ),
        Card(
            number=Number.ONE,
            shape=Shape.SQUIGGLE,
            shading=Shading.SOLID,
            color=Color.GREEN,
        ),
    ]
    true_combo_3 = [
        Card(
            number=Number.THREE,
            shape=Shape.SQUIGGLE,
            shading=Shading.OPEN,
            color=Color.GREEN,
        ),
        Card(
            number=Number.ONE,
            shape=Shape.DIAMOND,
            shading=Shading.SOLID,
            color=Color.PURPLE,
        ),
        Card(
            number=Number.TWO,
            shape=Shape.OVAL,
            shading=Shading.STRIPED,
            color=Color.RED,
        ),
    ]
    true_combo_4 = [
        Card(
            number=Number.THREE,
            shape=Shape.SQUIGGLE,
            shading=Shading.OPEN,
            color=Color.GREEN,
        ),
        Card(
            number=Number.TWO,
            shape=Shape.SQUIGGLE,
            shading=Shading.STRIPED,
            color=Color.GREEN,
        ),
        Card(
            number=Number.ONE,
            shape=Shape.SQUIGGLE,
            shading=Shading.SOLID,
            color=Color.GREEN,
        ),
    ]
    true_combo_5 = [
        Card(
            number=Number.ONE,
            shape=Shape.SQUIGGLE,
            shading=Shading.STRIPED,
            color=Color.RED,
        ),
        Card(
            number=Number.TWO,
            shape=Shape.DIAMOND,
            shading=Shading.STRIPED,
            color=Color.RED,
        ),
        Card(
            number=Number.THREE,
            shape=Shape.OVAL,
            shading=Shading.STRIPED,
            color=Color.RED,
        ),
    ]

    card_set = [
        Card(
            number=Number.TWO,
            shape=Shape.OVAL,
            shading=Shading.SOLID,
            color=Color.GREEN,
        ),
        Card(
            number=Number.ONE,
            shape=Shape.DIAMOND,
            shading=Shading.SOLID,
            color=Color.PURPLE,
        ),
        Card(
            number=Number.THREE,
            shape=Shape.SQUIGGLE,
            shading=Shading.SOLID,
            color=Color.GREEN,
        ),
        Card(
            number=Number.THREE,
            shape=Shape.DIAMOND,
            shading=Shading.SOLID,
            color=Color.RED,
        ),
        Card(
            number=Number.ONE,
            shape=Shape.DIAMOND,
            shading=Shading.SOLID,
            color=Color.GREEN,
        ),
        Card(
            number=Number.THREE,
            shape=Shape.DIAMOND,
            shading=Shading.SOLID,
            color=Color.GREEN,
        ),
        Card(
            number=Number.THREE,
            shape=Shape.DIAMOND,
            shading=Shading.STRIPED,
            color=Color.RED,
        ),
        Card(
            number=Number.ONE,
            shape=Shape.DIAMOND,
            shading=Shading.OPEN,
            color=Color.GREEN,
        ),
        Card(
            number=Number.TWO,
            shape=Shape.SQUIGGLE,
            shading=Shading.STRIPED,
            color=Color.GREEN,
        ),
        Card(
            number=Number.THREE,
            shape=Shape.SQUIGGLE,
            shading=Shading.OPEN,
            color=Color.GREEN,
        ),
        Card(
            number=Number.TWO,
            shape=Shape.SQUIGGLE,
            shading=Shading.STRIPED,
            color=Color.RED,
        ),
        Card(
            number=Number.TWO,
            shape=Shape.OVAL,
            shading=Shading.STRIPED,
            color=Color.RED,
        ),
        Card(
            number=Number.ONE,
            shape=Shape.SQUIGGLE,
            shading=Shading.STRIPED,
            color=Color.RED,
        ),
        Card(
            number=Number.THREE,
            shape=Shape.SQUIGGLE,
            shading=Shading.STRIPED,
            color=Color.PURPLE,
        ),
        Card(
            number=Number.ONE,
            shape=Shape.SQUIGGLE,
            shading=Shading.SOLID,
            color=Color.GREEN,
        ),
    ]

    def test_solve_three(self):
        false_combo_2 = [
            Card(
                number=Number.TWO,
                shape=Shape.OVAL,
                shading=Shading.SOLID,
                color=Color.GREEN,
            ),
            Card(
                number=Number.ONE,
                shape=Shape.DIAMOND,
                shading=Shading.SOLID,
                color=Color.RED,
            ),
            Card(
                number=Number.THREE,
                shape=Shape.SQUIGGLE,
                shading=Shading.SOLID,
                color=Color.GREEN,
            ),
        ]

        false_combo_1 = [
            Card(
                number=Number.TWO,
                shape=Shape.OVAL,
                shading=Shading.SOLID,
                color=Color.GREEN,
            ),
            Card(
                number=Number.ONE,
                shape=Shape.DIAMOND,
                shading=Shading.SOLID,
                color=Color.GREEN,
            ),
            Card(
                number=Number.ONE,
                shape=Shape.SQUIGGLE,
                shading=Shading.SOLID,
                color=Color.GREEN,
            ),
        ]

        self.assertEqual(solve_three(self.true_combo_1), True)
        self.assertEqual(solve_three(self.true_combo_2), True)
        self.assertEqual(solve_three(self.true_combo_3), True)
        self.assertEqual(solve_three(self.true_combo_4), True)
        self.assertEqual(solve_three(self.true_combo_5), True)

        self.assertEqual(solve_three(false_combo_1), False)
        self.assertEqual(solve_three(false_combo_2), False)

    def test_all_solutions(self):
        valid_sets = all_solutions(self.card_set)
        expected = [
            set([0, 2, 4]),
            set([0, 5, 14]),
            set([1, 9, 11]),
            set([6, 11, 12]),
            set([8, 9, 14]),
            set([8, 12, 13]),
        ]
        self.assertEqual([pair[0] for pair in valid_sets], expected)

    def test_choose_set_combo(self):
        valid_sets = all_solutions(self.card_set)
        valid_triplets = [pair[0] for pair in valid_sets]
        set_combo = choose_set_combo(valid_triplets)
        self.assertEqual(set(set_combo), set([0, 2, 5]))


class TestShapeMatch(unittest.TestCase):
    cards_directory = "./images/examples"

    def test_get_label_image_pairs(self):
        label_image_dict = get_label_image_pairs(self.cards_directory)

        card_match = 0

        number_match = 0
        shape_match = 0
        shading_match = 0
        color_match = 0

        for label, image_rgb in label_image_dict.items():
            label_number, label_shape, label_shading, label_color = label
            label_card = Card(
                number=label_number,
                shape=label_shape,
                shading=label_shading,
                color=label_color,
            )
            identity = get_img_identity(image_rgb)

            card_match += 1 * (identity == label_card)

            number_match += 1 * (identity.number == label_card.number)
            shape_match += 1 * (identity.shape == label_card.shape)
            shading_match += 1 * (identity.shading == label_card.shading)
            color_match += 1 * (identity.color == label_card.color)

        self.assertEqual(card_match, 8)

        self.assertEqual(number_match, 12)
        self.assertEqual(shape_match, 9)
        self.assertEqual(shading_match, 9)
        self.assertEqual(color_match, 12)


if __name__ == "__main__":
    unittest.main()
