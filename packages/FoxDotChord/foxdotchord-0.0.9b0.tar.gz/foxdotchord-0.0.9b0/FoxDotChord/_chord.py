"""Chord module."""

import re
from itertools import chain
from typing import List, Sequence, Union

try:  # pragma: no cover
    from renardo_lib.Patterns import Pattern, PGroup
    from renardo_lib.Root import Note, Root
    from renardo_lib.TimeVar import TimeVar
except ModuleNotFoundError:  # pragma: no cover
    try:
        from FoxDot.lib.Patterns import Pattern, PGroup
        from FoxDot.lib.Root import Note, Root
        from FoxDot.lib.TimeVar import TimeVar
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            '\n\tThe FoxDotChord package requires the renardo or FoxDot '
            'package to be installed.\n\tYou can install this with:\n'
            '\t$ pip install renardo  # https://renardo.org\n'
            '\tOR\n'
            '\t$ pip install FoxDot   # https://foxdot.org\n'
        ) from exc

from ._notes import from_chromatic
from ._pattern import ChordPattern

TNote = Union[int, float, None]


class ChordException(Exception):
    """Chord exception."""


class Chord(PGroup):
    """
    Musical chord to be manipulated by renardo or FoxDot.

    The chord class generates chords that can be used by renardo or FoxDot.

    Examples
    --------
    >>> Chord('C#7/9')
    Chord('C#7/9')
    """

    def __init__(self, chord: str):
        """Initialize a new chord."""
        if hasattr(chord, 'chord'):
            self.chord = chord.chord
        elif isinstance(chord, str) and hasattr(chord, 'strip'):
            self.chord: str = chord.strip()
        else:
            self.chord: str = f'undefined: <{type(chord)}>'

        super().__init__(self.notes)

    def __repr__(self):
        """Chord representation."""
        return f"Chord('{self.chord}')"

    __str__ = __repr__

    def true_copy(self, new_data=None):
        """Copy object."""
        new = self.__class__(self.chord)
        new.__dict__ = self.__dict__.copy()
        if new_data is not None:
            new.data = new_data
        return new

    def _get_note(self, pattern: str, tons: int) -> TNote:
        if not re.search(pattern, self.chord):
            return None

        if self.is_flat:
            tons -= 1
        if self.is_sharp:
            tons += 1
        return from_chromatic(self._tonic + tons)

    @property
    def tone(self) -> int:
        """Indicates whether the tone."""
        return Root.default

    @property
    def is_flat(self) -> bool:
        """
        Indicates whether the chord is flat.

        Examples
        --------
        >>> Chord('Cb').is_flat
        True
        >>> Chord('C#').is_flat
        False

        Returns
        -------
        bool:
            `True` if the chord is flat otherwise `False`.
        """
        return bool(re.search(r'[-b]', self.chord))

    @property
    def is_sharp(self) -> bool:
        """
        Indicates whether the chord is sharp.

        Examples
        --------
        >>> Chord('Cb').is_sharp
        False
        >>> Chord('C#').is_sharp
        True

        Returns
        -------
        bool:
            `True` if the chord is sharp otherwise `False`.
        """
        return bool(re.search(r'[+#]', self.chord))

    @property
    def is_dim(self) -> bool:
        """
        Indicates whether the chord is sharp.

        Examples
        --------
        >>> Chord('D').is_dim
        False
        >>> Chord('D⁰').is_dim
        True
        >>> Chord('D0').is_dim
        True
        >>> Chord('Do').is_dim
        True
        >>> Chord('DO').is_dim
        True
        >>> Chord('Ddim').is_dim
        True

        Returns
        -------
        bool:
            `True` if the chord is diminished otherwise `False`.
        """
        return bool(re.search(r'([⁰0oO]|dim)', self.chord))

    @property
    def is_sus(self) -> bool:
        """Indicates whether the chord is suspended.

        Examples
        --------
        >>> Chord('Eb').is_sus
        False
        >>> Chord('Ebsus').is_sus
        True
        >>> Chord('Ebsus4').is_sus
        True
        >>> Chord('Eb4').is_sus
        False
        >>> Chord('Eb3#').is_sus
        False

        Returns
        -------
        bool:
            `True` if the chord is suspended otherwise `False`.
        """
        return bool(re.search(r'(sus)', self.chord))

    @property
    def is_minor(self) -> Union[bool, None]:
        """Indicates if the chord is minor.

        Examples
        --------
        >>> Chord('E#').is_minor
        False
        >>> Chord('E#m').is_minor
        True
        >>> Chord('E#5').is_minor

        Returns
        -------
        bool:
            `True` if the chord is minor otherwise `False`.
        None:
            If it is a power chord there is no way to know if it is
            minor, because it doesn't have the III of the chord.
        """
        if self.is_power_chord:
            return None
        return bool(re.search(r'^[A-G][b#]?m', self.chord))

    @property
    def is_power_chord(self) -> bool:
        """
        Indicates if the chord is minor.

        Examples
        --------
        >>> Chord('E#').is_power_chord
        False

        >>> Chord('E#5').is_power_chord
        True

        Returns
        -------
        bool:
            `True` if it's a power chord otherwise `False`.

        """
        return bool(re.search(r'^([A-G][b#]?5)$', self.chord))

    @property
    def notes(self) -> List[int]:
        """
        Chord notes.

        Examples
        --------
        >>> Chord('C').notes
        [0, 2, 4]

        Returns
        -------
        list of int:
            List of notes
        """
        degrees = [
            self.tonic,
            self.supertonic,
            self.third,
            self.subdominant,
            self.dominant,
            self.submediant,
            self.maj,
            self.ninth,
            self.eleventh,
            self.thirteenth,
        ]
        return list(filter(lambda d: d is not None, degrees))

    @property
    def _tonic(self) -> int:
        if not (
            result := re.search(r'(^(?P<tone>[A-G]{1}[b#]?))', self.chord)
        ):
            raise ChordException(
                f'Tonic inválid: "{self.chord:.1}" from chord "{self.chord}"',
            )
        return Note(result.group('tone')) + self.tone

    @property
    def tonic(self) -> int:
        """Tonic I.

        Examples
        --------
        >>> Chord('C')
        Chord('C')
        """
        return from_chromatic(self._tonic)

    @property
    def supertonic(self) -> TNote:
        """Supertonic II."""
        if re.search(r'(sus)?2', self.chord):
            return from_chromatic(self._tonic + 2)
        return None

    @property
    def third(self) -> TNote:
        """Third III."""
        if self.is_power_chord or self.is_sus:
            return None

        if self.is_dim or self.is_minor:
            return from_chromatic(self._tonic + 3)
        return from_chromatic(self._tonic + 4)

    @property
    def subdominant(self) -> TNote:
        """Subdominant IV."""
        if re.search(r'(sus)2', self.chord) or (
            not re.search(r'4', self.chord)
            and not re.search(r'(sus)(3[\+#]|4)?', self.chord)
        ):
            return None
        return from_chromatic(self._tonic + 5)

    @property
    def dominant(self) -> TNote:
        """Dominant V."""
        if re.search(r'5[\+#]', self.chord):
            return from_chromatic(self._tonic + 8)
        if re.search(r'5[\-b]', self.chord) or self.is_dim:
            return from_chromatic(self._tonic + 6)
        return from_chromatic(self._tonic + 7)

    @property
    def submediant(self) -> TNote:
        """Submediant VI."""
        if re.search(r'6', self.chord):
            return from_chromatic(self._tonic + 9)
        return None

    @property
    def maj(self) -> TNote:
        """Maj VII."""
        if re.search(r'7(M|[Mm]aj)', self.chord):
            return from_chromatic(self._tonic + 11)
        if re.search(r'7', self.chord):
            return from_chromatic(self._tonic + 10)
        if self.is_dim:
            return from_chromatic(self._tonic + 9)
        return None

    @property
    def ninth(self) -> TNote:
        """Ninth IX."""
        if re.search(r'9[\+\#]', self.chord):
            return from_chromatic(self._tonic + 15)
        if re.search(r'9[\-b]', self.chord):
            return from_chromatic(self._tonic + 13)
        if re.search(r'9', self.chord):
            return from_chromatic(self._tonic + 14)
        return None

    @property
    def eleventh(self) -> TNote:
        """Eleventh XI."""
        if re.search(r'11[\+#]', self.chord):
            return from_chromatic(self._tonic + 18)
        if re.search(r'11[\-b]', self.chord):
            return from_chromatic(self._tonic + 16)
        if re.search(r'11', self.chord):
            return from_chromatic(self._tonic + 17)
        return None

    @property
    def thirteenth(self) -> TNote:
        """Thirteenth XIII."""
        if re.search(r'13[\+#]', self.chord):
            return from_chromatic(self._tonic + 22)
        if re.search(r'13[\-b]', self.chord):
            return from_chromatic(self._tonic + 20)
        if re.search(r'13', self.chord):
            return from_chromatic(self._tonic + 21)
        return None


