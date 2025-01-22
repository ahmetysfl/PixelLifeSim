import pygame
import saveSimulation as sim
from world import World
from creature import Creature
import parameters as params
from controlPanel import ControlPanel  # Kontrol paneli sınıfını içe aktar

def load_simulation(filename):
    """
    Kaydedilmiş bir simülasyon dosyasını yükler.

    :param filename: Yüklenecek simülasyon dosyasının adı.
    :return: Yüklenen simülasyon adımları.
    """
    return sim.load_simulation_steps(filename)

def create_creature_from_state(creature_state):
    """
    Creature state'inden yeni bir Creature nesnesi oluşturur.

    :param creature_state: Yaratığın iç durumu (get_internal_states ile elde edilen veri).
    :return: Yeni bir Creature nesnesi.
    """
    # Yeni bir yaratık oluştur
    new_creature = Creature(creature_state['x'], creature_state['y'])

    # Genetics bilgilerini ayarla
    new_creature.genetics.production_rate = creature_state['genetics']['production_rate']
    new_creature.genetics.consumption_rate = creature_state['genetics']['consumption_rate']
    new_creature.genetics.energy_capacity = creature_state['genetics']['energy_capacity']
    new_creature.genetics.action_zone_ratio = creature_state['genetics']['action_zone_ratio']
    new_creature.genetics.consume_other_creatures_ratio = creature_state['genetics']['consume_other_creatures_ratio']
    new_creature.genetics.resource_share_ratio = creature_state['genetics']['resource_share_ratio']
    new_creature.genetics.sense_radius = creature_state['genetics']['sense_radius']

    # Diğer özellikleri ayarla
    new_creature.energy = creature_state['energy']
    new_creature.creature_size = creature_state['creature_size']
    new_creature.calculate_color()

    return new_creature

def visualize_simulation(simulation_steps):
    """
    Simülasyon adımlarını pygame ile görselleştirir.

    :param simulation_steps: Simülasyon adımları.
    """
    # Pygame başlat
    pygame.init()
    window_width = params.WIDTH + 250  # Kontrol paneli için ekstra genişlik
    window_height = params.HEIGHT
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Simulation Visualization with Control Panel")
    clock = pygame.time.Clock()

    # Kontrol panelini başlat
    control_panel = ControlPanel(params.WIDTH, params.HEIGHT)

    # Simülasyon adımlarını döngüye al
    step_index = 0
    paused = False
    running = True

    while running:
        # Olayları işle
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Yaratık listesini handle_events fonksiyonuna geç
            if step_index < len(simulation_steps):
                creatures = [create_creature_from_state(creature_state) for creature_state in simulation_steps[step_index]]
                control_panel.handle_events(event, creatures)  # Yaratık listesini geç

        # Ekranı temizle
        screen.fill((0, 0, 0))

        # Kontrol paneli durumunu güncelle
        paused = control_panel.paused

        # Eğer simülasyon duraklatılmadıysa, bir sonraki adıma geç
        if not paused and step_index < len(simulation_steps):
            step = simulation_steps[step_index]
            step_index += 1

            # Her bir yaratık state'inden yeni bir Creature nesnesi oluştur
            creatures = [create_creature_from_state(creature_state) for creature_state in step]

            # Her bir yaratığı çiz
            for creature in creatures:
                pygame.draw.rect(screen, creature.color,
                                 (creature.x, creature.y, creature.creature_size, creature.creature_size))

        # Kontrol panelini çiz
        control_panel.draw(screen)

        # Ekranı güncelle
        pygame.display.flip()

        # FPS ayarla (örneğin, 10 FPS)
        clock.tick(1)

    # Pygame'i kapat
    pygame.quit()

# Simülasyon dosyasını yükle
simulation_steps = load_simulation("saved_simulations_steps/simulation_1.pkl")

# Simülasyonu görselleştir
visualize_simulation(simulation_steps)
