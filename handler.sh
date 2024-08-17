#!/bin/bash

if [ "$#" -ne 4 ]; then
    echo "wrong args"
    exit 1
fi

dir="$1"
theme="$2"
dark="$3"
img="$4"
echo dir ${dir}
echo theme ${theme}
echo dark ${dark}
echo img ${img}

cp ${dir}/base.css ~/.config/waybar/style.css
cat ${dir}/styles/${theme}.css >> ~/.config/waybar/style.css

xfconf-query -c xsettings -p /Net/ThemeName -s "Adwaita${dark}"
xfconf-query -c xsettings -p /Net/IconThemeName -s "Adwaita${dark}"

gsettings set org.gnome.desktop.interface gtk-theme "Adwaita${dark}"
gsettings set org.gnome.desktop.interface icon-theme "Adwaita${dark}"

swww img ${dir}/wallpapers/${img} --transition-fps 60 --transition-type grow --transition-pos 1.0,1.0 --transition-duration 0.5
killall -SIGUSR2 waybar
