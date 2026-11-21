

import random, json, os, time

SAVE_FILE = "savegame.json"

RARITY = {
    "Common":     {"mult": 1.0, "crit": 0},
    "Uncommon":   {"mult": 1.1, "crit": 2},
    "Rare":       {"mult": 1.3, "crit": 5},
    "Super Rare": {"mult": 1.5, "crit": 8},
    "Epic":       {"mult": 1.8, "crit": 12},
    "Mythical":   {"mult": 2.2, "crit": 18},
    "Legendary":  {"mult": 2.8, "crit": 25},
}

CLASSES = {
    "1": {"name": "Warrior",  "hp": 150, "mana": 40,  "atk": 22, "def": 14, "crit": 10,
          "skills": [("Slash", 10, 1.5), ("Shield Bash", 15, 1.8), ("Rage", 25, 2.4), ("Earthquake", 40, 3.2)]},
    "2": {"name": "Mage",     "hp": 100, "mana": 120, "atk": 26, "def": 6,  "crit": 15,
          "skills": [("Fireball", 15, 1.7), ("Ice Blast", 20, 2.0), ("Thunder Strike", 30, 2.6), ("Meteor", 50, 3.8)]},
    "3": {"name": "Archer",   "hp": 110, "mana": 70,  "atk": 20, "def": 9,  "crit": 25,
          "skills": [("Multi Shot", 12, 1.6), ("Poison Arrow", 18, 1.9), ("Explosive Arrow", 28, 2.5), ("Sniper Shot", 45, 3.5)]},
    "4": {"name": "Assassin", "hp": 85,  "mana": 80,  "atk": 28, "def": 5,  "crit": 35,
          "skills": [("Backstab", 12, 1.8), ("Smoke Bomb", 18, 2.1), ("Shadow Strike", 30, 2.8), ("Instant Kill", 60, 5.0)]},
}

WEAPONS = [
    ("Wooden Sword","Common",12,1,50), ("Rusty Axe","Common",14,1,60), ("Training Bow","Common",11,1,50),
    ("Iron Sword","Uncommon",18,5,150), ("Steel Axe","Uncommon",20,5,170), ("Hunter Bow","Uncommon",17,5,160),
    ("Iron Sword+","Rare",26,10,350), ("Steel Axe+","Rare",28,10,380), ("Long Bow","Rare",25,10,340),
    ("Crystal Blade","Super Rare",38,15,800), ("Shadow Dagger","Super Rare",40,15,850), ("Lightning Bow","Super Rare",37,15,820),
    ("Flame Sword","Epic",52,20,1500), ("Ice Spear","Epic",54,20,1550), ("Thunder Hammer","Epic",58,20,1650),
    ("Phoenix Blade","Mythical",75,30,3000), ("Demon Slayer","Mythical",80,30,3200), ("Celestial Staff","Mythical",78,30,3100),
    ("Dragon King's Sword","Legendary",110,40,6000), ("Blade of Eternity","Legendary",120,40,7000), ("Bow of the Gods","Legendary",115,40,6500),
]

ARMORS = [
    ("Leather Armor","Common",5,20,10,0,80), ("Cloth Robe","Common",3,10,30,0,70),
    ("Iron Armor","Uncommon",9,35,10,2,200), ("Mage Robe","Uncommon",5,20,50,2,220),
    ("Steel Plate","Rare",14,60,10,5,500), ("Shadow Cloak","Rare",8,30,40,8,550),
    ("Crystal Armor","Super Rare",20,90,30,10,1100), ("Dragon Scale","Super Rare",22,100,20,10,1200),
    ("Flame Armor","Epic",28,140,40,15,2000), ("Frost Armor","Epic",30,130,50,15,2100),
    ("Phoenix Armor","Mythical",40,200,80,20,4000), ("Celestial Armor","Mythical",42,190,100,20,4200),
    ("Armor of Eternity","Legendary",55,300,150,30,8000), ("Godslayer Armor","Legendary",60,280,120,30,8500),
]

