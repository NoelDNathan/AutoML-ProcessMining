import matplotlib.pyplot as plt
import seaborn as sns

class PlotUtils:
    @staticmethod
    def plot_bar(data, title, xlabel, ylabel, color="blue", limit=None):
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)[:limit]
        plt.figure(figsize=(12, 6))
        sns.barplot(x=[x[0] for x in sorted_data], y=[x[1] for x in sorted_data], color=color)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

    @staticmethod
    def plot_horizontal_bar(counts, labels, title, xlabel):
        plt.figure(figsize=(12, 6))
        sns.barplot(x=counts, y=labels, color="green")
        plt.title(title)
        plt.xlabel(xlabel)
        plt.tight_layout()

    @staticmethod
    def plot_histogram(data, title, xlabel, ylabel):
        plt.figure(figsize=(10, 6))
        sns.histplot(data, bins=20, kde=True)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.tight_layout()

    @staticmethod
    def plot_boxplot(data, title):
        plt.figure(figsize=(8, 5))
        sns.boxplot(y=data, color="teal")
        plt.title(title)
        plt.tight_layout()

    @staticmethod
    def plot_scatter(x,y, title, xlabel, ylabel):
        plt.figure(figsize=(8, 5))
        sns.scatterplot(x=x,y=y)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.tight_layout()
