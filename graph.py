# visualization.py
import matplotlib.pyplot as plt
import numpy as np

def plot_graph(steps, total_creatures, production_rates, plot_pause):
    """
    Simülasyonun toplam yaratık sayısını ve üretim oranlarını grafik olarak çizer.
    """
    plt.ion()  # Etkileşimli modu aç
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 4))

    while True:
        if steps and total_creatures:
            # Toplam Yaratık Sayısı Grafiği
            ax1.clear()
            ax1.plot(steps, total_creatures, label="Total Creatures", color="blue")
            ax1.set_xlabel("Simulation Steps")
            ax1.set_ylabel("Number of Creatures")
            ax1.set_title("Total Number of Creatures Over Time")
            ax1.legend()
            ax1.grid(True)

            # Üretim Oranı Grafiği (Hata Çubukları ile)
            if production_rates:
                avg_rates = [np.mean(rates) for rates in production_rates]
                min_rates = [np.min(rates) for rates in production_rates]
                max_rates = [np.max(rates) for rates in production_rates]

                yerr = [np.array(avg_rates) - np.array(min_rates), np.array(max_rates) - np.array(avg_rates)]
                ax2.clear()
                ax2.errorbar(steps, avg_rates, yerr=yerr, fmt='-o', color="green", ecolor="gray", capsize=5, label="Production Rate")
                ax2.set_xlabel("Simulation Steps")
                ax2.set_ylabel("Production Rate")
                ax2.set_title("Production Rate (Min, Max, Avg) Over Time")
                ax2.legend()
                ax2.grid(True)

            plt.pause(plot_pause)  # Grafiği güncellemek için duraklat

def plot_genetics_scatter(creatures):
    """
    Yaratıkların genetik özelliklerini scatter plot olarak çizer.
    """
    # Genetik özellikleri topla
    consumption_rates = [creature.genetics.consumption_rate for creature in creatures]
    production_rates = [creature.genetics.production_rate for creature in creatures]
    action_zone_ratios = [creature.genetics.action_zone_ratio for creature in creatures]
    energy_capacities = [creature.genetics.energy_capacity for creature in creatures]

    # Scatter plot oluştur
    plt.figure(figsize=(12, 8))

    # Tüketim Oranı vs Üretim Oranı
    plt.subplot(2, 2, 1)
    plt.scatter(consumption_rates, production_rates, c='blue', alpha=0.5)
    plt.xlabel('Consumption Rate')
    plt.ylabel('Production Rate')
    plt.title('Consumption Rate vs Production Rate')

    # Tüketim Oranı vs Eylem Bölgesi Oranı
    plt.subplot(2, 2, 2)
    plt.scatter(consumption_rates, action_zone_ratios, c='green', alpha=0.5)
    plt.xlabel('Consumption Rate')
    plt.ylabel('Action Zone Ratio')
    plt.title('Consumption Rate vs Action Zone Ratio')

    # Üretim Oranı vs Enerji Kapasitesi
    plt.subplot(2, 2, 3)
    plt.scatter(production_rates, energy_capacities, c='red', alpha=0.5)
    plt.xlabel('Production Rate')
    plt.ylabel('Energy Capacity')
    plt.title('Production Rate vs Energy Capacity')

    # Eylem Bölgesi Oranı vs Enerji Kapasitesi
    plt.subplot(2, 2, 4)
    plt.scatter(action_zone_ratios, energy_capacities, c='purple', alpha=0.5)
    plt.xlabel('Action Zone Ratio')
    plt.ylabel('Energy Capacity')
    plt.title('Action Zone Ratio vs Energy Capacity')

    plt.tight_layout()
    plt.show()