POTIONS = {
    "Small HP Potion": ("hp",50,30), "Medium HP Potion": ("hp",100,60), "Large HP Potion": ("hp",250,120),
    "Giant HP Potion": ("hp",500,220), "Ultimate HP Potion": ("hp",9999,400),
    "Small Mana Potion": ("mana",30,25), "Medium Mana Potion": ("mana",75,50), "Large Mana Potion": ("mana",150,100),
    "Giant Mana Potion": ("mana",300,180), "Ultimate Mana Potion": ("mana",9999,350),
    "Mixed Potion S": ("both",60,70), "Mixed Potion L": ("both",200,160), "Mixed Potion X": ("both",9999,500),
    "Attack Buff Potion": ("atk_buff",0,150), "Defense Buff Potion": ("def_buff",0,150), "Crit Buff Potion": ("crit_buff",0,150),
}

ENEMIES = [
    ("Goblin",1),("Wolf",1),("Slime",1),("Zombie",1),("Skeleton",1),
    ("Orc",11),("Bandit",11),("Troll",11),("Dark Archer",11),("Giant Spider",11),
    ("Vampire",21),("Werewolf",21),("Necromancer",21),("Ice Golem",21),("Fire Demon",21),
    ("Desert Scorpion",31),("Sand Wraith",31),("Ruins Guardian",41),("Stone Golem",41),
    ("Dark Knight",51),("Castle Mage",51),("Lava Beast",61),("Fire Dragonling",61),
    ("Frost Wolf",71),("Yeti",71),("Sky Serpent",81),("Storm Eagle",81),
    ("Demon Imp",91),("Hell Hound",91),("Chaos Fiend",95),
]

BOSSES = [
    (10,"Goblin King"),(20,"Forest Guardian"),(30,"Ancient Golem"),(40,"Vampire Lord"),
    (50,"Dragon Rider"),(60,"Demon General"),(70,"Ice Titan"),(80,"Shadow Emperor"),
    (90,"Celestial Dragon"),(100,"Ancient Demon King"),
]

REGIONS = ["Village","Forest","Cave","Desert","Ruins","Castle","Volcano","Frozen Mountain","Sky Temple","Demon Realm"]

def ask(prompt):
    return input(prompt).strip()

def ask_int(prompt, low, high):
    while True:
        try:
            v = int(input(prompt))
            if low <= v <= high: return v
            print(f"Enter {low} to {high} only!")
        except ValueError:
            print("Please enter a number only!")

def pause():
    input("\nPress Enter to continue...")

def new_player():
    print("\n=== LEGENDS OF THE FORGOTTEN REALM ===")
    print("Eldoria has fallen into darkness. Defeat bosses, reach Level 100, kill Ancient Demon King.")
    name = ask("Enter Player Name: ")
    if not name: name = "Hero"
    print("\nChoose Your Class:")
    for k,v in CLASSES.items(): print(f"{k}. {v['name']} - HP:{v['hp']} Mana:{v['mana']} ATK:{v['atk']} DEF:{v['def']} Crit:{v['crit']}%")
    c = str(ask_int("Choice: ",1,4))
    base = CLASSES[c]
    p = {"name":name,"class":base["name"],"level":1,"exp":0,"exp_next":100,
         "max_hp":base["hp"],"hp":base["hp"],"max_mana":base["mana"],"mana":base["mana"],
         "atk":base["atk"],"def":base["def"],"crit":base["crit"],"crit_dmg":2.0,
         "gold":100,"weapon":WEAPONS[0],"armor":ARMORS[0],
         "potions":{"Small HP Potion":2,"Small Mana Potion":1},
         "inventory":[],"bosses_defeated":[],"enemies_defeated":0,"weapons_collected":1,
         "region":0,"buff_turns":0,"buff_type":None,"play_time":0}
    return p

def save_game(p):
    try:
        # Convert tuple to list for JSON
        p2 = dict(p); p2["weapon"]=list(p["weapon"]); p2["armor"]=list(p["armor"])
        with open(SAVE_FILE,"w") as f: json.dump(p2,f,indent=2)
        print("Game Saved!")
    except Exception as e: print("Save failed:",e)

def load_game():
    try:
        with open(SAVE_FILE) as f: p=json.load(f)
        p["weapon"]=tuple(p["weapon"]); p["armor"]=tuple(p["armor"])
        print(f"Welcome back, {p['name']}! Level {p['level']}")
        return p
    except FileNotFoundError:
        print("No save found!")
        return None
    except Exception as e:
        print("Load failed:",e); return None

