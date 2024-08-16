import subprocess, os, sys, yaml

def run_command(command):
    subprocess.Popen(command,shell=True)

def load_theme(theme):
    if "theme" in theme:
        theme_override = theme["theme"]
    else:
        theme_override = "dark" if theme["dark"] else "light"
    dark = "-dark" if theme["dark"] else '""'
    run_command(f"{handler_file_path} {cwd} {theme_override} {dark} {theme['img']}")

cwd = os.path.dirname(os.path.realpath(__file__))
handler_file_path = os.path.join(cwd,"handler.sh")
current_file_path = os.path.join(cwd,"current.txt")
config_file_path = os.path.join(cwd,"config.yaml")

with open(current_file_path,"r") as f:
    current = int(f.read().strip())

with open(config_file_path, "r") as f:
    config = yaml.safe_load(f)

themes = config["themes"]

if len(sys.argv) > 1 and sys.argv[1] == "back":
    current -= 1
else:
    current += 1
    
if current >= len(themes):
    current = 0
if current < 0:
    current = len(themes)-1
next_theme = themes[current]

with open(current_file_path,"w") as f:
    f.write(str(current))

load_theme(next_theme)
