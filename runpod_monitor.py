import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import time
from runpod import RunPodScheduler
import requests

# Make sure the RunPodScheduler class is imported or defined in the same file.

class PodMonitorApplication:
    def __init__(self, master):

        # Initialize data storage lists
        self.gpu_usage_data = []
        self.gpu_mem_usage_data = []
        self.cpu_usage_data = []
        self.cpu_mem_usage_data = []
        self.time_data = []

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

        # Add a Text widget to display metrics
        self.metrics_text = tk.Text(master, height=6, width=40)
        self.metrics_text.pack()        

        self.is_monitoring = True
        self.start_monitoring()

    def fetch_metrics(self):
        runpod_id = self.scheduler.get_pod_id()
        url = f"https://{runpod_id}-8000.proxy.runpod.net/metrics"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
            data = response.json()
            # Here you can process your data or return it
            return data
        except requests.RequestException as e:
            print(f"Error fetching metrics: {e}")
            return None        

    def update_metrics_display(self):
        metrics = self.fetch_metrics()
        if metrics:
            display_text = f"Total Execution Time: {metrics['total_exec_time']:.2f}\n" \
                           f"Total Tokens Generated: {metrics['total_token_generated']}\n" \
                           f"Number of Calls: {metrics['number_call']}\n" \
                           f"Tokens per Second: {metrics['token_by_second']:.2f}\n" \
                           f"Average Tokens per Second: {metrics['average_token_second']:.2f}"
            self.metrics_text.delete("1.0", tk.END)
            self.metrics_text.insert(tk.END, display_text)


    def start_monitoring(self):
        threading.Thread(target=self.update_graph, daemon=True).start()

    def update_graph(self):
        while self.is_monitoring:

            # Update the metrics display
            self.update_metrics_display()
                        
            # Fetch runtime data
            runtime_data = self.scheduler.analyze_pod_runtime()
            if runtime_data:
                gpu_usage = runtime_data['gpus'][0]['gpuUtilPercent']
                gpu_mem_usage = runtime_data['gpus'][0]['memoryUtilPercent']
                cpu_usage = runtime_data['container']['cpuPercent']
                cpu_mem_usage = runtime_data['container']['memoryPercent']

                # Append new data points to the lists
                self.time_data.append(time.time())  # Store the current time
                self.gpu_usage_data.append(gpu_usage)
                self.gpu_mem_usage_data.append(gpu_mem_usage)
                self.cpu_usage_data.append(cpu_usage)
                self.cpu_mem_usage_data.append(cpu_mem_usage)        

                # Trim data to a fixed length if necessary
                max_length = 100  # maximum number of data points to show
                self.gpu_usage_data = self.gpu_usage_data[-max_length:]
                self.gpu_mem_usage_data = self.gpu_mem_usage_data[-max_length:]
                self.cpu_usage_data = self.cpu_usage_data[-max_length:]
                self.cpu_mem_usage_data = self.cpu_mem_usage_data[-max_length:]
                self.time_data = self.time_data[-max_length:]                        

                # Update plots to line plots
                self.ax1.cla()
                self.ax1.plot(self.time_data, self.gpu_usage_data)
                self.ax1.set_ylim(0, 100)
                self.ax1.set_ylabel('GPU Utilization (%)')

                self.ax2.cla()
                self.ax2.plot(self.time_data, self.gpu_mem_usage_data)
                self.ax2.set_ylim(0, 100)
                self.ax2.set_ylabel('GPU Memory Usage (%)')

                self.ax3.cla()
                self.ax3.plot(self.time_data, self.cpu_usage_data)
                self.ax3.set_ylim(0, 100)
                self.ax3.set_ylabel('CPU Utilization (%)')

                self.ax4.cla()
                self.ax4.plot(self.time_data, self.cpu_mem_usage_data)
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
