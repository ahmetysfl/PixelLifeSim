import saveSimulation as sim
import matplotlib.pyplot as plt

# Simülasyon adımlarını yükle
simulations_steps = sim.load_simulation_steps()

# Her bir adım için avg tüketim, üretim oranlarını, yaratık sayısını, consume_other_creatures_ratio, resource_share_ratio, energy_capacity, action_zone_ratio ve sense_radius değerlerini hesapla
avg_consumption_rates = []
avg_production_rates = []
creature_counts = []
avg_consume_other_ratio = []
avg_resource_share_ratio = []
avg_energy_capacity = []
avg_action_zone_ratio = []
avg_sense_radius = []

for step in simulations_steps:
    if (len(step) > 0 ):
        consumption_rates = [creature.genetics.consumption_rate for creature in step]
        production_rates = [creature.genetics.production_rate for creature in step]
        consume_other_ratios = [creature.genetics.consume_other_creatures_ratio for creature in step]
        resource_share_ratios = [creature.genetics.resource_share_ratio for creature in step]
        energy_capacities = [creature.genetics.energy_capacity for creature in step]
        action_zone_ratios = [creature.genetics.action_zone_ratio for creature in step]
        sense_radii = [creature.genetics.sense_radius for creature in step]

        # Consumption rate ortalaması
        avg_consumption_rates.append(sum(consumption_rates) / len(consumption_rates))

        # Production rate ortalaması
        avg_production_rates.append(sum(production_rates) / len(production_rates))

        # Consume other creatures ratio ortalaması
        avg_consume_other_ratio.append(sum(consume_other_ratios) / len(consume_other_ratios))

        # Resource share ratio ortalaması
        avg_resource_share_ratio.append(sum(resource_share_ratios) / len(resource_share_ratios))

        # Energy capacity ortalaması
        avg_energy_capacity.append(sum(energy_capacities) / len(energy_capacities))

        # Action zone ratio ortalaması
        avg_action_zone_ratio.append(sum(action_zone_ratios) / len(action_zone_ratios))

        # Sense radius ortalaması
        avg_sense_radius.append(sum(sense_radii) / len(sense_radii))

        # Yaratık sayısı
        creature_counts.append(len(step))

# Çizimi yap
fig, ax1 = plt.subplots(figsize=(18, 8))

# Tüketim oranları (ortalama)
ax1.plot(avg_consumption_rates, '-', label='Avg Consumption Rate', color='blue')

# Üretim oranları (ortalama)
ax1.plot(avg_production_rates, '-', label='Avg Production Rate', color='red')

# Consume other creatures ratio (ortalama)
ax1.plot(avg_consume_other_ratio, '-', label='Avg Consume Other Ratio', color='purple')

# Resource share ratio (ortalama)
ax1.plot(avg_resource_share_ratio, '-', label='Avg Resource Share Ratio', color='orange')

# Energy capacity (ortalama)
ax1.plot(avg_energy_capacity, '-', label='Avg Energy Capacity', color='cyan')

# Action zone ratio (ortalama)
ax1.plot(avg_action_zone_ratio, '-', label='Avg Action Zone Ratio', color='magenta')

# Sense radius (ortalama)
ax1.plot(avg_sense_radius, '-', label='Avg Sense Radius', color='brown')

ax1.set_xlabel('Simulation Step')
ax1.set_ylabel('Rate / Ratio / Capacity / Radius')
ax1.set_title(
    'Average Consumption, Production Rates, Consume Other Ratio, Resource Share Ratio, Energy Capacity, Action Zone Ratio, Sense Radius, and Creature Count Over Simulation Steps')
ax1.legend(loc='upper left')
ax1.grid(True)

# İkinci y ekseni için yaratık sayısını çiz
ax2 = ax1.twinx()
ax2.plot(creature_counts, '-', label='Creature Count', color='green')
ax2.set_ylabel('Creature Count')
ax2.legend(loc='upper right')

plt.show()
