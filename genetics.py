import random
import parameters as params

class Genetics:
    def __init__(self, max_energy=None, consumption_rate=None, production_rate=None):
        self.max_energy = max_energy if max_energy is not None else self.initialize_max_energy()
        self.consumption_rate = consumption_rate if consumption_rate is not None else self.initialize_consumption_rate()
        self.production_rate = production_rate if production_rate is not None else self.initialize_production_rate()

    def initialize_max_energy(self):
        """Initialize max energy with a random value."""
        return random.randint(params.GENERAL_ENERGY_CONSUMPTION, params.MAX_ENERGY_CAPACITY)

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
        self.max_energy = int(self.max_energy * (1 + random.uniform(-mutation_rate, mutation_rate)))

        # Ensure values stay within bounds
        self.max_energy = max(params.GENERAL_ENERGY_CONSUMPTION, min(params.MAX_ENERGY_CAPACITY, self.max_energy))
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
        new_max_energy = int(self.max_energy * (1 + random.uniform(-mutation_rate, mutation_rate)))
        new_consumption_rate = self.consumption_rate * (1 + random.uniform(-mutation_rate, mutation_rate))
        new_production_rate = self.production_rate * (1 + random.uniform(-mutation_rate, mutation_rate))

        # Ensure values stay within bounds
        new_max_energy = max(params.GENERAL_ENERGY_CONSUMPTION, min(params.MAX_ENERGY_CAPACITY, new_max_energy))
        new_consumption_rate = max(params.CONSUMPTION_RATE_MIN, min(params.CONSUMPTION_RATE_MAX, new_consumption_rate))
        new_production_rate = max(params.PRODUCTION_RATE_MIN, min(params.PRODUCTION_RATE_MAX, new_production_rate))

        return Genetics(
            max_energy=new_max_energy,
            consumption_rate=new_consumption_rate,
            production_rate=new_production_rate
        )
