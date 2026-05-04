\# Evolutionary Alpha Miner



A research prototype for formulaic alpha discovery using evolutionary computation and LLM-guided hybridization.



\## Core Idea



This project explores a family-aware alpha mining workflow:



1\. Collect historical alpha candidates.

2\. Normalize expressions and cluster them into seed families.

3\. Avoid near-duplicate parents by selecting representative seeds.

4\. Construct heterogeneous A-B parent pairs:

&#x20;  - A = main signal carrier

&#x20;  - B = gate, regime condition, or correlation breaker

5\. Generate candidate expressions under constraints.

6\. Validate expressions locally.

7\. Evaluate candidates through simulation and submission checks.

8\. Feed back pass/fail information into the next search round.



\## Method



The workflow is inspired by:



\- Genetic Programming

\- Symbolic Regression

\- Evolutionary Computation

\- Program Synthesis

\- Active Learning

\- Automated Alpha Discovery



The key design is constrained hybridization rather than unrestricted formula enumeration.



```text

seed family cleaning

→ heterogeneous parent pairing

→ constrained candidate generation

→ simulation/check feedback

→ next-round search