def show_stats(p):
    print(f"\n--- {p['name']} | {p['class']} | Lv {p['level']} ---")
    print(f"HP: {p['hp']}/{p['max_hp']}  Mana: {p['mana']}/{p['max_mana']}")
    print(f"ATK: {p['atk']}  DEF: {p['def']}  Crit: {p['crit']}%  Gold: {p['gold']}")
    print(f"EXP: {p['exp']}/{p['exp_next']}  Region: {REGIONS[p['region']]}")
    print(f"Weapon: {p['weapon'][0]} [{p['weapon'][1]}] +{p['weapon'][2]} DMG")
    print(f"Armor: {p['armor'][0]} [{p['armor'][1]}] +{p['armor'][2]} DEF")
    print(f"Enemies: {p['enemies_defeated']}  Bosses: {len(p['bosses_defeated'])}")

def level_up(p):
    while p["exp"] >= p["exp_next"]:
        p["exp"] -= p["exp_next"]; p["level"] += 1
        p["exp_next"] = int(p["exp_next"]*1.4)+50
        p["max_hp"]+=20; p["max_mana"]+=10; p["atk"]+=4; p["def"]+=2
        p["hp"]=p["max_hp"]; p["mana"]=p["max_mana"]
        print(f"\n*** LEVEL UP! You are now Level {p['level']} ***")
        if p["level"]%5==0:
            p["crit"]+=2; print("Passive unlocked: +2% Crit Chance!")
        # Boss check
        for lvl,boss in BOSSES:
            if p["level"]>=lvl and boss not in p["bosses_defeated"]:
                print(f"\n!!! BOSS UNLOCKED: {boss} (Level {lvl}) !!! Defeat it to unlock next region.")
                break

def get_weapon_damage(p):
    base = p["weapon"][2]
    mult = RARITY[p["weapon"][1]]["mult"]
    return int(base*mult)

def use_potion(p, name=None):
    if not p["potions"]:
        print("No potions!"); return False
    if name is None:
        print("\nPotions:")
        items=list(p["potions"].items())
        for i,(k,v) in enumerate(items,1): print(f"{i}. {k} x{v}")
        print("0. Back")
        ch=ask_int("Choice: ",0,len(items))
        if ch==0: return False
        name=items[ch-1][0]
    if p["potions"].get(name,0)<=0:
        print("You don't have that!"); return False
    p["potions"][name]-=1
    if p["potions"][name]==0: del p["potions"][name]
    kind,val,_ = POTIONS[name]
    if kind=="hp": p["hp"]=min(p["max_hp"],p["hp"]+val); print(f"+{val} HP! HP: {p['hp']}/{p['max_hp']}")
    elif kind=="mana": p["mana"]=min(p["max_mana"],p["mana"]+val); print(f"+{val} Mana!")
    elif kind=="both": p["hp"]=p["max_hp"]; p["mana"]=p["max_mana"]; print("Full HP + Mana restored!")
    elif kind=="atk_buff": p["buff_type"]="atk"; p["buff_turns"]=3; print("Attack buff for 3 turns!")
    elif kind=="def_buff": p["buff_type"]="def"; p["buff_turns"]=3; print("Defense buff for 3 turns!")
    elif kind=="crit_buff": p["buff_type"]="crit"; p["buff_turns"]=3; print("Crit buff for 3 turns!")
    return True

