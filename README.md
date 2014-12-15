# README #
Looks up distance in `meters` from `google distance matrix api`.
Currently reads `origin` and `destination` fields from a input csv file: `dist_matrix.csv` and creates a output csv file with `distance` field populated. Mode option can be `walking`, `driving`, `bicycling`  
### how to run it: ###
Setup the [Google APIs Client Library for Python](https://developers.google.com/api-client-library/python/start/get_started) and activate a proper api-key
This code requires the `simplejson` library which can be installed with [pip](https://pypi.python.org/pypi/pip):
```
pip install simplejson
```

### run for your data ###
Use the example: `dist_matrix.csv` to make input data, in command-line `cd` to src folder and run: `dist_matrix.py -i <inputfile> -o <outputfile> -m <mode>`
for example:
```
python dist_matrix.py -i dist_matrix.csv -o output.csv -m walking
```