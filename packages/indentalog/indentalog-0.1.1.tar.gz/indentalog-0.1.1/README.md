# indentalog

An easy-to-use progress bar decorator for Python functions and loops.

## Getting Started

**indentalog** will be available on PyPI once it reaches a stable version. For now, you can install it from the source code.

```bash
git clone git@github.com:bastienlc/indentalog.git
cd indentalog
poetry install
```

**indentalog** has the simplest API possible. Just import the `ilog` object and use it either as a decorator, as an iterator wrapper or as a context manager.

```python
from indentalog import ilog

@ilog()
def my_first_function():
    # Your code here
    pass

def my_second_function():
    for i in ilog(range(10)):
        # Your code here
        pass

my_first_function()
my_second_function()
```

![GIF for the first example.](https://raw.githubusercontent.com/bastienlc/indentalog/assets/example_1.gif)

The main advantage of **indentalog** is that it keeps track of the call stack, which allows displaying the progress of nested functions or loops.

```python
from indentalog import ilog

@ilog()
def my_inner_function():
    # Your code here
    pass

def my_main_function():
    for i in ilog(range(3), name="Main function"):
        # Your code here
        my_inner_function()
        pass

my_main_function()
```

![GIF for the first example.](https://raw.githubusercontent.com/bastienlc/indentalog/assets/example_2.gif)


### Future features
- [ ] Passing data to the endpoints
- [ ] Support for custom styles or themes
