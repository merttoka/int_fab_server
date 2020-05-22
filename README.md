
*Tested on Windows 10 with Python 3.7.*

**[Printrun](https://github.com/kliment/Printrun) module:**
```
git submodule init
git submodule update

cd Printrun 
```

**Windows (powershell):**
```powershell
> py -3 -m venv venv
> .\venv\Scripts\activate.bat
> python -m pip install -r requirements.txt
> python -m pip install Cython
> python setup.py build_ext --inplace
```

**MacOS (terminal):**
```bash
$ python3 -m venv venv  # create an virtual environment
$ . venv/bin/activate  # activate the virtual environment (notice the space after the dot)
(venv) $ python -m pip install -r requirements.txt  # intall the rest of dependencies
(venv) $ python -m pip install Cython
(venv) $ python setup.py build_ext --inplace
```

#### Adjusting serial port 
In `main.py`, change the following `port` variable to correct serial port for Ender 3.
```python
## main.py

port = 'COM4' # <-- Windows 'COM#', Mac '/dev/ttyUSB#'
p = printcore(port, 115200)
```

#### Run 
```bash
> cd .. # jump back to root directory
> python .\main.py
```

#### Keys
`r`   Auto Home

`x` - `s` increments and decrements the x dimension, respectively

`y` - `h` increments and decrements the y dimension, respectively

`z` - `a` increments and decrements the z dimension, respectively




