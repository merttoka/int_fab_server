
This repository acts as a mediator between [the frontend](https://github.com/merttoka/int_fab_frontend.git) and Ender 3 Pro using [Printrun](https://github.com/kliment/Printrun) module. 

*Tested on:*
- *Windows 10 with Python 3.7*
- *Ubuntu 18.04 (in WSL) with Python 3.7* 

## Install
```
git clone https://github.com/merttoka/int_fab_server.git
cd int_fab_server

git submodule init
git submodule update

cd Printrun 
```

### Printrun 

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

## Run 
```bash
> cd .. # jump back to root directory

> pip install python-osc # osc library

# on windows
> python .\main.py --serial=COM#
# on macos
$ python main.py --serial=/dev/ttyUSB#
```

- *Note:* You can find the serial port in your system settings.

- *Note 2:* MacOS users might need to allow Python in accesibility settings to be able to use keybindings.

#### Key bindings
`ESC` Shuts down
`T`   Set temperature to 200/50
`R`   Auto Home & Move to first layer
`E`   Clear material from nozzlehead (extrudes on the side)

