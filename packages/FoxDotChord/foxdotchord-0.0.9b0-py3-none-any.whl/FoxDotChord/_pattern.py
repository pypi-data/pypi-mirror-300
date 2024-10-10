from functools import reduce
from itertools import chain
from operator import iconcat
from typing import Collection, List, Union

try:  # pragma: no cover
    from renardo_lib.Patterns import Pattern
except ModuleNotFoundError:  # pragma: no cover
    try:
        from FoxDot.lib.Patterns import Pattern
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            '\n\tThe FoxDotChord package requires the renardo or FoxDot '
            'package to be installed.\n\tYou can install this with:\n'
            '\t$ pip install renardo  # https://renardo.org\n'
            '\tOR\n'
            '\t$ pip install FoxDot   # https://foxdot.org\n'
        ) from exc


class ChordPattern(Pattern):
    _degrees = {
        'I': 'tonic',
        'II': 'supertonic',
        'III': 'third',
        'IV': 'subdominant',
        'V': 'dominant',
        'VI': 'submediant',
        'VII': 'maj',
        'IX': 'ninth',
        'XI': 'eleventh',
        'XIII': 'thirteenth',
    }

    def degrees(self, grades: Union[str, List[str]], *args: str) -> Pattern:
        if isinstance(grades, str):
            grades = grades.split(',')

        notes = (
            getattr(c, self._degrees.get(a.strip(), '_'), None)
            for c in self.data
            for a in map(str.upper, chain(grades, args))
        )

        return Pattern(list(filter(lambda n: n is not None, notes)))

    deg = degrees

    @property
    def i(self) -> Pattern:
        return self.degrees('I')

    @property
    def ii(self) -> Pattern:
        return self.degrees('II')

    @property
    def iii(self) -> Pattern:
        return self.degrees('III')

    @property
    def iv(self) -> Pattern:
        return self.degrees('IV')

    @property
    def v(self) -> Pattern:
        return self.degrees('V')

    @property
    def vi(self) -> Pattern:
        return self.degrees('VI')

    @property
    def vii(self) -> Pattern:
        return self.degrees('VII')

    @property
    def ix(self) -> Pattern:
        return self.degrees('IX')

    @property
    def xi(self) -> Pattern:
        return self.degrees('XI')

    @property
    def xiii(self) -> Pattern:
        return self.degrees('XIII')

    tonic = i
    supertonic = ii
    third = iii
    subdominant = iv
    dominant = v
    submediant = vi
    maj = vii
    ninth = ix
    eleventh = xi
    thirteenth = xiii

    def arp(self, arp_pattern: Union[Collection, None] = None):
        """
        Create a arpeggio pattern.

        Parameters
        ----------
        arp_pattern : Collection, optional
            Arpeggio pattern.

        Examples
        --------

        You can create arpeggios with all chords.

        >>> from FoxDotChord import PChord
        >>> PChord['C, G'].arp()
        P[0, 2, 4, 4, 6, 8]

        Or create  a new Pattern with each item repeated len(arp_pattern) times
        and incremented by arp_pattern.

        >>> PChord['C, G'].arp([0, 3])
        P[0, 3, 2, 5, 4, 7, 4, 7, 6, 9, 8, 11]

        Returns
        -------
        Pattern[int]
            Arpeggio pattern.
        """
        notes = [a.notes if hasattr(a, 'notes') else [a] for a in self]
        pattern = Pattern(reduce(iconcat, notes))

        if arp_pattern:
            return pattern.stutter(len(arp_pattern)) + arp_pattern
        return pattern
