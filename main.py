import random
import re

INTEGER_PATTERN = r"[\-\+]?\d+"

class Enemy:
    def __init__(self, article, printable_name: str, flavor_text: str,  bounds: dict[str, int]):
        self.article = article
        self.printable_name = printable_name
        self.lowerbounds = bounds.get("lower", 0)
        self.upperbounds = bounds.get("upper", 1004)
        self.number = random.randint(self.lowerbounds,self.upperbounds)
        self.flavor_text = flavor_text

    def __str__(self):
        return self.printable_name

class Golbin(Enemy):
    def __init__(self):
        super().__init__("a", "golbin", 'the golbin looks at you with a look of disgust\n"you think you know numbers? you probably don\'t even know what a transcendental is. hah."', {"lower": 0, "upper": 100})

class HomelessMan(Enemy):
    def __init__(self):
        super().__init__("a", "homeless man", 'he looks at you with bleary eyes\n"where am I? can you help me?"', {"lower": -3, "upper": 46})

class Homunculus(Enemy):
    def __init__(self):
        super().__init__("a", "homunculus", 'the homunculus looks at you with sad human-looking eyes\nit is silent', {"lower": 0, "upper": 3})

class Spooder(Enemy):
    def __init__(self):
        super().__init__("a", "spooder", 'the spooder is huge!\n"is the metal thing tasty? I hope it is tasty. it looks like a metal human fehfehfehch"',{"lower": -200, "upper": 150})

class Boblin(Enemy):
    def __init__(self):
        super().__init__("a", "boblin", 'the boblin is identical to a golbin, except for the yellow eyes\n"I don\'t even like numbers! can\'t we do a spelling bee or something?"', {"lower": 0, "upper": 200})

class Zombie(Enemy):
    def __init__(self):
        super().__init__("a", "zombie", 'it\'s bones are exposed in some places\n"gehhhhh"', {"lower": 0, "upper": 10})

class Vampire(Enemy):
    def __init__(self):
        super().__init__("a", "vampire", 'he is well-dressed\n"you don\'t have any blood-born diseases do you?"',{"lower": 100, "upper": 300})

enemies: list[tuple[int,list[type[Enemy]]]] = [
    (
        10,
        [
            Golbin,
            HomelessMan,
            Homunculus,
            Spooder,
        ]
    ),
    (
        15,
        [
            Boblin,
            Zombie,
            Vampire,
            Spooder,
        ]
    ),
]

def encounter(state: dict, ec: int):
    enemy: Enemy = random.choice(enemies[state["rank"]][1])()
    print(f"you encountered {enemy.article} {enemy}!")
    print(f"{enemy.flavor_text}")
    print(f"the {enemy} has chosen a number from {enemy.lowerbounds}-{enemy.upperbounds}")
    while state["health"] > 0:
        print(f"enemy count: {ec}\nhp: \x1b[{"91" if state["health"] < 3 else "93" if state["health"] < 7 else "0"}m{state["health"]}\x1b[0m\nkill streak: {state["streak"]}\ntrinkets: \x1b[{"0" if state["trinkets"] <= 0 else "95"}m{state["trinkets"]}\x1b[0m")
        print("enter one of the following:")
        if state["trinkets"] > 0:
            print("|\tuse (to use a trinket of halving)")
        print("|\trun (to run from the fight)")
        print("|\tguess NUMBER")
        player_input = input("+- ").strip().lower()
        match player_input.split():
            case ["guess", n] | [n] if re.fullmatch(INTEGER_PATTERN, n):
                guess = int(n)
                enemyDamage = random.randint(1, 5)
                if guess > enemy.number:
                    toPrint = "too high!"
                    if state["previous side"] == 0 and random.randint(0,3) == 0:
                        state["health"] -= enemyDamage
                        toPrint += f" -{enemyDamage} hp :O"
                    elif state["previous side"] == 1 and random.randint(0,1) == 0:
                        state["health"] -= enemyDamage
                        toPrint += f" -{enemyDamage} hp :O"
                    state["previous side"] = 1
                    print(toPrint)
                elif guess < enemy.number:
                    toPrint="too low!"
                    if state["previous side"] == 1 and random.randint(0,3) == 0:
                        state["health"] -= enemyDamage
                        toPrint += f" -{enemyDamage} hp :O"
                    elif state["previous side"] == 0 and random.randint(0,1) == 0:
                        state["health"] -= enemyDamage
                        toPrint += f" -{enemyDamage} hp :O"
                    state["previous side"] = 0
                    print(toPrint)
                else:
                    print(f"you killed 'em! +{state["bonus hp"]} hp :]")
                    state["health"] += state["bonus hp"]
                    state["streak"] += 1
                    if state["streak"] % 3 == 0 and state["streak"] > 0:
                        state["bonus hp"] += 1
                    if random.randint(0,5) == 0:
                        print("you got a trinket! :D")
                        state["trinkets"] += 1
                    return -1
            case ["run"]:
                if random.randint(0, 4) != 0:
                    print("you live to run another day. coward. :/")
                    should_reward = random.randint(0,2)
                    match should_reward:
                        case 0 if state["health"] < 10:
                            hp_up = random.randint(1,3)
                            print("you managed to grab and eat some berries on the way out")
                            print(f"+{hp_up}hp")
                            state["health"] += hp_up
                        case 1 if state["health"] < 5:
                            print("woah, you got imbued with the cowards blessing")
                            print("2x hp")
                            state["health"] *= 2
                        case _:
                            ...
                    state["streak"] *= 0
                    return
                else:
                    print("oof they got you whilst you were escaping! :|")
                    state["health"] *= 0
            case ["use"]:
                if state["trinkets"] > 0:
                    print("you used a trinket of halving! :O")
                    print(f"the {enemy}'s number is halved! :D")
                    state["trinkets"] -= 1
                    enemy.number //= 2
                else:
                    print("you haven't a trinket! :/")
                    print(f"the {enemy} attacks! -1 hp :[")
                    state["health"] -= 1
            case []:
                pass
            case _:
                state["invalid inputs"] += 1
                dmg = random.randint(1,state["invalid inputs"])
                print(f"WRONG ANSWER YOU FOOL! -{dmg} hp! >:(")
                state["health"] -= dmg
            

def main():
    state = {
        "health": 10,
        "trinkets": 0,
        "streak": 0,
        "bonus hp": 1,
        "rank": 0,
        "secret": random.randint(0, 99),
        "previous side": 2,
        "invalid inputs": 0,
    }
    print("are you ready to go integer dungeon? o_O")
    input("(Y/n) > ")
    print("well I don't care! you're going regardless! >:]")
    enemy_count = enemies[state["rank"]][0]
    while state["health"] > 0:
        result = encounter(state, enemy_count)
        enemy_count += result if result is not None else 0
        if enemy_count <= 0 and len(enemies) > state["rank"] + 1:
            state["rank"] += 1
            enemy_count = enemies[state["rank"]][0]
        elif enemy_count <= 0:
            break
    print("you win! :D" if state["health"] > 0 else "YOU LOSE HAHAHAHA >:D")

if __name__ == "__main__":
    main()
