import random
import pyperclip

# true = True
# false = False

health = 10
trinkets = 0

def run():
    global health
    if random.randint(0, 4) == 0:
        print(
            "you try to run, but then you feel a massive impact and see your body fall down in front of you"
        )
        print("you are dead now. X)")
        raise Exception("PlayerKilled")
    else:
        print("you live to run another day. coward. +1 hp")
        health += 1

def enemy():
    global health, trinkets
    prompt = ["an enemy approaches!"]
    prompt.append("fight or try to run?\n(fight/run) > ")
    pyperclip.copy('\n'.join(prompt))
    print('\n'.join(prompt), end='')
    if input().lower() == "fight":
        prompt = []
        lim = random.randint(10, 100)
        enemy_num = random.randint(1, lim)
        prompt.append(f"the number is from 1 to {lim}, inclusive")
        while health > 0:
            prompt = []
            prompt.append(f"health points: {health}")
            prompt.append(f"trinkets left: {trinkets}")
            prompt.append("options:")
            prompt.append(f"\tguess an integer [0-{lim}]")
            prompt.append("\tuse a trinket of halving [use]")
            prompt.append("\trun from fight [run]")
            pyperclip.copy('\n'.join(prompt))
            print('\n'.join(prompt), end='')
            choice = input().lower()
            if choice == "run":
                run()
                return
            elif choice == "use":
                if trinkets > 0:
                    prompt = []
                    prompt.append("you used a trinket!")
                    enemy_num //= 2
                    trinkets -= 1
                    prompt.append(f"enemy num is now from 0 to {lim//2}")
                    pyperclip.copy('\n'.join(prompt))
                    print('\n'.join(prompt), end='')
                    continue
                else:
                    prompt = []
                    prompt.append("out of trinkets :D the enemy did 1 damage")
                    health -= 1
                    pyperclip.copy('\n'.join(prompt))
                    print('\n'.join(prompt), end='')
                    continue
            elif choice.isdigit():
                guess = int(choice)
            else:
                dmdmg = random.randint(2,5)
                print(f"WRONG ANSWER! dungeon master did {dmdmg} damage")
                health -= dmdmg
                continue
            if guess == enemy_num:
                print("you killed 'em! +1 hp")
                health += 1
                if (random.randint(0,2) == 0):
                    print("you got a  trinket of halving!")
                    trinkets += 1
                else:
                    print("they had nothing of value")
                break
            elif guess < enemy_num:
                print("Ooooh, too low! the enemy did 1 damage")
                health -= 1
            elif guess > enemy_num:
                print("Ooooh, too high! the enemy did 1 damage")
                health -= 1
        if health <= 0:
            raise Exception("PlayerKilled")
    else:
        run()

def main():
    print("hello and welcome to the integer dungeon :D")
    print("dost thou dare to adventure?")
    if input("(y/N) > ").lower() != "y":
        return
    print("ok, prepare to meet thy doom! >:)")
    for i in range(10):
        enemy()
    raise Exception("EnemiesAllKilled")


if __name__ == "__main__":
    main()
