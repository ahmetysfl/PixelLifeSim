import random
import numpy as np
import selenium.common.exceptions

import parameters as params
from genetics import Genetics


class Creature:
    def __init__(self, x, y, genetics=None):
        self.x = x
        self.y = y
        self.genetics = genetics if genetics is not None else Genetics()
        self.action_cost = self.calculate_action_cost()
        self.genetic_cost = self.calculate_genetic_cost()
        self.sensed_color = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.energy = random.uniform(1, self.genetics.energy_capacity * params.MAX_ENERGY_CAPACITY)  # Energy between 1 and energy_capacity * MAX_ENERGY_CAPACITY
        self.last_energy = self.energy
        self.maturity_level = int(params.MATURITY_LEVEL_MIN + params.MATURITY_LEVEL_MAX * self.genetics.production_rate)
        self.lifespan = 0
        self.crowded_calculation_ratio = 1
        self.actions = [self.move_up, self.move_down, self.move_left, self.move_right, self.stay_still, self.consume_other_creatures, self.share_resource_to_other_creatures]
        self.brain = self.initialize_brain()
        self.mutation_rate = params.MUTATION_RATE
        self.color = self.calculate_color()

        self.creature_size = params.CREATURE_SIZE_MIN + int(
            min(params.CREATURE_SIZE_MAX * self.genetics.energy_capacity, params.CREATURE_SIZE_MAX)
        )

    def calculate_action_cost(self):
        """
        Calculate the action cost based on genetic parameters and their respective weights.
        Higher values of genetic parameters result in higher action cost.
        """
        # Normalize genetic parameters
        production_rate_norm = self.genetics.production_rate / params.PRODUCTION_RATE_MAX
        energy_capacity_norm = self.genetics.energy_capacity
        action_zone_ratio_norm = self.genetics.action_zone_ratio
        consume_other_creatures_ratio_norm = self.genetics.consume_other_creatures_ratio / params.CONSUME_OTHER_CREATURES_RATIO_MAX
        resource_share_ratio_norm = self.genetics.resource_share_ratio / params.RESOURCE_SHARE_RATIO_MAX
        sense_radius_norm = self.genetics.sense_radius / params.SENSE_RADIUS_MAX  # Yeni eklenen değer

        # Calculate weighted sum of genetic parameters using action cost weights
        weighted_sum = (
                production_rate_norm * params.ACTION_COST_PRODUCTION_RATE_WEIGHT +
                energy_capacity_norm * params.ACTION_COST_ENERGY_CAPACITY_WEIGHT +
                action_zone_ratio_norm * params.ACTION_COST_ACTION_ZONE_WEIGHT +
                consume_other_creatures_ratio_norm * params.ACTION_COST_CONSUME_OTHERS_WEIGHT +
                resource_share_ratio_norm * params.ACTION_COST_RESOURCE_SHARE_WEIGHT +
                sense_radius_norm * params.ACTION_COST_SENSE_RADIUS_WEIGHT  # Yeni eklenen değer
        )

        # Scale the weighted sum by the general energy consumption factor
        return weighted_sum * params.ACTION_COST_GENERAL_RATIO

    def calculate_genetic_cost(self):
        genetic_cost = 0
        genetic_cost += self.genetics.production_rate * self.genetics.consumption_rate
        genetic_cost += self.genetics.energy_capacity * self.genetics.action_zone_ratio
        genetic_cost += self.genetics.resource_share_ratio * self.genetics.consume_other_creatures_ratio
        return genetic_cost * params.GENERAL_GENETIC_COST

    def initialize_brain(self):
        """Initialize a neural network with two hidden layers."""
        input_size = len(self.get_inputs())
        hidden_layer1_size = params.BRAIN_LAYER1_SIZE  # İlk gizli katmanın boyutu
        hidden_layer2_size = params.BRAIN_LAYER2_SIZE  # İkinci gizli katmanın boyutu

        brain = {
            'input_to_hidden1': np.random.rand(input_size, hidden_layer1_size),
            'hidden1_to_hidden2': np.random.rand(hidden_layer1_size, hidden_layer2_size),
            'hidden2_to_output': np.random.rand(hidden_layer2_size, len(self.actions))
        }
        return brain

    def perform_action_cost(self):
        self.energy -= self.action_cost

    def calculate_action(self):
        """Determine an action using the neural network with two hidden layers."""
        inputs = self.get_inputs()

        # İlk gizli katmanın çıktısını hesapla
        hidden_layer1_output = np.tanh(np.dot(inputs, self.brain['input_to_hidden1']))

        # İkinci gizli katmanın çıktısını hesapla
        hidden_layer2_output = np.tanh(np.dot(hidden_layer1_output, self.brain['hidden1_to_hidden2']))

        # Çıktı katmanının çıktısını hesapla
        outputs = np.dot(hidden_layer2_output, self.brain['hidden2_to_output'])

        return np.argmax(outputs)

    def random_update_brain(self, mutation_rate=0.1):
        """
        Randomly update the brain weights.
        mutation_rate: Controls the magnitude of random changes.
        """
        for layer in self.brain:
            # Generate random noise with the same shape as the layer weights
            random_noise = np.random.uniform(-mutation_rate, mutation_rate, self.brain[layer].shape)
            # Update the weights with the random noise
            self.brain[layer] += random_noise

    def get_inputs(self):
        """Return normalized inputs for the neural network."""
        inputs = [
            self.energy / (self.genetics.energy_capacity * params.MAX_ENERGY_CAPACITY),  # Normalized energy
            self.last_energy / (self.genetics.energy_capacity * params.MAX_ENERGY_CAPACITY),  # Normalized energy
            self.lifespan / params.AGING_LEVEL_STARTS,
            self.genetics.production_rate,
            self.genetics.consume_other_creatures_ratio,
            self.genetics.consumption_rate,
            self.crowded_calculation_ratio,
            self.action_cost,
            self.genetics.resource_share_ratio
        ]
        inputs += self.sensed_color
        return np.array(inputs)

    def calculate_color(self):
        """
        Calculate the color of the creature based on its genetic parameters.
        - High production rate: Brighter green.
        - High consumption rate or tendency to consume other creatures: Brighter red.
        - High resource share ratio: Brighter blue.
        - Balanced traits: Bright yellow, with intensity based on the average of traits.
        """
        # Normalize genetic parameters to a range of 0-1
        production_rate_norm = self.genetics.production_rate / params.PRODUCTION_RATE_MAX
        consumption_rate_norm = self.genetics.consumption_rate / params.CONSUMPTION_RATE_MAX
        consume_other_creatures_ratio_norm = self.genetics.consume_other_creatures_ratio / params.CONSUME_OTHER_CREATURES_RATIO_MAX
        resource_share_ratio_norm = self.genetics.resource_share_ratio / params.RESOURCE_SHARE_RATIO_MAX

        # Calculate the dominant trait and its intensity
        if production_rate_norm > max(consumption_rate_norm, consume_other_creatures_ratio_norm,
                                      resource_share_ratio_norm) + 0.2:
            # Green is dominant, intensity based on production rate
            green_intensity = int(255 * production_rate_norm)
            return (0, green_intensity, 0)  # Green with variable intensity
        elif consume_other_creatures_ratio_norm > max(production_rate_norm, consumption_rate_norm,
                                                      resource_share_ratio_norm) + 0.2:
            # Red is dominant, intensity based on consume_other_creatures_ratio
            red_intensity = int(255 * consume_other_creatures_ratio_norm)
            return (red_intensity, 0, 0)  # Red with variable intensity
        elif consumption_rate_norm > max(production_rate_norm, consume_other_creatures_ratio_norm,
                                         resource_share_ratio_norm) + 0.2:
            # Red is dominant, intensity based on consumption rate
            red_intensity = int(255 * consumption_rate_norm)
            return (red_intensity, 0, 0)  # Red with variable intensity
        elif resource_share_ratio_norm > max(production_rate_norm, consumption_rate_norm,
                                             consume_other_creatures_ratio_norm) + 0.2:
            # Blue is dominant, intensity based on resource_share_ratio
            blue_intensity = int(255 * resource_share_ratio_norm)
            return (0, 0, blue_intensity)  # Blue with variable intensity
        else:
            # Balanced traits: Bright yellow, intensity based on the average of traits
            average_intensity = int(
                255 * (
                            production_rate_norm + consumption_rate_norm + consume_other_creatures_ratio_norm + resource_share_ratio_norm) / 4)
            return (average_intensity, average_intensity, 0)  # Bright yellow with variable intensity

    def update(self, world):
        """Update the creature's state."""
        if self.energy > 0:
            # Apply general energy consumption and production
            self.energy -= params.GENERAL_ENERGY_CONSUMPTION * self.genetics.consumption_rate
            # Aging effect
            self.energy -= params.GENERAL_ENERGY_CONSUMPTION * (self.lifespan / params.AGING_LEVEL_STARTS)
            self.energy -= self.genetic_cost
            self.crowded_calculation_ratio = min(1,params.CROWDED_ZONE_THRESHOLD / world.get_crowded_zone_count(self))
            self.energy += params.GENERAL_ENERGY_PRODUCTION * self.genetics.production_rate * self.crowded_calculation_ratio
            self.energy = min(self.energy, self.genetics.energy_capacity * params.MAX_ENERGY_CAPACITY) # Keep energy within bounds
            self.lifespan += 1  # Increment lifespan
            self.calculate_action_cost()
            action_index = self.calculate_action()
            self.sense_8_directions(world)
            self.perform_action(action_index, world)  # Perform the chosen action
            self.reproduction(world)
        else:
            self.lifespan = -1  # Mark as dead if energy is 0
            world.delete_creature(self)

        self.last_energy = self.energy
    def perform_action(self, action_index, world):
        """Perform the action corresponding to the given index and subtract action cost."""
        if 0 <= action_index < len(self.actions):
            # Subtract action cost from energy
            self.energy -= self.action_cost
            # Perform the action
            self.actions[action_index](world)

    def reproduction(self, world):
        """Reproduce if conditions are met."""
        if self.lifespan > self.maturity_level:
            # Define the 8 possible neighbor positions
            directions = [
                (-self.creature_size, -self.creature_size),  # Top-left
                (0, -self.creature_size),  # Top
                (self.creature_size, -self.creature_size),  # Top-right
                (-self.creature_size, 0),  # Left
                (self.creature_size, 0),  # Right
                (-self.creature_size, self.creature_size),  # Bottom-left
                (0, self.creature_size),  # Bottom
                (self.creature_size, self.creature_size)  # Bottom-right
            ]

            # Shuffle the directions to try them in random order
            random.shuffle(directions)

            for dx, dy in directions:
                new_x = self.x + dx
                new_y = self.y + dy

                # Check if the new position is valid
                if world.can_fit(new_x, new_y, self.creature_size):
                    # Split energy between parent and child
                    new_energy = self.energy / 2
                    self.energy /= 2
                    self.lifespan = 0
                    self.genetics.mutate(self.mutation_rate)
                    # Apply mutation
                    new_genetics = self.genetics.create_new_genetics(self.mutation_rate)
                    self.calculate_genetic_cost()

                    # Create new creature
                    new_creature = Creature(new_x, new_y, genetics=new_genetics)
                    new_creature.energy = new_energy

                    # Copy the parent's brain weights to the child
                    new_creature.brain = {
                        'input_to_hidden1': self.brain['input_to_hidden1'].copy(),
                        'hidden1_to_hidden2': self.brain['hidden1_to_hidden2'].copy(),
                        'hidden2_to_output': self.brain['hidden2_to_output'].copy()
                    }

                    # Apply mutation to the child's brain
                    new_creature.random_update_brain(self.mutation_rate)

                    world.add_creature(new_creature)
                    break

    def move_up(self, world):
        new_x = self.x
        new_y = self.y - self.creature_size
        if world.move_square(self.x, self.y, self.creature_size, new_x, new_y):
            self.x, self.y = new_x, new_y
            self.perform_action_cost()

    def move_down(self, world):
        new_x = self.x
        new_y = self.y + self.creature_size
        if world.move_square(self.x, self.y, self.creature_size, new_x, new_y):
            self.x, self.y = new_x, new_y
            self.perform_action_cost()

    def move_left(self, world):
        new_x = self.x - self.creature_size
        new_y = self.y
        if world.move_square(self.x, self.y, self.creature_size, new_x, new_y):
            self.x, self.y = new_x, new_y
            self.perform_action_cost()

    def move_right(self, world):
        new_x = self.x + self.creature_size
        new_y = self.y
        if world.move_square(self.x, self.y, self.creature_size, new_x, new_y):
            self.x, self.y = new_x, new_y
            self.perform_action_cost()

    def stay_still(self, world):
        pass  # Do nothing

    def consume_other_creatures(self, world):
        creatures_in_zone = world.get_creatures_in_action_zone(self)
        for other_creature in creatures_in_zone:
            energy_to_eat = params.GENERAL_ENERGY_CONSUMPTION * (self.genetics.consumption_rate + 0.5) * self.genetics.consume_other_creatures_ratio
            other_creature.energy -= energy_to_eat
            self.energy += energy_to_eat
        self.perform_action_cost()

    def share_resource_to_other_creatures(self, world):
        """
        Share energy with other creatures in the action zone based on resource_share_ratio.
        """
        # Get creatures in the action zone
        creatures_in_zone = world.get_creatures_in_action_zone(self)

        # Calculate the amount of energy to share
        energy_to_share = self.energy * self.genetics.resource_share_ratio

        # Distribute the energy equally among all creatures in the zone (including self)
        num_creatures = len(creatures_in_zone)
        if num_creatures > 0:
            energy_per_creature = energy_to_share / num_creatures
            for other_creature in creatures_in_zone:
                other_creature.energy += energy_per_creature
                self.energy -= energy_per_creature

        # Subtract action cost
        self.perform_action_cost()

    def sense_8_directions(self, world):
        """Sense in 8 directions (N, NE, E, SE, S, SW, W, NW) and return a list of sensed colors."""
        directions = [
            (0, -1),  # North
            (1, -1),  # Northeast
            (1, 0),  # East
            (1, 1),  # Southeast
            (0, 1),  # South
            (-1, 1),  # Southwest
            (-1, 0),  # West
            (-1, -1)  # Northwest
        ]

        i = 0
        for dx, dy in directions:
            color = self.sense_color_in_direction(world, dx, dy)
            self.sensed_color[i] = color[0] / 255
            self.sensed_color[i+1] = color[1] / 255
            self.sensed_color[i+2] = color[2] / 255
            i +=1

    def sense_color_in_direction(self, world, dx, dy):
        """Sense in a specific direction and return the color of the first creature encountered within the sense radius."""
        for i in range(1, int(self.genetics.sense_radius*params.SENSE_RADIUS_GENERAL) + 1):
            x = self.x + dx * i
            y = self.y + dy * i
            if x > world.width or y > world.height:
                break
            creature = world.get_creature_at(x, y)
            if creature is not None:
                return creature.color  # Return the color of the sensed creature
        return  [0,0,0]  # Return None if no creature is sensed