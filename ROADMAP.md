# Roadmap

Evolutionary Alpha Miner is intentionally small at this stage. The goal is to turn a clear research idea into a reproducible public toolkit step by step.

## v0.1 — Public Framework

- [x] Define family-aware evolutionary alpha mining framework
- [x] Add sanitized README
- [x] Add dependency list
- [x] Add privacy-oriented `.gitignore`
- [x] Add public contribution boundary

## v0.2 — Toy Demonstration

- [x] Add synthetic symbolic-alpha dataset
- [x] Implement expression normalization
- [x] Implement seed-family hashing
- [x] Implement diverse A-B parent sampling
- [x] Add simple mutation and hybridization templates
- [x] Add fake simulation/evaluation loop
- [ ] Add lightweight tests for deterministic behavior

## v0.3 — Feedback-Guided Search

- [ ] Add feedback memory
- [ ] Track failure reasons
- [ ] Downweight duplicated or failed families
- [ ] Visualize search history
- [ ] Compare against random formula generation
- [ ] Export search-round summaries as CSV or JSON

## v0.4 — Research Notebook

- [ ] Add reproducible toy notebook
- [ ] Add diagrams
- [ ] Add experiment summary
- [ ] Add limitations and future directions

## v0.5 — Modular Toolkit

- [ ] Split demo logic into reusable modules
- [ ] Add expression parser abstraction
- [ ] Add mutation-template registry
- [ ] Add pluggable evaluator interface
- [ ] Add minimal CLI for toy experiments
