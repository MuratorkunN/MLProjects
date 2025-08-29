class Orkun():
    def __init__(self, name: str ,ml_score: float, is_handsome: bool):
        self.name, self.ml_score, self.__is_handsome = name, ml_score, is_handsome

    def __repr__(self):
        if self.__is_handsome:
            return f"{self.name} is a handsome with an ml score of {self.ml_score}"
        else:
            return f"{self.name} is not a handsome with an ml score of {self.ml_score}"

    def __le__(self, other):
        if self.__is_handsome:
            if other.__is_handsome:
                return self.ml_score <= other.ml_score
            else:
                return False

        else:
            if other.__is_handsome:
                return True
            else:
                return self.ml_score <= other.ml_score

    def __gt__(self, other):
        return not self <= other

    def __eq__(self, other):
        if self.__is_handsome == other.__is_handsome and self.ml_score == other.ml_score:
            return True
        else:
            return False


orkun1 = Orkun("orkun1",50,True)
orkun2 = Orkun("orkun2",55,True)
orkun3 = Orkun("orkun3",90,False)
orkun4 = Orkun("orkun4",95,False)
orkun5 = Orkun("orkun5",95,False)

print(orkun1)

print(orkun1<=orkun2)
print(orkun2<=orkun3)
print(orkun3<=orkun4)

print(orkun4>orkun1)

print(orkun4==orkun5)
