import globals
import random

from engine import colors, draw, array


class Piece(object):
    """
    This is a game piece.
    """

    def __init__(self, spec):
        self.spec = spec
        self.frames = spec["frames"]
        self.size = spec["size"]
        self.current_frame = 0

    def frame(self):
        """
        This returns the current frame for the piece, based on rotation.
        """

        return self.frames[self.current_frame]

    def clockwise(self):
        """
        This rotates the piece clockwise.
        """

        self.current_frame += 1
        if self.current_frame == len(self.frames):
            self.current_frame = 0

    def counterclockwise(self):
        """
        This rotates the piece counterclockwise.
        """

        self.current_frame -= 1
        if self.current_frame < 0: 
            self.current_frame = len(self.frames) - 1


def random_piece():
    """
    This returns a random new game piece.
    """

    return Piece(
        random.choice([O_PIECE, I_PIECE, J_PIECE, L_PIECE, T_PIECE, S_PIECE, Z_PIECE])
    )


O_PIECE = {
    "size": 2,
    "frames": [
        # fmt: off
        array.TwoDArray(2, 2, data=[
            3, 3,
            3, 3,
        ])
        # fmt: on
    ],
}


I_PIECE = {
    "size": 4,
    "frames": [
        # fmt: off
        array.TwoDArray(4, 4, data=[
            0, 0, 0, 0,
            0, 0, 0, 0,
            3, 3, 3, 3,
        ]),
        array.TwoDArray(3, 4, data=[
            0, 0, 3,
            0, 0, 3,
            0, 0, 3,
            0, 0, 3,
        ])
        # fmt: on
    ],
}

J_PIECE = {
    "size": 3,
    "frames": [
        # fmt: off
        array.TwoDArray(3, 3, data=[
            0, 0, 0,
            3, 3, 3,
            0, 0, 3,
        ]),
        array.TwoDArray(2, 3, data=[
            0, 3,
            0, 3,
            3, 3,
        ]),
        array.TwoDArray(3, 3, data=[
            3, 0, 0,
            3, 3, 3,
        ]),
        array.TwoDArray(3, 3, data=[
            0, 3, 3,
            0, 3, 0,
            0, 3, 0,
        ])
        # fmt: on
    ],
}

L_PIECE = {
    "size": 3,
    "frames": [
        # fmt: off
        array.TwoDArray(3, 2, data=[
            0, 0, 3,
            3, 3, 3,
        ]),
        array.TwoDArray(3, 3, data=[
            0, 3, 0,
            0, 3, 0,
            0, 3, 3,
        ]),
        array.TwoDArray(3, 3, data=[
            0, 0, 0,
            3, 3, 3,
            3, 0, 0,
        ]),
        array.TwoDArray(2, 3, data=[
            3, 3,
            0, 3,
            0, 3,
        ])
        # fmt: on
    ],
}

T_PIECE = {
    "size": 3,
    "frames": [
        # fmt: off
        array.TwoDArray(3, 3, data=[
            0, 0, 0,
            3, 3, 3,
            0, 3, 0,
        ]),
        array.TwoDArray(3, 3, data=[
            0, 3, 0,
            0, 3, 3,
            0, 3, 0,
        ]),
        array.TwoDArray(3, 2, data=[
            0, 3, 0,
            3, 3, 3,
        ]),
        array.TwoDArray(2, 3, data=[
            0, 3,
            3, 3,
            0, 3,
        ])
        # fmt: on
    ],
}

S_PIECE = {
    "size": 3,
    "frames": [
        # fmt: off
        array.TwoDArray(3, 3, data=[
            0, 0, 0,
            0, 3, 3,
            3, 3, 0,
        ]),
        array.TwoDArray(3, 3, data=[
            0, 3, 0,
            0, 3, 3,
            0, 0, 3,
        ]),
        # fmt: on
    ],
}

Z_PIECE = {
    "size": 3,
    "frames": [
        # fmt: off
        array.TwoDArray(3, 3, data=[
            3, 3, 0, 
            0, 3, 3, 
        ]),
        array.TwoDArray(3, 3, data=[
            0, 0, 3, 
            0, 3, 3, 
            0, 3, 0, 
        ]),
        # fmt: on
    ],
}
