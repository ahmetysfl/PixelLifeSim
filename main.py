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
# import saveSimulation as sim

import pickle
import os
import inspect

# Initialize the world
w = World(params.WIDTH, params.HEIGHT)

# Pygame settings
pygame.init()
screen = pygame.display.set_mode((params.WIDTH, params.HEIGHT))
pygame.display.set_caption("Life Simulation - Fixed Step")

# Initial time
last_step_time = time.time()

# Data storage for plotting
steps = []
total_creatures = []
production_rates = []

# Initialize creatures
while len(w.creatures) < params.MAX_CREATURES:
    x = random.randint(0, params.WIDTH - params.CREATURE_SIZE_MAX)
    y = random.randint(0, params.HEIGHT - params.CREATURE_SIZE_MAX)
    if w.can_fit(x, y, params.CREATURE_SIZE_MAX):
        # Create a new creature with random genetics
        new_genetics = Genetics()
        new_creature = Creature(x, y, genetics=new_genetics)
        w.creatures.append(new_creature)
    else:
        continue

# Function to plot the graph in a separate thread
def plot_graph():
    plt.ion()  # Turn on interactive mode
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 4))

    while running:
        if steps and total_creatures:
            # Plot Total Creatures
            ax1.clear()
            ax1.plot(steps, total_creatures, label="Total Creatures", color="blue")
            ax1.set_xlabel("Simulation Steps")
            ax1.set_ylabel("Number of Creatures")
            ax1.set_title("Total Number of Creatures Over Time")
            ax1.legend()
            ax1.grid(True)

            # Plot Error Bar for Production Rate
            if production_rates:
                avg_rates = [np.mean(rates) for rates in production_rates]
                min_rates = [np.min(rates) for rates in production_rates]
                max_rates = [np.max(rates) for rates in production_rates]

                yerr = [np.array(avg_rates) - np.array(min_rates), np.array(max_rates) - np.array(avg_rates)]
                ax2.clear()
                ax2.errorbar(steps, avg_rates, yerr=yerr, fmt='-o', color="green", ecolor="gray", capsize=5, label="Production Rate")
                ax2.set_xlabel("Simulation Steps")
                ax2.set_ylabel("Production Rate")
                ax2.set_title("Production Rate (Min, Max, Avg) Over Time")
                ax2.legend()
                ax2.grid(True)

            plt.pause(params.PLOT_PAUSE)  # Pause to update the plot

    plt.close(fig)

# Start the graph plotting thread
running = True
graph_thread = threading.Thread(target=plot_graph)
#graph_thread.start()

# Simülasyon durumunu kaydet
def save_simulation_state(w, params, save_dir="saved_simulations"):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    existing_files = [f for f in os.listdir(save_dir) if f.startswith("simulation_")]
    simulation_number = len(existing_files) + 1
    simulation_filename = os.path.join(save_dir, f"simulation_{simulation_number}.pkl")
    params_dict = {name: value for name, value in inspect.getmembers(params) if not name.startswith("__")}
    with open(simulation_filename, "wb") as file:
        pickle.dump({"w": w, "params": params_dict}, file)
    print(f"Simulation state saved to {simulation_filename}")
    return simulation_filename

# Simülasyon durumunu yükle
def load_simulation_state(simulation_filename):
    with open(simulation_filename, "rb") as file:
        data = pickle.load(file)
    import parameters as params_module
    for key, value in data["params"].items():
        setattr(params_module, key, value)
    print(f"Simulation state loaded from {simulation_filename}")
    return data["w"], params_module

#save_simulation_state(w, params)
w, params = load_simulation_state("saved_simulations/simulation_4.pkl")
# Main loop
step_count = 0
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
        print(f"Total creatures: {len(w.creatures)}")


        if (len(w.creatures)) < 1:
            break
        last_step_time = current_time

    # Draw creatures
    for creature in w.creatures:
        pygame.draw.rect(screen, creature.color, (creature.x, creature.y, creature.creature_size, creature.creature_size))

    # Update display
    pygame.display.flip()

# Wait for the graph thread to finish
#graph_thread.join()

# Quit Pygame
pygame.quit()
