import random

health = 10

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
    global health
    print("an enemy approaches!")
    if input("fight or try to run?\n(fight/run) > ").lower() == "fight":
        lim = random.randint(10, 100)
        enemy_num = random.randint(1, lim)
        print(f"the number is from 1 to {lim}, inclusive")
        while health > 0:
            print(f"hp: {health}")
            try:
                guess = int(input("guess [integer] or run > "))
            except ValueError:
                run()
                return
            if guess == enemy_num:
                print("you killed 'em! +1 hp")
                health += 1
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
