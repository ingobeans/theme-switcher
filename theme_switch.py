import subprocess, os, sys, json, shutil

def load_theme(theme, old_theme, force):
    gtk_theme_dark = theme.get("dark",True)
    if gtk_theme_dark:
        gtk_theme = config["gtk_theme_dark"]
    else:
        gtk_theme = config["gtk_theme_light"]
    # update gtk theme
    subprocess.Popen(["xfconf-query","-c","xsettings","-p","/Net/ThemeName","-s",gtk_theme])
    subprocess.Popen(["gsettings","set","org.gnome.desktop.interface","gtk-theme",gtk_theme])
    # update wallpaper
    subprocess.Popen(["swww","img",f"{wallpaper_path}/{theme.get('img')}","--transition-fps","60","--transition-type","grow","--transition-pos","1.0,1.0","--transition-duration","0.5"])
    # update waybar css
    css = ""
    for css_theme in theme.get("themes"):
        with open(f"{styles_path}/{css_theme}.css") as css_theme:
            css += css_theme.read()


    with open(os.path.expanduser("~/.config/waybar/style.css"),"w") as f:
        f.write(css)

cwd = os.path.dirname(os.path.realpath(__file__))
handler_file_path = os.path.join(cwd,"handler.sh")

config_path = os.path.expanduser("~/.config/theme_switcher")
current_file_path = os.path.join(config_path,"current.txt")
config_file_path = os.path.join(config_path,"config.json")
wallpaper_path = os.path.join(config_path,"wallpapers")
styles_path = os.path.join(config_path,"styles")

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

            "profiles":[
                {
                    "img":"light.png", # wallpaper
                    "dark":False # if to use dark gtk theme
                },
                {
                    "img":"dark.png",
                    "themes": ["dark"]
                },
                {
                    "img":"bright yellow.png",
                    "dark":False, # use light gtk theme
                    "themes": ["light","yellow"]
                }
            ]
        },f,indent=4)

with open(current_file_path,"r") as f:
    current = int(f.read().strip())

with open(config_file_path, "r") as f:
    config = json.load(f)

themes = config["profiles"]

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
