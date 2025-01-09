import pickle
import os
import inspect
import glob

def save_simulation_state(w, params, save_dir="saved_simulations"):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    existing_files = [f for f in os.listdir(save_dir) if f.startswith("simulation_")]
    simulation_number = len(existing_files) + 1
    simulation_filename = os.path.join(save_dir, f"simulation_{simulation_number}.pkl")
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