class __chords__:  # noqa: N801
    """
    Creates a harmonic progression based on a list of chords.

    Parameters
    ----------
    chords : str
        Many chords

    Examples
    --------

    ## Pattern chords

    You can create a chord pattern in a few ways.

    One of them is using `[]` or `()` with a list of strings:

    >>> PChord['Am7', 'C(7/9)', 'F7Maj', 'G(4/9/13)']
    P[Chord('Am7'), Chord('C(7/9)'), Chord('F7Maj'), Chord('G(4/9/13)')]
    >>> PChord('Am7', 'C(7/9)', 'F7Maj', 'G(4/9/13)')
    P[Chord('Am7'), Chord('C(7/9)'), Chord('F7Maj'), Chord('G(4/9/13)')]

    Or use `[]` or `()` passing a string of chords separated by `,`:

    >>> PChord['Am7, C(7/9), F7Maj, G(4/9/13)']
    P[Chord('Am7'), Chord('C(7/9)'), Chord('F7Maj'), Chord('G(4/9/13)')]
    >>> PChord('Am7,C(7/9),F7Maj,G(4/9/13)')
    P[Chord('Am7'), Chord('C(7/9)'), Chord('F7Maj'), Chord('G(4/9/13)')]

    ## Arpeggios

    You can create arpeggios with all chords.

    >>> PChord['C, G'].arp()
    P[0, 2, 4, 4, 6, 8]

    Or create  a new Pattern with each item repeated len(arp_pattern) times
    and incremented by arp_pattern.

    >>> PChord['C, G'].arp([0, 3])
    P[0, 3, 2, 5, 4, 7, 4, 7, 6, 9, 8, 11]

    You can also create the arpeggio of a single chord when defining it.

    >>> PChord['C@, G']
    P[0, 2, 4, Chord('G')]

    ## Repetition

    You can also set how many times the chord will be repeated

    >>> PChord['C!4, Dm!2'].json_value()
    ['TimeVar', [Chord('C'), Chord('Dm')], [4, 2]]

    Or repeat the number of times the arpeggio will be made

    >>> PChord['C!4, Dm!2, G7!2@'].json_value()
    ['TimeVar', [Chord('C'), Chord('Dm'), 4, 6, 8, 10], [4, 2, 2, 2, 2, 2]]

    ## Degrees

    If you want, you can also get the degrees of the chords, to use on the
    bass, for example.

    Picking up the tonic:

    >>> PChord['C, G'].i
    P[0, 4]
    >>> PChord['C, G'].tonic
    P[0, 4]

    Picking up the supertonic:

    >>> PChord['C2, G2'].ii
    P[1, 5]
    >>> PChord['C2, G2'].supertonic
    P[1, 5]

    Picking up the supertonic:

    >>> PChord['C, G'].iii
    P[2, 6]
    >>> PChord['C, G'].third
    P[2, 6]

    Picking up the subdominant:

    >>> PChord['C4, G4'].iv
    P[3, 7]
    >>> PChord['C4, G4'].subdominant
    P[3, 7]

    Picking up the dominant:

    >>> PChord['C5b, G5#'].v
    P[3.5, 8.5]
    >>> PChord['C5+, G5-'].dominant
    P[4.5, 7.5]

    Picking up the submediant:

    >>> PChord['C6, G6'].vi
    P[5, 9]
    >>> PChord['C6, G6'].submediant
    P[5, 9]

    Picking up the maj:

    >>> PChord['C7Maj, G7'].vii
    P[6, 10]
    >>> PChord['C7, G7M'].maj
    P[5.5, 10.5]

    Picking up the ninth:

    >>> PChord['C9b, G9#'].ix
    P[7.5, 12.5]
    >>> PChord['C9+, G9-'].ninth
    P[8.5, 11.5]

    Picking up the eleventh:

    >>> PChord['C11b, G11#'].xi
    P[9, 14.5]
    >>> PChord['C11+, G11-'].eleventh
    P[10.5, 13]

    Picking up the thirteenth:

    >>> PChord['C13b, G13#'].xiii
    P[11.5, 17]
    >>> PChord['C13+, G13-'].thirteenth
    P[12.5, 15.5]

    Taking more than one degree of the chords:

    >>> PChord['C, G'].deg('i, iii')
    P[0, 2, 4, 6]
    >>> PChord['C, G'].degrees('i, v')
    P[0, 4, 4, 8]

    ## Mixing inputs

    >>> PChord['C, D', [1, 4], 'Dm, E#', (2, 3), 1]
    P[Chord('C'), Chord('D'), P[1, 4], Chord('Dm'), Chord('E#'), P(2, 3), 1]

    >>> PChord[1, 'C, D', [1, 4], 'Dm, E#@', (2, 3)]
    P[1, Chord('C'), Chord('D'), P[1, 4], Chord('Dm'), 3, 5, 7, P(2, 3)]

    >>> PChord[(2, 3), 'C!4, D', [1, 4], 'Dm!3@', 1].json_value()
    ['TimeVar', [P(2, 3), Chord('C'), Chord('D'), 1, 1, 3, 5, 1, P(2, 3), Chord('C'), Chord('D'), 4, 1, 3, 5, 1], [1, 4, 1, 1, 3, 3, 3, 1]]

    Returns
    -------
    ChordPattern[Chord]
        A `Chord` pattern.
    """  # noqa: E501

    @staticmethod
    def __get(chords, args):
        if isinstance(chords, str):
            chords = chords.split(',')
        elif not isinstance(chords, Sequence):
            chords = [chords]

        for arg in chain(chords, args):
            if isinstance(arg, str):
                yield from map(str.strip, arg.split(','))
            else:
                yield arg

    def __new(
        self, chords: Union[str, list], *args: str
    ) -> Union[Pattern, TimeVar]:

        harmony = []
        repets = []
        for chord in self.__get(chords, args):
            repet = 1
            if not isinstance(chord, str):
                harmony.append(chord)
                repets.append(repet)
                continue

            if matcher := re.search(r'[A-Z].*!(?P<repet>\d{1,})', chord):
                chord = re.sub(r'!(?P<repet>\d{1,})', '', chord)
                repet = int(matcher.group('repet'))
            repets.append(repet)

            if chord.endswith('@'):
                harmony.extend(notes := Chord(chord.removesuffix('@')).notes)
                for _ in range(len(notes) - 1):
                    repets.append(repet)
            else:
                harmony.append(Chord(chord))

        pattern = ChordPattern(harmony)
        if any(filter(lambda r: r > 1, repets)):
            return TimeVar(pattern, repets)
        return pattern

    __getitem__ = __call__ = __new


PChord = __chords__()
