"""Store and load progress data."""

from argparse import ArgumentParser
from pathlib import Path

from ..metadata import NAME
from ..model.language import Language
from ..model.quiz.progress import Progress
from ..model.quiz.quiz import Quizzes
from .folder import home
from .json_file import dump_json, load_json


def get_progress_filepath(target_language: Language) -> Path:
    """Return the filename of the progress file for the specified target language."""
    return home() / f".{NAME.lower()}-progress-{target_language}.json"


def load_progress(target_language: Language, quizzes: Quizzes, argument_parser: ArgumentParser) -> Progress:
    """Load the progress from the user's home folder."""
    progress_filepath = get_progress_filepath(target_language)
    try:
        progress_dict = load_json(progress_filepath, default={})
    except Exception as reason:  # noqa: BLE001
        return argument_parser.error(
            f"""{NAME} cannot parse the progress information in {progress_filepath}: {reason}.
To fix this, remove or rename {progress_filepath} and start {NAME} again. Unfortunately, this will reset your progress.
Please consider opening a bug report at https://github.com/fniessink/{NAME.lower()}. Be sure to attach the invalid
progress file to the issue.
""",
        )
    return Progress(progress_dict, target_language, quizzes)


def save_progress(progress: Progress) -> None:
    """Save the progress to the user's home folder."""
    progress_filepath = get_progress_filepath(progress.target_language)
    dump_json(progress_filepath, progress.as_dict())
