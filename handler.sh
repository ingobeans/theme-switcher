#!/bin/bash

if [ "$#" -ne 4 ]; then
    echo "wrong args"
    exit 1
fi

dir="$1"
theme="$2"
gtk_theme="$3"
img="$4"
echo dir ${dir}
echo theme ${theme}
echo gtk_theme ${gtk_theme}
echo img ${img}

swww img ${dir}/wallpapers/${img} --transition-fps 60 --transition-type grow --transition-pos 1.0,1.0 --transition-duration 0.5

if [[ $theme != "skipvalue" ]]; then
    cp ${dir}/base.css ~/.config/waybar/style.css
    if [[ $theme != "" ]]; then
        cat ${dir}/styles/${theme}.css >> ~/.config/waybar/style.css
    else
        echo "just reset"
    fi
    killall -SIGUSR2 waybar
fi

if [[ $gtk_theme != "skipvalue" ]]; then
    xfconf-query -c xsettings -p /Net/ThemeName -s "${gtk_theme}"
    gsettings set org.gnome.desktop.interface gtk-theme "${gtk_theme}"
fi