import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from quantum.environmental_experiment import run_vibration_frequency_sweep


def main() -> None:
    results = run_vibration_frequency_sweep()

    frequencies = [
        result.conditions.vibration_frequency_hz
        for result in results
    ]
    noise_percentages = [
        result.estimated_noise_probability * 100
        for result in results
    ]

    plt.figure(figsize=(9, 5))
    plt.plot(frequencies, noise_percentages, marker="o")
    plt.axvline(
        x=100,
        linestyle="--",
        label="Natural frequency: 100 Hz",
    )
    plt.title("Simulated Vibration Frequency vs Environmental Noise")
    plt.xlabel("Vibration frequency (Hz)")
    plt.ylabel("Estimated noise probability (%)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("experiments/vibration_frequency_plot.png", dpi=150)
    plt.close()

    print("Grafik kaydedildi: experiments/vibration_frequency_plot.png")
    print("Not: Grafik, gerçek donanım ölçümü değil, model simülasyonudur.")


if __name__ == "__main__":
    main()
