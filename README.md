## .FIT File Processing Project
This is where I will be extracting data from .fit files.
I have started with a simple tkinter visualisation tool which allows any .fit file to be uploaded and extracts:
  - heart rate
  - latitude and longitude
  - distance
  - "enhanced" speed
if they exist in the file.

.fit files are general containers for fitness data, they can contain a wide range of different metrics and any subset of those. I have focussed on metrics relevant to our analysis.

## Instructions for use

Run `python -m venv myvenv`

Run `source myvenv/bin/activate`

Run `pip install`

Run `python fit_file_viewer.py` to open the .fit file visualisation tool.

