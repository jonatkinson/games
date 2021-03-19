import cx_Freeze

executables = [cx_Freeze.Executable("snake.py")]

cx_Freeze.setup(
    name="Snake.py",
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
