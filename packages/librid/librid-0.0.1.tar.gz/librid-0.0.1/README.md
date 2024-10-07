#### For Ubuntu:
`apt install python3-scriptforge`

#### Start a listening LibreOffice instance
`/usr/lib/libreoffice/program/soffice --accept='socket,host=your_host,port=port_number;urp;'`
- replace `your_host` and `port_number`.
- add  `--invisible` to run in background.
- after running your `python` scripts kill the process (e.g. with `ctrl + C`)

#### Workdir
In `src` directory `mkdir workdir workdir/input workdir/output workdir/temp` or change the predefined paths in `src/core/document.py`. (Maybe create a directory structure somewhere on your computer for these kind of tasks and create symlinks - idk yet.)

#### Interactivity
When you start a listening LibreOffice instance you can use it interactively via the Python REPL. In Visual Studio Code there is a `Run Selection/Line in Python REPL` option. The shortcut for it is `Shift+Enter`. You don't have to build the whole project every time, also you can catch data in variables once and work with it (e.g. only one API call is enough to work with the response). If you want to see the LibreOffice results in realtime do not use the `--invisible` switch.


