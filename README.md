# CreateSpecFile

This code contains functions and a GUI for converting data files from APS beamlines 9-BM, 20-BM, 20-ID, and 4-ID-C to spec-like files. This program works on data files that have a .#### extension, where #### is a series of four number characters, which is the convention used at all four beamlines listed above. These files written by the SPC Group LabVIEW control panel at beamlines 9-BM, 20-BM, and 20-ID. All data files in a given folder will be copied to a sigle spec file, and the original data files will not be editied or deleted. After creation, the spec-like file can be opened with PyMca or other data viewers compatible with spec files.

The GUI can be run from the terminal by navigating to the directory containing CreateSpecFile.py and, depending on the python installation and environment, typing either

```
$ python CreateSpecFile.py
```

or

```
$ pythonw CreateSpecFile.py
```

From the GUI, one can select a folder containing data files generated at one of the above beamlines, select an output destination and filename for the spec-like file, and generate the spec-like file.

This code will also generate a spec-like file from data generated at beamline 4-ID-C, which also has a .#### extension.
