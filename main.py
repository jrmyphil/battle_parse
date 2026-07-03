import math
import tkinter as tk
from tkinter import simpledialog

def set_vital_stats(atd, wipe, pointdmg):
    if atd > 0.0:
        avg_total_damage.set(str(atd))
    else:
        avg_total_damage.set("Error")
    if wipe > 0.0:
        shots_to_wipe.set(str(wipe))
    else:
        shots_to_wipe.set("∞")
    if pointdmg > 0.0:
        damage_per_point.set(str(pointdmg))
    else:
        damage_per_point.set("Error")

def parse_random_string(s):
    if s.isdigit():
        return (0, 0, float(s))
    try:
        s = s.upper()
        d_idx = s.find('D')
        plus_idx = s.find('+')
        minus_idx = s.find('-')
        bonus = 0
        if d_idx == 0:
            num_dice = 1
        else:
            num_dice = int(s[:d_idx])
        die_type = int(s[d_idx+1])
        if plus_idx > -1:
            bonus = int(s[plus_idx+1:])
        elif minus_idx > -1:
            bonus = -1 * int(s[minus_idx+1:])

        return [num_dice, die_type, bonus]
    except (IndexError, ValueError):
        return [-1.0, -1.0, -1.0]

def parse_sv_string(s):
    try:
        plus_idx = s.find('+')

        if plus_idx == -1:
            result = float(s)
        else:
            result = float(s[:plus_idx])

        if result < 1 or result > 6:
            result = 7.0

        return result

    except ValueError:
        return 7.0

def parse_ap_string(s):
    try:
        if s == '':
            return 0

        minus_idx = s.find('-')

        if minus_idx == -1:
            result = int(s)
        else:
            result = int(s[minus_idx+1:])

        return max(result, 0)

    except ValueError:
        return 0