def roll_loot(p, is_boss=False):
    # Rarity chances from PDF: Common 50, Uncommon 25, Rare 15, Super 6, Epic 3, Mythical 0.9, Legendary 0.1
    r=random.random()*100
    if r<50: rank="Common"
    elif r<75: rank="Uncommon"
    elif r<90: rank="Rare"
    elif r<96: rank="Super Rare"
    elif r<99: rank="Epic"
    elif r<99.9: rank="Mythical"
    else: rank="Legendary"
    if is_boss and rank in ("Common","Uncommon"): rank="Rare"
    gold = random.randint(20,60)+p["level"]*5
    if is_boss: gold*=5
    p["gold"]+=gold
    print(f"Loot: +{gold} Gold")
    # 30% weapon/armor drop
    if random.random()<0.35 or is_boss:
        pool=[w for w in WEAPONS if w[1]==rank] or WEAPONS
        w=random.choice(pool)
        p["inventory"].append(("weapon",w)); print(f"Found Weapon: {w[0]} [{w[1]}]")
        p["weapons_collected"]+=1
    if random.random()<0.25 or is_boss:
        pool=[a for a in ARMORS if a[1]==rank] or ARMORS
        a=random.choice(pool)
        p["inventory"].append(("armor",a)); print(f"Found Armor: {a[0]} [{a[1]}]")
    if random.random()<0.5:
        pot=random.choice(list(POTIONS.keys()))
        p["potions"][pot]=p["potions"].get(pot,0)+1
        print(f"Found Potion: {pot}")

