import random
import parameters as params


class Genetics:
    def __init__(self, energy_capacity=None, consumption_rate=None, production_rate=None):
        self.energy_capacity = energy_capacity if energy_capacity is not None else self.initialize_energy_capacity()
        self.consumption_rate = consumption_rate if consumption_rate is not None else self.initialize_consumption_rate()
        self.production_rate = production_rate if production_rate is not None else self.initialize_production_rate()

    def initialize_energy_capacity(self):
        """Initialize energy capacity with a random value between MIN_ENERGY_CAPACITY/MAX_ENERGY_CAPACITY and 1."""
        return random.uniform(params.MIN_ENERGY_CAPACITY / params.MAX_ENERGY_CAPACITY, 1)

    def initialize_consumption_rate(self):
        """Initialize consumption rate with a random value."""
        return random.uniform(params.CONSUMPTION_RATE_MIN, params.CONSUMPTION_RATE_MAX)

    def initialize_production_rate(self):
        """Initialize production rate with a random value."""
        return random.uniform(params.PRODUCTION_RATE_MIN, params.PRODUCTION_RATE_MAX)

    def mutate(self, mutation_rate):
        """Mutate the genetic traits."""
        self.consumption_rate *= (1 + random.uniform(-mutation_rate, mutation_rate))
        self.production_rate *= (1 + random.uniform(-mutation_rate, mutation_rate))
        self.energy_capacity *= (1 + random.uniform(-mutation_rate, mutation_rate))

        # Ensure values stay within bounds
        self.energy_capacity = max(params.MIN_ENERGY_CAPACITY / params.MAX_ENERGY_CAPACITY,
                                   min(self.energy_capacity, 1))
        self.consumption_rate = max(params.CONSUMPTION_RATE_MIN,
                                    min(params.CONSUMPTION_RATE_MAX, self.consumption_rate))
        self.production_rate = max(params.PRODUCTION_RATE_MIN, min(params.PRODUCTION_RATE_MAX, self.production_rate))

    def create_new_genetics(self, mutation_rate=0.1):
        """
        Create a new Genetics object based on the current one, with optional mutation.

        Args:
            mutation_rate (float): The rate at which the genetic traits can mutate.

        Returns:
            Genetics: A new Genetics object with potentially mutated traits.
        """
        new_energy_capacity = self.energy_capacity * (1 + random.uniform(-mutation_rate, mutation_rate))
        new_consumption_rate = self.consumption_rate * (1 + random.uniform(-mutation_rate, mutation_rate))
        new_production_rate = self.production_rate * (1 + random.uniform(-mutation_rate, mutation_rate))

        # Ensure values stay within bounds
        new_energy_capacity = max(params.MIN_ENERGY_CAPACITY / params.MAX_ENERGY_CAPACITY,
                                  min(new_energy_capacity, 1))
        new_consumption_rate = max(params.CONSUMPTION_RATE_MIN, min(params.CONSUMPTION_RATE_MAX, new_consumption_rate))
        new_production_rate = max(params.PRODUCTION_RATE_MIN, min(params.PRODUCTION_RATE_MAX, new_production_rate))

        return Genetics(
            energy_capacity=new_energy_capacity,
            consumption_rate=new_consumption_rate,
            production_rate=new_production_rate
        )
