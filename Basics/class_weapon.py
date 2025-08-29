class Bug:
    def __init__(self, name: str, hp: float, damage: float):
        self.name, self.hp, self.damage = name, hp, damage

    def __repr__(self):
        return f"I'm {self.name}, one of the bugs of Hallownest. \nHP: {self.hp} \nDamage: {self.damage}"

    def reduce_life(self, hit):
        if self.hp > hit:
            self.hp -= hit
        else:
            self.hp = 0
            print (f"{self.name} is dead.")

    def display_hp(self):
        print(f"{self.name}'s HP: {self.hp}")

    def display_damage(self):
        print(f"{self.name}'s Damage: {self.damage}")

class Knight:
    def __init__(self, name: str, hp: float, damage: float):
        self.name, self.hp, self.damage = name, hp, damage

    def __repr__(self):
        return f"I'm {self.name}, the knight. \nHP: {self.hp} \nDamage: {self.damage}"

    def hit(self, bug: Bug):
        bug.reduce_life(self.damage)
        print(f"{bug.name} new HP: {bug.hp}")

    def fight(self, bug: Bug):
        bug.reduce_life(self.damage)
        self.reduce_life(bug.damage)

    def display_hp(self):
        print(f"{self.name}'s HP: {self.hp}")

    def display_damage(self):
        print(f"{self.name}'s Damage: {self.damage}")

    def reduce_life(self, hit):
        if self.hp > hit:
            self.hp -= hit
        else:
            self.hp = 0
            print (f"{self.name} is dead.")

class HollowKnight(Knight):
    def __init__(self, name: str, hp: float, damage: float):
        super().__init__(name, hp, damage)
        self.is_enchanted = False

    def __repr__(self):
        return f"I'm {self.name}, the Hollow Knight. \nHP: {self.hp} \nDamage: {self.damage}"

    def enchant(self):
        if not self.is_enchanted:
            self.is_enchanted = True
        self.damage *= 1.25
        print("Nail enchanted!")

bug1 = Bug("Grimm", 150, 45)
print(bug1)

knight1 = Knight("Hornet", 130, 80)
print(knight1)

knight1.hit(bug1)
knight1.fight(bug1)
knight1.display_hp()

bug2 = Bug("Pure Vessel", 200, 65)
print(bug2)

knight2 = HollowKnight("THK", 250, 90)
print(knight2)

knight2.hit(bug2)
knight2.enchant()
knight2.display_damage()
knight2.fight(bug2)
knight2.display_hp()