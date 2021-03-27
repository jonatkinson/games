from engine import colors

tetraminos = [
    # O piece.
    {
        'color': colors.ORANGE,
        'size': 2,
        'frames': [
            [
                1, 1,
                1, 1,
            ]
        ]
    },
    # I piece.
    {
        'color': colors.PURPLE,
        'size': 4,
        'frames': [
            [
                0, 0, 0, 0,
                0, 0, 0, 0,
                1, 1, 1, 1,
                0, 0, 0, 0
            ],
            [
                0, 0, 1, 0,
                0, 0, 1, 0,
                0, 0, 1, 0,
                0, 0, 1, 0
            ]
        ]
    },
    # J piece.
    {
        'color': colors.ORANGE,
        'size': 3,
        'frames': [
            [
                0, 0, 0,
                1, 1, 1,
                0, 0, 1,
            ],
            [
                0, 1, 0,
                0, 1, 0,
                1, 1, 0,
            ],
            [
                1, 0, 0,
                1, 1, 1,
                0, 0, 0,
            ],
            [
                0, 1, 1,
                0, 1, 0,
                0, 1, 0,
            ]
        ]
    },
    # J piece.
    {
        'color': colors.PURPLE,
        'size': 3,
        'frames': [
            [
                0, 0, 1,
                1, 1, 1,
                0, 0, 0,
            ],
            [
                0, 1, 0,
                0, 1, 0,
                0, 1, 1,
            ],
            [
                0, 0, 0,
                1, 1, 1,
                1, 0, 0,
            ],
            [
                1, 1, 0,
                0, 1, 0,
                0, 1, 0,
            ]
        ]
    },
    # T piece.
    {
        'color': colors.ORANGE,
        'size': 3,
        'frames': [
            [
                0, 0, 0,
                1, 1, 1,
                0, 1, 0,
            ],
            [
                0, 1, 0,
                0, 1, 1,
                0, 1, 0,
            ],
            [
                0, 1, 0,
                1, 1, 1,
                0, 0, 0,
            ],
            [
                0, 1, 0,
                1, 1, 0,
                0, 1, 0,
            ]
        ]
    },
    # S piece.
    {
        'color': colors.PURPLE,
        'size': 3,
        'frames': [
            [
                0, 0, 0,
                0, 1, 1,
                1, 1, 0,
            ],
            [
                0, 1, 0,
                0, 1, 1,
                0, 0, 1,
            ],
        ]
    },
    # Z piece.
    {
        'color': colors.ORANGE,
        'size': 3,
        'frames': [
            [
                1, 1, 0,
                0, 1, 1,
                0, 0, 0,
            ],
            [
                0, 0, 1,
                0, 1, 1,
                0, 1, 0,
            ],
        ]
    }
]
