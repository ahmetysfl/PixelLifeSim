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
#start_new_sim = False
start_basic_sim = True
start_basic_sim = False
use_saved_brains = True
use_saved_brains = False


start_py_game = True
start_py_game = False

draw_radius = True
draw_radius = False

if start_basic_sim:
    w = World(params.WIDTH, params.HEIGHT)
    new_creature = Creature(20, 20)
    new_creature.genetics.sense_radius = 1
    w.add_creature(new_creature)
    new_creature = Creature(20, 40)
    new_creature.genetics.sense_radius = 1
    w.add_creature(new_creature)
elif start_new_sim:
    # Initialize the world
    w = World(params.WIDTH, params.HEIGHT)
    # Initialize creatures
    genetics_list = []
    #genetics_list = sim.create_new_genetics_list()
    if use_saved_brains:
        old_brains = sim.load_brain_states()
        print(len(old_brains))
        old_brains_to_max_creatures = sim.extend_list_to_size(old_brains,params.MAX_CREATURES + 20)
        print(len(old_brains_to_max_creatures))
        random.shuffle(old_brains_to_max_creatures)
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

            if use_saved_brains:
                new_creature.brain = old_brains_to_max_creatures.pop()
            else:
                pass
            w.add_creature(new_creature)
        else:
            continue
    sim.save_simulation_state(w, params)
else:
    w, params = sim.load_simulation_state()

if start_py_game:
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
step_count = 0
max_step_count = 500
all_creatures = []
# Main loop
running = True
while running:
    # Olayları işle
    if start_py_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            control_panel.handle_events(event,w.creatures)  # Kontrol paneli olaylarını işle

        # Ekranı temizle
        screen.fill((0, 0, 0))

        # Simülasyon ekranını çiz
        for creature in w.creatures:
            pygame.draw.rect(screen, creature.color, (creature.x, creature.y, creature.creature_size, creature.creature_size))

            if draw_radius:
                # Eylem yarıçapı için sarı daire çiz
                action_radius_color = (255, 255, 0)  # Sarı renk (RGB: 255, 255, 0)
                action_radius = creature.genetics.action_zone_ratio * params.ACTION_ZONE_MAX  # Eylem yarıçapını hesapla
                pygame.draw.circle(screen, action_radius_color,
                                   (creature.x + creature.creature_size // 2, creature.y + creature.creature_size // 2),
                                   int(action_radius), 1)  # 1 çizgi kalınlığı

                # Algı yarıçapı için beyaz daire çiz
                sense_radius_color = (255, 255, 255)  # Beyaz renk (RGB: 255, 255, 255)
                sense_radius = creature.genetics.sense_radius * params.SENSE_RADIUS_GENERAL  # Algı yarıçapını hesapla
                pygame.draw.circle(screen, sense_radius_color,
                                   (creature.x + creature.creature_size // 2, creature.y + creature.creature_size // 2),
                                   int(sense_radius), 1)  # 1 çizgi kalınlığı
        # Kontrol panelini çiz
        control_panel.draw(screen)

        pygame.display.flip()

        # Simülasyon durdurulduysa döngüden çık
        if control_panel.stopped:
            sim.save_brain_states(w)
            break

    if start_py_game:
    # Simülasyon duraklatılmadıysa ve durdurulmadıysa devam et
        if not control_panel.paused and not control_panel.stopped:
            current_time = time.time()
            if current_time - last_step_time >= params.FIXED_STEP_DURATION:
                # Canlıları güncelle
                for creature in w.creatures:
                    creature.update(w)
                last_step_time = current_time
    else:
        # Canlıları güncelle
        for creature in w.creatures:
            creature.update(w)
    all_creatures.append(w.creatures)
    print(step_count)
    step_count += 1
    if step_count > max_step_count or len(w.creatures) == 0:
        running = False

sim.save_simulation_steps(all_creatures)
# Pygame'i kapat
if start_py_game:
    pygame.quit()
