Speech recognition
==================

Alongside the network-related part of `noded` is launched a service for recognizing phrases and parsing them. Phrases are placed (at this point in time) in `config.py` in the `voice_coms` variable (phrase to Python script). Then, if given phrase is recognized, the associated script is executed.

The parsing is provided, as of now, by a cloud service interfaced through `speechrecognition` package.
