import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


# ============================================================
# User-adjustable parameters
# ============================================================

FIG_WIDTH = 12
FIG_HEIGHT = 7
FONT_SIZE_BOX = 16
FONT_SIZE_GROUP = 22
FONT_SIZE_LABEL = 16
BOX_LINEWIDTH = 1.8
ARROW_LINEWIDTH = 1.6

SAVE_FIGURE = True
OUTPUT_PATH = "figures/chapter2/fig_comm_system_block_diagram.png"


# ============================================================
# Helper functions
# ============================================================

def draw_box(ax, x, y, w, h, text, fontsize=16):
    """
    Draw a rectangular block with centered text.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes to draw on.
    x, y : float
        Bottom-left corner of the box.
    w, h : float
        Width and height of the box.
    text : str
        Text shown inside the box.
    fontsize : int
        Font size of the text.
    """
    rect = Rectangle(
        (x, y), w, h,
        fill=False,
        linewidth=BOX_LINEWIDTH,
        edgecolor="black"
    )
    ax.add_patch(rect)

    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize
    )


def draw_arrow(ax, x1, y1, x2, y2, linestyle="-"):
    """
    Draw an arrow from (x1, y1) to (x2, y2).
    """
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle="->",
            linewidth=ARROW_LINEWIDTH,
            linestyle=linestyle,
            color="black",
            shrinkA=0,
            shrinkB=0
        )
    )


def draw_group_box(ax, x, y, w, h):
    """
    Draw a dashed group box.
    """
    rect = Rectangle(
        (x, y), w, h,
        fill=False,
        linewidth=1.8,
        linestyle=(0, (4, 4)),
        edgecolor="black"
    )
    ax.add_patch(rect)


# ============================================================
# Main plotting routine
# ============================================================

def plot_comm_system_block_diagram():
    """
    Plot the basic link diagram of a digital communication system.
    """
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis("off")

    # --------------------------------------------------------
    # Layout parameters
    # --------------------------------------------------------
    box_w = 2.5
    box_h = 1.15

    # Top row (Transmitter): left to right
    top_y = 7.0
    top_x = [1.4, 4.3, 7.2, 10.1]
    top_labels = ["Source", "Source\nCoding", "Channel\nCoding", "Modulation"]

    # Bottom row (Receiver): left to right in placement,
    # but signal flow is right to left
    bottom_y = 1.6
    bottom_x = [1.4, 4.3, 7.2, 10.1]
    bottom_labels = ["Destination", "Decoding", "Demodulation", "Reception"]

    # Wireless channel
    channel_x = 10.3
    channel_y = 4.4
    channel_w = 2.7
    channel_h = 1.45

    # --------------------------------------------------------
    # Draw transmitter blocks
    # --------------------------------------------------------
    for x, label in zip(top_x, top_labels):
        draw_box(ax, x, top_y, box_w, box_h, label, fontsize=FONT_SIZE_BOX)

    # Arrows between transmitter blocks
    for i in range(len(top_x) - 1):
        draw_arrow(
            ax,
            top_x[i] + box_w, top_y + box_h / 2,
            top_x[i + 1],     top_y + box_h / 2
        )

    # --------------------------------------------------------
    # Draw wireless channel
    # --------------------------------------------------------
    draw_box(
        ax,
        channel_x, channel_y,
        channel_w, channel_h,
        "Wireless\nChannel",
        fontsize=FONT_SIZE_BOX
    )

    # Arrow from modulation down to wireless channel
    mod_center_x = top_x[-1] + box_w / 2
    mod_bottom_y = top_y
    channel_top_y = channel_y + channel_h

    draw_arrow(
        ax,
        mod_center_x, mod_bottom_y,
        mod_center_x, channel_top_y
    )

    ax.text(
        mod_center_x + 0.2, (mod_bottom_y + channel_top_y) / 2 + 0.05,
        "RF signal",
        fontsize=FONT_SIZE_LABEL,
        va="center",
        ha="left"
    )

    # --------------------------------------------------------
    # Draw receiver blocks
    # --------------------------------------------------------
    for x, label in zip(bottom_x, bottom_labels):
        draw_box(ax, x, bottom_y, box_w, box_h, label, fontsize=FONT_SIZE_BOX)

    # Receiver flow: right to left
    for i in range(len(bottom_x) - 1, 0, -1):
        draw_arrow(
            ax,
            bottom_x[i],            bottom_y + box_h / 2,
            bottom_x[i - 1] + box_w, bottom_y + box_h / 2
        )

    # Arrow from wireless channel down to reception
    rx_center_x = bottom_x[-1] + box_w / 2
    rx_top_y = bottom_y + box_h
    channel_bottom_y = channel_y

    draw_arrow(
        ax,
        rx_center_x, channel_bottom_y,
        rx_center_x, rx_top_y
    )

    ax.text(
        rx_center_x + 0.2, (channel_bottom_y + rx_top_y) / 2,
        "Distorted\nsignal",
        fontsize=FONT_SIZE_LABEL,
        va="center",
        ha="left"
    )

    # --------------------------------------------------------
    # Noise / Interference
    # --------------------------------------------------------
    noise_start_x = 8.8
    noise_start_y = 5.15
    noise_end_x = channel_x
    noise_end_y = 5.15

    draw_arrow(
        ax,
        noise_start_x, noise_start_y,
        noise_end_x, noise_end_y,
        linestyle=(0, (4, 4))
    )

    ax.text(
        8.5, 5.15,
        "Noise/\nInterference",
        fontsize=FONT_SIZE_LABEL,
        va="center",
        ha="right"
    )

    # --------------------------------------------------------
    # Group boxes
    # --------------------------------------------------------
    draw_group_box(ax, 0.9, 6.35, 13.8, 2.5)   # Transmitter group
    draw_group_box(ax, 0.9, 1.0, 13.8, 2.1)    # Receiver group

    # --------------------------------------------------------
    # Group titles
    # --------------------------------------------------------
    ax.text(
        8.0, 9.45,
        "Transmitter",
        fontsize=FONT_SIZE_GROUP,
        fontweight="bold",
        ha="center",
        va="center"
    )

    ax.text(
        8.0, 0.25,
        "Receiver",
        fontsize=FONT_SIZE_GROUP,
        fontweight="bold",
        ha="center",
        va="center"
    )

    fig.tight_layout()

    if SAVE_FIGURE:
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        fig.savefig(OUTPUT_PATH, dpi=300, bbox_inches="tight")
        print(f"Figure saved to: {OUTPUT_PATH}")

    plt.show()


# ============================================================
# Script entry point
# ============================================================

if __name__ == "__main__":
    plot_comm_system_block_diagram()