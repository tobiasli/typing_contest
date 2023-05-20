import typing as ty
import os
import sys
import statistics

import tregex
from matplotlib import pyplot as plt
import numpy as np


def get_contestants_and_filenames(folder: str) -> ty.Dict[str, ty.Dict[str, ty.Any]]:
    """Return a dictionary of contestants and filename."""
    return {os.path.splitext(os.path.basename(file))[0]: dict(name=os.path.splitext(os.path.basename(file))[0],
                                                              filename=os.path.abspath(os.path.join(folder, file))) for
            file in
            os.listdir(folder)}


def get_file_contents(filename: str) -> str:
    with open(filename, "r") as file:
        data = file.readlines()
        for i, line in enumerate(data):
            data[i] = data[i].strip("\n")
    return data


def score_two_files(candidate_filename: str, fasit_filename: str) -> ty.Tuple[float, ty.List[float]]:
    candidate = get_file_contents(candidate_filename)
    fasit = get_file_contents(fasit_filename)

    scores = list()
    score = None
    for i, fasit_line in enumerate(fasit):
        if len(candidate) - 1 >= i:
            candidate_line = candidate[i]
            scores.append(tregex.similarity(candidate_line, fasit_line))
        else:
            scores.append(0)

    score = statistics.mean(scores)
    return score, scores


def rank_contestants(contestants: ty.Dict[str, ty.Dict]) -> ty.List[ty.Dict]:
    iterable = [v for v in contestants.values()]

    return sorted(iterable, key=lambda c: c['score'], reverse=True)


def histogram(contestants) -> None:
    # Creating dataset
    marks = np.array([c['score'] for c in contestants])
    labels = [f"{c['name']}" for c in contestants]

    # Create bar plot
    fig, ax = plt.subplots(1, 1)
    bars = ax.bar(labels, marks)

    # Add labels above the two bar graphs
    for rect, label in zip(bars, labels):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2.0, height, f'{label}', ha='center', va='bottom')

    ax.get_xaxis().set_visible(False)
    ax.set_ylim([0, 1])

    plt.show()


if __name__ == "__main__":
    game_dir = os.environ['typing_contest_game_dir']
    fasit_filename = os.environ['typing_contest_fasit_filename']

    contestants = get_contestants_and_filenames(game_dir)

    for person in contestants.values():
        person['score'], person['scores'] = score_two_files(candidate_filename=person['filename'],
                                                            fasit_filename=fasit_filename)

    ranked = rank_contestants(contestants)

    histogram(ranked)
