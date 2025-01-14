import parameters as params
import math


class World:
    def __init__(self, width, height):
        self.width = width + params.CREATURE_SIZE_MAX
        self.height = height + params.CREATURE_SIZE_MAX
        self.world = [[None] * self.width for _ in range(self.height)]  # None ile başlat
        self.creatures = []

    def add_square(self, x, y, size, creature):
        """Belirtilen koordinatlara bir yaratık ekler."""
        if self.can_fit(x, y, size):
            for i in range(y, y + size):
                for j in range(x, x + size):
                    self.world[i][j] = creature
            return True
        return False

    def can_fit(self, x, y, size):
        """Belirtilen koordinatlara yaratık eklenebilir mi kontrol eder."""
        if x + size > self.width or y + size > self.height:
            return False
        for i in range(y, y + size):
            for j in range(x, x + size):
                if self.world[i][j] is not None:  # None kontrolü
                    return False
        return True

    def remove_square(self, x, y, size):
        """Belirtilen koordinatlardaki yaratığı kaldırır."""
        for i in range(y, y + size):
            for j in range(x, x + size):
                self.world[i][j] = None

    def move_square(self, old_x, old_y, size, new_x, new_y, creature):
        """Yaratığı eski konumundan yeni konuma taşır."""
        if new_x < 0 or new_y < 0 or new_x + size > self.width or new_y + size > self.height:
            return False

        self.remove_square(old_x, old_y, size)

        if self.can_fit(new_x, new_y, size):
            self.add_square(new_x, new_y, size, creature)
            return True
        else:
            self.add_square(old_x, old_y, size, creature)  # Eski konuma geri ekle
            return False

    def add_creature(self, creature):
        """Yeni bir yaratık ekler."""
        if self.can_fit(creature.x, creature.y, creature.creature_size):
            self.creatures.append(creature)
            self.add_square(creature.x, creature.y, creature.creature_size, creature)
            return True
        return False

    def delete_creature(self, creature):
        """Bir yaratığı siler."""
        if creature in self.creatures:
            self.remove_square(creature.x, creature.y, creature.creature_size)
            self.creatures.remove(creature)
            return True
        return False

    def get_creatures_in_action_zone(self, creature):
        """
        Verilen yaratığın etki alanındaki diğer yaratıkları bulur.

        Args:
            creature (Creature): Etki alanı kontrol edilecek yaratık.

        Returns:
            list: Etki alanındaki yaratıkların listesi.
        """
        creatures_in_zone = []
        center_x = creature.x + creature.creature_size // 2  # Yaratığın merkezi
        center_y = creature.y + creature.creature_size // 2  # Yaratığın merkezi

        # Etki alanı yarıçapını hesapla
        action_zone_radius = creature.genetics.action_zone_ratio * params.ACTION_ZONE_MAX

        for other_creature in self.creatures:
            if other_creature == creature:
                continue  # Kendisini atla

            # Diğer yaratığın merkezini hesapla
            other_center_x = other_creature.x + other_creature.creature_size // 2
            other_center_y = other_creature.y + other_creature.creature_size // 2

            # İki yaratık arasındaki mesafeyi hesapla
            distance = math.sqrt((center_x - other_center_x) ** 2 + (center_y - other_center_y) ** 2)

            # Etki alanında mı kontrol et
            if distance <= action_zone_radius:
                creatures_in_zone.append(other_creature)

        return creatures_in_zone

    def get_crowded_zone_count(self, creature):
        """
        Verilen yaratığın kalabalık bölgesindeki yaratık sayısını bulur.

        Args:
            creature (Creature): Kalabalık bölgesi kontrol edilecek yaratık.

        Returns:
            int: Kalabalık bölgedeki yaratık sayısı.
        """
        crowded_zone_count = 0
        center_x = creature.x + creature.creature_size // 2  # Yaratığın merkezi
        center_y = creature.y + creature.creature_size // 2  # Yaratığın merkezi

        # Kalabalık bölge yarıçapı
        crowded_zone_radius = params.CROWDED_ZONE_RADIUS

        for other_creature in self.creatures:
            # Diğer yaratığın merkezini hesapla
            other_center_x = other_creature.x + other_creature.creature_size // 2
            other_center_y = other_creature.y + other_creature.creature_size // 2

            # İki yaratık arasındaki mesafeyi hesapla
            distance = math.sqrt((center_x - other_center_x) ** 2 + (center_y - other_center_y) ** 2)

            # Kalabalık bölgede mi kontrol et
            if distance <= crowded_zone_radius:
                crowded_zone_count += 1

        return crowded_zone_count

    def get_creature_at(self, x, y):
        """Verilen koordinatlardaki yaratığı döndürür."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.world[y][x]
        return None
