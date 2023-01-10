# CreateSpecFile

This code contains functions and a GUI for converting data files written by the SPC group LabVIEW control panel to a spec-like file. The spec-like file can be opened with pymca or other data viewers compatible with spec files.

The GUI can be run from the terminal by navigating to the directory containing CreateSpecFile.py and typing,

```
$ Python CreateSpecFile.py
```

or

```
$ Pythonw CreateSpecFile.py
```

From the GUI, one can select a folder containing data files written by the SPC group LabVIEW control panel, which have a .#### extension, where #### is a series of four number characters, select an output destination and filename for the spec-like file, and generate the spec-like file.
