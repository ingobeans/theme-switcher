import subprocess, os, sys, json

def run_command(command):
    subprocess.Popen(command,shell=True)

def load_theme(theme, old_theme, force):
    css_theme = "skipvalue"
    if old_theme.get("theme","skipvalue") != theme.get("theme","skipvalue") or force:
        css_theme = theme.get("theme",'""')
    gtk_theme = "skipvalue"
    if old_theme.get("dark",True) != theme.get("dark",True) or force:
        gtk_theme = theme.get("dark",True)
    run_command(f"{handler_file_path} {config_path} {css_theme} {gtk_theme} {theme['img']}")

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
            "gtk_theme_light":"Adwaita",    # gtk theme when "dark" is True
            "gtk_theme_dark":"Adwaita-dark",# gtk theme when "dark" is False

            "themes":[
                {
                    "img":"light.png", # wallpaper
                    "dark":False # if to use dark gtk theme
                },
                {
                    "img":"dark.png"
                    # no need to specify dark, is default
                    # you can however (and most likely want to) specify
                    # a dark override theme
                    # ex: "theme":"my_dark_override"
                    # will append the contents of ~/.config/styles/my_dark_override.css to
                    # base.css, allowing you to override the default theme
                },
                {
                    "img":"bright yellow.png",
                    "dark":False, # use light gtk theme
                    "theme":"yellow" # override default theme
                }
            ]
        },f,indent=4)

with open(current_file_path,"r") as f:
    current = int(f.read().strip())

with open(config_file_path, "r") as f:
    config = json.load(f)

themes = config["themes"]

old_theme = themes[current]

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

force = theme == old_theme
load_theme(theme,old_theme,force)