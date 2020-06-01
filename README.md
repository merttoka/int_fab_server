
This repository acts as a mediator between [the frontend](https://github.com/merttoka/int_fab_frontend.git) and Ender 3 Pro using [Printrun](https://github.com/kliment/Printrun) module. 

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
> python -m pip install sneakysnek # detect keys
> python setup.py build_ext --inplace
```

**MacOS (terminal):**
```bash
$ python3 -m venv venv  # create an virtual environment
$ . venv/bin/activate  # activate the virtual environment (notice the space after the dot)
(venv) $ python -m pip install -r requirements.txt  # intall the rest of dependencies
(venv) $ python -m pip install Cython
(venv) $ python -m pip install sneakysnek # detect keys
(venv) $ python setup.py build_ext --inplace
```

#### Run 
```bash
> cd .. # jump back to root directory

# windows
> python .\main.py --serial=COM#
# macos
$ python main.py --serial=/dev/ttyUSB#
```

#### Keys
`ESC` Shuts down
`r`   Auto Home


