# Evolutionary Alpha Miner

**Family-aware evolutionary alpha mining with LLM-guided symbolic hybridization.**

This repository introduces a research framework for automated formulaic alpha discovery.  
The core idea is to treat alpha expressions as evolvable symbolic programs, then use seed-family deduplication, heterogeneous parent pairing, constrained LLM generation, and simulation feedback to search for new candidates.

> This public repository is a sanitized framework.  
> It does not contain private alpha expressions, API keys, credentials, proprietary datasets, or real simulation results.

---

## Motivation

Naively generating formulaic alphas often leads to near-duplicate expressions, unstable backtests, or high self-correlation with existing candidates.

This project explores a more structured approach:

- avoid near-duplicate parents
- preserve useful seed signals
- hybridize heterogeneous expression families
- use weak gates / regime conditions / correlation breakers
- feed pass/fail results back into the next generation

The goal is not unrestricted formula enumeration, but **correlation-aware evolutionary search**.

---

## Core Workflow

```text
historical candidates
        ↓
expression normalization
        ↓
seed family clustering
        ↓
family-aware parent sampling
        ↓
A-B hybridization
        ↓
LLM-constrained candidate generation
        ↓
local validation
        ↓
simulation / submission checks
        ↓
feedback memory
        ↓
next generation
