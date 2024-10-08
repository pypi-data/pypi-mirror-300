import time
import psutil
import numpy as np
import threading
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns


class EnergyConsumptionML:
    def __init__(self, model, pcpu_idle, pcpu_full):
        """
        Initialize the model trainer with the given machine-specific power values.
        
        :param model: The machine learning model to train.
        :param pcpu_idle: The idle power consumption of the CPU (in watts).
        :param pcpu_full: The full load power consumption of the CPU (in watts).
        """
        self.model = model
        self.pcpu_idle = pcpu_idle  # CPU power when idle
        self.pcpu_full = pcpu_full  # CPU power at full utilization
        self.cpu_logs = []
        self.memory_logs = []
        self.start_time = None
        self.end_time = None
        self.monitor_thread = None
        self.monitoring = False

    def _monitor_system_usage(self):
        """
        Monitors the system CPU and memory utilization in the background.
        """
        while self.monitoring:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
            self.cpu_logs.append(cpu_percent / 100)  # Store CPU utilization as α (0 to 1)
            self.memory_logs.append(memory_percent)

    def fit(self, X_train, y_train):
        """
        Train the model while tracking CPU and memory utilization in a separate thread.
        """

        # Start the system usage monitoring in a separate thread
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_system_usage)
        self.monitor_thread.start()

        self.start_time = time.time()
        # Train the model
        self.model.fit(X_train, y_train)
        self.end_time = time.time()
        # Stop monitoring and wait for the monitoring thread to finish
        self.monitoring = False
        self.monitor_thread.join()


    def predict(self, X_test):
        """
        Make predictions using the trained model.
        """
        return self.model.predict(X_test)

    def generate_report(self, X_train, y_train, X_test, y_test):
        """
        Generate a report including CPU and memory utilization, power, energy, and evaluation metrics.
        """
        # Train the model
        self.fit(X_train, y_train)

        # Calculate average CPU and memory utilization
        avg_cpu_utilization = np.mean(self.cpu_logs)
        avg_memory_utilization = np.mean(self.memory_logs)
        
        # Calculate total training time
        training_time = self.end_time - self.start_time

        # Power consumption calculation
        power_consumption = ((1 - avg_cpu_utilization) * self.pcpu_idle) + (avg_cpu_utilization * self.pcpu_full)

        # Energy consumption calculation
        energy_consumption = training_time * power_consumption

        # Get predictions and classification report
        predictions = self.predict(X_test)
        report = classification_report(y_test, predictions)
        confusion = confusion_matrix(y_test, predictions)

        # Print the final report
        print(f"--- Training Report ---")
        print(f"Training Time: {training_time:.2f} seconds")
        print(f"Average CPU Utilization: {avg_cpu_utilization * 100:.2f}%")
        print(f"Average Memory Utilization: {avg_memory_utilization:.2f}%")
        print(f"Power Consumption: {power_consumption:.2f} W")
        print(f"Energy Consumption: {energy_consumption:.2f} J (Joules)")
        print(f"\nClassification Report:\n{report}")
        print(f"\nConfusion Matrix:\n{confusion}")

    def plot_cpu_usage(self):
        """
        Plots the CPU utilization logs as a modern line graph.
        """
        sns.set(style="whitegrid", palette="muted", rc={'figure.figsize': (10, 6)})

        # Create the line plot
        plt.plot(self.cpu_logs, color='b', linewidth=2)

        # Add labels and title
        plt.title("CPU Utilization During Model Training", fontsize=18, fontweight='bold')
        plt.xlabel("Time (seconds)", fontsize=14)
        plt.ylabel("CPU Utilization (0 to 1)", fontsize=14)

        # Add grid for better readability
        plt.grid(True)

        # Display the plot
        plt.show()