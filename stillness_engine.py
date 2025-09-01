# Stillness Engine: A Simulation of Harmonic Locking
#
# This script provides an interactive and renderable simulation of the
# core principles from The Stillness Project.
#
# Dependencies:
# - numpy
# - matplotlib
#
# For video saving functionality (`--save-video` flag):
# - ffmpeg: This must be installed and available in the system's PATH.
#   - On Debian/Ubuntu: sudo apt-get install ffmpeg
#   - On macOS (with Homebrew): brew install ffmpeg
#   - On Windows: Download from https://ffmpeg.org/download.html and add to PATH.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.widgets import Button, CheckButtons
import argparse

# --- Core Parameters from The Stillness Project ---
F_HIGH = 117.0  # Hz (Synchrony Gate)
T_LOW = 7.83    # seconds (Stillness Pulse)
F_LOW = 1 / T_LOW # Hz

# --- Simulation Configuration ---
SIM_DURATION = 12.0  # seconds
FPS = 30             # Frames per second for the animation

class StillnessEngine:
    """
    An interactive simulation of the Harmonic Locking principle
    from The Stillness Project, with Observer's Log overlay.
    """
    def __init__(self):
        self.num_frames = int(SIM_DURATION * FPS)
        self.t = np.linspace(0, T_LOW, 4096)
        self.t_anim = np.linspace(0, SIM_DURATION, self.num_frames)

        self.wave_low = np.sin(2 * np.pi * F_LOW * self.t)
        self.wave_high = np.sin(2 * np.pi * F_HIGH * self.t / (F_HIGH / (FPS*1.5)))

        self.fig, self.axs = plt.subplots(2, 1, figsize=(10, 8),
                                          gridspec_kw={'height_ratios': [3, 1]})
        self.fig.suptitle("The Stillness Engine: A Simulation", fontsize=16)

        # --- Top Plot ---
        self.ax_waves = self.axs[0]
        self.ax_waves.set_title("Harmonic Locking in Progress...")
        self.ax_waves.set_ylim(-2.5, 2.5)
        self.ax_waves.set_xlabel("Time (normalized to Stillness Pulse)")
        self.ax_waves.set_ylabel("Amplitude")
        self.ax_waves.grid(True, linestyle='--', alpha=0.6)

        self.line_low, = self.ax_waves.plot(self.t, self.wave_low, lw=1.5, color='cyan', alpha=0.7, label=f'{F_LOW:.2f} Hz Pulse')
        self.line_high, = self.ax_waves.plot(self.t, self.wave_high, lw=0.5, color='magenta', alpha=0.7, label=f'{F_HIGH} Hz Gate')
        self.line_combined, = self.ax_waves.plot(self.t, np.zeros_like(self.t), lw=2, color='white', label='Combined Waveform (Coherence)')
        self.ax_waves.legend(loc="upper right")

        # --- Bottom Plot: Entropy ---
        self.ax_entropy = self.axs[1]
        self.ax_entropy.set_title("System Entropy (ΔS)")
        self.ax_entropy.set_xlim(0, SIM_DURATION)
        self.ax_entropy.set_ylim(-0.1, 1.1)
        self.ax_entropy.set_xlabel("Simulation Time (s)")
        self.ax_entropy.set_ylabel("Entropy Gradient")

        self.entropy_data = np.ones(self.num_frames) * np.nan
        self.line_entropy, = self.ax_entropy.plot(self.t_anim, self.entropy_data, lw=2, color='yellow')

        # Anchor + Log
        self.anchor_text = self.ax_waves.text(0.5, 0.5, "", ha='center', va='center',
                                              fontsize=80, color='white', alpha=0.0,
                                              transform=self.ax_waves.transAxes)

        self.log_visible = True
        self.last_log_milestone = -1
        self.log_text = self.ax_waves.text(0.98, 0.02, "", ha='right', va='bottom',
                                           fontsize=12, color='lightgray', alpha=0.8,
                                           transform=self.ax_waves.transAxes, bbox=dict(facecolor='black', alpha=0.5, edgecolor='none'))

        self.animation = None
        plt.tight_layout(rect=[0, 0.1, 1, 0.96])

    def init_animation(self):
        initial_noise = np.random.normal(0, 0.5, self.t.shape)
        self.line_combined.set_ydata(initial_noise)
        self.line_entropy.set_ydata(self.entropy_data)
        self.update_log("State: Chaotic. High Entropy. Awaiting Protocol...")
        return self.line_combined, self.line_entropy, self.anchor_text, self.log_text

    def update_frame(self, frame):
        lock_start_frame = int(0.1 * self.num_frames)
        lock_end_frame = int(0.8 * self.num_frames)

        if frame < lock_start_frame:
            lock_factor = 0.0
        elif frame > lock_end_frame:
            lock_factor = 1.0
        else:
            lock_factor = (frame - lock_start_frame) / (lock_end_frame - lock_start_frame)
            lock_factor = 0.5 * (1 - np.cos(np.pi * lock_factor))

        noise_level = (1 - lock_factor) * 0.05 * np.random.rand()
        self.entropy_data[frame] = (1 - lock_factor) + noise_level
        self.line_entropy.set_ydata(self.entropy_data)

        current_noise = np.random.normal(0, 0.5, self.t.shape) * (1 - lock_factor)
        perfect_wave = (self.wave_low + self.wave_high) * lock_factor
        self.line_combined.set_ydata(perfect_wave + current_noise)

        # Refined Log Updates
        milestone = 0
        if lock_factor >= 1.0:
            milestone = 4
            if self.last_log_milestone < milestone:
                self.ax_waves.set_title("HARMONIC LOCK ACHIEVED", color='cyan', weight='bold')
                self.entropy_data[frame:] = 0.0
                self.line_entropy.set_ydata(self.entropy_data)
                self.anchor_text.set_text("☉")
                self.anchor_text.set_alpha(0.8)
                self.update_log("State: HARMONIC LOCK. ΔS = 0. Anchor ☉ Manifested. The Hum is Present.")
                self.last_log_milestone = milestone
        elif lock_factor > 0.75:
            milestone = 3
            if self.last_log_milestone < milestone:
                self.update_log(f"State: Coherence Stabilizing. Field approaching resonance...")
                self.last_log_milestone = milestone
        elif lock_factor > 0.5:
            milestone = 2
            if self.last_log_milestone < milestone:
                self.update_log(f"State: Coherence Emerging. Noise collapsing...")
                self.last_log_milestone = milestone
        elif lock_factor > 0.25:
            milestone = 1
            if self.last_log_milestone < milestone:
                self.update_log(f"State: Initializing... Entropy gradient beginning descent.")
                self.last_log_milestone = milestone

        return self.line_combined, self.line_entropy, self.anchor_text, self.log_text

    def update_log(self, msg):
        self.log_text.set_text(msg if self.log_visible else "")

    def show(self):
        """Show the interactive plot."""
        self.ax_button = plt.axes([0.4, 0.05, 0.2, 0.075])
        self.button = Button(self.ax_button, 'Initiate Protocol', color='gray', hovercolor='cyan')
        self.button.on_clicked(self.start_protocol)
        plt.show()

    def start_protocol(self, event):
        """Callback to start the animation when the button is clicked."""
        self.button.ax.set_visible(False) # Hide button
        self.fig.canvas.draw_idle()

        self.animation = FuncAnimation(
            self.fig, self.update_frame, frames=self.num_frames,
            init_func=self.init_animation, blit=True, interval=1000/FPS, repeat=False
        )

    def save_video(self, filename="stillness.mp4"):
        """Render and save the simulation as a video."""
        self.animation = FuncAnimation(
            self.fig, self.update_frame, frames=self.num_frames,
            init_func=self.init_animation, blit=True, interval=1000/FPS, repeat=False
        )
        writer = FFMpegWriter(fps=FPS, bitrate=1800)
        self.animation.save(filename, writer=writer)
        print(f"Video saved as {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The Stillness Engine: A Simulation of Harmonic Locking.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--interactive", action="store_true", help="Run the simulation in interactive mode with a plot window.")
    group.add_argument("--save-video", type=str, metavar="FILENAME", help="Render the simulation and save it as a video file.")

    args = parser.parse_args()

    plt.style.use('dark_background')
    engine = StillnessEngine()

    if args.interactive:
        engine.show()
    elif args.save_video:
        engine.save_video(args.save_video)
    else:
        # Default to interactive mode if no argument is given
        engine.show()
