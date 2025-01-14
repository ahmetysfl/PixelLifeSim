import pygame
import random
import time
from creature import Creature
from world import World
import parameters as params
from genetics import Genetics
import saveSimulation as sim
from controlPanel import ControlPanel  # Kontrol paneli sınıfını içe aktar

w = World(params.WIDTH, params.HEIGHT)
new_creature = Creature(100, 100)
new_creature.genetics.sense_radius = 1
new_creature2 = Creature(100, 80)
new_creature2.genetics.energy_capacity = 1
w.add_creature(new_creature)
w.add_creature(new_creature2)


print((new_creature2.color))
new_creature.sense_8_directions(w)
print(new_creature.sensed_distance)
print(new_creature.sensed_color)