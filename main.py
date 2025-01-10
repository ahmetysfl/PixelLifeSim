import pygame
import random
import time
import matplotlib.pyplot as plt
from creature import Creature
from world import World
import parameters as params
import threading
import numpy as np
from genetics import Genetics
import saveSimulation as sim
import graph as graph

start_new_sim = True
#start_new_sim = False

if (start_new_sim):
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
            if (len(genetics_list)>0):
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
window_width = w.width + 300  # Simülasyon ekranı + kontrol paneli
window_height = max(w.height, 200)  # Yükseklik, simülasyon ekranı veya kontrol paneli için yeterli olmalı
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Life Simulation with Control Panel")

# Butonların konum ve boyutları
pause_button_rect = pygame.Rect(w.width + 50, 50, 100, 50)  # Duraklat butonu
stop_button_rect = pygame.Rect(w.width + 50, 120, 100, 50)  # Durdur butonu

# Duraklatma ve durdurma durumları
paused = False
stopped = False

# Buton çizme fonksiyonu
def draw_button(screen, text, rect, color):
    pygame.draw.rect(screen, color, rect)
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

# Buton tıklama kontrolü
def is_button_clicked(mouse_pos, button_rect):
    return button_rect.collidepoint(mouse_pos)

# Initial time
last_step_time = time.time()

# Data storage for plotting
steps = []
total_creatures = []
production_rates = []

# Main loop
step_count = 0

# Start the graph plotting thread
running = True
#graph_thread = threading.Thread(target=graph.plot_genetics_scatter(w.creatures))
#graph_thread.start()

while running:
    # Kontrol ekranı olaylarını işle
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if is_button_clicked(mouse_pos, pause_button_rect):
                paused = not paused  # Duraklatma durumunu tersine çevir
            elif is_button_clicked(mouse_pos, stop_button_rect):
                stopped = True  # Simülasyonu durdur

    # Ekranı temizle
    screen.fill((0, 0, 0))

    # Simülasyon ekranını çiz
    for creature in w.creatures:
        pygame.draw.rect(screen, creature.color, (creature.x, creature.y, creature.creature_size, creature.creature_size))

    # Kontrol panelini çiz
    draw_button(screen, "Duraklat", pause_button_rect, (0, 128, 255))
    draw_button(screen, "Durdur", stop_button_rect, (255, 0, 0))

    pygame.display.flip()

    # Simülasyon durdurulduysa döngüden çık
    if stopped:
        break

    # Simülasyon duraklatılmadıysa ve durdurulmadıysa devam et
    if not paused and not stopped:
        current_time = time.time()
        if current_time - last_step_time >= params.FIXED_STEP_DURATION:
            # Canlıları güncelle
            for creature in w.creatures:
                creature.update(w)

            last_step_time = current_time

# Pygame'i kapat
pygame.quit()
