# Evolutionary Alpha Miner

**Family-aware evolutionary alpha mining with LLM-guided symbolic hybridization.**

This repository presents a research framework for automated formulaic alpha discovery.  
The core idea is to treat alpha expressions as symbolic programs that can be cleaned, clustered, recombined, evaluated, and improved through feedback.

> This public repository is a sanitized research framework.  
> It does not contain private alpha expressions, API keys, credentials, proprietary datasets, real alpha IDs, or real simulation results.

---

## Why This Project Exists

Naively generating formulaic alphas often leads to:

- near-duplicate expressions
- unstable backtests
- excessive self-correlation
- repeated parent signals
- poor out-of-sample robustness

This project explores a more structured workflow:

- clean and deduplicate seed families
- sample heterogeneous parent pairs
- preserve useful parent signals
- use weak gates, regime conditions, or correlation breakers
- validate generated expressions
- evaluate candidates
- feed pass/fail results into future search rounds

The goal is not unrestricted formula enumeration, but **correlation-aware evolutionary search**.

---

## Core Idea

The framework is built around **A-B hybridization**:

- **A** is the main signal carrier.
- **B** is a weak modifier, gate, regime condition, dataset inspiration, or correlation breaker.

Instead of blindly combining formulas, the system tries to preserve useful signal structure while reducing redundancy.

```text
historical candidates
        ↓
expression normalization
        ↓
seed family clustering
        ↓
diverse parent sampling
        ↓
A-B hybridization
        ↓
candidate generation
        ↓
local validation
        ↓
simulation / check feedback
        ↓
memory update
        ↓
next generation
```

---

## Method Overview

### 1. Seed Family Cleaning

Many alpha expressions are only superficial variants of the same idea.  
The framework normalizes expressions and groups similar structures into seed families.

This helps avoid breeding near-duplicate parents.

### 2. Diverse Parent Sampling

Parent pairs are sampled with diversity constraints:

- avoid identical expression families
- reduce repeated parent usage
- balance different data families
- prefer heterogeneous tag pairs
- track used parent-pair hashes

Example tag pairs:

```text
price + volume
price + option
volume + fundamental
option + price
news + price
analyst + price
```

### 3. Constrained Hybrid Generation

The generator is not asked to freely invent formulas.

Instead, it follows constrained mutation logic:

- preserve A's core signal
- use B as a weak modifier
- avoid destructive A-B spreads
- avoid repeated templates
- avoid excessive smoothing
- prefer interpretable hybrid structures

Typical mutation modes include:

```text
weak_gate_hybrid
regime_hybrid
mild_corr_breaker
dataset_substitution
directional_switch
```

### 4. Validation and Feedback

Candidates are checked and categorized into feedback buckets:

- confirmed landed candidates
- strong but not landed candidates
- failed candidates
- suspected self-correlation traps
- low Sharpe / low fitness candidates
- concentrated-weight failures
- turnover failures

This feedback can be used to guide the next generation.

---

## Toy Demo

This repository includes a public toy demo using synthetic expressions and a fake evaluator.

It does **not** use real alpha expressions or external trading APIs.

Run:

```bash
pip install -r requirements.txt
python examples/toy_demo.py
```

The toy demo shows:

```text
synthetic seed pool
→ family hashing
→ diverse A-B parent pairing
→ candidate hybridization
→ fake evaluation
→ feedback summary
```

---

## Repository Structure

```text
Evolutionary-Alpha-Miner/
├── README.md
├── ROADMAP.md
├── LICENSE
├── requirements.txt
├── .gitignore
└── examples/
    └── toy_demo.py
```

---

## Research Context

This project sits at the intersection of:

- Genetic Programming
- Symbolic Regression
- Evolutionary Computation
- Program Synthesis
- LLM Agents
- Active Learning
- Automated Alpha Discovery
- Quantitative Finance Research

The central research question is:

> Can LLMs improve symbolic alpha search when constrained by seed-family memory, parent diversity, and evaluation feedback?

---

## What This Repository Does Not Contain

For safety and privacy, this public repository excludes:

- private credentials
- API keys
- real alpha expressions
- real alpha IDs
- proprietary datasets
- real simulation outputs
- platform-specific private results
- production mining notebooks

The public version focuses on the general research framework and reproducible toy examples.

---

## Planned Work

See [ROADMAP.md](./ROADMAP.md).

Planned additions include:

- toy symbolic dataset
- expression normalization module
- seed-family clustering module
- diverse parent sampler
- mutation template library
- feedback memory module
- failure-reason analytics
- search loop visualization
- benchmark against random generation

---

## Disclaimer

This project is for research and educational purposes only.

It does not provide financial advice, investment advice, trading signals, or proprietary alpha formulas.  
Any examples in this repository are synthetic and should not be interpreted as real trading strategies.

---

## Citation

If you find this project useful, feel free to star the repository or reference it as:

```text
Evolutionary Alpha Miner: Family-aware evolutionary alpha mining with LLM-guided symbolic hybridization.
```
