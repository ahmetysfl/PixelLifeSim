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
screen = pygame.display.set_mode((w.width, w.height))
pygame.display.set_caption("Life Simulation - Fixed Step")

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
    screen.fill((0, 0, 0))  # Clear screen

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fixed-step simulation
    current_time = time.time()
    if current_time - last_step_time >= params.FIXED_STEP_DURATION:
        # Update creatures
        rates = []
        for creature in w.creatures:
            creature.update(w)
            rates.append(creature.genetics.production_rate)

        # Record data for plotting
        steps.append(step_count)
        total_creatures.append(len(w.creatures))
        production_rates.append(rates)
        step_count += 1
        # Print computation time
        computation_time = time.time() - last_step_time
        #print(f"Step computation time: {computation_time:.4f}")
        #print(f"Total creatures: {len(w.creatures)}")


        if (len(w.creatures)) < 1:
            break
        last_step_time = current_time

    # Draw creatures and their action zones
    for creature in w.creatures:
        # Draw the creature itself
        pygame.draw.rect(screen, creature.color,
                         (creature.x, creature.y, creature.creature_size, creature.creature_size))

        # Calculate the center of the creature
        center_x = creature.x + creature.creature_size // 2
        center_y = creature.y + creature.creature_size // 2

        # Calculate the radius of the action zone based on action_zone_ratio
        action_zone_radius = creature.genetics.action_zone_ratio * params.ACTION_ZONE_MAX  # Ensure a minimum radius

        # Draw the action zone as a circle
        #pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), action_zone_radius, 1)  # White circle with 1px border

    # Update display
    pygame.display.flip()

# Wait for the graph thread to finish
graph_thread.join()

# Quit Pygame
pygame.quit()
