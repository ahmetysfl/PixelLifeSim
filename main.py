import pygame
import random
import time
from creature import Creature
from world import World
import parameters as params
from genetics import Genetics
import saveSimulation as sim
from controlPanel import ControlPanel  # Kontrol paneli sınıfını içe aktar

start_new_sim = True
# start_new_sim = False

if start_new_sim:
    # Initialize the world
    w = World(params.WIDTH, params.HEIGHT)
    # Initialize creatures
    genetics_list = []
    producer_genetics = Genetics()
    producer_genetics.consumption_rate = 0
    producer_genetics.action_zone_ratio = 0
    producer_genetics.production_rate = 1
    producer_genetics.energy_capacity = 0.2
    producer_genetics.consume_other_creatures_ratio = 0
    for _ in range(0):
        genetics_list.append(producer_genetics)

    consumer_genetics = Genetics()
    consumer_genetics.consumption_rate = 0.25
    consumer_genetics.action_zone_ratio = 0.5
    consumer_genetics.production_rate = 0.2
    consumer_genetics.energy_capacity = 0.6
    consumer_genetics.consume_other_creatures_ratio = 1
    for _ in range(0):
        genetics_list.append(consumer_genetics)

    while len(w.creatures) < params.MAX_CREATURES:
        x = random.randint(0, params.WIDTH - params.CREATURE_SIZE_MAX)
        y = random.randint(0, params.HEIGHT - params.CREATURE_SIZE_MAX)
        if w.can_fit(x, y, params.CREATURE_SIZE_MAX):
            # Create a new creature with random genetics
            if len(genetics_list) > 0:
                new_genetics = genetics_list.pop()
            else:
                new_genetics = Genetics()
            new_creature = Creature(x, y, genetics=new_genetics)
            w.add_creature(new_creature)
        else:
            continue
    sim.save_simulation_state(w, params)
else:
    w, params = sim.load_simulation_state()

# Pygame settings
pygame.init()
# Pencere boyutunu artırın
window_width = w.width + 250  # Simülasyon ekranı + kontrol paneli
window_height = max(w.height, 100)  # Yükseklik, simülasyon ekranı veya kontrol paneli için yeterli olmalı
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Life Simulation with Control Panel")

# Kontrol panelini başlat
control_panel = ControlPanel(w.width, w.height)

# Initial time
last_step_time = time.time()

# Main loop
running = True
while running:
    # Olayları işle
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        control_panel.handle_events(event,w.creatures)  # Kontrol paneli olaylarını işle

    # Ekranı temizle
    screen.fill((0, 0, 0))

    # Simülasyon ekranını çiz
    for creature in w.creatures:
        pygame.draw.rect(screen, creature.color, (creature.x, creature.y, creature.creature_size, creature.creature_size))

    # Kontrol panelini çiz
    control_panel.draw(screen)

    pygame.display.flip()

    # Simülasyon durdurulduysa döngüden çık
    if control_panel.stopped:
        break

    # Simülasyon duraklatılmadıysa ve durdurulmadıysa devam et
    if not control_panel.paused and not control_panel.stopped:
        current_time = time.time()
        if current_time - last_step_time >= params.FIXED_STEP_DURATION:
            # Canlıları güncelle
            for creature in w.creatures:
                creature.update(w)
            last_step_time = current_time

# Pygame'i kapat
pygame.quit()
