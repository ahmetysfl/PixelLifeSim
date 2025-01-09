import parameters as params
import math


class World:
    def __init__(self, width, height):
        self.width = width + params.CREATURE_SIZE_MAX
        self.height = height + params.CREATURE_SIZE_MAX
        self.world = [[0] * self.width for _ in range(self.height)]
        self.creatures = []

    def add_square(self, x, y, size):
        if self.can_fit(x, y, size):
            for i in range(y, y + size):
                for j in range(x, x + size):
                    self.world[i][j] = 1
            return True
        return False

    def can_fit(self, x, y, size):
        if x + size > self.width or y + size > self.height:
            return False
        for i in range(y, y + size):
            for j in range(x, x + size):
                if self.world[i][j] == 1:
                    return False
        return True

    def remove_square(self, x, y, size):
        for i in range(y, y + size):
            for j in range(x, x + size):
                self.world[i][j] = 0

    def move_square(self, old_x, old_y, size, new_x, new_y):
        if new_x < 0 or new_y < 0 or new_x + size > self.width or new_y + size > self.height:
            return False

        self.remove_square(old_x, old_y, size)

        if self.can_fit(new_x, new_y, size):
            self.add_square(new_x, new_y, size)
            return True
        else:
            self.add_square(old_x, old_y, size)
            return False

    def add_creature(self, creature):
        """Add a new creature to the world."""
        if self.can_fit(creature.x, creature.y, creature.creature_size):
            self.creatures.append(creature)
            self.add_square(creature.x, creature.y, creature.creature_size)
            return True
        return False

    def delete_creature(self, creature):
        """Delete a creature from the world."""
        if creature in self.creatures:
            self.remove_square(creature.x, creature.y, creature.creature_size)
            self.creatures.remove(creature)
            return True
        return False

    def get_creatures_in_action_zone(self, creature):
        """
        Get all creatures within the action zone of the given creature.

        Args:
            creature (Creature): The creature whose action zone is being checked.

        Returns:
            list: A list of creatures within the action zone.
        """
        creatures_in_zone = []
        center_x = creature.x + creature.creature_size // 2  # Center of the creature
        center_y = creature.y + creature.creature_size // 2  # Center of the creature

        # Calculate the radius of the action zone
        action_zone_radius = creature.genetics.action_zone_ratio * params.ACTION_ZONE_MAX

        for other_creature in self.creatures:
            if other_creature == creature:
                continue  # Skip the creature itself

            # Calculate the center of the other creature
            other_center_x = other_creature.x + other_creature.creature_size // 2
            other_center_y = other_creature.y + other_creature.creature_size // 2

            # Calculate the distance between the two creatures
            distance = math.sqrt((center_x - other_center_x) ** 2 + (center_y - other_center_y) ** 2)

            # Check if the other creature is within the action zone
            if distance <= action_zone_radius:
                creatures_in_zone.append(other_creature)

        return creatures_in_zone

    def get_crowded_zone_count(self, creature):
        """
        Get the number of creatures in the crowded zone around the given creature.

        Args:
            creature (Creature): The creature whose crowded zone is being checked.

        Returns:
            int: The number of creatures in the crowded zone.
        """
        crowded_zone_count = 0
        center_x = creature.x + creature.creature_size // 2  # Center of the creature
        center_y = creature.y + creature.creature_size // 2  # Center of the creature

        # Calculate the radius of the crowded zone
        crowded_zone_radius = params.CROWDED_ZONE_RADIUS

        for other_creature in self.creatures:

            # Calculate the center of the other creature
            other_center_x = other_creature.x + other_creature.creature_size // 2
            other_center_y = other_creature.y + other_creature.creature_size // 2

            # Calculate the distance between the two creatures
            distance = math.sqrt((center_x - other_center_x) ** 2 + (center_y - other_center_y) ** 2)

            # Check if the other creature is within the crowded zone
            if distance <= crowded_zone_radius:
                crowded_zone_count += 1

        return crowded_zone_count
