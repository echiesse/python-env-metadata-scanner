# python-env-metadata-scanner
A scanner for python packages metadata

Currently only license information is being retrieved

## Usage
```python
python scan-env.py environments.txt
```

The file `environments.txt` must be in the following format:
```
<env 1 name> = <env 1 path>
<env 2 name> = <env 2 path>
...
```

# Example:
environments.txt:
```
WebApp = /home/myhome/.pyenv/versions/3.8.1/envs/webapp/lib/python3.8/site-packages
Service = /home/myhome/.pyenv/versions/3.8.1/envs/service/lib/python3.8/site-packages
```

```python
python scan-env.py environments.txt
```

For the above data the program will output two .csv files with the information it could find about all packages installed in each environment.
The information includes package name, version and the license name.

All information is obtained from the actual packages installed. No attempt to request data from the web is made.
