# py-solfege

A Python library for dealing with musical scales and there solfège.

[![Static Badge](https://img.shields.io/badge/PyPI-solfege-black)](https://pypi.org/project/solfege)
 [![GitHub Repo](https://img.shields.io/badge/github-mshafer1%2Fpy--solfege-blue?logo=github)](https://github.com/mshafer1/py-solfege)
 [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Why?

I needed a library that I could ask for "in this key, what is the solfege name for this note?"

JS has the [Teoria](https://www.npmjs.com/package/teoria) library that could do the scale, but I needed this in Python.

I was unable to find a complete implementation in Python.
All other projects I found on Pypi.org, github.com, and using Google search did NOT handle non-diatonic notes (and many required numpy as a dependency -> which is a quite heavy handed dependency for such a task...).

Usage:

```python
>>> import solfege

>>> scale = solfege.Scale(solfege.Note("C"))
>>> scale.solfege(solfege.Note("C"))
'Do'
>>> scale.solfege(solfege.Note("D"))
'Re'
>>> scale.solfege(solfege.Note("B"))
'Ti'

# accidentals are handled
>>> scale.solfege(solfege.Note("C#"))
'Di'


>>> a_major_scale = solfege.Scale(solfege.Note("A"))
>>> a_major_scale.solfege(solfege.Note("A"))
'Do'
>>> a_major_scale.solfege(solfege.Note("B"))
'Re'
>>> a_major_scale.solfege(solfege.Note("C#"))
'Mi'

# minor scales are done with movable-Do, La-based method: https://en.wikipedia.org/wiki/Solf%C3%A8ge
>>> a_minor_scale = solfege.Scale(solfege.Note("A"), solfege.ScaleType.MINOR)
>>> a_minor_scale.solfege(solfege.Note("A"))
'La'
>>> a_minor_scale.solfege(solfege.Note("C"))
'Do'

```

See [the docs](https://mshafer1.github.io/py-solfege).