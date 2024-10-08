[this code home repository](https://github.com/jul/iwish)

[filling an issue](https://github.com/jul/iwish/issues)

[this module on pypi](https://pypi.org/project/iwish/)

# iwish interactive wish (tcl/tk interpreter)

iwish is a script that gives interactive features to wish like navigating with
arrows backward search ... history files (all that readline can offer).

Due to my limitations, however, input are line based and eval in tcl before being
interpreted.

It is made for tinkering with tcl/tk to test something fast with the help of an
interactive shell.

A typical session looks like this
``` 
# pack [ button .c -text that -command { puts "hello" } ]
# 
tcl output> hello # here we pressed the button "that"
tcl output> hello # here we pressed the button "that"


# set name 32
# puts $name

tcl output> 32

# #?

#l print current recorded session
#? print current help
#! calls python code like
  #!save(name="temp") which saves the current session in current dir in "temp" file
bye exit quit quit the current session

# #l
pack [ button .c -text that -command { puts "hello" } ]
set name 32
puts $name

# #!save("my_test.tcl")
# quit
```

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
