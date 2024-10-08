import os
import pickle
from record import Irasas

def clear():
    '''
    Clears the terminal screen and scroll back to present
    the user with a nice clean, new screen. Useful for managing
    menu screens in terminal applications.
    '''
    os.system('cls' if os.name == 'nt' else 'echo -e \\\\033c')
   
class Biudzetas:
    def __init__(self) -> None:
        self.zurnalas = []
 
    def prideti_pajamu_irasa(self, suma: float) -> None:
        self.zurnalas.append(Irasas("Pajamos", suma))
 
    def prideti_islaidu_irasa(self, suma: float) -> None:
        self.zurnalas.append(Irasas("Išlaidos", suma))
 
    def gauti_balansą(self) -> float:
        balance = 0
        
        for record in self.zurnalas:
            balance += record.suma * (1, -1)[record.tipas == "Išlaidos" or record.suma < 0]
        return balance
 
    def parodyti_ataskaita(self) -> None:
        print("Biudžeto ataskaita:")
        for money in self.zurnalas:
            print(" " * (3 , 5)[money.tipas == "Išlaidos"] + f"{money.tipas}: {money.suma}")

clear() # - clear terminal

obj_bdz = Biudzetas()
 
while True:
    action = int(input("Pasirinkite veiksmą:\n\
    Įvesti pajamas      - 1\n\
    Įvesti išlaidas     - 2\n\
    Parodyti balansą    - 3\n\
    Biudžeto ataskaitą  - 4\n\
    Baigti darbą        - 5\nKokį veiksmą norite atlikti?: "))
    
    clear()

    match action:
        case num if num in range(1, 3):
            in_out = ('islaidu', 'pajamu')[action == 1]
            method_name = f"prideti_{in_out}_irasa"
            amount = float(input(f"Įveskite {in_out.replace("u", "ų").replace("s", "š")} sumą: "))
            amount = amount * (1, -1)[amount < 0]
            getattr(obj_bdz, method_name)(amount)
        case 3:
            print(f"Balansas: {obj_bdz.gauti_balansą()}")
        case 4:
            obj_bdz.parodyti_ataskaita()
        case _:
            with open("zurnalas.pkl", "wb") as p_out:
                pickle.dump(obj_bdz.zurnalas, p_out)

            print("Programa baigta!")
            break