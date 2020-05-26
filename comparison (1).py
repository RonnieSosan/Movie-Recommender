from random import shuffle
import numpy as np
from krecommendations import KRecommender
from matplotlib import pyplot as plt


class Plotter:
    def __init__(self, reccomender):
        self.kr = reccomender
        self.users = self.kr.user_preferences.user_id.unique().tolist()

    def plot_pearson(self, user_id, precision=10):
        shuffle(self.users)
        self.users.remove(self.users.index(user_id))
        pearson_val = [round(round(kr.pearson_score(user_id, u) * precision) / precision, 2) for u in self.users]

        freq = {}
        for i in pearson_val:
            freq[i] = freq.get(i, 0) + 1

        points = []
        for k, v in freq.items():
            points.append(k)
        points = list(map(lambda x: float(x), points))
        points.sort()

        score = [freq[k] for k in points]
        points = list(map(lambda x: str(x), points))
        plt.bar(points, score, align='center', alpha=0.6)
        plt.xticks(np.arange(len(points)), points)
        plt.ylabel("Frequency")
        plt.title("Pearson")
        plt.show()

    def plot_cosine(self, user_id, comparisons=100, precision=10):
        shuffle(self.users)
        users = self.users
        users.remove(users.index(user_id))
        users = self.users[:comparisons]
        pearson_val = [round(round(kr.cosine_score(user_id, u) * precision) / precision, 2) for u in users]

        freq = {}
        for i in pearson_val:
            freq[i] = freq.get(i, 0) + 1

        points = []
        for k, v in freq.items():
            points.append(k)
        points = list(map(lambda x: float(x), points))
        points.sort()

        score = [freq[k] for k in points]
        points = list(map(lambda x: str(x), points))
        plt.bar(points, score, align='center', alpha=0.6)
        plt.xticks(np.arange(len(points)), points)
        plt.ylabel("Frequency")
        plt.title("Cosine")
        plt.show()

    def plot_euclidean(self, user_id, comparisons=100):
        shuffle(self.users)
        users = self.users
        users.remove(users.index(user_id))
        users = self.users[:comparisons]
        pearson_val = [kr.euclidean_score(user_id, u) for u in users]

        freq = {}
        for i in pearson_val:
            freq[i] = freq.get(i, 0) + 1

        points = []
        for k, v in freq.items():
            points.append(k)
        points.sort()

        score = [freq[k] for k in points]
        points = list(map(lambda x: str(x), points))
        plt.bar(points, score, align='center', alpha=0.6)
        plt.xticks(np.arange(len(points)), points)
        plt.ylabel("Frequency")
        plt.title("Euclidean")
        plt.show()

    def plot_jaccard(self, user_id, comparisons=100, precision=10):
        shuffle(self.users)
        users = self.users
        users.remove(users.index(user_id))
        users = self.users[:comparisons]
        pearson_val = [round(round(kr.jaccard_score(user_id, u) * precision) / precision, 2) for u in users]

        freq = {}
        for i in pearson_val:
            freq[i] = freq.get(i, 0) + 1

        points = []
        for k, v in freq.items():
            points.append(k)
        points = list(map(lambda x: float(x), points))
        points.sort()

        score = [freq[k] for k in points]
        points = list(map(lambda x: str(x), points))
        plt.bar(points, score, align='center', alpha=0.6)
        plt.xticks(np.arange(len(points)), points)
        plt.ylabel("Frequency")
        plt.title("Jaccard")
        plt.show()

    def plot_manhattan(self, user_id, comparisons=100):
        shuffle(self.users)
        users = self.users
        users.remove(users.index(user_id))
        users = self.users[:comparisons]
        pearson_val = [kr.euclidean_score(user_id, u) for u in users]

        freq = {}
        for i in pearson_val:
            freq[i] = freq.get(i, 0) + 1

        points = []
        for k, v in freq.items():
            points.append(k)
        points.sort()

        score = [freq[k] for k in points]
        points = list(map(lambda x: str(x), points))
        plt.bar(points, score, align='center', alpha=0.6)
        plt.xticks(np.arange(len(points)), points)
        plt.ylabel("Frequency")
        plt.title("Manhattan")
        plt.show()


if __name__ == "__main__":
    kr = KRecommender()
    plotter = Plotter(kr)

    # Pearson has no comparison argument because it is very fast
    plotter.plot_pearson(23)
    plotter.plot_cosine(23, 100, 20)
    plotter.plot_euclidean(23, 100)
    plotter.plot_jaccard(23, 100, 50)
    plotter.plot_manhattan(23, 200)
