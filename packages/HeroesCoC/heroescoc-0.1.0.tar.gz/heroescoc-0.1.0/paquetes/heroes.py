#!/usr/bin/python3
class Heroe:
    
    def __init__(self, heroe, nivel, mascota ):
        self.heroe = heroe
        self.nivel = nivel
        self.mascota = mascota
    def __repr__(self):
        return f"{self.heroe} {self.nivel} {self.mascota}"

heroes = [
        Heroe("Reina Arquera de nivel", 80, "y su mascota es el unicornio"),
        Heroe("Rey Barbaro de nivel", 66, "y su mascota es LASSI"),
        Heroe("Gran Centinela de nivel", 55, "y su mascota es el Buho Electrico"),
        Heroe("Luchadora Real de nivel", 30, "y su mascota es el Yak")
]

def lista_heroes():
    for heroe in heroes:
        print(heroe)


