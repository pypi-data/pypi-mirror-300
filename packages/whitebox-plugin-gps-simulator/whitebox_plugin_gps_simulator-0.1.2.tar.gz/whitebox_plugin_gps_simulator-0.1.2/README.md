# Whitebox Plugin - GPS Simulator

This is a plugin for [whitebox](https://gitlab.com/whitebox-aero) that simulates GPS data.

## Installation

Simply install the plugin to whitebox:

```
poetry add whitebox-plugin-gps-simulator
```

## For Developers

1. Set up whitebox locally.
2. Clone this repository.
3. Add plugin to whitebox using the following command: `poetry add -e path/to/plugin.`
4. Run the whitebox server.

## Running Tests

Test suite can only run over CI due to the need for running a whitebox server with plugins loaded and plugin tests moved to whitebox test suite. In future, we will add docker support for running tests locally.

## Contribution Guidelines

1. Write tests for each new feature.
2. Ensure coverage is 90% or more.
3. [Google style docstrings](https://mkdocstrings.github.io/griffe/docstrings/#google-style)
   should be used for all functions and classes.
