import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# User-adjustable parameters
# ============================================================

START_FREQUENCY_HZ = 77.0e9      # 77.0 GHz
BANDWIDTH_HZ = 0.5e9             # 0.5 GHz sweep bandwidth
CHIRP_DURATION_S = 40e-6         # 40 microseconds per chirp
IDLE_TIME_S = 2e-6               # small gap between chirps
NUM_CHIRPS = 4                   # number of chirps in the sequence
POINTS_PER_CHIRP = 400           # number of sampled points per chirp

FIG_WIDTH = 8
FIG_HEIGHT = 4.8
SAVE_FIGURE = False
OUTPUT_PATH = "fig_fmcw_chirp_sequence.png"


# ============================================================
# Derived parameters
# ============================================================

END_FREQUENCY_HZ = START_FREQUENCY_HZ + BANDWIDTH_HZ
CHIRP_SLOPE_HZ_PER_S = BANDWIDTH_HZ / CHIRP_DURATION_S


# ============================================================
# Helper function
# ============================================================

def generate_chirp_sequence(start_freq_hz, bandwidth_hz, chirp_duration_s,
                            idle_time_s, num_chirps, points_per_chirp):
    """
    Generate the time-frequency traces of an FMCW chirp sequence.

    Parameters
    ----------
    start_freq_hz : float
        Start frequency of each chirp in Hz.
    bandwidth_hz : float
        Sweep bandwidth of each chirp in Hz.
    chirp_duration_s : float
        Duration of one chirp in seconds.
    idle_time_s : float
        Idle gap between two adjacent chirps in seconds.
    num_chirps : int
        Number of chirps in the sequence.
    points_per_chirp : int
        Number of sample points used to draw one chirp.

    Returns
    -------
    chirp_time_list : list of ndarray
        Time coordinates for each chirp.
    chirp_freq_list : list of ndarray
        Frequency coordinates for each chirp.
    """
    chirp_time_list = []
    chirp_freq_list = []

    for chirp_idx in range(num_chirps):
        # Time offset of the current chirp in the whole sequence
        chirp_start_time = chirp_idx * (chirp_duration_s + idle_time_s)

        # Local time within one chirp
        t_local = np.linspace(0, chirp_duration_s, points_per_chirp)

        # Absolute time in the whole chirp sequence
        t_global = chirp_start_time + t_local

        # Linear frequency sweep: f(t) = f0 + S t
        f_chirp = start_freq_hz + (bandwidth_hz / chirp_duration_s) * t_local

        chirp_time_list.append(t_global)
        chirp_freq_list.append(f_chirp)

    return chirp_time_list, chirp_freq_list


# ============================================================
# Main plotting routine
# ============================================================

def plot_fmcw_chirp_sequence():
    """
    Plot the instantaneous frequency of an FMCW chirp sequence.
    """
    chirp_time_list, chirp_freq_list = generate_chirp_sequence(
        start_freq_hz=START_FREQUENCY_HZ,
        bandwidth_hz=BANDWIDTH_HZ,
        chirp_duration_s=CHIRP_DURATION_S,
        idle_time_s=IDLE_TIME_S,
        num_chirps=NUM_CHIRPS,
        points_per_chirp=POINTS_PER_CHIRP
    )

    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))

    # Plot each chirp
    for idx, (t, f) in enumerate(zip(chirp_time_list, chirp_freq_list)):
        ax.plot(t * 1e6, f / 1e9, linewidth=2)

        # Label each chirp near its center
        mid_idx = len(t) // 2
        ax.text(
            t[mid_idx] * 1e6,
            f[mid_idx] / 1e9 + 0.02,
            f"Chirp {idx + 1}",
            ha="center",
            va="bottom",
            fontsize=9
        )

    # Mark the start and end frequency levels for visual guidance
    ax.axhline(START_FREQUENCY_HZ / 1e9, linestyle="--", linewidth=1)
    ax.axhline(END_FREQUENCY_HZ / 1e9, linestyle="--", linewidth=1)

    # Axis labels and title
    ax.set_xlabel("Time (μs)")
    ax.set_ylabel("Frequency (GHz)")
    ax.set_title("Illustration of an FMCW Chirp Sequence")

    # Add a small text box for key parameters
    parameter_text = (
        f"Start frequency: {START_FREQUENCY_HZ / 1e9:.1f} GHz\n"
        f"Bandwidth: {BANDWIDTH_HZ / 1e9:.1f} GHz\n"
        f"Chirp duration: {CHIRP_DURATION_S * 1e6:.0f} μs\n"
        f"Chirp slope: {CHIRP_SLOPE_HZ_PER_S / 1e12:.2f} THz/s"
    )
    ax.text(
        0.02, 0.98, parameter_text,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.9)
    )

    # Improve readability
    ax.grid(True, linestyle="--", alpha=0.4)

    # Set axis limits with a small margin
    total_time_s = NUM_CHIRPS * CHIRP_DURATION_S + (NUM_CHIRPS - 1) * IDLE_TIME_S
    ax.set_xlim(0, total_time_s * 1e6)
    ax.set_ylim(
        START_FREQUENCY_HZ / 1e9 - 0.05,
        END_FREQUENCY_HZ / 1e9 + 0.08
    )

    fig.tight_layout()

    if SAVE_FIGURE:
        fig.savefig(OUTPUT_PATH, dpi=300, bbox_inches="tight")
        print(f"Figure saved to: {OUTPUT_PATH}")

    plt.show()


# ============================================================
# Script entry point
# ============================================================

if __name__ == "__main__":
    plot_fmcw_chirp_sequence()