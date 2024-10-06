"""Classes to represent a scale of notes."""

import enum
import functools
import itertools
import typing
from types import MappingProxyType

from solfege import note

_KEYS_PROGRESSION = [
    "C",
    "D",
    "E",
    "F",
    "G",
    "A",
    "B",
]


_KEY_INDEX_MAP = MappingProxyType({k: i for i, k in enumerate(_KEYS_PROGRESSION)})


def _half_step(i: typing.Iterable[str]):
    return next(i)


def _whole_step(i: typing.Iterable[str]):
    _half_step(i)
    return _half_step(i)


class ScaleType(enum.Enum):
    """Supported scale types."""

    MAJOR = 0
    """Enum for selecting a Major scale."""
    MINOR = enum.auto
    """Enum for selecting a Natural Minor scale."""


_SCALE_KEY_SIGNATURES = {
    "C#": ["c#", "d#", "e#", "f#", "g#", "a#", "b#"],
    "F#": ["f#", "g#", "a#", "c#", "d#", "e#"],
    "B": ["c#", "d#", "f#", "g#", "a#"],
    "E": ["f#", "g#", "c#", "d#"],
    "A": ["c#", "f#", "g#"],
    "D": ["f#", "c#"],
    "G": ["f#"],
    "C": [],
    "F": ["bb"],
    "Bb": ["bb", "eb"],
    "Eb": ["eb", "ab", "bb"],
    "Ab": ["ab", "bb", "db", "eb"],
    "Db": ["db", "eb", "gb", "ab", "bb"],
    "Gb": ["gb", "ab", "bb", "cb", "db", "eb"],
    "Cb": ["cb", "db", "eb", "fb", "gb", "ab", "bb"],
    # minors
    "A#m": ["a#", "b#", "c#", "d#", "e#", "f#", "g#"],
    "D#m": ["d#", "e#", "f#", "g#", "a#", "c#"],
    "G#m": ["g#", "a#", "c#", "d#", "f#"],
    "C#m": ["c#", "d#", "f#", "g#"],
    "F#m": ["f#", "g#", "c#"],
    "Bm": ["c#", "f#"],
    "Em": ["f#"],
    "Am": [],
    "Dm": ["bb"],
    "Gm": ["bb", "eb"],
    "Cm": ["eb", "ab", "bb"],
    "Fm": ["ab", "bb", "db", "eb"],
    "Bbm": ["bb", "db", "eb", "gb", "ab"],
    "ebm": ["eb", "gb", "ab", "bb", "cb", "db"],
    "abm": ["ab", "bb", "cb", "db", "eb", "fb", "gb"],
}

_SCALE_KEY_MAPPING = {
    key: {note_name.upper(): modifier for note_name, modifier in part}
    for key, part in _SCALE_KEY_SIGNATURES.items()
}


@functools.lru_cache(maxsize=100)
def _scale_notes(starting_note: note.Note, major_minor: str):
    for key in itertools.cycle(_KEYS_PROGRESSION):
        modifier = _SCALE_KEY_MAPPING[starting_note.name + major_minor].get(key.upper()) or ""
        yield key + modifier


def _rotate(o: typing.Container, n: int):
    repeated = itertools.cycle(o)
    return list(itertools.islice(repeated, n, len(o) + n))


_DIATONIC_SOLFEGE_NAMES = ("Do", "Re", "Mi", "Fa", "Sol", "La", "Ti", "Do")

_MINOR_DIATONIC_SOLFEGE_NAMES = _rotate(_DIATONIC_SOLFEGE_NAMES[:-1], 5)
_MINOR_DIATONIC_SOLFEGE_NAMES.append(_MINOR_DIATONIC_SOLFEGE_NAMES[0])

_CHROMATIC_SOLFEGE = (
    {"b": "Ti", "#": "Di"},  # Do
    {"b": "Ra", "#": "Ri"},  # Re
    {"b": "Me", "#": "Fa"},  # Mi
    {"b": "Mi", "#": "Fi"},  # Fa
    {"b": "Se", "#": "Si"},  # Sol
    {"b": "Le", "#": "Li"},  # La
    {"b": "Te", "#": "Do"},  # Ti
)

_MINOR_CHROMATIC_SOLFEGE = _rotate(_CHROMATIC_SOLFEGE, 5)


class Scale:
    """A representation of a musical scale."""

    def __init__(self, starting_note: note.Note, type: ScaleType = ScaleType.MAJOR):
        """Initialize a scale.

        Args:
            starting_note (note.Note): the tonic note the scale starts on.
            type (ScaleType): Which type of scale to load in.
        """
        self._starting_note = starting_note
        self._type = type

        self._starting_note_index = _KEY_INDEX_MAP[f"{self._starting_note.letter}"]

        self._diatonic_notes = list(
            note.Note(x, octave=starting_note.octave if i < 8 else starting_note.octave + 1)
            for i, x in enumerate(
                itertools.islice(
                    _scale_notes(
                        self._starting_note,
                        major_minor=("m" if self._type == ScaleType.MINOR else ""),
                    ),
                    self._starting_note_index,
                    self._starting_note_index + len(_KEYS_PROGRESSION) + 1,
                )
            )
        )
        self._diatonic_position_map = {
            f"{note_.name}": (i if type == ScaleType.MAJOR else (i) % len(self._diatonic_notes))
            for i, note_ in enumerate(self._diatonic_notes[:-1])
        }

    def solfege(self, note_: note.Note) -> str:
        """Get the movable-do solfege name for a note in this scale.

        For minor keys, moving-do la-based minor is used.

        Args:
            note_ (note.Note): The note in question.

        Returns:
            str: The solfege name for that note.
        """
        index = self._diatonic_position_map.get(note_.name)
        if index is not None:
            return (
                _DIATONIC_SOLFEGE_NAMES[index]
                if self._type == ScaleType.MAJOR
                else _MINOR_DIATONIC_SOLFEGE_NAMES[index]
            )

        base_index, base_note = next(
            (
                (i, note_base)
                for i, note_base in enumerate(self._diatonic_notes)
                if note_base.letter == note_.letter
            ),
            (None, None),
        )
        if base_index is None:
            raise ValueError(
                f"Either {note_} is not valid in the key of {self._starting_note.name}"
            )

        if base_note.letter == note_.letter:
            # this is the note that was shifted
            chromatic_map = (
                _CHROMATIC_SOLFEGE if self._type == ScaleType.MAJOR else _MINOR_CHROMATIC_SOLFEGE
            )
            result = chromatic_map[base_index].get(note_.accidental)
            if result is not None:
                return result
            if base_note.accidental and not note_.accidental:
                if base_note.accidental == "#":  # base note is sharp, return as if it were lowered
                    return chromatic_map[base_index].get("b")
                else:
                    return chromatic_map[base_index].get("#")

            raise ValueError("This case was not handled.")
