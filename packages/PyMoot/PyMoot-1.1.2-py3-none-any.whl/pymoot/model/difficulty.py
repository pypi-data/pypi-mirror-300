from typing import Final, List


class DifficultyGrade:
    """List of available difficulty grades."""

    EASY: Final[str] = "easy"
    MODERATE: Final[str] = "moderate"
    DIFFICULT: Final[str] = "difficult"

    @classmethod
    def list_all(cls) -> List[str]:
        """
        List all possible difficulty grades.

        :return: list of supported difficulty grades
        """
        return [
            getattr(cls, attr) for attr in dir(cls) if not attr.startswith('__') and not callable(getattr(cls, attr))
        ]


class Difficulty:

    def __init__(self, grade: str, explanation_technical: str, explanation_fitness: str):
        """
        Difficulty: describes estimated difficulty of the tour.

        :param grade: difficulty grade
        :param explanation_technical: technical explanation of the difficulty
        :param explanation_fitness: physical explanation of the difficulty
        """
        if grade not in DifficultyGrade.list_all():
            raise ValueError(f"Unexpected difficulty grade: {grade}")
        self.grade: str = grade
        self.explanation_technical: str = explanation_technical
        self.explanation_fitness: str = explanation_fitness
