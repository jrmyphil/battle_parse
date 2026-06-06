import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import random


def calculate(*args):
    global chance_stringvar, props


    # ADD: Parse variable number of attacks

    # Hit chance calculation
    # chance_to_hit = (6 - ballistic_skill.get() + 1) / 6

    # Update the chance variable for display
    chance_stringvar.set("Chance: " + str(0.5))


def build_all_props_list(box):
    global PROPERTIES
    for i in range(len(PROPERTIES)):
        box.insert(i, PROPERTIES[i])


def add_prop():
    global PROPERTIES, all_props, props
    selected_keys = all_props.curselection()
    prop_names = []
    for i in range(len(selected_keys)):
        prop_names.append(all_props.get(selected_keys[i]))
        if not is_in_listbox(props, prop_names[i]):
            props.insert(selected_keys[i], prop_names[i])
    calculate()


def remove_prop():
    global props
    selected_key = props.curselection()[0]
    props.delete(selected_key)
    calculate()


def remove_all():
    global props
    props.delete(0, 'end')


def get_key(d, target):
    for key in d.keys():
        if d[key] == target:
            return key
    return -1


def is_in_listbox(box, target):
    for i in range(box.size()):
        if box.get(i) == target:
            return True
    return False


def light_infantry():
    pass


def medium_infantry():
    pass


def heavy_infantry():
    pass


def bike():
    pass


def save_to_file():
    global root, attacks, ballistic_skill, strength, toughness_num, armor_num, invuln_num, chance_stringvar, props
    title = simpledialog.askstring("Input", "Enter a title:")
    properties_string = ''
    properties_tuple = props.get(0, 'end')
    for thing in properties_tuple:
        if properties_string != '':
            properties_string += ', '
        properties_string += str(thing)
    chance_string = chance_stringvar.get()
    zero_idx = chance_string.find("0")
    chance_string = chance_string[zero_idx:]
    chance_float = float(chance_string)
    chance_float *= 100
    chance_float = round(chance_float, 3)
    string = ''
    # string = ("\n\n=============================\n" +
    #           title +
    #           "\n=============================" +
    #           "\nChance to damage: " + str(chance_float) + "%" +
    #           "\nAttacker Profile:" +
    #           "\nA: " + str(attacks.get()) +
    #           "\tB: " + str(ballistic_skill.get()) +
    #           "\tC: " + str(strength.get()) +
    #           "\n" + properties_string +
    #           "\n----------------------------" +
    #           "\nDefender Profile:" +
    #           "\nX: " + str(toughness_num.get()) +
    #           "\tY: " + str(armor_num.get()) +
    #           "\tZ: " + str(invuln_num.get()))

    with open("results.txt", "a", encoding="utf-8") as f:
        f.write(string)


base_chance = 0.5
PROPERTIES = {0:"Anti", 1:"Blast/Cleave", 2:"Crit 4+", 3:"Crit 5+", 4:"Devastating Wounds",
              5:"Lethal Hits", 6:"Melta", 7:"Reroll 1s to Hit", 8:"Reroll 1s to Wound",
              9:"Reroll All Misses", 10:"Sustained Hits", 11:"Torrent", 12:"Twin-Linked"}

# Create the window
root = tk.Tk()
root.geometry('510x600')

menubar = tk.Menu(root, bg='#6E6E6E', fg='#FFFFFF', activebackground='#ABABAB', relief='raised')
profiles = tk.Menu(menubar, tearoff=0, bg='#6E6E6E', activebackground='#ABABAB', relief='raised')
menubar.add_cascade(label='Defender Profiles', menu=profiles)
profiles.add_command(label='Light Infantry', command=light_infantry)
profiles.add_command(label='Medium Infantry', command=medium_infantry)
profiles.add_command(label='Heavy Infantry', command=heavy_infantry)
profiles.add_command(label='Bike', command=bike)
profiles.add_command(label='Light Vehicle')
profiles.add_command(label='Heavy Vehicle')

root.config(menu=menubar)

# Create the save button
save_button = tk.Button(root, text='Save to File', command=save_to_file)
save_button.place(anchor='nw', relx=0.01, rely=0.004)

# Create the chance output
chance_stringvar = tk.StringVar(root, value=("Chance: " + str(base_chance)))
chance_label = tk.Label(root, bg='white', width=12, anchor='w', textvariable=chance_stringvar)
chance_label.place(anchor='n', relx=0.5, rely=0.01)

