import numpy as np
import time
import psutil
import threading
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
# from tensorflow.keras.datasets import mnist
# from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt
import seaborn as sns

class EnergyConsumptionDL:
    def __init__(self, model, pcpu_idle, pcpu_full):
        """
        Initialize the class for tracking energy efficiency during training.
        
        :param model: The Keras model to train.
        :param pcpu_idle: Idle power consumption of the CPU (in watts).
        :param pcpu_full: Full load power consumption of the CPU (in watts).
        """
        self.model = model
        self.pcpu_idle = pcpu_idle
        self.pcpu_full = pcpu_full
        self.cpu_logs = []
        self.memory_logs = []
        self.start_time = None
        self.end_time = None
        self.monitor_thread = None
        self.monitoring = False

    def _monitor_system_usage(self):
        """
        Monitors CPU and memory usage in the background.
        """
        while self.monitoring:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
            self.cpu_logs.append(cpu_percent / 100)  # Store CPU utilization (as a fraction of 1)
            self.memory_logs.append(memory_percent)

    def fit(self, x_train, y_train, epochs=5, batch_size=64, validation_split=0.2):
        """
        Train the model while tracking CPU and memory utilization.
        
        :param x_train: Training data.
        :param y_train: Training labels.
        :param epochs: Number of epochs to train the model.
        :param batch_size: Size of batches to use for training.
        :param validation_split: Fraction of training data to use for validation.
        """
        # Start monitoring system usage in a separate thread
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_system_usage)
        self.monitor_thread.start()

        self.start_time = time.time()
        
        # Train the model
        self.model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=validation_split)

        self.end_time = time.time()
        
        # Stop monitoring and wait for the monitoring thread to finish
        self.monitoring = False
        self.monitor_thread.join()

    def evaluate(self, x_test, y_test):
        """
        Evaluate the model on the test set.
        
        :param x_test: Test data.
        :param y_test: Test labels.
        :return: Test loss and accuracy.
        """
        return self.model.evaluate(x_test, y_test)

    def generate_report(self, x_train, y_train, x_test, y_test, epochs=5, batch_size=64, validation_split=0.2):
        """
        Generate a report on CPU and memory utilization, power, energy, and model performance.
        """
        # Train the model
        self.fit(x_train, y_train, epochs, batch_size, validation_split)

        # Calculate average CPU and memory utilization
        avg_cpu_utilization = np.mean(self.cpu_logs)
        avg_memory_utilization = np.mean(self.memory_logs)

        # Calculate total training time
        training_time = self.end_time - self.start_time

        # Power consumption calculation
        power_consumption = ((1 - avg_cpu_utilization) * self.pcpu_idle) + (avg_cpu_utilization * self.pcpu_full)

        # Energy consumption calculation
        energy_consumption = training_time * power_consumption

        # Evaluate the model
        test_loss, test_acc = self.evaluate(x_test, y_test)

        # Print the final report
        print(f"--- Training Report ---")
        print(f"Training Time: {training_time:.2f} seconds")
        print(f"Average CPU Utilization: {avg_cpu_utilization * 100:.2f}%")
        print(f"Average Memory Utilization: {avg_memory_utilization:.2f}%")
        print(f"Power Consumption: {power_consumption:.2f} W")
        print(f"Energy Consumption: {energy_consumption:.2f} J (Joules)")
        print(f"Test Accuracy: {test_acc:.4f}")
    
    def plot_cpu_usage(self):
        """
        Plots the CPU utilization logs as a line graph.
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

