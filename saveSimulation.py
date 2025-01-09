import pickle
import os

# Simülasyon durumunu kaydet
def save_simulation_state(w, params, save_dir="saved_simulations"):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    existing_files = [f for f in os.listdir(save_dir) if f.startswith("simulation_")]
    simulation_number = len(existing_files) + 1
    simulation_filename = os.path.join(save_dir, f"simulation_{simulation_number}.pkl")
    with open(simulation_filename, "wb") as file:
        pickle.dump({"w": w, "params": params}, file)
    print(f"Simulation state saved to {simulation_filename}")
    return simulation_filename

# Simülasyon durumunu yükle
def load_simulation_state(simulation_filename):
    with open(simulation_filename, "rb") as file:
        data = pickle.load(file)
    print(f"Simulation state loaded from {simulation_filename}")
    return data["w"], data["params"]