# Create the attacker stat list and UI widgets
a_stat_list = ["A", "BS", "S", "AP", "D"]
a_stats = {"A":tk.StringVar(root, value=''),
          "BS":tk.StringVar(root, value=''),
          "S":tk.StringVar(root, value=''),
          "AP":tk.StringVar(root, value=''),
          "D":tk.StringVar(root, value='')}
a_labels = {"A":tk.Label(root, bg='white', text='# Attacks'),
            "BS":tk.Label(root, bg='white', text='BS/WS'),
            "S":tk.Label(root, bg='white', text='Strength'),
            "AP":tk.Label(root, bg='white', text='AP'),
            "D":tk.Label(root, bg='white', text='Damage')}
a_boxes = {"A":tk.Entry(root, textvariable=a_stats['A']),
           "BS":tk.Entry(root, textvariable=a_stats['BS']),
           "S":tk.Entry(root, textvariable=a_stats['S']),
           "AP":tk.Entry(root, textvariable=a_stats['AP']),
           "D":tk.Entry(root, textvariable=a_stats['D'])}

# Create the section label
attacker_sect_label = tk.Label(root, bg='blue', fg='white', text='==Attacker==', width=50)
attacker_sect_label.place(anchor='n', relx=0.5, rely=0.06)

# Set common box properties and place boxes to be moved later
for i in range(len(a_stat_list)):
    a_boxes[a_stat_list[i]].config(width=5)
    a_stats[a_stat_list[i]].trace_add("write", calculate)
    a_boxes[a_stat_list[i]].place(x=0, y=0)
root.update()

atkY = 0.125
offset = 10
for i in range(len(a_stat_list)):
    a_labels[a_stat_list[i]].place(anchor='w', x=offset, rely=atkY)
    a_boxes[a_stat_list[i]].place(anchor='w', x=offset + a_boxes[a_stat_list[i]].winfo_width()/2 - a_boxes[a_stat_list[i]].winfo_width()/2, rely=atkY+0.04)
    root.update()
    offset += a_labels[a_stat_list[i]].winfo_width() + 20


# Create a listbox of ALL possible properties
all_props = tk.Listbox(root, width=20, height=len(PROPERTIES), selectmode="multiple")
build_all_props_list(all_props)
all_props.place(anchor='nw', relx=0.01, rely=atkY+0.1)

# Create the listbox of selected properties
props = tk.Listbox(root, width=20, height=len(PROPERTIES), selectmode="multiple")
props.place(anchor='ne', relx=0.985, rely=atkY+0.1)

# Create the add and remove properties buttons (--> and <--)
add_button = tk.Button(root, text="☑", font=("Times New Roman", 18), command=add_prop)
add_button.place(anchor='nw', relx=0.3, rely=0.25)

remove_button = tk.Button(root, text="☒", font=("Times New Roman", 18), command=remove_prop)
remove_button.place(anchor='ne', relx=0.695, rely=0.25)

remove_all_button = tk.Button(root, text="☒☒", font=("Times New Roman", 18), command=remove_all)
remove_all_button.place(anchor='ne', relx=0.695, rely=0.325)

# Create the attacker stat list and UI widgets
t_stat_list = ["T", "Sv", "Inv", "W", "M"]
t_stats = {"T":tk.StringVar(root, value=''),
          "Sv":tk.StringVar(root, value=''),
          "Inv":tk.StringVar(root, value=''),
          "W":tk.StringVar(root, value=''),
          "M":tk.StringVar(root, value='')}
t_labels = {"T":tk.Label(root, bg='white', text='Toughness'),
            "Sv":tk.Label(root, bg='white', text='Armor Save'),
            "Inv":tk.Label(root, bg='white', text='Invuln Save'),
            "W":tk.Label(root, bg='white', text='Wounds per Model'),
            "M":tk.Label(root, bg='white', text='# of Models')}
t_boxes = {"T":tk.Entry(root, textvariable=t_stats['T']),
           "Sv":tk.Entry(root, textvariable=t_stats['Sv']),
           "Inv":tk.Entry(root, textvariable=t_stats['Inv']),
           "W":tk.Entry(root, textvariable=t_stats['W']),
           "M":tk.Entry(root, textvariable=t_stats['M'])}

# Create the section label
target_sect_label = tk.Label(root, bg='red', fg='white', text='==Target==', width=50)
target_sect_label.place(anchor='n', relx=0.5, rely=0.6)

