"""
FMCW beat frequency visualization.

This script illustrates how a delayed echo in an FMCW radar produces
a beat frequency after mixing with the local transmitted chirp.

Simplified model:
    - Doppler effect is ignored.
    - The transmitted chirp is linear in frequency.
    - The received echo is modeled as a delayed version of the transmitted chirp.

Main relationship:
    f_b ≈ S * tau

where:
    S   : chirp slope
    tau : round-trip propagation delay
    f_b : beat frequency
"""

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# User-adjustable parameters
# ============================================================

SPEED_OF_LIGHT = 3.0e8             # Speed of light in m/s

START_FREQUENCY_HZ = 77.0e9        # 77 GHz automotive radar band
BANDWIDTH_HZ = 0.5e9               # 0.5 GHz chirp bandwidth
CHIRP_DURATION_S = 40e-6           # 40 microseconds chirp duration

TARGET_RANGE_M = 60.0              # Target range in meters

NUM_POINTS = 2000                  # Number of samples for plotting
BEAT_SIGNAL_DURATION_S = 2e-6      # Time window for plotting beat signal

FIG_WIDTH = 8.5
FIG_HEIGHT = 6.0

SAVE_FIGURE = True
OUTPUT_PATH = "figures/chapter2/fig_fmcw_beat_frequency.png"


# ============================================================
# Derived parameters
# ============================================================

CHIRP_SLOPE_HZ_PER_S = BANDWIDTH_HZ / CHIRP_DURATION_S

ROUND_TRIP_DELAY_S = 2.0 * TARGET_RANGE_M / SPEED_OF_LIGHT

BEAT_FREQUENCY_HZ = CHIRP_SLOPE_HZ_PER_S * ROUND_TRIP_DELAY_S


# ============================================================
# Data generation functions
# ============================================================

def generate_frequency_traces(
    chirp_duration_s: float,
    chirp_slope_hz_per_s: float,
    time_delay_s: float,
    num_points: int,
):
    """
    Generate frequency-offset traces for the transmitted chirp and delayed echo.

    The vertical axis is frequency offset from the start frequency f0,
    rather than the absolute carrier frequency. This makes the beat
    frequency easier to see.

    Returns
    -------
    time_s : ndarray
        Time samples within one chirp.
    tx_offset_hz : ndarray
        Frequency offset of the transmitted chirp.
    rx_offset_hz : ndarray
        Frequency offset of the delayed echo.
    valid_echo_mask : ndarray of bool
        Boolean mask indicating the time region where the delayed echo exists.
    """
    time_s = np.linspace(0.0, chirp_duration_s, num_points)

    # Transmitted chirp frequency offset:
    # f_tx(t) - f0 = S * t
    tx_offset_hz = chirp_slope_hz_per_s * time_s

    # Delayed echo frequency offset:
    # f_rx(t) - f0 = S * (t - tau)
    # It is only physically meaningful for t >= tau.
    rx_offset_hz = chirp_slope_hz_per_s * (time_s - time_delay_s)

    valid_echo_mask = time_s >= time_delay_s

    return time_s, tx_offset_hz, rx_offset_hz, valid_echo_mask


def generate_beat_signal(
    beat_frequency_hz: float,
    duration_s: float,
    num_points: int,
):
    """
    Generate a simplified low-frequency beat signal.

    The actual received signal and local chirp are high-frequency RF signals.
    After mixing and low-pass filtering, the beat signal can be represented
    as a low-frequency sinusoid with frequency f_b.
    """
    time_s = np.linspace(0.0, duration_s, num_points)
    beat_signal = np.cos(2.0 * np.pi * beat_frequency_hz * time_s)

    return time_s, beat_signal


# ============================================================
# Plotting function
# ============================================================

