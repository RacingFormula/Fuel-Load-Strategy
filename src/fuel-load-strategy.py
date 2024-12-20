import numpy as np
import matplotlib.pyplot as plt

class FuelLoadStrategy:
    def __init__(self, config):
        self.fuel_capacity = config.get("fuel_capacity", 100)  # Litres
        self.fuel_consumption_rate = config.get("fuel_consumption_rate", 2.5)  # Litres per lap
        self.base_lap_time = config.get("base_lap_time", 80)  # Seconds
        self.lap_time_penalty_per_litre = config.get("lap_time_penalty_per_litre", 0.02)  # Seconds per litre
        self.race_distance = config.get("race_distance", 50)  # Laps
        self.pit_stop_time = config.get("pit_stop_time", 25)  # Seconds

    def simulate_strategy(self, initial_fuel_load):
        remaining_fuel = initial_fuel_load
        total_time = 0
        lap_times = []

        for lap in range(1, self.race_distance + 1):
            lap_time = self.base_lap_time + remaining_fuel * self.lap_time_penalty_per_litre
            total_time += lap_time

            remaining_fuel -= self.fuel_consumption_rate

            if remaining_fuel < 0:  # Refuel if fuel runs out
                total_time += self.pit_stop_time
                remaining_fuel = self.fuel_capacity - abs(remaining_fuel)

            lap_times.append(lap_time)

        return {
            "lap_times": lap_times,
            "total_time": total_time
        }

    def optimise_fuel_load(self):
        results = {}

        for initial_fuel_load in range(20, self.fuel_capacity + 1, 10):
            print(f"Simulating strategy for initial fuel load: {initial_fuel_load}L...")
            results[f"{initial_fuel_load}L"] = self.simulate_strategy(initial_fuel_load)

        return results

    def plot_results(self, results):
        laps = range(1, self.race_distance + 1)

        plt.figure(figsize=(14, 8))

        # Plot lap times
        plt.subplot(2, 1, 1)
        for strategy, data in results.items():
            plt.plot(laps, data["lap_times"], label=f"{strategy} Lap Times")
        plt.title("Lap Times Over Race Distance")
        plt.xlabel("Lap")
        plt.ylabel("Lap Time (s)")
        plt.legend()
        plt.grid(True)

        # Plot total race times
        plt.subplot(2, 1, 2)
        total_times = {strategy: data["total_time"] for strategy, data in results.items()}
        plt.bar(total_times.keys(), total_times.values(), color="skyblue")
        plt.title("Total Race Time Per Fuel Strategy")
        plt.xlabel("Strategy")
        plt.ylabel("Total Time (s)")
        plt.grid(True)

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    config = {
        "fuel_capacity": 100,
        "fuel_consumption_rate": 2.5,
        "base_lap_time": 80,
        "lap_time_penalty_per_litre": 0.02,
        "race_distance": 50,
        "pit_stop_time": 25
    }

    strategy_tool = FuelLoadStrategy(config)
    results = strategy_tool.optimise_fuel_load()
    strategy_tool.plot_results(results)