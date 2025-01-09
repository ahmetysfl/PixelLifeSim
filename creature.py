import random
import numpy as np
import parameters as params
from genetics import Genetics


class Creature:
    def __init__(self, x, y, genetics=None):
        self.x = x
        self.y = y
        self.genetics = genetics if genetics is not None else Genetics()
        self.action_cost = self.calculate_action_cost()
        self.energy = random.uniform(1, self.genetics.energy_capacity * params.MAX_ENERGY_CAPACITY)  # Energy between 1 and energy_capacity * MAX_ENERGY_CAPACITY
        self.maturity_level = int(params.MATURITY_LEVEL_MIN + params.MATURITY_LEVEL_MAX * self.genetics.production_rate)
        self.lifespan = 0
        self.actions = [self.move_up, self.move_down, self.move_left, self.move_right, self.stay_still, self.consume_other_creature]
        self.brain = self.initialize_brain()
        self.mutation_rate = params.MUTATION_RATE
        self.color = self.calculate_color()
        self.creature_size = params.CREATURE_SIZE_MIN + int(
            min(params.CREATURE_SIZE_MAX * self.genetics.energy_capacity, params.CREATURE_SIZE_MAX)
        )

    def calculate_action_cost(self):
        """
        Calculate the action cost based on production rate and energy capacity.
        Higher production rate and energy capacity result in higher action cost.
        """
        # Action cost is directly proportional to production rate and energy capacity
        ratio1 = self.genetics.production_rate / params.PRODUCTION_RATE_MAX
        ratio2 = self.genetics.energy_capacity  # Already normalized between MIN/MAX and 1
        ratio3 = self.genetics.action_zone_ratio  # Already normalized between MIN/MAX and 1
        ratio4 = self.genetics.consume_other_creatures_ratio  # Already normalized between MIN/MAX and 1
        return (ratio1 + ratio2 + ratio3 + ratio4) * params.GENERAL_ENERGY_CONSUMPTION / 4  # 0.01 scaling factor to keep it reasonable

    def initialize_brain(self):
        """Initialize a simple neural network."""
        input_size = len(self.get_inputs())
        hidden_layer_size = 8
        brain = {
            'input_to_hidden': np.random.rand(input_size, hidden_layer_size),
            'hidden_to_output': np.random.rand(hidden_layer_size, len(self.actions))
        }
        return brain

    def perform_action_cost(self):
        self.energy -= self.action_cost

    def calculate_action(self):
        """Determine an action using the neural network."""
        inputs = self.get_inputs()
        hidden_layer_output = np.tanh(np.dot(inputs, self.brain['input_to_hidden']))
        outputs = np.dot(hidden_layer_output, self.brain['hidden_to_output'])
        return np.argmax(outputs)

    def get_inputs(self):
        """Return normalized inputs for the neural network."""
        inputs = [
            self.x / params.WIDTH,
            self.y / params.HEIGHT,
            self.energy,  # Normalized energy
            self.genetics.energy_capacity * params.MAX_ENERGY_CAPACITY,
            self.lifespan / 100,
            self.action_cost
        ]
        return np.array(inputs)

    def calculate_color(self):
        """
        Calculate the color of the creature based on its genetic parameters.
        - High production rate: More green.
        - High consumption rate or tendency to consume other creatures: More red.
        - Other parameters (energy_capacity, action_zone_ratio): Influence blue.
        """
        # Normalize genetic parameters to a range of 0-1
        production_rate_norm = self.genetics.production_rate / params.PRODUCTION_RATE_MAX
        consumption_rate_norm = self.genetics.consumption_rate / params.CONSUMPTION_RATE_MAX
        consume_other_creatures_ratio_norm = self.genetics.consume_other_creatures_ratio / params.CONSUME_OTHER_CREATURES_RATIO_MAX
        energy_capacity_norm = self.genetics.energy_capacity  # Already normalized between MIN/MAX and 1
        action_zone_ratio_norm = self.genetics.action_zone_ratio  # Already normalized between MIN/MAX and 1

        # Calculate dominant color components
        # Green is dominant if production rate is significantly higher than consumption rate
        green_value = int(54 + production_rate_norm * 200)
        # Red is dominant if consumption rate or tendency to consume other creatures is high
        red_value = int(54 + max(consumption_rate_norm, consume_other_creatures_ratio_norm) * 200)
        # Blue is influenced by energy capacity and action zone ratio
        blue_value = int(54 + (energy_capacity_norm + action_zone_ratio_norm) / 2 * 200)

        # Adjust colors to make dominant traits more visible
        if production_rate_norm > consumption_rate_norm and production_rate_norm > consume_other_creatures_ratio_norm:
            # More green if production is dominant
            green_value = min(255, green_value + 50)
            red_value = max(0, red_value - 50)
        elif consume_other_creatures_ratio_norm > production_rate_norm and consume_other_creatures_ratio_norm > consumption_rate_norm:
            # More red if consuming other creatures is dominant
            red_value = min(255, red_value + 50)
            green_value = max(0, green_value - 50)
        elif consumption_rate_norm > production_rate_norm and consumption_rate_norm > consume_other_creatures_ratio_norm:
            # More red if consumption is dominant
            red_value = min(255, red_value + 50)
            green_value = max(0, green_value - 50)

        # Ensure color values are within the valid range (0-255)
        red_value = min(red_value, 255)
        green_value = min(green_value, 255)
        blue_value = min(blue_value, 255)

        return (red_value, green_value, blue_value)

    def update(self, world):
        """Update the creature's state."""
        if self.energy > 0:
            # Apply general energy consumption and production
            self.energy -= params.GENERAL_ENERGY_CONSUMPTION * self.genetics.consumption_rate
            # Aging effect
            self.energy -= params.GENERAL_ENERGY_CONSUMPTION * (self.lifespan / params.AGING_LEVEL_STARTS)
            crowded_calculation_ratio = min(1,params.CROWDED_ZONE_THRESHOLD / world.get_crowded_zone_count(self))
            self.energy += params.GENERAL_ENERGY_PRODUCTION * self.genetics.production_rate * crowded_calculation_ratio
            self.energy = min(self.energy, self.genetics.energy_capacity * params.MAX_ENERGY_CAPACITY) # Keep energy within bounds
            self.lifespan += 1  # Increment lifespan
            self.calculate_action_cost()
            action_index = self.calculate_action()
            self.perform_action(action_index, world)  # Perform the chosen action
            self.reproduction(world)
        else:
            self.lifespan = -1  # Mark as dead if energy is 0
            world.delete_creature(self)

        self.color = self.calculate_color()  # Update color based on energy

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
                    # Apply mutation
                    new_genetics = self.genetics.create_new_genetics(self.mutation_rate)

                    # Create new creature
                    new_creature = Creature(new_x, new_y, genetics=new_genetics)
                    new_creature.energy = new_energy
                    new_creature.color = new_creature.calculate_color()
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

    def consume_other_creature(self, world):
        creatures_in_zone = world.get_creatures_in_action_zone(self)
        for other_creature in creatures_in_zone:
            energy_to_eat = params.GENERAL_ENERGY_CONSUMPTION * self.genetics.consume_other_creatures_ratio
            other_creature.energy -= energy_to_eat
            self.energy += energy_to_eat
        self.perform_action_cost()