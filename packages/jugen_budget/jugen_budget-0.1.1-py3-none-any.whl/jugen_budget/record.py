class Irasas:
    def __init__(self, tipas: str, suma: float) -> None:
        self.tipas = tipas
        self.suma = suma
 
    def __str__(self) -> str:
        return f"{self.tipas}: {self.suma}"