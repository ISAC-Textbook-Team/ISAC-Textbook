"""
Neyman-Pearson threshold visualization.

This script provides:
1. A static figure for textbook use.
2. An interactive Matplotlib window with a P_FA slider.

Simplified detection model:
    T | H0 ~ N(mu_h0, sigma^2)
    T | H1 ~ N(mu_h1, sigma^2)

The detector decides H1 if:
    T > gamma

Definitions:
    P_FA = P(T > gamma | H0)
    P_D  = P(T > gamma | H1)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from scipy.stats import norm


# ============================================================
# User-adjustable parameters
# ============================================================

MU_H0 = 0.0          # Mean of the detection statistic under H0
MU_H1 = 2.5          # Mean of the detection statistic under H1
SIGMA = 1.0          # Standard deviation under both hypotheses

P_FA_INIT = 0.05     # Initial false alarm probability
P_FA_MIN = 0.001     # Minimum slider value
P_FA_MAX = 0.30      # Maximum slider value

NUM_POINTS = 1200

SAVE_STATIC_FIGURE = True
STATIC_OUTPUT_PATH = "fig_np_threshold_static.png"


# ============================================================
# Computation functions
# ============================================================

def compute_np_threshold(p_fa, mu_h0=MU_H0, mu_h1=MU_H1, sigma=SIGMA):
    """
    Compute the Neyman-Pearson threshold and detection probability.

    Parameters
    ----------
    p_fa : float
        Prescribed false alarm probability.
    mu_h0 : float
        Mean of T under H0.
    mu_h1 : float
        Mean of T under H1.
    sigma : float
        Standard deviation of T under both hypotheses.

    Returns
    -------
    gamma : float
        Threshold satisfying P(T > gamma | H0) = p_fa.
    p_d : float
        Detection probability P(T > gamma | H1).
    """
    if not 0.0 < p_fa < 1.0:
        raise ValueError("p_fa must be between 0 and 1.")

    if sigma <= 0.0:
        raise ValueError("sigma must be positive.")

    # The threshold is determined by the right-tail probability under H0.
    gamma = norm.ppf(1.0 - p_fa, loc=mu_h0, scale=sigma)

    # The detection probability is the right-tail probability under H1.
    p_d = 1.0 - norm.cdf(gamma, loc=mu_h1, scale=sigma)

    return gamma, p_d


def generate_grid(mu_h0=MU_H0, mu_h1=MU_H1, sigma=SIGMA, num_points=NUM_POINTS):
    """
    Generate the x-axis grid and the two probability density functions.
    """
    x_min = min(mu_h0, mu_h1) - 4.0 * sigma
    x_max = max(mu_h0, mu_h1) + 4.0 * sigma

    x = np.linspace(x_min, x_max, num_points)

    pdf_h0 = norm.pdf(x, loc=mu_h0, scale=sigma)
    pdf_h1 = norm.pdf(x, loc=mu_h1, scale=sigma)

    return x, pdf_h0, pdf_h1


def add_tail_regions(ax, x, gamma, mu_h0, mu_h1, sigma, color_h0, color_h1):
    """
    Add shaded regions for P_FA and P_D.

    Visualization strategy:
    - P_FA is shown as the full right-tail area under p(T|H0).
    - To avoid confusing overlap, the orange region does NOT fill the entire
      right-tail area under p(T|H1). Instead, it only highlights the portion
      of p(T|H1) that lies above p(T|H0) for T > gamma.

    Note:
    - The true P_D is still computed from the full right-tail area under H1.
    - The orange shading is only a visualization aid.
    """
    x_tail = x[x >= gamma]

    pdf_h0_tail = norm.pdf(x_tail, loc=mu_h0, scale=sigma)
    pdf_h1_tail = norm.pdf(x_tail, loc=mu_h1, scale=sigma)

    # Full P_FA region under H0
    pfa_region = ax.fill_between(
        x_tail,
        0,
        pdf_h0_tail,
        color=color_h0,
        alpha=0.28,
        label=r"$P_{FA}$ region under $H_0$",
        zorder=1,
    )

    # Only highlight the additional part of H1 above H0
    mask = pdf_h1_tail > pdf_h0_tail

    pd_region = ax.fill_between(
        x_tail,
        pdf_h0_tail,
        pdf_h1_tail,
        where=mask,
        facecolor=color_h1,
        alpha=0.12,
        hatch="//",
        edgecolor=color_h1,
        linewidth=0.0,
        label=r"additional $P_D$ region under $H_1$",
        zorder=2,
    )

    return pfa_region, pd_region


def format_axes(ax):
    """
    Apply common axis formatting.
    """
    ax.set_xlabel(r"Detection statistic $T$")
    ax.set_ylabel("Probability density")
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.set_ylim(bottom=0)


# ============================================================
# Static figure
# ============================================================

def plot_static_np_figure(
    p_fa=P_FA_INIT,
    mu_h0=MU_H0,
    mu_h1=MU_H1,
    sigma=SIGMA,
    save_path=STATIC_OUTPUT_PATH,
):
    """
    Create and save a static NP threshold illustration.
    """
    color_h0 = "tab:blue"
    color_h1 = "tab:orange"
    color_threshold = "black"

    gamma, p_d = compute_np_threshold(p_fa, mu_h0, mu_h1, sigma)
    x, pdf_h0, pdf_h1 = generate_grid(mu_h0, mu_h1, sigma)

    fig, ax = plt.subplots(figsize=(12, 8))

    ax.plot(
        x,
        pdf_h0,
        color=color_h0,
        linewidth=2.2,
        label=r"$p(T\mid H_0)$",
        zorder=4,
    )

    ax.plot(
        x,
        pdf_h1,
        color=color_h1,
        linewidth=2.2,
        label=r"$p(T\mid H_1)$",
        zorder=4,
    )

    add_tail_regions(
        ax=ax,
        x=x,
        gamma=gamma,
        mu_h0=mu_h0,
        mu_h1=mu_h1,
        sigma=sigma,
        color_h0=color_h0,
        color_h1=color_h1,
    )

    ax.axvline(
        gamma,
        color=color_threshold,
        linestyle="--",
        linewidth=2.0,
        label=r"Threshold $\gamma$",
        zorder=5,
    )

    text = (
        rf"$P_{{FA}}={p_fa:.3f}$" + "\n"
        rf"$\gamma={gamma:.3f}$" + "\n"
        rf"$P_D={p_d:.3f}$"
    )

    ax.text(
        0.03,
        0.95,
        text,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=11,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.90),
    )

    ax.set_title("Neyman-Pearson Threshold Illustration")
    format_axes(ax)
    ax.legend(loc="upper right", fontsize=10)

    fig.tight_layout()

    if save_path is not None:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Static figure saved to: {save_path}")

    plt.show()


# ============================================================
# Interactive figure
# ============================================================

def run_interactive_np_demo(
    p_fa_init=P_FA_INIT,
    mu_h0=MU_H0,
    mu_h1=MU_H1,
    sigma=SIGMA,
):
    """
    Run an interactive Matplotlib demo with a P_FA slider.

    This function does not require Jupyter Notebook.
    It uses matplotlib.widgets.Slider and a callback function.
    """
    color_h0 = "tab:blue"
    color_h1 = "tab:orange"
    color_threshold = "black"

    gamma_init, p_d_init = compute_np_threshold(
        p_fa_init,
        mu_h0,
        mu_h1,
        sigma,
    )

    x, pdf_h0, pdf_h1 = generate_grid(mu_h0, mu_h1, sigma)

    fig, ax = plt.subplots(figsize=(12, 8))
    plt.subplots_adjust(bottom=0.28)

    ax.plot(
        x,
        pdf_h0,
        color=color_h0,
        linewidth=2.2,
        label=r"$p(T\mid H_0)$",
        zorder=4,
    )

    ax.plot(
        x,
        pdf_h1,
        color=color_h1,
        linewidth=2.2,
        label=r"$p(T\mid H_1)$",
        zorder=4,
    )

    pfa_region, pd_region = add_tail_regions(
        ax=ax,
        x=x,
        gamma=gamma_init,
        mu_h0=mu_h0,
        mu_h1=mu_h1,
        sigma=sigma,
        color_h0=color_h0,
        color_h1=color_h1,
    )

    threshold_line = ax.axvline(
        gamma_init,
        color=color_threshold,
        linestyle="--",
        linewidth=2.0,
        label=r"Threshold $\gamma$",
        zorder=5,
    )

    info_text = ax.text(
        0.03,
        0.95,
        "",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=11,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.90),
    )

    def update_text(p_fa, gamma, p_d):
        """
        Update the numerical values displayed on the plot.
        """
        info_text.set_text(
            rf"$P_{{FA}}={p_fa:.3f}$" + "\n"
            rf"$\gamma={gamma:.3f}$" + "\n"
            rf"$P_D={p_d:.3f}$"
        )

    update_text(p_fa_init, gamma_init, p_d_init)

    ax.set_title("Interactive Neyman-Pearson Threshold Illustration")
    format_axes(ax)
    ax.legend(loc="upper right", fontsize=10)

    slider_ax = fig.add_axes([0.14, 0.10, 0.58, 0.04])

    pfa_slider = Slider(
        ax=slider_ax,
        label=r"$P_{FA}$",
        valmin=P_FA_MIN,
        valmax=P_FA_MAX,
        valinit=p_fa_init,
        valstep=0.001,
    )

    def update(val):
        """
        Callback function triggered when the P_FA slider changes.
        """
        nonlocal pfa_region, pd_region

        p_fa = pfa_slider.val
        gamma, p_d = compute_np_threshold(p_fa, mu_h0, mu_h1, sigma)

        # Move the threshold line.
        threshold_line.set_xdata([gamma, gamma])

        # Remove old shaded regions.
        pfa_region.remove()
        pd_region.remove()

        # Add updated shaded regions.
        pfa_region, pd_region = add_tail_regions(
            ax=ax,
            x=x,
            gamma=gamma,
            mu_h0=mu_h0,
            mu_h1=mu_h1,
            sigma=sigma,
            color_h0=color_h0,
            color_h1=color_h1,
        )

        update_text(p_fa, gamma, p_d)

        fig.canvas.draw_idle()

    pfa_slider.on_changed(update)

    reset_ax = fig.add_axes([0.80, 0.095, 0.10, 0.05])
    reset_button = Button(reset_ax, "Reset")

    def reset(event):
        """
        Reset the slider to its initial value.
        """
        pfa_slider.reset()

    reset_button.on_clicked(reset)

    plt.show()


# ============================================================
# Main execution
# ============================================================

if __name__ == "__main__":
    if SAVE_STATIC_FIGURE:
        plot_static_np_figure()

    run_interactive_np_demo()