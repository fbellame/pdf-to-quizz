import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import time
from runpod import RunPodScheduler
import requests

# Ensure the RunPodScheduler class is imported or defined in the same file.

class PodMonitorApplication:
    def __init__(self, master):
        self.master = master
        self.scheduler = RunPodScheduler()
        title = f"Pod GPU/CPU Usage Monitor - {self.scheduler.get_pod_id()}" if self.scheduler.get_pod_id() else "Pod GPU/CPU Usage Monitor"
        self.master.title(title)

        # Adjusted figure size for more subplots
        self.fig = Figure(figsize=(12, 8), dpi=100)
        
        # Initialize axes for GPU and CPU usage/memory
        self.ax1 = self.fig.add_subplot(331)  # GPU Usage
        self.ax2 = self.fig.add_subplot(332)  # GPU Memory Usage
        self.ax3 = self.fig.add_subplot(333)  # CPU Usage
        self.ax4 = self.fig.add_subplot(334)  # CPU Memory Usage

        # Initialize axes for new metrics
        self.ax5 = self.fig.add_subplot(335)  # Total Execution Time
        self.ax6 = self.fig.add_subplot(336)  # Total Tokens Generated
        self.ax7 = self.fig.add_subplot(337)  # Number of Calls
        self.ax8 = self.fig.add_subplot(338)  # Tokens per Second
        self.ax9 = self.fig.add_subplot(339)  # Average Tokens per Second

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Add a Text widget to display metrics
        self.metrics_text = tk.Text(master, height=6, width=40)
        self.metrics_text.pack()

        # Initialize data storage lists for GPU, CPU, and other metrics
        self.gpu_usage_data = []
        self.gpu_mem_usage_data = []
        self.cpu_usage_data = []
        self.cpu_mem_usage_data = []
        self.total_exec_time_data = []
        self.total_tokens_generated_data = []
        self.number_of_calls_data = []
        self.tokens_per_second_data = []
        self.avg_tokens_per_second_data = []

        self.is_monitoring = True
        self.start_monitoring()

    def fetch_metrics(self):
        runpod_id = self.scheduler.get_pod_id()
        url = f"https://{runpod_id}-8000.proxy.runpod.net/metrics"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
            data = response.json()
            return data
        except requests.RequestException as e:
            print(f"Error fetching metrics: {e}")
            return None
        
    def update_metrics_display(self):
        # Check if the data lists have elements and get the latest value, otherwise set to 'N/A'
        latest_exec_time = f"{self.total_exec_time_data[-1][1]:.2f}" if self.total_exec_time_data else 'N/A'
        latest_tokens_generated = self.total_tokens_generated_data[-1][1] if self.total_tokens_generated_data else 'N/A'
        latest_number_of_calls = self.number_of_calls_data[-1][1] if self.number_of_calls_data else 'N/A'
        latest_tokens_per_second = f"{self.tokens_per_second_data[-1][1]:.2f}" if self.tokens_per_second_data else 'N/A'
        latest_avg_tokens_per_second = f"{self.avg_tokens_per_second_data[-1][1]:.2f}" if self.avg_tokens_per_second_data else 'N/A'

        # Format the display text
        display_text = f"Latest Total Execution Time: {latest_exec_time} s\n" \
                    f"Latest Total Tokens Generated: {latest_tokens_generated}\n" \
                    f"Latest Number of Calls: {latest_number_of_calls}\n" \
                    f"Latest Tokens per Second: {latest_tokens_per_second}\n" \
                    f"Latest Average Tokens per Second: {latest_avg_tokens_per_second}"

        # Update the metrics_text widget
        self.metrics_text.delete("1.0", tk.END)
        self.metrics_text.insert(tk.END, display_text)

    def start_monitoring(self):
        threading.Thread(target=self.update_graph, daemon=True).start()

    def update_graph(self):
        while self.is_monitoring:
            # Fetch runtime data for GPU and CPU
            runtime_data = self.scheduler.analyze_pod_runtime()
            print("Runtime Data:", runtime_data)  # Debugging line
            if runtime_data:
                gpu_usage = runtime_data['gpus'][0]['gpuUtilPercent']
                gpu_mem_usage = runtime_data['gpus'][0]['memoryUtilPercent']
                cpu_usage = runtime_data['container']['cpuPercent']
                cpu_mem_usage = runtime_data['container']['memoryPercent']

                # Update the data lists for GPU and CPU
                current_time = time.time()
                self.gpu_usage_data.append((current_time, gpu_usage))
                self.gpu_mem_usage_data.append((current_time, gpu_mem_usage))
                self.cpu_usage_data.append((current_time, cpu_usage))
                self.cpu_mem_usage_data.append((current_time, cpu_mem_usage))

            # Fetch and update the other metrics
            metrics = self.fetch_metrics()
            if metrics:
                self.total_exec_time_data.append((current_time, metrics['total_exec_time']))
                self.total_tokens_generated_data.append((current_time, metrics['total_token_generated']))
                self.number_of_calls_data.append((current_time, metrics['number_call']))
                self.tokens_per_second_data.append((current_time, metrics['token_by_second']))
                self.avg_tokens_per_second_data.append((current_time, metrics['average_token_second']))

            # Trim data to a fixed length if necessary
            max_length = 100  # Adjust as needed
            self.trim_data_lists(max_length)

            # Update the new graphs
            self.update_new_graphs()

            self.update_metrics_display()

            self.canvas.draw()

            time.sleep(1)  # Wait for 1 second before the next update

    def update_new_graphs(self):

        # Unpack and plot GPU and CPU data
        gpu_times, gpu_values = zip(*self.gpu_usage_data) if self.gpu_usage_data else ([], [])
        gpu_mem_times, gpu_mem_values = zip(*self.gpu_mem_usage_data) if self.gpu_mem_usage_data else ([], [])
        cpu_times, cpu_values = zip(*self.cpu_usage_data) if self.cpu_usage_data else ([], [])
        cpu_mem_times, cpu_mem_values = zip(*self.cpu_mem_usage_data) if self.cpu_mem_usage_data else ([], [])

        self.ax1.cla()
        self.ax1.plot(gpu_times, gpu_values, label='GPU Usage')
        self.ax1.set_ylabel('GPU Usage (%)')
        self.ax1.legend()

        self.ax2.cla()
        self.ax2.plot(gpu_mem_times, gpu_mem_values, label='GPU Memory Usage')
        self.ax2.set_ylabel('GPU Memory Usage (%)')
        self.ax2.legend()

        self.ax3.cla()
        self.ax3.plot(cpu_times, cpu_values, label='CPU Usage')
        self.ax3.set_ylabel('CPU Usage (%)')
        self.ax3.legend()

        self.ax4.cla()
        self.ax4.plot(cpu_mem_times, cpu_mem_values, label='CPU Memory Usage')
        self.ax4.set_ylabel('CPU Memory Usage (%)')
        self.ax4.legend()


        # Unpack the time and value for each metric
        exec_times, exec_values = zip(*self.total_exec_time_data) if self.total_exec_time_data else ([], [])
        token_counts, token_values = zip(*self.total_tokens_generated_data) if self.total_tokens_generated_data else ([], [])
        call_times, call_values = zip(*self.number_of_calls_data) if self.number_of_calls_data else ([], [])
        token_sec_times, token_sec_values = zip(*self.tokens_per_second_data) if self.tokens_per_second_data else ([], [])
        avg_token_sec_times, avg_token_sec_values = zip(*self.avg_tokens_per_second_data) if self.avg_tokens_per_second_data else ([], [])

        # Update graphs for each metric
        self.ax5.cla()
        self.ax5.plot(exec_times, exec_values, label='Total Execution Time')
        self.ax5.set_ylabel('Execution Time (s)')
        self.ax5.legend()

        self.ax6.cla()
        self.ax6.plot(token_counts, token_values, label='Total Tokens Generated')
        self.ax6.set_ylabel('Tokens Generated')
        self.ax6.legend()

        self.ax7.cla()
        self.ax7.plot(call_times, call_values, label='Number of Calls')
        self.ax7.set_ylabel('Calls')
        self.ax7.legend()

        self.ax8.cla()
        self.ax8.plot(token_sec_times, token_sec_values, label='Tokens per Second')
        self.ax8.set_ylabel('Tokens/Sec')
        self.ax8.legend()

        self.ax9.cla()
        self.ax9.plot(avg_token_sec_times, avg_token_sec_values, label='Average Tokens per Second')
        self.ax9.set_ylabel('Avg Tokens/Sec')
        self.ax9.legend()

    def stop_monitoring(self):
        self.is_monitoring = False

    def trim_data_lists(self, max_length):
        # Trim lists for GPU and CPU data
        self.gpu_usage_data = self.gpu_usage_data[-max_length:]
        self.gpu_mem_usage_data = self.gpu_mem_usage_data[-max_length:]
        self.cpu_usage_data = self.cpu_usage_data[-max_length:]
        self.cpu_mem_usage_data = self.cpu_mem_usage_data[-max_length:]

        # Trim lists for other metrics
        self.total_exec_time_data = self.total_exec_time_data[-max_length:]
        self.total_tokens_generated_data = self.total_tokens_generated_data[-max_length:]
        self.number_of_calls_data = self.number_of_calls_data[-max_length:]
        self.tokens_per_second_data = self.tokens_per_second_data[-max_length:]
        self.avg_tokens_per_second_data = self.avg_tokens_per_second_data[-max_length:]

# Main window
root = tk.Tk()
app = PodMonitorApplication(root)

# Start the Tkinter loop
root.mainloop()
