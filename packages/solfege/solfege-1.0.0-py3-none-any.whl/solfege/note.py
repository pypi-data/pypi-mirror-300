"""Classes to represent a note on the scale."""

import typing


# TODO: nameTuple??
class Note:
    """Represent a note on a scale."""

    def __init__(self, name: str, octave: typing.Optional[int] = None) -> None:
        """Initialize a Note.

        Args:
          name (str): The letter name of the note (use, b for flat and # for sharp)
          octave (int): (optional) the octave it is in (where Middle C begins octave 4)
        """
        self._letter = name[0]
        self._accidental = None
        self._octave = octave

        if len(name) > 1:
            if name[1] not in "b#":
                raise ValueError(
                    "Invalid modifier. Use 'b' for flat and '#' for sharp (that is all that is supported for now)."
                )
            self._accidental = name[1]

    @property
    def letter(self):
        """The letter part of the note name."""
        return self._letter

    @property
    def accidental(self) -> typing.Optional[str]:
        """If # or b or None if no accidental on this note."""
        return self._accidental

    @property
    def name(self):
        """The short name of the note.

        e.g. C or A# or Bb
        """
        return self._letter + (self._accidental if self._accidental else "")

    @property
    def octave(self):
        """The octave this note is in."""
        return self._octave
