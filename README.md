# Windows

## Install

- Install Python 3.11
- pip install pipenv
- python -m pipenv shell


## Run GUI
python VDF_GUI.py
pyinstaller -F VDF_GUI.py
pyinstaller VDF_GUI.spec

## Run Milestone
python coverage.py
pyinstaller coverage.spec

## Run Requirement
python VDF_Requirement.py
pyinstaller -F VDF_Requirement.py