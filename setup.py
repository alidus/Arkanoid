import cx_Freeze

executables = [cx_Freeze.Executable("game.py")]

cx_Freeze.setup(
    name="aArkanoid",
    options={"build_exe": {"packages":["pygame", "os", "math", "random"],
                           "include_files":["eztext.py", "map_editor.py", "res", "maps"]}},
    executables = executables

    )