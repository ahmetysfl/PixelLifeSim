import random
import time
from creature import Creature
from world import World
import parameters as params
from genetics import Genetics
import saveSimulation as sim
import copy

def place_random_creatures(world, num_creatures, creature_size_max):
    """
    Dünyaya rastgele konumlarda belirli sayıda yaratık yerleştirir.

    :param world: Yaratıkların ekleneceği World nesnesi.
    :param num_creatures: Yerleştirilecek yaratık sayısı.
    :param creature_size_max: Yaratıkların maksimum boyutu.
    """
    for _ in range(num_creatures):
        while True:
            # Rastgele x ve y koordinatları oluştur
            x = random.randint(0, world.width - creature_size_max)
            y = random.randint(0, world.height - creature_size_max)

            # Yaratığın dünyaya sığabileceği bir konum bulunana kadar dene
            if world.can_fit(x, y, creature_size_max):
                # Yeni bir yaratık oluştur ve dünyaya ekle
                new_creature = Creature(x, y)
                world.add_creature(new_creature)
                break


def simulate_world(world, max_steps):
    """
    Dünyadaki tüm yaratıkları sırasıyla simüle eder.
    Maksimum adım sayısına ulaşana veya tüm yaratıklar ölene kadar devam eder.

    :param world: Simüle edilecek World nesnesi.
    :param max_steps: Maksimum adım sayısı.
    """
    step_count = 0
    all_creatures = []
    while step_count < max_steps and len(world.creatures) > 0:
        # Her bir yaratığı güncelle
        creature_info = []
        for creature in world.creatures:  # Kopya üzerinde döngü yap
            creature.update(world)
            creature_info.append(creature.get_internal_states())

        # Adım sayısını artır
        all_creatures.append(creature_info)
        step_count += 1
        print(f"Step {step_count}: {len(world.creatures)} creatures remaining.")

    sim.save_simulation_steps(all_creatures)
    # Simülasyon sonuçlarını yazdır
    if len(world.creatures) == 0:
        print("All creatures have died.")
    else:
        print(f"Simulation ended after {max_steps} steps with {len(world.creatures)} creatures remaining.")
        for _ in world.creatures:
            world.dead_creatures.append(_)

def expand_list_to_target_size(input_list, target_size):
    """
    Verilen listeyi hedef boyuta çıkarır. Eğer liste hedef boyuttan küçükse,
    mevcut elemanları kopyalayarak listeyi genişletir.

    :param input_list: Genişletilecek liste.
    :param target_size: Hedef liste boyutu.
    :return: Hedef boyuta ulaşmış liste.
    """
    if not input_list:
        raise ValueError("Input list cannot be empty.")  # Boş liste hatası

    current_size = len(input_list)
    if current_size >= target_size:
        return input_list[:target_size]  # Hedef boyuttan büyükse, kes

    # Kaç tane kopya gerektiğini hesapla
    num_copies = (target_size // current_size) + 1
    # Mevcut elemanları kopyalayarak listeyi genişlet
    expanded_list = (input_list * num_copies)[:target_size]

    return expanded_list

def create_world_from_creature_list(creature_list, world_width, world_height, max_attempts=100):
    """
    Verilen listedeki yaratıkların genetics ve brain değerlerini kullanarak yeni bir dünya oluşturur.
    Yeni yaratıklar, dünyada uygun bir konum bulunana kadar rastgele yerleştirilir.

    :param creature_list: Dünyaya eklenecek yaratıkların listesi.
    :param world_width: Dünyanın genişliği.
    :param world_height: Dünyanın yüksekliği.
    :param max_attempts: Bir yaratık için maksimum yerleştirme denemesi sayısı.
    :return: Yaratıkların eklendiği yeni World nesnesi.
    """
    world = World(world_width, world_height)
    for creature in creature_list:
        attempts = 0
        placed = False

        # Yeni bir yaratık oluştur (sadece genetics ve brain değerlerini al)
        new_creature = Creature(0, 0)  # Varsayılan konum (0, 0)
        new_creature.genetics = copy.deepcopy(creature.genetics)  # Genetics'i kopyala
        new_creature.brain = copy.deepcopy(creature.brain)  # Brain'i kopyala
        new_creature.energy = random.uniform(1, new_creature.genetics.energy_capacity * params.MAX_ENERGY_CAPACITY)  # Rastgele enerji
        new_creature.color = new_creature.calculate_color()  # Renk hesapla

        # Yaratığı dünyaya yerleştirmeye çalış
        while not placed and attempts < max_attempts:
            # Rastgele bir konum seç
            x = random.randint(0, world_width - new_creature.creature_size)
            y = random.randint(0, world_height - new_creature.creature_size)

            # Yaratığı dünyaya eklemeyi dene
            if world.can_fit(x, y, new_creature.creature_size):
                new_creature.x = x
                new_creature.y = y
                world.add_creature(new_creature)
                placed = True
            attempts += 1

        if not placed:
            print(f"Warning: Could not place creature after {max_attempts} attempts.")

    return world

def create_random_world(num_creatures, world_width, world_height):
    """
    Rastgele yaratıklarla dolu bir dünya oluşturur.

    :param num_creatures: Dünyaya eklenecek yaratık sayısı.
    :param world_width: Dünyanın genişliği.
    :param world_height: Dünyanın yüksekliği.
    :return: Yaratıkların eklendiği yeni World nesnesi.
    """
    world = World(world_width, world_height)
    for _ in range(num_creatures):
        x = random.randint(0, world_width - params.CREATURE_SIZE_MAX)
        y = random.randint(0, world_height - params.CREATURE_SIZE_MAX)
        new_creature = Creature(x, y)
        world.add_creature(new_creature)
    return world

def run_simulation_loop(max_generations, initial_num_creatures, world_width, world_height, max_steps_per_generation):
    """
    Belirli bir nesil sayısına kadar simülasyonları ardışık olarak çalıştırır.
    Her nesilde, önceki nesilden kalan yaratıklarla yeni bir dünya oluşturulur.

    :param max_generations: Maksimum nesil sayısı.
    :param initial_num_creatures: İlk nesildeki yaratık sayısı.
    :param world_width: Dünyanın genişliği.
    :param world_height: Dünyanın yüksekliği.
    :param max_steps_per_generation: Her nesildeki maksimum adım sayısı.
    """
    # İlk dünyayı oluştur
    world = create_random_world(initial_num_creatures, world_width, world_height)

    for generation in range(max_generations):
        print(f"\n--- Generation {generation + 1} ---")

        # Dünyanın durumunu kaydet
        sim.save_simulation_state(world, params)
        print(f"World state saved before generation {generation + 1}.")

        # Simülasyonu çalıştır
        simulate_world(world, max_steps_per_generation)

        # son ölen yaratıkları al
        remaining_creatures = world.creatures
        print(f"Remaining creatures after generation {generation + 1}: {len(remaining_creatures)}")

        succesfull_creatures = list(world.dead_creatures)
        # Kalan yaratıklarla yeni bir dünya oluştur
        world = create_world_from_creature_list(succesfull_creatures, world_width, world_height)
        print(len(world.creatures))
    print("\nSimulation loop completed.")


# Simülasyon döngüsünü başlat
run_simulation_loop(
    max_generations=10000,  # Maksimum nesil sayısı
    initial_num_creatures=200,  # İlk nesildeki yaratık sayısı
    world_width=params.WIDTH,  # Dünyanın genişliği
    world_height=params.HEIGHT,  # Dünyanın yüksekliği
    max_steps_per_generation=1000  # Her nesildeki maksimum adım sayısı
)