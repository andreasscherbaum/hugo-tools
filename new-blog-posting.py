#!/usr/bin/env python3

import os
import sys
import tkinter as tk
from datetime import date, timedelta
import re
import subprocess


def t(text):
    # for some reasons, $LANG is set to "en_US.UTF-8", not "de_DE.UTF-8" on relevant systems
    username = os.environ['LOGNAME']
    # detect language, good enough for now
    if (username == 'ea'):
        sys_lang = 'de'
    else:
        sys_lang = 'en'

    if (sys_lang == 'de'):
        if (text == 'New Blog Posting'):
            return 'Neues Blogposting'
        elif (text == 'Enter the title of the new blog posting'):
            return 'Gib den Titel des neuen Blogpostings ein'
        elif (text == 'Blog article already exists'):
            return 'Dieser Blogartikel existiert schon'
        elif (text == 'Title'):
            return 'Titel'
        elif (text == 'Path'):
            return 'Pfad'
        elif (text == 'Directory'):
            return 'Verzeichnis'
        elif (text == 'Today'):
            return 'Heute'
        elif (text == 'Yesterday'):
            return 'Gestern'
        elif (text == 'Day before yesterday'):
            return 'Vorgestern'
        elif (text == 'Tomorrow'):
            return 'Morgen'
        elif (text == 'Day after tomorrow'):
            return 'Übermorgen'
        else:
            print("Unknown translation!")
            print(text)
            return text

    # just return the English/original text
    return text


def create_blog_posting(button):
    blog_title = entry.get()
    if (len(blog_title) < 2):
        entry.configure(bg = "red")
        return

    if (button == "Today"):
        today = date.today()
        iso_date = today.isoformat()
        entry.configure(bg = "green")
    elif (button == "Yesterday"):
        today = date.today()
        yesterday = today - timedelta(days = 1)
        iso_date = yesterday.isoformat()
        entry.configure(bg = "green")
    elif (button == "Day before yesterday"):
        today = date.today()
        day_before_yesterday = today - timedelta(days = 2)
        iso_date = day_before_yesterday.isoformat()
        entry.configure(bg = "green")
    elif (button == "Tomorrow"):
        today = date.today()
        tomorrow = today + timedelta(days = 1)
        iso_date = tomorrow.isoformat()
        entry.configure(bg = "green")
    elif (button == "Day after tomorrow"):
        today = date.today()
        tomorrow = today + timedelta(days = 2)
        iso_date = tomorrow.isoformat()
        entry.configure(bg = "green")
    else:
        entry.configure(bg = "red")
        return

    # transform title into a pathname
    blog_title = re.sub(r'\s+', ' ', blog_title)
    blog_url = blog_title

    # replace all umlauts
    umlaut_replacements = {
        'ä': 'ae',
        'ö': 'oe',
        'ü': 'ue',
        'Ä': 'Ae',
        'Ö': 'Oe',
        'Ü': 'Ue',
        'ß': 'ss'
    }
    for umlaut, replacement in umlaut_replacements.items():
        blog_url = blog_url.replace(umlaut, replacement)

    # other replacements
    other_replacements = {
        ' ': '-',
        '+': '-',
        ':': '-',
        ';': '-',
        '!': '-',
        '?': '-',
        '=': '-',
        ',': '-',
        '&': '-',
        '/': '-',
        '\\': '-',
        '(': '-',
        ')': '-',
        '*': '-',
        '.': '-',
        "'": ''
    }
    for other, replacement in other_replacements.items():
        blog_url = blog_url.replace(other, replacement)

    # url is lowercase
    blog_url = blog_url.lower()

    # having dashes in the url leads to ugly '---'
    blog_url = re.sub(r'\-+', '-', blog_url)
    blog_url = blog_url.strip('-')

    blog_url = "{date}_{url}".format(date = iso_date, url = blog_url)
    blog_path = "content/post/{url}/index.md".format(url = blog_url)
    #print(blog_title)
    #print(blog_url)
    #print(blog_path)

    if os.path.exists(blog_path):
        entry.configure(bg = "red")
        print(t("Blog article already exists") + '!')
        return

    abs_path = os.path.abspath(blog_path)

    print("{text}: {title}".format(text = t('Title'), title = blog_title))
    print("{text}: {path}".format(text = t('Path'), path = blog_path))
    print("{text}: {path}/".format(text = t('Directory'), path = os.path.dirname(abs_path)))

    args = ['hugo', 'new', blog_path]
    #print(args)
    result = subprocess.run(args, capture_output = True, text = True)
    #print(result.stdout)

    with open(abs_path, 'r') as fh:
        content = fh.read()
    content = content.splitlines()

    for i in range(len(content)):
        # replace the auto-generated title with the original title
        if content[i].startswith("title: "):
            content[i] = 'title: "{title}"'.format(title = blog_title)
        # set the new date, as selected with the button
        if content[i].startswith("date: "):
            date_line = content[i][6:]
            date_time = date_line[10:]
            content[i] = "date: {date}{time}".format(date = iso_date, time = date_time)
    content_to_write = '\n'.join(content)

    with open(abs_path, 'w') as fh:
        fh.write(content_to_write)


    print("")
    print("")
    print(abs_path)
    print("")
    print("")

    root.destroy()
    sys.exit(0)

    return



def exit_on_ctrl_q(event):
    if event.state == 4 and event.keysym.lower() == 'q':
        root.destroy()

    return



# create the main window
root = tk.Tk()
root.title(t("New Blog Posting"))

help_label = tk.Label(root, text = t("Enter the title of the new blog posting") + ':')
help_label.grid(row = 0, column = 0, columnspan = 5, pady = 5)

# create an Entry widget for text input
entry = tk.Entry(root, width = 80)
entry.grid(row = 1, column = 0, columnspan = 5, pady = 5)
entry.focus_set()

button1 = tk.Button(root, text = t("Day before yesterday"), command = lambda: create_blog_posting("Day before yesterday"))
button1.grid(row = 2, column = 0, padx = 5, pady = 10)

button2 = tk.Button(root, text = t("Yesterday"), command = lambda: create_blog_posting("Yesterday"))
button2.grid(row = 2, column = 1, padx = 5, pady = 10)

button3 = tk.Button(root, text = t("Today"), command = lambda: create_blog_posting("Today"))
button3.grid(row = 2, column = 2, padx = 5, pady = 10)
button3.configure(font = ('Sans','14','bold'))

button4 = tk.Button(root, text = t("Tomorrow"), command = lambda: create_blog_posting("Tomorrow"))
button4.grid(row = 2, column = 3, padx = 5, pady = 10)

button5 = tk.Button(root, text = t("Day after tomorrow"), command = lambda: create_blog_posting("Day after tomorrow"))
button5.grid(row = 2, column = 4, padx = 5, pady = 10)

root.bind("<Control-q>", exit_on_ctrl_q)

# Start the main loop
root.mainloop()
