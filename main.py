import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import random


def calculate():
    global base_chance, chance_stringvar, props, WA_num, WX_num
    new_chance = base_chance
    props_list = props.get(0, props.size())
    if "Sustained" in props_list:
        new_chance = min(new_chance + 0.125, 1.0)
    if "Reroll 1s" in props_list:
        new_chance = min(new_chance + 0.125, 1.0)

    new_chance += 0.05 * (WA_num.get() - WX_num.get())
    new_chance = max(0, new_chance)
    new_chance = min(0.834, new_chance)

    chance_stringvar.set("Chance: " + str(new_chance))


def build_all_props_list(box):
    global PROPERTIES
    for i in range(4):
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
    global WX_num, WY_num, WZ_num
    WX_num.set(3)
    WY_num.set(3)
    WZ_num.set(1)


def medium_infantry():
    global WX_num, WY_num, WZ_num
    WX_num.set(4)
    WY_num.set(3)
    WZ_num.set(1)
    calculate()


def heavy_infantry():
    global WX_num, WY_num, WZ_num
    WX_num.set(4)
    WY_num.set(4)
    WZ_num.set(2)
    calculate()


def bike():
    global WX_num, WY_num, WZ_num
    WX_num.set(3)
    WY_num.set(5)
    WZ_num.set(2)
    calculate()


def save_to_file():
    global root, WA_num, WB_num, WC_num, WX_num, WY_num, WZ_num, chance_stringvar, props
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
    string = ("\n\n=============================\n" +
              title +
              "\n=============================" +
              "\nChance to damage: " + str(chance_float) + "%" +
              "\nAttacker Profile:" +
              "\nA: " + str(WA_num.get()) +
              "\tB: " + str(WB_num.get()) +
              "\tC: " + str(WC_num.get()) +
              "\n" + properties_string +
              "\n----------------------------" +
              "\nDefender Profile:" +
              "\nX: " + str(WX_num.get()) +
              "\tY: " + str(WY_num.get()) +
              "\tZ: " + str(WZ_num.get()))

    with open("results.txt", "a", encoding="utf-8") as f:
        f.write(string)


base_chance = 0.5
PROPERTIES = {0: "Anti", 1: "Reroll 1s",
              2: "Sustained", 3: "Twin-linked"}

# Create the window
root = tk.Tk()
root.geometry('480x600')

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

# Create the main UI frame
# frame = tk.Frame(root)

# Create the save button
save_button = tk.Button(root, text='Save to File', command=save_to_file)
save_button.place(anchor='nw', relx=0.01, rely=0.004)

# Create the chance output
chance_stringvar = tk.StringVar(root, value=("Chance: " + str(base_chance)))
chance_label = tk.Label(root, bg='white', width=12, anchor='w', textvariable=chance_stringvar)
chance_label.place(anchor='n', relx=0.5, rely=0.01)

# Create the section label
attacker_sect_label = tk.Label(root, bg='blue', fg='white', text='==Attacker==', width=50)
attacker_sect_label.place(anchor='n', relx=0.5, rely=0.06)

# Create IntVars, labels, and Scales for each ATTACKER attribute
WA_num = tk.IntVar(root, value=4)
WA_label = tk.Label(root, bg='white', text='A:')
WA_box = tk.Spinbox(root, from_=1, to=30, width=1, textvariable=WA_num, command=calculate)
WA_label.place(anchor='w', relx=0.01, rely=0.125)
WA_box.place(anchor='w', relx=0.05, rely=0.125)

WB_num = tk.IntVar(root, value=4)
WB_label = tk.Label(root, bg='white', text='B:')
WB_box = tk.Spinbox(root, from_=1, to=30, width=1, textvariable=WB_num, command=calculate)
WB_label.place(anchor='w', relx=0.12, rely=0.125)
WB_box.place(anchor='w', relx=0.16, rely=0.125)

WC_num = tk.IntVar(root, value=4)
WC_label = tk.Label(root, bg='white', text='C:')
WC_box = tk.Spinbox(root, from_=1, to=30, width=1, textvariable=WC_num, command=calculate)
WC_label.place(anchor='w', relx=0.23, rely=0.125)
WC_box.place(anchor='w', relx=0.27, rely=0.125)

# Create a listbox of ALL possible properties
all_props = tk.Listbox(root, width=15, selectmode="multiple")
build_all_props_list(all_props)
all_props.place(anchor='nw', relx=0.01, rely=0.15)

# Create the listbox of selected properties
props = tk.Listbox(root, width=15, selectmode="multiple")
props.place(anchor='ne', relx=0.985, rely=0.15)

# Create the add and remove properties buttons (--> and <--)
add_button = tk.Button(root, text="☑", font=("Times New Roman", 18), command=add_prop)
add_button.place(anchor='nw', relx=0.3, rely=0.25)

remove_button = tk.Button(root, text="☒", font=("Times New Roman", 18), command=remove_prop)
remove_button.place(anchor='ne', relx=0.695, rely=0.25)

remove_all_button = tk.Button(root, text="☒☒", font=("Times New Roman", 18), command=remove_all)
remove_all_button.place(anchor='ne', relx=0.695, rely=0.325)

# Create the section label
target_sect_label = tk.Label(root, bg='red', fg='white', text='==Target==', width=50)
target_sect_label.place(anchor='n', relx=0.5, rely=0.5)

# Create IntVars, labels, and Scales for each TARGET attribute
WX_num = tk.IntVar(root, value=4)
WX_label = tk.Label(root, bg='white', text='X:')
WX_box = tk.Spinbox(root, from_=1, to=30, width=1, textvariable=WX_num, command=calculate)
WX_label.place(anchor='w', relx=0.01, rely=0.565)
WX_box.place(anchor='w', relx=0.05, rely=0.565)

WY_num = tk.IntVar(root, value=4)
WY_label = tk.Label(root, bg='white', text='Y:')
WY_box = tk.Spinbox(root, from_=1, to=30, width=1, textvariable=WY_num, command=calculate)
WY_label.place(anchor='w', relx=0.12, rely=0.565)
WY_box.place(anchor='w', relx=0.16, rely=0.565)

WZ_num = tk.IntVar(root, value=4)
WZ_label = tk.Label(root, bg='white', text='Z:')
WZ_box = tk.Spinbox(root, from_=1, to=30, width=1, textvariable=WZ_num, command=calculate)
WZ_label.place(anchor='w', relx=0.23, rely=0.565)
WZ_box.place(anchor='w', relx=0.27, rely=0.565)

# Show window
root.mainloop()