def battle(p, enemy_name, enemy_hp, enemy_atk, enemy_def, is_boss=False):
    print(f"\n{'='*40}\n{'BOSS BATTLE!' if is_boss else 'WILD BATTLE!'} {enemy_name}\nHP: {enemy_hp} ATK: {enemy_atk} DEF: {enemy_def}\n{'='*40}")
    defending=False; turn=1
    # Class skills
    skills = next(v["skills"] for v in CLASSES.values() if v["name"]==p["class"])
    while True:
        print(f"\n--- YOUR TURN (Turn {turn}) ---")
        print(f"You: HP {p['hp']}/{p['max_hp']} Mana {p['mana']}/{p['max_mana']} | {enemy_name}: HP {enemy_hp}")
        print("1 Attack  2 Skills  3 Heal  4 Use Potion  5 Defend  6 Inventory  7 View Stats  8 Run")
        ch=ask_int("Choice: ",1,8)
        dmg=0; used_turn=True
        atk_bonus = 5 if p.get("buff_type")=="atk" and p["buff_turns"]>0 else 0
        crit_bonus = 15 if p.get("buff_type")=="crit" and p["buff_turns"]>0 else 0
        if ch==1:
            dmg = max(1, p["atk"]+atk_bonus+get_weapon_damage(p)-enemy_def)
        elif ch==2:
            print("\nSkills:")
            for i,(n,c,m) in enumerate(skills,1): print(f"{i}. {n} - Mana {c} - x{m} DMG")
            print("0. Back")
            s=ask_int("Choice: ",0,len(skills))
            if s==0: continue
            n,c,m = skills[s-1]
            if p["mana"]<c: print("Not enough mana!"); continue
            p["mana"]-=c
            if n=="Instant Kill" and random.random()<0.08:
                print("INSTANT KILL!!!"); enemy_hp=0; dmg=0
            else:
                dmg=int(max(1,p["atk"]+get_weapon_damage(p)-enemy_def)*m)
            print(f"Used {n}!")
        elif ch==3:
            heal=int(p["max_hp"]*0.25); p["hp"]=min(p["max_hp"],p["hp"]+heal)
            print(f"Healed +{heal} HP!"); dmg=0
        elif ch==4:
            if not use_potion(p): continue
            dmg=0
        elif ch==5:
            defending=True; print("You defend! Next damage -50%"); dmg=0
        elif ch==6:
            show_inventory(p); continue
        elif ch==7:
            show_stats(p); continue
        elif ch==8:
            if is_boss: print("Cannot run from Boss!"); continue
            if random.random()<0.5: print("You escaped!"); return "run"
            else: print("Failed to run!")

        # Crit roll
        if dmg>0:
            total_crit = p["crit"]+crit_bonus+RARITY[p["weapon"][1]]["crit"]
            if random.random()*100 < total_crit:
                dmg=int(dmg*p["crit_dmg"]); print(f"CRITICAL HIT! You dealt {dmg} Damage!")
            else: print(f"You dealt {dmg} Damage!")
            enemy_hp-=dmg

        if enemy_hp<=0:
            print(f"\n*** You defeated {enemy_name}! ***")
            exp_gain = (20+p["level"]*10)*(5 if is_boss else 1)
            p["exp"]+=exp_gain; p["enemies_defeated"]+=1
            print(f"+{exp_gain} EXP")
            roll_loot(p,is_boss)
            if is_boss and enemy_name not in p["bosses_defeated"]:
                p["bosses_defeated"].append(enemy_name)
                if p["region"]<len(REGIONS)-1: p["region"]+=1
                print(f"Region Unlocked: {REGIONS[p['region']]}!")
                if enemy_name=="Ancient Demon King":
                    victory(p); return "victory"
            level_up(p); save_game(p); return "win"

        # Enemy turn
        if turn%3==0 and is_boss:
            print(f"{enemy_name} uses SPECIAL ATTACK!")
            e_dmg=int(enemy_atk*1.8)
        else:
            e_dmg=max(1, enemy_atk - p["def"] - p["armor"][2]//3)
            if is_boss and random.random()<0.2:
                enemy_hp+=30; print(f"{enemy_name} heals +30 HP!")
        if defending:
            e_dmg//=2; defending=False
        if p.get("buff_type")=="def" and p["buff_turns"]>0: e_dmg=max(1,e_dmg-5)
        p["hp"]-=e_dmg
        print(f"{enemy_name} dealt {e_dmg} damage! Your HP: {max(0,p['hp'])}/{p['max_hp']}")
        if p["buff_turns"]>0: p["buff_turns"]-=1
        if p["hp"]<=0:
            print("\nGAME OVER! You died.")
            print("1 Retry (Full HP)  2 Load Save  3 Exit")
            c=ask_int("Choice: ",1,3)
            if c==1: p["hp"]=p["max_hp"]; p["mana"]=p["max_mana"]; return "retry"
            elif c==2:
                loaded=load_game()
                if loaded: p.clear(); p.update(loaded)
                return "load"
            else: return "exit"
        turn+=1

def show_inventory(p):
    print("\n--- INVENTORY ---")
    if not p["inventory"] and not p["potions"]: print("Empty!"); return
    for i,(typ,item) in enumerate(p["inventory"],1):
        print(f"{i}. [{typ}] {item[0]} [{item[1]}] Price:{item[-1] if typ=='weapon' else item[-1]}")
    print("\nPotions:", p["potions"])
    print("1 Equip Item  2 Sell Item  3 Drop Item  0 Back")
    ch=ask_int("Choice: ",0,3)
    if ch==0 or not p["inventory"]: return
    idx=ask_int(f"Item number (1-{len(p['inventory'])}): ",1,len(p["inventory"]))-1
    typ,item = p["inventory"][idx]
    if ch==1:
        if typ=="weapon":
            if p["level"] < item[3]: print(f"Need Level {item[3]}!"); return
            p["inventory"].append(("weapon",p["weapon"])); p["weapon"]=item
        else:
            p["inventory"].append(("armor",p["armor"])); p["armor"]=item
        p["inventory"].pop(idx); print(f"Equipped {item[0]}!")
    elif ch==2:
        price=item[4]//2 if typ=="weapon" else item[6]//2
        p["gold"]+=price; p["inventory"].pop(idx); print(f"Sold for {price} Gold!")
    elif ch==3:
        p["inventory"].pop(idx); print("Dropped!")

def shop(p):
    while True:
        print(f"\n--- VILLAGE SHOP | Gold: {p['gold']} ---")
        print("1 Buy Weapon  2 Buy Armor  3 Buy Potion  4 Sell Item  0 Exit Shop")
        ch=ask_int("Choice: ",0,4)
        if ch==0: break
        if ch==1:
            avail=[w for w in WEAPONS if w[3]<=p["level"]+5]
            for i,w in enumerate(avail,1): print(f"{i}. {w[0]} [{w[1]}] DMG {w[2]} Lv {w[3]} - {w[4]} Gold")
            idx=ask_int("Buy (0=back): ",0,len(avail))
            if idx==0: continue
            w=avail[idx-1]
            if p["gold"]<w[4]: print("Not enough gold!")
            else: p["gold"]-=w[4]; p["inventory"].append(("weapon",w)); print(f"Bought {w[0]}!")
        elif ch==2:
            for i,a in enumerate(ARMORS,1): print(f"{i}. {a[0]} [{a[1]}] DEF {a[2]} HP+{a[3]} - {a[6]} Gold")
            idx=ask_int("Buy (0=back): ",0,len(ARMORS))
            if idx==0: continue
            a=ARMORS[idx-1]
            if p["gold"]<a[6]: print("Not enough gold!")
            else: p["gold"]-=a[6]; p["inventory"].append(("armor",a)); print(f"Bought {a[0]}!")
        elif ch==3:
            items=list(POTIONS.items())
            for i,(n,(k,v,pr)) in enumerate(items,1): print(f"{i}. {n} - {pr} Gold")
            idx=ask_int("Buy (0=back): ",0,len(items))
            if idx==0: continue
            n,(k,v,pr)=items[idx-1]
            if p["gold"]<pr: print("Not enough gold!")
            else: p["gold"]-=pr; p["potions"][n]=p["potions"].get(n,0)+1; print(f"Bought {n}!")
        elif ch==4: show_inventory(p)

def explore(p):
    # Enemy scaling by player level
    pool=[e for e in ENEMIES if e[1]<=p["level"]+10]
    name,base = random.choice(pool)
    e_hp = 40 + p["level"]*18 + random.randint(0,20)
    e_atk = 8 + p["level"]*2 + random.randint(0,5)
    e_def = 2 + p["level"]//2
    return battle(p,name,e_hp,e_atk,e_def,False)

def boss_battle(p):
    # Find next boss
    for lvl,boss in BOSSES:
        if boss not in p["bosses_defeated"]:
            if p["level"]<lvl:
                print(f"Next Boss: {boss} at Level {lvl}. You are Level {p['level']}. Grind more!")
                return
            e_hp=200+lvl*25; e_atk=15+lvl*2; e_def=5+lvl//2
            battle(p,boss,e_hp,e_atk,e_def,True)
            return
    print("All bosses defeated!")

def victory(p):
    print("\n"+"="*50)
    print("VICTORY! ANCIENT DEMON KING DEFEATED!")
    print("Eldoria is free! You are a LEGEND!")
    print(f"Player: {p['name']} | Final Level: {p['level']} | Gold: {p['gold']}")
    print(f"Bosses: {len(p['bosses_defeated'])} | Enemies: {p['enemies_defeated']} | Weapons: {p['weapons_collected']}")
    print("="*50)
    try: os.remove(SAVE_FILE)
    except: pass

def instructions():
    print("\n--- INSTRUCTIONS ---")
    print("Explore -> fight enemies -> gain EXP & Gold -> Level up -> Defeat Boss every 10 levels")
    print("Shop in Village to buy weapons/armor/potions. Save often. Reach Lv 100 & kill Ancient Demon King.")
    print("Battle: Attack / Skills (mana) / Heal / Potion / Defend (-50% dmg) / Run")

def main():
    p=None
    while True:
        print("\n"+"="*40+"\nLEGENDS OF THE FORGOTTEN REALM\n"+"="*40)
        print("1 New Game  2 Continue  3 Instructions  4 Exit")
        ch=ask_int("Choice: ",1,4)
        if ch==1: p=new_player(); break
        elif ch==2:
            p=load_game()
            if p: break
        elif ch==3: instructions(); pause()
        else: return
    # Main loop
    while True:
        print(f"\n--- {REGIONS[p['region']]} | {p['name']} Lv {p['level']} HP {p['hp']}/{p['max_hp']} Gold {p['gold']} ---")
        print("1 Explore (Fight)  2 Boss Battle  3 Shop  4 Inventory  5 Stats  6 Use Potion  7 Save  8 Heal at Village (Free)  9 Exit")
        ch=ask_int("Choice: ",1,9)
        if ch==1:
            r=explore(p)
            if r=="exit": break
        elif ch==2: boss_battle(p)
        elif ch==3: shop(p)
        elif ch==4: show_inventory(p)
        elif ch==5: show_stats(p)
        elif ch==6: use_potion(p)
        elif ch==7: save_game(p)
        elif ch==8: p["hp"]=p["max_hp"]; p["mana"]=p["max_mana"]; print("Fully healed at Village!")
        elif ch==9: save_game(p); print("Thanks for playing!"); break
        if p["level"]>=100 and "Ancient Demon King" in p["bosses_defeated"]:
            break

if __name__=="__main__":
    main()