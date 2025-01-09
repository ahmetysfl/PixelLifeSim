import parameters


class World:
    def __init__(self, width, height):
        self.width = width + parameters.CREATURE_SIZE_MAX
        self.height = height + parameters.CREATURE_SIZE_MAX
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
