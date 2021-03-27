import cx_Freeze

executables = [cx_Freeze.Executable("tetris.py")]

cx_Freeze.setup(
    name="Tetris.py",
    options={"build_exe": {
        "packages": [
            "pygame"
        ],
        "include_files":[
            "levels.py",
            "collect.wav",
            "collide.wav",
            "slkscr.ttf",
        ],
        }
    },
    executables = executables
)