def calculate(*args):
    global props
    my_props = props.get(0, tk.END)

    print("==Calculating==")

    # Attacker Stats
    attacks = parse_random_string(a_boxes['A'].get())
    damage = parse_random_string(a_boxes['D'].get())
    BS = parse_sv_string(a_boxes['BS'].get())
    strength = a_boxes['S'].get()
    AP = parse_ap_string(a_boxes['AP'].get())
    points = points_num.get()
    if points.isdigit():
        points = float(points)
    else:
        points = -1.0
    if BS < 7:
        # Adjust for heavy
        if 'Heavy' in my_props and heavy_bool.get():
            BS = max(2.0, (BS - 1))
    if strength.isdigit():
        strength = float(strength)
    else:
        strength = -1.0


    # Target Stats
    toughness = t_boxes['T'].get()
    save = parse_sv_string(t_boxes['Sv'].get())
    invuln = parse_sv_string(t_boxes['Inv'].get())
    wounds = t_boxes['W'].get()
    models = t_boxes['M'].get()
    FNP = parse_sv_string(fnp_num.get())
    if toughness.isdigit():
        toughness = float(toughness)
    else:
        toughness = -1.0
    if wounds.isdigit():
        wounds = float(wounds)
    else:
        wounds = -1.0
    if models.isdigit():
        models = float(models)
    else:
        models = -1.0

    # Make my_props tuple
    my_props = props.get(0, tk.END)

    # Calculate full number of attacks
    blast_x = float(blast_box.get())
    attacks_die_num = attacks[0]
    attacks_die_size = attacks[1]
    attacks_bonus = attacks[2]
    avg_attacks = 0
    blast_bonus = blast_x * (math.floor(models // 5))
    if attacks_die_num == 0:
        avg_attacks += attacks_bonus + blast_bonus
    else:
        if not "Reroll # Attacks" in my_props:
            blasted_attacks = attacks_die_num + blast_bonus
            avg_attacks = blasted_attacks * ((1 + attacks_die_size) / 2) + attacks_bonus
        else:
            blasted_attacks = attacks_die_num + blast_bonus
            avg_roll = (1 + attacks_die_size) / 2
            rerolled_die = 0
            for num in range(1, int(attacks_die_size) + 1):
                if num < avg_roll:
                    rerolled_die += avg_roll
                else:
                    rerolled_die += num
            rerolled_die /= attacks_die_size
            avg_attacks = blasted_attacks * rerolled_die + attacks_bonus

    print(f"avg_attacks: {avg_attacks}")


    # Hit chance calculation
    reroll_1s = 'Reroll 1s to Hit' in my_props
    reroll_misses = 'Reroll All Misses' in my_props
    torrent = 'Torrent' in my_props

    hit_chance = (7 - BS) / 6

    if torrent:
        hit_chance = 1.0
    elif reroll_misses:
        hit_chance += (1 - hit_chance) * hit_chance
    elif reroll_1s:
        hit_chance += (1 / 6) * hit_chance

    # Average number of hits calculation
    crit_target_num = int(crit_num.get())
    sustained_addition = int(sustained_num.get())

    avg_hits = (avg_attacks * hit_chance)
    avg_hits += avg_attacks * (((7 - crit_target_num) / 6) * sustained_addition)

    print(f"avg_hits: {avg_hits}")

    # Wound chance calculation
    twin_linked = 'Twin-Linked' in my_props
    lethal_hits = 'Lethal Hits' in my_props
    anti = 'Anti' in my_props
    anti_target_num = int(anti_num.get())
    lancer = 'Lance' in my_props and lance_bool.get()
    reroll_1s_to_wound = "Reroll 1s to Wound" in my_props

    anti_wound_chance = (7 - anti_target_num) / 6
    wound_chance = 0
    if strength <= (toughness / 2):
        wound_chance = 1 / 6
    elif strength < toughness:
        if lancer:
            wound_chance = 3 / 6
        else:
            wound_chance = 2 / 6
    elif strength == toughness:
        if lancer:
            wound_chance = 4 / 6
        else:
            wound_chance = 3 / 6
    elif strength >= (toughness * 2):
        wound_chance = 5 / 6
    elif strength > toughness:
        if lancer:
            wound_chance = 5 / 6
        else:
            wound_chance = 4 / 6

    if anti and (wound_chance < anti_wound_chance):
        wound_chance = anti_wound_chance

    if twin_linked:
        wound_chance += (1 - wound_chance) * wound_chance
    elif reroll_1s_to_wound:
        wound_chance += (1 / 6) * wound_chance

    if lethal_hits:
        lethal_chance = (7 - crit_target_num) / 6
    else:
        lethal_chance = 0

    wound_chance = max((1/6), min((5/6), wound_chance))

    print(f"wound_chance: {wound_chance}")

    # Average number of wounds calculation
    avg_lethals = lethal_chance * avg_attacks
    hits_minus_auto_wounds = avg_hits - avg_lethals

    # Devastating Wounds addendum
    devastating = "Devastating Wounds" in my_props
    num_devastating_crits = 0
    non_auto_wound_rolls = hits_minus_auto_wounds

    if devastating:
        if anti:
            num_devastating_crits = hits_minus_auto_wounds * ((7 - anti_target_num) / 6)
            non_auto_wound_rolls = hits_minus_auto_wounds * ((anti_target_num - 1) / 6)
        else:
            num_devastating_crits = hits_minus_auto_wounds * (1 / 6)
            non_auto_wound_rolls = hits_minus_auto_wounds * (5 / 6)

    saveable_wounds = (non_auto_wound_rolls + avg_lethals) * wound_chance
    print(f"saveable_wounds: {saveable_wounds}")

    # Save calculations
    save_target_num = min((save + AP), invuln)
    save_chance = (7 - save_target_num) / 6
    save_failure_chance = 1.0 - save_chance
    print(f"save_failure_chance: {save_failure_chance}")
    FNP_chance = (7 - FNP) / 6
    FNP_failure_chance = 1.0 - FNP_chance
    total_unsaved_attacks = (saveable_wounds * save_failure_chance) + num_devastating_crits
    print(f"FNP_failure_chance: {FNP_failure_chance}")
    print(f"total_unsaved_attacks: {total_unsaved_attacks}")

    # Damage calculations
    melta = 'Melta' in my_props
    damage_die_num = damage[0]
    damage_die_size = damage[1]
    damage_bonus = damage[2]
    if melta:
        damage_bonus += int(melta_num.get())
    if damage_die_size > 0:
        avg_d_stat = damage_die_num + ((damage_die_size + 1) / 2) + damage_bonus
    else:
        avg_d_stat = damage_bonus
    damage_after_FNP = avg_d_stat * FNP_failure_chance
    print(f"avg_d_stat: {avg_d_stat}")

    # Full damage calculations (iterative)
    full_damage = 0.0
    models_remaining = models
    current_model_wounds = wounds
    for hit in range(int(total_unsaved_attacks)):
        full_damage += min(damage_after_FNP, current_model_wounds)
        current_model_wounds -= damage_after_FNP
        if current_model_wounds <= 0:
            current_model_wounds = wounds
            models_remaining -= 1
            if models_remaining == 0:
                break

    fractional_attack = total_unsaved_attacks % 1.0
    if models_remaining > 0 and fractional_attack > 0:
        fractional_damage = fractional_attack * min(damage_after_FNP, current_model_wounds)
        full_damage += fractional_damage
        current_model_wounds -= fractional_damage
        if current_model_wounds <= 0:
            models_remaining -= 1

    print(f"full_damage: {full_damage}")

    # Rounds to Wipe calculation
    rounds_to_wipe = 0.0
    try:
        kills_per_round = models - models_remaining
        print(f"--models: {models}")
        print(f"--models_remaining: {models_remaining}")
        print(f"--kills_per_round: {kills_per_round}")
        rounds_to_wipe = models // kills_per_round
        if models % kills_per_round > 0:
            rounds_to_wipe += 1.0
    except:
        rounds_to_wipe = -1.0
    print(f"--rounds_to_wipe: {rounds_to_wipe}")
    # Points per Damage calculation
    if points > 0:
        points_per_damage = full_damage / points
    else:
        points_per_damage = -1.0

    # Set vital stats
    full_damage = round(full_damage, 2)
    points_per_damage = round(points_per_damage, 2)
    try:
        set_vital_stats(full_damage, rounds_to_wipe, points_per_damage)
    except:
        set_vital_stats(-1.0, -1.0, -1.0)


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
    if 'Anti' in prop_names:
        anti_label.place(relx=0.26, y=305)
        anti_box.place(relx=0.38, y=307)
    if 'Blast/Cleave' in prop_names:
        blast_label.place(relx=0.50, y=305)
        blast_box.place(relx=0.681, y=307)
    if 'Melta' in prop_names:
        melta_num.set('1')
        melta_label.place(relx=0.26, y=332)
        melta_box.place(relx=0.38, y=334)
    if 'Crit X+' in prop_names:
        crit_label.place(relx=0.59, y=332)
        crit_box.place(relx=0.681, y=334)
    if 'Heavy' in prop_names:
        heavy_label.place(relx=0.258, y=359)
        heavy_box.place(relx=0.37, y=358)
    if 'Sustained Hits' in prop_names:
        sustained_label.place(relx=0.48, y=359)
        sustained_box.place(relx=0.681, y=361)
    if 'Lance' in prop_names:
        lance_label.place(relx=0.258, y=386)
        lance_box.place(relx=0.37, y=385)
    calculate()


def remove_prop():
    global props
    selected_key = props.curselection()[0]
    props.delete(selected_key)
    my_props = props.get(0, tk.END)
    if not 'Anti' in my_props:
        anti_label.place_forget()
        anti_box.place_forget()
        anti_num.set('0')
    if not 'Melta' in my_props:
        melta_label.place_forget()
        melta_box.place_forget()
        melta_num.set('0')
    if not 'Heavy' in my_props:
        heavy_label.place_forget()
        heavy_box.place_forget()
        heavy_bool.set(False)
    if not 'Lance' in my_props:
        lance_label.place_forget()
        lance_box.place_forget()
        lance_bool.set(False)
    if not 'Blast/Cleave' in my_props:
        blast_label.place_forget()
        blast_box.place_forget()
        blast_num.set('0')
    if not 'Crit X+' in my_props:
        crit_label.place_forget()
        crit_box.place_forget()
        crit_num.set('6')
    if not 'Sustained Hits' in my_props:
        sustained_label.place_forget()
        sustained_box.place_forget()
        sustained_num.set('0')
    calculate()


def remove_all():
    global props, blast_label, blast_box, blast_num
    props.delete(0, 'end')
    anti_label.place_forget()
    anti_box.place_forget()
    anti_num.set('0')
    melta_label.place_forget()
    melta_box.place_forget()
    melta_num.set('0')
    heavy_label.place_forget()
    heavy_box.place_forget()
    heavy_bool.set(False)
    lance_label.place_forget()
    lance_box.place_forget()
    lance_bool.set(False)
    blast_label.place_forget()
    blast_box.place_forget()
    blast_num.set('0')
    crit_label.place_forget()
    crit_box.place_forget()
    crit_num.set('6')
    sustained_label.place_forget()
    sustained_box.place_forget()
    sustained_num.set('0')
    calculate()

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
    t_boxes['T'].delete(0, tk.END)
    t_boxes['T'].insert(0, '3')
    t_boxes['Sv'].delete(0, tk.END)
    t_boxes['Sv'].insert(0, '4+')
    t_boxes['Inv'].delete(0, tk.END)
    t_boxes['Inv'].insert(0, '')
    t_boxes['W'].delete(0, tk.END)
    t_boxes['W'].insert(0, '1')
    t_boxes['M'].delete(0, tk.END)
    t_boxes['M'].insert(0, '10')
    a_boxes['A'].delete(0, tk.END)
    a_boxes['A'].insert(0, '1')
    a_boxes['BS'].delete(0, tk.END)
    a_boxes['BS'].insert(0, '4+')
    a_boxes['S'].delete(0, tk.END)
    a_boxes['S'].insert(0, '3')
    a_boxes['AP'].delete(0, tk.END)
    a_boxes['AP'].insert(0, '0')
    a_boxes['D'].delete(0, tk.END)
    a_boxes['D'].insert(0, '1')
    calculate()

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
PROPERTIES = {0:"Anti", 1:"Blast/Cleave", 2:"Crit X+", 3:"Devastating Wounds", 4:"Heavy", 5: "Lance",
              6:"Lethal Hits", 7:"Melta", 8:"Reroll # Attacks", 9:"Reroll 1s to Hit", 10:"Reroll 1s to Wound",
              11:"Reroll All Misses", 12:"Sustained Hits", 13:"Torrent", 14:"Twin-Linked"}

# Create the window
root = tk.Tk()
root.geometry('510x800')

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
save_button.place(anchor='nw', x=4, y=3)

# Create the section label
vital_stats_sect_label = tk.Label(root, bg='black', fg='white', text='==Vital Stats==', width=50)
vital_stats_sect_label.place(anchor='n', relx=0.5, y=650)

# Create the vital stats and output labels for them
avg_total_damage_title = tk.Label(root, text="Avg Total Damage:", bg='black', fg='white', width=28, anchor='w')
avg_total_damage_title.place(anchor='nw', x=10, y=680)
avg_total_damage = tk.StringVar(root, value="0.0")
avg_total_damage_label = tk.Label(root, bg='black', fg='white', width=6, anchor='e', textvariable=avg_total_damage)
avg_total_damage_label.place(anchor='nw', x=160, y=680)

shots_to_wipe_title = tk.Label(root, text="Avg Rounds to Wipe Unit:", bg='black', fg='white', width=28, anchor='w')
shots_to_wipe_title.place(anchor='nw', x=10, y=704)
shots_to_wipe = tk.StringVar(root, value="0.0")
shots_to_wipe_label = tk.Label(root, bg='black', fg='white', width=6, anchor='e', textvariable=shots_to_wipe)
shots_to_wipe_label.place(anchor='nw', x=160, y=704)

damage_per_point_title = tk.Label(root, text="Avg Damage per Point:", bg='black', fg='white', width=28, anchor='w')
damage_per_point_title.place(anchor='nw', x=10, y=728)
damage_per_point = tk.StringVar(root, value="0.0")
damage_per_point_label = tk.Label(root, bg='black', fg='white', width=6, anchor='e', textvariable=damage_per_point)
damage_per_point_label.place(anchor='nw', x=160, y=728)

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
attacker_sect_label.place(anchor='n', relx=0.5, y=36)

# Set common box properties and place boxes to be moved later
for i in range(len(a_stat_list)):
    a_boxes[a_stat_list[i]].config(width=5)
    a_stats[a_stat_list[i]].trace_add("write", calculate)
    a_boxes[a_stat_list[i]].place(x=0, y=0)
root.update()

atkY = 75
offset = 10
for i in range(len(a_stat_list)):
    a_labels[a_stat_list[i]].place(anchor='w', x=offset, y=atkY)
    a_boxes[a_stat_list[i]].place(anchor='w', x=offset, y=atkY+24)
    root.update()
    offset += a_labels[a_stat_list[i]].winfo_width() + 64

points_num = tk.StringVar(root, value='')
points_num.trace_add("write", calculate)
points_label = tk.Label(root, bg='white', text='Points Per Model')
points_box = tk.Entry(root, textvariable=points_num, width=5)
points_label.place(anchor='w', x=10, y=atkY+52)
points_box.place(anchor='w', x=10, y=atkY+76)

# Create a listbox of ALL possible properties
all_props = tk.Listbox(root, width=20, height=len(PROPERTIES), selectmode="multiple")
build_all_props_list(all_props)
all_props.place(anchor='nw', x=6, y=atkY+100)

# Create the listbox of selected properties
props = tk.Listbox(root, width=20, height=len(PROPERTIES), selectmode="multiple")
props.place(anchor='ne', x=500, y=atkY+100)

# Create the add and remove properties buttons (--> and <--)
add_button = tk.Button(root, text="Add -->", font=("Times New Roman", 12), command=add_prop)
add_button.place(anchor='nw', x=132, y=atkY+100)

remove_button = tk.Button(root, text="<-- Remove", font=("Times New Roman", 12), command=remove_prop)
remove_button.place(anchor='ne', x=375, y=atkY+100)

remove_all_button = tk.Button(root, text="<-- Remove All", font=("Times New Roman", 12), command=remove_all)
remove_all_button.place(anchor='ne', x=375, y=atkY+135)

anti_label = tk.Label(root, text="Anti X = ")
anti_num = tk.StringVar(root, value='0')
anti_box = tk.Spinbox(root, width=1, textvariable=anti_num, command=calculate, from_=1, to=6)

blast_label = tk.Label(root, text="Blast/Cleave X = ")
blast_num = tk.StringVar(root, value='0')
blast_box = tk.Spinbox(root, width=1, textvariable=blast_num, command=calculate, from_=0, to=9)

crit_label = tk.Label(root, text="Crit X = ")
crit_num = tk.StringVar(root, value='6')
crit_box = tk.Spinbox(root, width=1, textvariable=crit_num, command=calculate, from_=1, to=6)

heavy_label = tk.Label(root, text="Stationary: ")
heavy_bool = tk.BooleanVar(root, value=False)
heavy_box = tk.Checkbutton(root, variable=heavy_bool, onvalue=True, offvalue=False, command=calculate)

lance_label = tk.Label(root, text="Charging: ")
lance_bool = tk.BooleanVar(root, value=False)
lance_box = tk.Checkbutton(root, variable=lance_bool, onvalue=True, offvalue=False, command=calculate)

sustained_label = tk.Label(root, text="Sustained Hits X = ")
sustained_num = tk.StringVar(root, value='0')
sustained_box = tk.Spinbox(root, width=1, textvariable=sustained_num, command=calculate, from_=0, to=9)

melta_label = tk.Label(root, text="Melta X = ")
melta_num = tk.StringVar(root, value='0')
melta_box = tk.Spinbox(root, width=1, textvariable=melta_num, command=calculate, from_=1, to=9)

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
target_sect_label.place(anchor='n', relx=0.5, y=460)

# Set common box properties and place boxes to be moved later
for i in range(len(t_stat_list)):
    t_boxes[t_stat_list[i]].config(width=5)
    t_stats[t_stat_list[i]].trace_add("write", calculate)
    t_boxes[t_stat_list[i]].place(x=0, y=0)
root.update()

tgtY = 500
offset = 10
for i in range(len(t_stat_list)):
    t_labels[t_stat_list[i]].place(anchor='w', x=offset, y=tgtY)
    t_boxes[t_stat_list[i]].place(anchor='w', x=offset, y=tgtY+24)
    root.update()
    offset += t_labels[t_stat_list[i]].winfo_width() + 24

fnp_label = tk.Label(root, bg='white', text='Feel No Pain')
fnp_num = tk.StringVar(root, value='')
fnp_num.trace_add("write", calculate)
fnp_box = tk.Entry(root, textvariable=fnp_num, width=5)
fnp_label.place(anchor='w', x=10, y=tgtY+60)
fnp_box.place(anchor='w', x=10, y=tgtY+84)

# Show window
root.mainloop()