def plot_fmcw_beat_frequency():
    """
    Plot frequency-offset traces and the corresponding beat signal.
    """
    time_s, tx_offset_hz, rx_offset_hz, valid_echo_mask = generate_frequency_traces(
        chirp_duration_s=CHIRP_DURATION_S,
        chirp_slope_hz_per_s=CHIRP_SLOPE_HZ_PER_S,
        time_delay_s=ROUND_TRIP_DELAY_S,
        num_points=NUM_POINTS,
    )

    beat_time_s, beat_signal = generate_beat_signal(
        beat_frequency_hz=BEAT_FREQUENCY_HZ,
        duration_s=BEAT_SIGNAL_DURATION_S,
        num_points=NUM_POINTS,
    )

    fig, axes = plt.subplots(
        nrows=2,
        ncols=1,
        figsize=(FIG_WIDTH, FIG_HEIGHT),
        sharex=False,
    )

    ax_freq = axes[0]
    ax_beat = axes[1]

    # ========================================================
    # Subplot 1: transmitted chirp and delayed echo
    # ========================================================

    ax_freq.plot(
        time_s * 1e6,
        tx_offset_hz / 1e6,
        linewidth=2.2,
        label="Transmitted chirp",
    )

    ax_freq.plot(
        time_s[valid_echo_mask] * 1e6,
        rx_offset_hz[valid_echo_mask] / 1e6,
        linewidth=2.2,
        linestyle="--",
        label="Delayed echo",
    )

    # Choose a reference time to annotate the beat frequency.
    reference_time_s = 0.65 * CHIRP_DURATION_S
    tx_ref_hz = CHIRP_SLOPE_HZ_PER_S * reference_time_s
    rx_ref_hz = CHIRP_SLOPE_HZ_PER_S * (reference_time_s - ROUND_TRIP_DELAY_S)

    ax_freq.annotate(
        "",
        xy=(reference_time_s * 1e6, tx_ref_hz / 1e6),
        xytext=(reference_time_s * 1e6, rx_ref_hz / 1e6),
        arrowprops=dict(arrowstyle="<->", linewidth=1.5),
    )

    ax_freq.text(
        reference_time_s * 1e6 + 1.0,
        (tx_ref_hz + rx_ref_hz) / 2.0 / 1e6,
        r"$f_b \approx S\tau$",
        va="center",
        fontsize=10,
    )

    # Mark the round-trip delay on the time axis.
    ax_freq.annotate(
        "",
        xy=(ROUND_TRIP_DELAY_S * 1e6, 20),
        xytext=(0, 20),
        arrowprops=dict(arrowstyle="<->", linewidth=1.4),
    )

    ax_freq.text(
        ROUND_TRIP_DELAY_S * 0.5 * 1e6,
        35,
        r"Delay $\tau$",
        ha="center",
        va="bottom",
        fontsize=10,
    )

    ax_freq.set_ylabel("Frequency offset from $f_0$ (MHz)")
    ax_freq.set_title("FMCW Chirp and Delayed Echo")
    ax_freq.grid(True, linestyle="--", alpha=0.4)
    ax_freq.legend(loc="upper left")

    # ========================================================
    # Subplot 2: beat signal after mixing
    # ========================================================

    ax_beat.plot(
        beat_time_s * 1e6,
        beat_signal,
        linewidth=2.0,
        label="Beat signal after mixing",
    )

    ax_beat.set_xlabel("Time (μs)")
    ax_beat.set_ylabel("Amplitude")
    ax_beat.set_title("Beat Signal")
    ax_beat.grid(True, linestyle="--", alpha=0.4)
    ax_beat.legend(loc="upper right")

    # Add a compact parameter box.
    parameter_text = (
        f"Target range: {TARGET_RANGE_M:.0f} m\n"
        f"Delay τ: {ROUND_TRIP_DELAY_S * 1e6:.3f} μs\n"
        f"Chirp slope S: {CHIRP_SLOPE_HZ_PER_S / 1e12:.2f} THz/s\n"
        f"Beat frequency: {BEAT_FREQUENCY_HZ / 1e6:.2f} MHz"
    )

    ax_beat.text(
        0.02,
        0.95,
        parameter_text,
        transform=ax_beat.transAxes,
        ha="left",
        va="top",
        fontsize=9,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.9),
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
    plot_fmcw_beat_frequency()