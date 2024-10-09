# pyml-regression-example1

Example from Chapter 1 of the book [Hands-on Machine Learning with Scikit-Learn, Keras and TensorFlow](https://github.com/ageron/handson-ml3). This example illustrates regression techniques.

## Installation from Git source
```
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install .
```
or if you plan to change the source code, install for development like this:
```
$ uv venv
$ uv sync   # Install dependencies
$ source .venv/bin/activate
$ source shell_completion/bash.sh   # optionally enable shell completions
```
Then, test the installed script:
```
$ life-expectancy --help
# Test a sub command, e.g. download-data
$ life-expectancy download-data
```

For more information, see [the documentation](https://hakonhagland.github.io/pyml-regression-example1/).
