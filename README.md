# 0x00. AirBnB Clone - The Console

## Description

This project is part of the AirBnB clone series, focusing on the back-end part
of the application. It introduces the first step towards building a full web
application: the command interpreter. This console is used to manage objects for
our AirBnB clone project, including operations such as creating new objects,
retrieving an object, doing operations on objects, updating attributes of an
object, and destroying objects.

## Installation

To use the console, clone this repository to your local machine:
`https://github.com/abdelhafid-mahmoudi-env/AirBnB_clone`

## Execution

Your shell should work like this in interactive mode:

```linux
$ ./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  help  quit

(hbnb) 
(hbnb) 
(hbnb) quit
$
```

But also in non-interactive mode: (like the Shell project in C)

```linux
$ echo "help" | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb) 
$
$ cat test_help
help
$
$ cat test_help | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb) 
$
```

## Tests

All the files, classes, functions are tested with unit tests
```linux
python3 -m unittest discover tests
```

Unit tests also work in non-interactive mode:
```linux
echo "python3 -m unittest discover tests" | bash
```

## Authors

- Abdelhafid Mahmoudi <abdelhafid.mahmoudi.env@gmail.com>
- Amine El Orche <amineelorche@gmail.com>

## License
See the LICENSE file for details.
