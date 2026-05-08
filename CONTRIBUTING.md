# Contributing

Thanks for your interest in Evolutionary Alpha Miner.

This repository is a public research prototype. Contributions are welcome when they improve the synthetic demo, documentation, reproducibility, or modular research workflow.

## Good First Contributions

- Improve expression normalization examples.
- Add more synthetic seed expressions.
- Add unit tests for family hashing and parent sampling.
- Add a small visualization for the search loop.
- Improve documentation around failure categories.
- Add benchmark scripts against random candidate generation.

## Safety Boundary

Please do not submit:

- private alpha formulas
- proprietary datasets
- API keys or credentials
- real platform simulation output
- non-public research notebooks

Synthetic examples are preferred.

## Development

Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the toy demo:

```bash
python examples/toy_demo.py
```

Before opening a pull request, make sure the demo runs successfully and the README still reflects the public, sanitized scope of the project.
