import os
import csv

from matplotlib import pyplot as plt


class SaveUtils:
    """Helper class for saving results and managing directories."""

    @staticmethod
    def ensure_dir(directory):
        """Ensure a directory exists."""
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def save_plot(filename, subfolder="plots"):
        """Save the current plot to the specified folder."""
        path = os.path.join("results", subfolder, filename)
        SaveUtils.ensure_dir(os.path.dirname(path))
        print(f"Saving plot to: {path}")
        plt.savefig(path, dpi=300, bbox_inches="tight")
        plt.close()

    @staticmethod
    def save_summary(filename, content):
        """Save summary content to a text file."""
        path = os.path.join("results", filename)
        with open(path, "w") as file:
            file.write(content)
        print(f"Saved summary to: {path}")

    @staticmethod
    def save_csv(filename, data, header):
        """Save data to a CSV file."""
        path = os.path.join("results", filename)
        SaveUtils.ensure_dir(os.path.dirname(path))
        with open(path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(data)
        print(f"Saved data to: {path}")
