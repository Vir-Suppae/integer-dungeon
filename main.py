from time import sleep
from random import randint

def encounter(state: dict):
    print("you encountered a golbin!")
    lim = randint(10, 100)
    enemy_num = randint(0, lim)
    print(f"the golbin has chosen a number from 0-{lim}")
    while state["health"] > 0:
        print(f"hp: {state["health"]}\nkill streak: {state["streak"]}\ntrinkets: {state["trinkets"]}")
        print("enter one of the following:")
        print("\tuse (to use a trinket of halving)")
        print("\trun (to run from the fight)")
        print("\tguess <n> (where n is any non-negative integer)")
        player_input = input("\u21aa ").strip().lower()
        match player_input.split():
            case ["guess", n] if n.isdigit():
                guess = int(n)
                if guess > enemy_num:
                    print("too high! -1 hp :O")
                    state["health"] -= 1
                elif guess < enemy_num:
                    print("too low! -1 hp :[")
                    state["health"] -= 1
                else:
                    print(f"you killed 'em! +{state["bonus hp"]} hp :]")
                    state["health"] += state["bonus hp"]
                    state["enemy_count"] -= 1
                    state["streak"] += 1
                    if state["streak"] % 3 == 0 and state["streak"] > 0:
                        state["bonus hp"] += 1
                    if randint(0,5) == 0:
                        print("you got a trinket! :D")
                        state["trinkets"] += 1
                    return
            case ["run"]:
                if randint(0, 4) != 0:
                    print("you live to run another day. coward. :/")
                    should_reward = randint(0,2)
                    match should_reward:
                        case 0:
                            hp_up = randint(1,3)
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
                    print("the golbin's number is halved! :D")
                    state["trinkets"] -= 1
                    enemy_num //= 2
                else:
                    print("you haven't a trinket! :/")
                    print("the golbin attacks! -1 hp :[")
                    state["health"] -= 1
            case _:
                dmg = randint(1,5)
                print(f"WRONG ANSWER YOU FOOL! -{dmg} hp! >:(")
                state["health"] -= dmg
            

def main():
    state = {
        "health": 10,
        "trinkets": 0,
        "enemy_count": 10,
        "streak": 0,
        "bonus hp": 1,
        "secret": randint(0, 99),
    }
    print(end="are \x1b[97myou\x1b[39m ready to go \x1b[33minteger dungeon\x1b[39m? \x1b[95mo_O\n\x1b[36m(Y/n) \x1b[39m> ")
    sleep(2)
    print("\nwell I don't care! you're going regardless! >:]")
    while state["enemy_count"] > 0 and state["health"] > 0:
        encounter(state)
    print("you win! :D" if state["health"] > 0 else "YOU LOSE HAHAHAHA >:D")

if __name__ == "__main__":
    main()
