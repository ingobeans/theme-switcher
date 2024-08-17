import subprocess, os, sys, json

def run_command(command):
    subprocess.Popen(command,shell=True)

def load_theme(theme):
    if "theme" in theme:
        theme_override = theme["theme"]
    else:
        theme_override = "dark" if theme["dark"] else "light"
    dark = "-dark" if theme["dark"] else '""'
    run_command(f"{handler_file_path} {config_path} {theme_override} {dark} {theme['img']}")

cwd = os.path.dirname(os.path.realpath(__file__))
handler_file_path = os.path.join(cwd,"handler.sh")

config_path = os.path.expanduser("~/.config/theme_switcher")
current_file_path = os.path.join(config_path,"current.txt")
config_file_path = os.path.join(config_path,"config.json")
wallpaper_path = os.path.join(config_path,"wallpapers")
styles_path = os.path.join(config_path,"styles")
base_style_path = os.path.join(config_path,"base.css")

if not os.path.isdir(config_path):
    os.mkdir(config_path)
    os.mkdir(wallpaper_path)
    os.mkdir(styles_path)
    with open(current_file_path,"w") as f:
        f.write("0")
    with open(base_style_path,"w") as f:
        f.write("")
    with open(config_file_path,"w") as f:
        json.dump({
            "themes":[
                {
                    "img":"dark.png",
                    "dark":True
                },
                {
                    "img":"light.png",
                    "dark":False
                }
            ]
        },f,indent=4)

with open(current_file_path,"r") as f:
    current = int(f.read().strip())

with open(config_file_path, "r") as f:
    config = json.load(f)

themes = config["themes"]

if len(sys.argv) > 1 and sys.argv[1] == "previous":
    current -= 1
elif len(sys.argv) > 1 and sys.argv[1] == "next":
    current += 1
    
if current >= len(themes):
    current = 0
if current < 0:
    current = len(themes)-1
theme = themes[current]

with open(current_file_path,"w") as f:
    f.write(str(current))

load_theme(theme)

