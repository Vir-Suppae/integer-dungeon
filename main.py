from time import sleep
import random
import re

INTEGER_PATTERN = r"[\-\+]?\d+"

class Enemy:
    def __init__(self, article, printable_name: str, bounds: dict[str, int]):
        self.article = article
        self.printable_name = printable_name
        self.lowerbounds = bounds.get("lower", 0)
        self.upperbounds = bounds.get("upper", 1004)
        self.number = random.randint(self.lowerbounds,self.upperbounds)

    def __str__(self):
        return self.printable_name

class Golbin(Enemy):
    def __init__(self):
        super().__init__("a", "golbin", {"lower": 0, "upper": 100})

enemies: list[list[type[Enemy]]] = [
    [
        Golbin,
    ],
]

def encounter(state: dict):
    enemy: Enemy = random.choice(enemies[state["rank"]])()
    print(f"you encountered {enemy.article} {enemy}!")
    print(f"the {enemy} has chosen a number from {enemy.lowerbounds}-{enemy.upperbounds}")
    while state["health"] > 0:
        print(f"hp: {state["health"]}\nkill streak: {state["streak"]}\ntrinkets: {state["trinkets"]}")
        print("enter one of the following:")
        print("\tuse (to use a trinket of halving)")
        print("\trun (to run from the fight)")
        print("\tguess <n> (where n is any integer)")
        player_input = input("\u21aa ").strip().lower()
        match player_input.split():
            case ["guess", n] if re.fullmatch(INTEGER_PATTERN, n):
                guess = int(n)
                if guess > enemy.number:
                    print("too high! -1 hp :O")
                    state["health"] -= 1
                elif guess < enemy.number:
                    print("too low! -1 hp :[")
                    state["health"] -= 1
                else:
                    print(f"you killed 'em! +{state["bonus hp"]} hp :]")
                    state["health"] += state["bonus hp"]
                    state["enemy_count"] -= 1
                    state["streak"] += 1
                    if state["streak"] % 3 == 0 and state["streak"] > 0:
                        state["bonus hp"] += 1
                    if random.randint(0,5) == 0:
                        print("you got a trinket! :D")
                        state["trinkets"] += 1
                    return
            case ["run"]:
                if random.randint(0, 4) != 0:
                    print("you live to run another day. coward. :/")
                    should_reward = random.randint(0,2)
                    match should_reward:
                        case 0:
                            hp_up = random.randint(1,3)
                            print("you managed to grab and eat some berries on the way out")
                            print(f"+{hp_up}hp")
                            state["health"] += hp_up
                        case 1:
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
            case _:
                dmg = random.randint(1,5)
                print(f"WRONG ANSWER YOU FOOL! -{dmg} hp! >:(")
                state["health"] -= dmg
            

def main():
    state = {
        "health": 10,
        "trinkets": 0,
        "enemy_count": 10,
        "streak": 0,
        "bonus hp": 1,
        "rank": 0,
        "secret": random.randint(0, 99),
    }
    print(end="are \x1b[97myou\x1b[39m ready to go \x1b[33minteger dungeon\x1b[39m? \x1b[95mo_O\n\x1b[36m(Y/n) \x1b[39m> ")
    sleep(2)
    print("\nwell I don't care! you're going regardless! >:]")
    while state["enemy_count"] > 0 and state["health"] > 0:
        encounter(state)
    print("you win! :D" if state["health"] > 0 else "YOU LOSE HAHAHAHA >:D")

if __name__ == "__main__":
    main()
