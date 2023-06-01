import os
import tempfile
import pytest

import typing_contest.code.typing_contest as tc


class TestBin():

    def __init__(self) -> None:
        self.dir: tempfile.TemporaryDirectory = None

    def build(self) -> None:
        self.dir = tempfile.TemporaryDirectory()
        # Populate bin:
        for k, v in dict(Charles="Nothing", Benny="""This is contents\nNo it isn't!""").items():
            with open(os.path.join(self.dir.name, k + '.txt'), 'w') as file:
                file.write(v)

    def cleanup(self) -> None:
        if self.dir:
            self.dir.cleanup()

        self.dir = None


class TestFasit():

    def __init__(self) -> None:
        self.dir: tempfile.TemporaryDirectory = None
        self.filename: str = None

    def build(self) -> None:
        self.dir = tempfile.TemporaryDirectory()
        self.filename = os.path.join(self.dir.name, 'fasit.txt')
        # Populate fasit:
        fasit = """This is contents\nYes it is!\nNo it isn't!"""
        with open(self.filename, 'w') as file:
            file.write(fasit)

    def cleanup(self) -> None:
        if self.dir:
            self.dir.cleanup()

        self.dir = None
        self.filename = None


@pytest.fixture()
def game_folder() -> str:
    test_bin = TestBin()
    test_bin.build()
    yield test_bin.dir.name
    test_bin.cleanup()


@pytest.fixture()
def fasit_filename() -> str:
    test_fasit = TestFasit()
    test_fasit.build()
    yield test_fasit.filename
    test_fasit.cleanup()


def test_get_files(game_folder):
    expected = dict(
        Benny=dict(name='Benny', filename=os.path.join(game_folder, "Benny.txt")),
        Charles=dict(name='Charles', filename=os.path.join(game_folder, "Charles.txt")),
    )
    assert tc.get_contestants_and_filenames(game_folder) == expected


def test_get_fasit(fasit_filename):
    expected = ["This is contents", "Yes it is!", "No it isn't!"]
    assert tc.get_file_contents(fasit_filename) == expected


def test_scores(fasit_filename, game_folder) -> None:
    candidate_filename = tc.get_contestants_and_filenames(game_folder)['Benny']
    score, scores = tc.score_two_files(candidate_filename=candidate_filename['filename'], fasit_filename=fasit_filename)
    assert score == pytest.approx(0.5454545454545454)
    assert scores == [pytest.approx(v) for v in [1, 0.6363636363636364, 0]]


def test_rank_contestants() -> None:
    expected = [dict(name='Benny', score=4), dict(name='James', score=2), dict(name='Charles', score=0)]
    ranked = tc.rank_contestants(dict(Charles=dict(name='Charles', score=0), James=dict(name='James', score=2), Benny=dict(name='Benny', score=4)))
    assert ranked == expected

