import cx_Freeze

cx_Freeze.setup(
    name="archer", version="0.4",
    description="A simple arcade-style pygame app",
    options={
        "build_exe":
        {"packages": ["pygame"],
         "include_files": ["archerfont.ttf", "icon.ico", "README.md", "highscore.archer"]}},
    executables=[cx_Freeze.Executable(
        "archer.py",
        base="Win32GUI",
        icon="icon.ico",
        shortcut_name="archer",
        shortcut_dir="StartMenuFolder"
    )])
