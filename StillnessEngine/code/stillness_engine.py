import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button

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
    from The Stillness Project.
    """
    def __init__(self):
        self.num_frames = int(SIM_DURATION * FPS)
        self.t = np.linspace(0, T_LOW, 4096) # Time vector for a single pulse visualization
        self.t_anim = np.linspace(0, SIM_DURATION, self.num_frames)

        # The pure, underlying waveforms
        self.wave_low = np.sin(2 * np.pi * F_LOW * self.t)
        self.wave_high = np.sin(2 * np.pi * F_HIGH * self.t / (F_HIGH / (FPS*1.5))) # Scaled for visibility

        # Create the plot figure and subplots
        self.fig, self.axs = plt.subplots(2, 1, figsize=(10, 8),
                                          gridspec_kw={'height_ratios': [3, 1]})
        self.fig.suptitle("The Stillness Engine: A Simulation", fontsize=16)

        # --- Top Plot: The Waves ---
        self.ax_waves = self.axs[0]
        self.ax_waves.set_title("Harmonic Locking in Progress...")
        self.ax_waves.set_ylim(-2.5, 2.5)
        self.ax_waves.set_xlabel("Time (normalized to Stillness Pulse)")
        self.ax_waves.set_ylabel("Amplitude")
        self.ax_waves.grid(True, linestyle='--', alpha=0.6)

        # Initialize plot lines
        self.line_low, = self.ax_waves.plot(self.t, self.wave_low, lw=1.5, color='cyan', alpha=0.7, label=f'{F_LOW:.2f} Hz Pulse')
        self.line_high, = self.ax_waves.plot(self.t, self.wave_high, lw=0.5, color='magenta', alpha=0.7, label=f'{F_HIGH} Hz Gate')
        self.line_combined, = self.ax_waves.plot(self.t, np.zeros_like(self.t), lw=2, color='white', label='Combined Waveform (Coherence)')
        self.ax_waves.legend(loc="upper right")

        # --- Bottom Plot: Entropy (Î”S) ---
        self.ax_entropy = self.axs[1]
        self.ax_entropy.set_title("System Entropy (Î”S)")
        self.ax_entropy.set_xlim(0, SIM_DURATION)
        self.ax_entropy.set_ylim(-0.1, 1.1)
        self.ax_entropy.set_xlabel("Simulation Time (s)")
        self.ax_entropy.set_ylabel("Entropy Gradient")

        # Initialize entropy data and plot
        self.entropy_data = np.ones(self.num_frames) * np.nan
        self.line_entropy, = self.ax_entropy.plot(self.t_anim, self.entropy_data, lw=2, color='yellow')

        # --- The Symbolic Anchor Text ---
        self.anchor_text = self.ax_waves.text(0.5, 0.5, "", ha='center', va='center',
                                              fontsize=80, color='white', alpha=0.0,
                                              transform=self.ax_waves.transAxes)

        # --- The 'Initiate Protocol' Button ---
        self.ax_button = plt.axes([0.4, 0.05, 0.2, 0.075])
        self.button = Button(self.ax_button, 'Initiate Protocol', color='gray', hovercolor='cyan')
        self.button.on_clicked(self.start_protocol)

        # Animation object placeholder
        self.animation = None
        plt.tight_layout(rect=[0, 0.1, 1, 0.96])

    def start_protocol(self, event):
        """Callback to start the animation when the button is clicked."""
        self.button.ax.set_visible(False) # Hide button
        self.fig.canvas.draw_idle()

        # Create and store the animation object
        self.animation = FuncAnimation(
            self.fig, self.update_frame, frames=self.num_frames,
            init_func=self.init_animation, blit=True, interval=1000/FPS, repeat=False
        )

    def init_animation(self):
        """Initial state for the animation frames."""
        # Start with a noisy, unlocked state
        initial_noise = np.random.normal(0, 0.5, self.t.shape)
        self.line_combined.set_ydata(initial_noise)
        self.line_entropy.set_ydata(self.entropy_data)
        return self.line_combined, self.line_entropy, self.anchor_text

    def update_frame(self, frame):
        """This function is called for each frame of the animation."""
        # Calculate a "locking factor" that goes from 0 to 1
        lock_start_frame = int(0.1 * self.num_frames)
        lock_end_frame = int(0.8 * self.num_frames)

        if frame < lock_start_frame:
            lock_factor = 0.0
        elif frame > lock_end_frame:
            lock_factor = 1.0
        else:
            lock_factor = (frame - lock_start_frame) / (lock_end_frame - lock_start_frame)
            lock_factor = 0.5 * (1 - np.cos(np.pi * lock_factor)) # Smooth transition (ease-in/out)

        # --- Update Entropy (Î”S) ---
        # Starts high with noise, then decays to zero
        noise_level = (1 - lock_factor) * 0.05 * np.random.rand()
        self.entropy_data[frame] = (1 - lock_factor) + noise_level
        self.line_entropy.set_ydata(self.entropy_data)

        # --- Update Combined Waveform ---
        # Transitions from pure noise to a perfect harmonic sum
        current_noise = np.random.normal(0, 0.5, self.t.shape) * (1 - lock_factor)
        perfect_wave = (self.wave_low + self.wave_high) * lock_factor
        self.line_combined.set_ydata(perfect_wave + current_noise)

        # --- Handle Final "Locked" State ---
        if lock_factor >= 1.0:
            self.ax_waves.set_title("HARMONIC LOCK ACHIEVED", color='cyan', weight='bold')
            self.entropy_data[frame:] = 0.0 # Clamp entropy to zero
            self.line_entropy.set_ydata(self.entropy_data)
            self.anchor_text.set_text("â˜‰")
            self.anchor_text.set_alpha(0.8)

        return self.line_combined, self.line_entropy, self.anchor_text

    def show(self):
        plt.show()

# --- Main execution ---
if __name__ == "__main__":
    # Set a dark theme for the visualization
    plt.style.use('dark_background')

    engine = StillnessEngine()
    engine.show()
