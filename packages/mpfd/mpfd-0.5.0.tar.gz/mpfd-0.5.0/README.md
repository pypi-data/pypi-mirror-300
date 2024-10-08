# mpfd - Make Parallel Function Decorator

`mpfd` is a simple Python package that provides a decorator, `make_parallel`, which allows you to make a function run in parallel using multithreading. This is built on top of Python's `concurrent.futures` module.

## Installation

Install the package via pip :

```bash
pip install mpfd
```

## Usage

To use the ```make_parallel``` decorator :

```python
from mpfd import make_parallel

@make_parallel
def my_function(param):
    print(param)

my_function(
    [
        "Hello, parallel world!1",
        "Hello, parallel world!2",
        "Hello, parallel world!3",
        "Hello, parallel world!4",
    ]
)
```

This will execute ```my_function``` in parallel using multithreading.
