import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import time
from runpod import RunPodScheduler

# Make sure the RunPodScheduler class is imported or defined in the same file.

class PodMonitorApplication:
    def __init__(self, master):
        self.master = master
        self.scheduler = RunPodScheduler()
        title = f"Pod GPU/CPU Usage Monitor - {self.scheduler.get_pod_id()}" if self.scheduler.get_pod_id() else "Pod GPU/CPU Usage Monitor"
        self.master.title(title)

        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax1 = self.fig.add_subplot(221)  # GPU Usage
        self.ax2 = self.fig.add_subplot(222)  # GPU Memory Usage
        self.ax3 = self.fig.add_subplot(223)  # CPU Usage
        self.ax4 = self.fig.add_subplot(224)  # CPU Memory Usage

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.is_monitoring = True
        self.start_monitoring()

    def start_monitoring(self):
        threading.Thread(target=self.update_graph, daemon=True).start()

    def update_graph(self):
        while self.is_monitoring:
            # Fetch runtime data
            runtime_data = self.scheduler.analyze_pod_runtime()
            if runtime_data:
                gpu_usage = runtime_data['gpus'][0]['gpuUtilPercent']
                gpu_mem_usage = runtime_data['gpus'][0]['memoryUtilPercent']
                cpu_usage = runtime_data['container']['cpuPercent']
                cpu_mem_usage = runtime_data['container']['memoryPercent']

                # Update GPU Usage graph
                self.ax1.cla()
                self.ax1.bar('GPU', gpu_usage)
                self.ax1.set_ylim(0, 100)
                self.ax1.set_ylabel('GPU Utilization (%)')

                # Update GPU Memory Usage graph
                self.ax2.cla()
                self.ax2.bar('GPU Memory', gpu_mem_usage)
                self.ax2.set_ylim(0, 100)
                self.ax2.set_ylabel('GPU Memory Usage (%)')

                # Update CPU Usage graph
                self.ax3.cla()
                self.ax3.bar('CPU', cpu_usage)
                self.ax3.set_ylim(0, 100)
                self.ax3.set_ylabel('CPU Utilization (%)')

                # Update CPU Memory Usage graph
                self.ax4.cla()
                self.ax4.bar('CPU Memory', cpu_mem_usage)
                self.ax4.set_ylim(0, 100)
                self.ax4.set_ylabel('CPU Memory Usage (%)')

                # Draw the updated figures
                self.canvas.draw()
                
            time.sleep(1)  # Wait for 1 second before the next update

    def stop_monitoring(self):
        self.is_monitoring = False

# Main window
root = tk.Tk()
app = PodMonitorApplication(root)

# Start the Tkinter loop
root.mainloop()