# Set common box properties and place boxes to be moved later
for i in range(len(t_stat_list)):
    t_boxes[t_stat_list[i]].config(width=5)
    t_stats[t_stat_list[i]].trace_add("write", calculate)
    t_boxes[t_stat_list[i]].place(x=0, y=0)
root.update()

tgtY = 0.665
offset = 10
for i in range(len(t_stat_list)):
    t_labels[t_stat_list[i]].place(anchor='w', x=offset, rely=tgtY)
    t_boxes[t_stat_list[i]].place(anchor='w', x=offset + t_boxes[t_stat_list[i]].winfo_width()/2 - t_boxes[t_stat_list[i]].winfo_width()/2, rely=tgtY+0.04)
    root.update()
    offset += t_labels[t_stat_list[i]].winfo_width() + 20

"""
TGTY = 0.665
OFFSET = 10

# Create IntVars, labels, and Scales for each TARGET attribute
toughness_num = tk.IntVar(root, value=4)
toughness_label = tk.Label(root, bg='white', text='Toughness')
toughness_box = tk.Spinbox(root, from_=1, to=30, width=1, textvariable=toughness_num, command=calculate)
toughness_label.place(anchor='w', x=OFFSET, rely=TGTY)
toughness_box.place(x=0, y=0)
root.update()
toughness_box.place(anchor='w', x=OFFSET + toughness_label.winfo_width()/2 - toughness_box.winfo_width()/2, rely=TGTY+0.04)

OFFSET += toughness_label.winfo_width() + 15

armor_num = tk.IntVar(root, value=4)
armor_label = tk.Label(root, bg='white', text='Armor Save')
armor_box = tk.Spinbox(root, from_=1, to=30, width=1, textvariable=armor_num, command=calculate)
armor_label.place(anchor='w', x=OFFSET, rely=TGTY)
armor_box.place(x=0, y=0)
root.update()
armor_box.place(anchor='w', x=OFFSET + armor_label.winfo_width()/2 - armor_box.winfo_width()/2, rely=TGTY+0.04)

OFFSET += armor_label.winfo_width() + 15

invuln_num = tk.IntVar(root, value=4)
invuln_label = tk.Label(root, bg='white', text='Invuln Save')
invuln_box = tk.Spinbox(root, from_=1, to=30, width=1, textvariable=invuln_num, command=calculate)
invuln_label.place(anchor='w', x=OFFSET, rely=TGTY)
invuln_box.place(x=0, y=0)
root.update()
invuln_box.place(anchor='w', x=OFFSET + invuln_label.winfo_width()/2 - invuln_box.winfo_width()/2, rely=TGTY+0.04)

OFFSET += invuln_label.winfo_width() + 15

model_wounds_num = tk.IntVar(root, value=4)
model_wounds_label = tk.Label(root, bg='white', text='Wounds')
model_wounds_box = tk.Spinbox(root, from_=1, to=30, width=1, textvariable=model_wounds_num, command=calculate)
model_wounds_label.place(anchor='w', x=OFFSET, rely=TGTY)
model_wounds_box.place(x=0, y=0)
root.update()
model_wounds_box.place(anchor='w', x=OFFSET + model_wounds_label.winfo_width()/2 - model_wounds_box.winfo_width()/2, rely=TGTY+0.04)

OFFSET += model_wounds_label.winfo_width() + 15

num_targets_num = tk.IntVar(root, value=4)
num_targets_label = tk.Label(root, bg='white', text='# of Targets')
num_targets_box = tk.Spinbox(root, from_=1, to=30, width=1, textvariable=num_targets_num, command=calculate)
num_targets_label.place(anchor='w', x=OFFSET, rely=TGTY)
num_targets_box.place(x=0, y=0)
root.update()
num_targets_box.place(anchor='w', x=OFFSET + num_targets_label.winfo_width()/2 - num_targets_box.winfo_width()/2, rely=TGTY+0.04)

OFFSET += num_targets_label.winfo_width() + 15

point_cost_num = tk.IntVar(root, value=4)
point_cost_label = tk.Label(root, bg='white', text='Points per Model')
point_cost_box = tk.Spinbox(root, from_=1, to=30, width=1, textvariable=point_cost_num, command=calculate)
point_cost_label.place(anchor='w', x=OFFSET, rely=TGTY)
point_cost_box.place(x=0, y=0)
root.update()
point_cost_box.place(anchor='w', x=OFFSET + point_cost_label.winfo_width()/2 - point_cost_box.winfo_width()/2, rely=TGTY+0.04)

OFFSET += point_cost_label.winfo_width() + 15
"""

# Show window
root.mainloop()



