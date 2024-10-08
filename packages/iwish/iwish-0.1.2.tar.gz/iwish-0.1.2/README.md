# iwish interactive wish (tcl/tk interpreter)

iwish is a script that gives interactive features to wish like navigating with
arrows backward search ... history files (all that readline can offer).

Due to my limitations, however, input are line based and eval in tcl before being
interpreted.

It is made for tinkering with tcl/tk to test something fast with the help of an
interactive shell.

To use it just call : `iwish`

## special words

### quit bye exit

These bare keywords exit the shell

### #l

This shortcut list the current session

### #?

This shortcut call the inline help

## Evaluating python

### #!...

... being a python command will be evaled in current content

### #!save(fn="temp")

Calls the `save` function which saves the current session in file given as an
argument or "temp" in the current directory by default.

### #!load(fn="temp")

Loads a tcl file and evaluate it LINE BY LINE (which may break valid multiline
tcl code).


