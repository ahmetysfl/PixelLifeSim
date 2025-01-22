import pickle
import os
import inspect
import glob
import random
from genetics import Genetics


def save_simulation_state(w, params, save_dir="saved_simulations", filename=None):
    """
    Simülasyon durumunu kaydeder.

    :param w: World nesnesi.
    :param params: Parametreler.
    :param save_dir: Kaydedilecek dizin (varsayılan: "saved_simulations").
    :param filename: Kaydedilecek dosya adı (opsiyonel).
    :return: Kaydedilen dosyanın tam yolu.
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Dosya adı belirtilmemişse, otomatik bir dosya adı oluştur
    if filename is None:
        existing_files = [f for f in os.listdir(save_dir) if f.startswith("simulation_")]
        simulation_number = len(existing_files) + 1
        filename = f"simulation_{simulation_number}.pkl"

    simulation_filename = os.path.join(save_dir, filename)
    params_dict = {name: value for name, value in inspect.getmembers(params) if not name.startswith("__")}
    with open(simulation_filename, "wb") as file:
        pickle.dump({"w": w, "params": params_dict}, file)
    print(f"Simulation state saved to {simulation_filename}")
    return simulation_filename


def load_simulation_state(simulation_filename=None, save_dir="saved_simulations"):
    # Eğer dosya adı belirtilmemişse, en son kaydedilen dosyayı bul
    if simulation_filename is None:
        list_of_files = glob.glob(os.path.join(save_dir, "simulation_*.pkl"))
        if not list_of_files:
            raise FileNotFoundError("No saved simulation files found.")
        simulation_filename = max(list_of_files, key=os.path.getctime)
        print(f"Loading the most recent simulation file: {simulation_filename}")

    # Dosyayı yükle
    with open(simulation_filename, "rb") as file:
        data = pickle.load(file)

    # Parametreleri güncelle
    import parameters as params_module
    for key, value in data["params"].items():
        setattr(params_module, key, value)

    print(f"Simulation state loaded from {simulation_filename}")
    return data["w"], params_module

def save_brain_states(w,save_dir="saved_brains"):
    file_name = "brain_states_"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    existing_files = [f for f in os.listdir(save_dir) if f.startswith(file_name)]
    simulation_number = len(existing_files) + 1
    save_filename = os.path.join(save_dir, f"{file_name}{simulation_number}.pkl")
    brains = [crature.brain for crature in w.creatures]
    with open(save_filename, "wb") as file:
        pickle.dump(brains, file)
    print(f"Brain state saved to {save_filename}")
    return save_filename
def load_brain_states(simulation_filename=None, save_dir="saved_brains"):
    # Eğer dosya adı belirtilmemişse, en son kaydedilen dosyayı bul
    file_name = "brain_states_"
    if simulation_filename is None:
        list_of_files = glob.glob(os.path.join(save_dir, f"{file_name}*.pkl"))
        if not list_of_files:
            raise FileNotFoundError("No saved simulation files found.")
        simulation_filename = max(list_of_files, key=os.path.getctime)
        print(f"Loading the most recent simulation file: {simulation_filename}")

    # Dosyayı yükle
    with open(simulation_filename, "rb") as file:
        data = pickle.load(file)
    return data


def extend_list_to_size(original_list, target_size):
    # Eğer liste zaten hedef boyuttan büyük veya eşitse, olduğu gibi döndür
    if len(original_list) >= target_size:
        return original_list

    # Yeni listeyi orijinal liste ile başlat
    extended_list = original_list.copy()

    # Rastgele elemanlar ekle
    while len(extended_list) < target_size:
        random_element = random.choice(original_list)
        extended_list.append(random_element)

    return extended_list

def create_new_genetics_list ():
    genetics_list = []
    producer_genetics = Genetics()
    producer_genetics.consumption_rate = 0
    producer_genetics.action_zone_ratio = 0
    producer_genetics.production_rate = 1
    producer_genetics.energy_capacity = 0.2
    producer_genetics.consume_other_creatures_ratio = 0
    for _ in range(0):
        genetics_list.append(producer_genetics)

    consumer_genetics = Genetics()
    consumer_genetics.consumption_rate = 0.25
    consumer_genetics.action_zone_ratio = 0.5
    consumer_genetics.production_rate = 0.2
    consumer_genetics.energy_capacity = 0.6
    consumer_genetics.consume_other_creatures_ratio = 1
    for _ in range(0):
        genetics_list.append(consumer_genetics)
    return genetics_list


def save_simulation_steps(creatures_list, save_dir="saved_simulations_steps", filename=None):
    """
    Simülasyon adımlarını kaydeder.

    :param creatures_list: Yaratık listesi.
    :param save_dir: Kaydedilecek dizin (varsayılan: "saved_simulations_steps").
    :param filename: Kaydedilecek dosya adı (opsiyonel).
    :return: Kaydedilen dosyanın tam yolu.
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Dosya adı belirtilmemişse, otomatik bir dosya adı oluştur
    if filename is None:
        existing_files = [f for f in os.listdir(save_dir) if f.startswith("simulation_")]
        simulation_number = len(existing_files) + 1
        filename = f"simulation_{simulation_number}.pkl"

    simulation_filename = os.path.join(save_dir, filename)
    with open(simulation_filename, "wb") as file:
        pickle.dump(creatures_list, file)
    print(f"Simulation state saved to {simulation_filename}")
    return simulation_filename


def load_simulation_steps(simulation_filename=None, save_dir="saved_simulations_steps"):
    """
    Kaydedilmiş simülasyon adımlarını yükler.

    Args:
        simulation_filename (str, optional): Yüklenecek dosyanın adı.
            Belirtilmezse en son kaydedilen dosya yüklenir.
        save_dir (str, optional): Kaydedilmiş dosyaların bulunduğu dizin.
            Varsayılan: "saved_simulations_steps".

    Returns:
        list: Yüklenen yaratık listesi.
    """
    # Eğer dosya adı belirtilmemişse, en son kaydedilen dosyayı bul
    if simulation_filename is None:
        list_of_files = glob.glob(os.path.join(save_dir, "simulation_*.pkl"))
        if not list_of_files:
            raise FileNotFoundError("No saved simulation files found.")
        simulation_filename = max(list_of_files, key=os.path.getctime)
        print(f"Loading the most recent simulation file: {simulation_filename}")

    # Dosyayı yükle
    with open(simulation_filename, "rb") as file:
        creatures_list = pickle.load(file)

    print(f"Simulation steps loaded from {simulation_filename}")
    return creatures_list
