"""
Toy demo for Evolutionary Alpha Miner.

This file uses synthetic symbolic expressions and a fake evaluator.
It does NOT contain real alpha expressions, real platform APIs, credentials,
or proprietary data.

Goal:
    Demonstrate the core workflow:

    seed family cleaning
    -> diverse A-B parent pairing
    -> constrained hybrid generation
    -> fake simulation feedback
    -> next-round summary
"""

from __future__ import annotations

import hashlib
import random
import re
from dataclasses import dataclass
from typing import Dict, List, Tuple

import pandas as pd


# ---------------------------------------------------------------------
# 1. Synthetic seed pool
# ---------------------------------------------------------------------

SEED_POOL = [
    ("price", "rank(ts_delta(close, 5))"),
    ("price", "rank(close / open - 1)"),
    ("price", "ts_rank(returns, 20)"),
    ("price", "rank(vwap - close)"),
    ("price", "ts_zscore(close / ts_mean(close, 20), 20)"),
    ("volume", "rank(volume / ts_mean(volume, 20))"),
    ("volume", "ts_rank(volume, 10)"),
    ("volume", "rank(adv20 / volume)"),
    ("volume", "ts_zscore(volume, 30)"),
    ("option", "rank(implied_volatility_call_120 - implied_volatility_put_120)"),
    ("option", "ts_rank(implied_volatility_call_120, 20)"),
    ("option", "rank(implied_volatility_put_120 / implied_volatility_call_120)"),
    ("fundamental", "rank(cashflow / assets)"),
    ("fundamental", "rank(sales / assets)"),
    ("fundamental", "rank(income / liabilities)"),
    ("analyst", "rank(analyst_estimate_revision)"),
    ("analyst", "ts_rank(analyst_recommendation_change, 60)"),
    ("news", "rank(news_sentiment_score)"),
    ("news", "ts_mean(news_buzz, 10)"),
    ("unknown", "rank(custom_dataset_signal)"),
]


@dataclass
class Seed:
    seed_id: str
    tag: str
    expression: str
    family_hash: str
    score: float


@dataclass
class Pair:
    pair_id: str
    a: Seed
    b: Seed
    tag_pair: str


# ---------------------------------------------------------------------
# 2. Expression normalization and family hashing
# ---------------------------------------------------------------------

def normalize_expression(expr: str) -> str:
    """Normalize expression text to reduce superficial duplicates."""
    expr = expr.lower().strip()
    expr = re.sub(r"\s+", "", expr)
    expr = re.sub(r"\d+\.\d+|\d+", "N", expr)
    return expr


def short_hash(text: str, length: int = 10) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:length]


def family_hash(expr: str) -> str:
    return short_hash(normalize_expression(expr))


def build_seed_pool(raw_pool: List[Tuple[str, str]], random_seed: int = 7) -> List[Seed]:
    """Build a synthetic seed pool with fake prior scores."""
    random.seed(random_seed)

    seeds: List[Seed] = []
    seen_families = set()

    for idx, (tag, expr) in enumerate(raw_pool, start=1):
        fh = family_hash(expr)

        if fh in seen_families:
            continue

        seen_families.add(fh)

        # Fake historical quality score.
        # In a real system this could come from prior Sharpe/Fitness/pass-rate.
        base = {
            "price": 1.00,
            "volume": 0.90,
            "option": 0.75,
            "fundamental": 0.70,
            "analyst": 0.55,
            "news": 0.50,
            "unknown": 0.40,
        }.get(tag, 0.40)

        score = base + random.random() * 0.60

        seeds.append(
            Seed(
                seed_id=f"S{idx:03d}",
                tag=tag,
                expression=expr,
                family_hash=fh,
                score=round(score, 4),
            )
        )

    return seeds


# ---------------------------------------------------------------------
# 3. Diverse A-B parent sampling
# ---------------------------------------------------------------------

TAG_PAIR_TARGETS = [
    ("price", "volume"),
    ("volume", "price"),
    ("price", "option"),
    ("option", "price"),
    ("price", "fundamental"),
    ("fundamental", "price"),
    ("volume", "option"),
    ("option", "volume"),
    ("volume", "fundamental"),
    ("fundamental", "volume"),
    ("news", "price"),
    ("analyst", "price"),
    ("unknown", "price"),
]


def sample_diverse_pairs(seeds: List[Seed], n_pairs: int = 16, random_seed: int = 11) -> List[Pair]:
    """
    Sample diverse A-B pairs.

    Constraints:
        - A and B must come from different seed families.
        - Prefer heterogeneous tag pairs.
        - Avoid reusing the same parent too often.
    """
    random.seed(random_seed)

    by_tag: Dict[str, List[Seed]] = {}
    for seed in seeds:
        by_tag.setdefault(seed.tag, []).append(seed)

    for tag in by_tag:
        by_tag[tag] = sorted(by_tag[tag], key=lambda x: x.score, reverse=True)

    pairs: List[Pair] = []
    used_pair_hashes = set()
    parent_usage: Dict[str, int] = {}

    def pick_from_tag(tag: str, excluded: set[str]) -> Seed | None:
        candidates = [
            s for s in by_tag.get(tag, [])
            if s.family_hash not in excluded
        ]
        if not candidates:
            return None

        weights = [
            max(0.05, s.score) / (1 + parent_usage.get(s.family_hash, 0))
            for s in candidates
        ]

        return random.choices(candidates, weights=weights, k=1)[0]

    attempts = 0

    while len(pairs) < n_pairs and attempts < 1000:
        attempts += 1

        a_tag, b_tag = TAG_PAIR_TARGETS[len(pairs) % len(TAG_PAIR_TARGETS)]

        a = pick_from_tag(a_tag, excluded=set())
        if a is None:
            continue

        b = pick_from_tag(b_tag, excluded={a.family_hash})
        if b is None:
            continue

        pair_hash = short_hash(a.family_hash + "::" + b.family_hash, 12)

        if pair_hash in used_pair_hashes:
            continue

        used_pair_hashes.add(pair_hash)
        parent_usage[a.family_hash] = parent_usage.get(a.family_hash, 0) + 1
        parent_usage[b.family_hash] = parent_usage.get(b.family_hash, 0) + 1

        pairs.append(
            Pair(
                pair_id=f"P{len(pairs) + 1:04d}_{pair_hash}",
                a=a,
                b=b,
                tag_pair=f"{a.tag}+{b.tag}",
            )
        )

    return pairs


# ---------------------------------------------------------------------
# 4. Candidate hybrid generation
# ---------------------------------------------------------------------

def generate_candidate(pair: Pair) -> Dict[str, str]:
    """
    Generate a synthetic hybrid formula.

    This mimics the design rule:
        A = main signal carrier
        B = weak gate / regime / correlation breaker
    """
    a = pair.a.expression
    b = pair.b.expression

    templates = [
        {
            "mode": "weak_gate_hybrid",
            "expression": f"trade_when(rank({b}) > 0.55, {a}, -1)",
            "hypothesis": "Use B as a weak gate while preserving A as the main signal.",
        },
        {
            "mode": "regime_hybrid",
            "expression": f"if_else(ts_rank({b}, 20) > 0.5, {a}, 0.5 * {a})",
            "hypothesis": "Use B as a regime condition to reduce unstable exposure.",
        },
        {
            "mode": "mild_corr_breaker",
            "expression": f"group_neutralize({a} * (1 + 0.1 * rank({b})), sector)",
            "hypothesis": "Use B as a mild modifier to break correlation without destroying A.",
        },
        {
            "mode": "dataset_substitution",
            "expression": f"rank({a}) + 0.05 * rank({b})",
            "hypothesis": "Add a small heterogeneous component from B.",
        },
    ]

    selected = random.choice(templates)

    return {
        "candidate_name": f"C_{pair.pair_id}",
        "pair_id": pair.pair_id,
        "tag_pair": pair.tag_pair,
        "parent_a": pair.a.seed_id,
        "parent_b": pair.b.seed_id,
        "mutation_mode": selected["mode"],
        "candidate_expression": selected["expression"],
        "hypothesis": selected["hypothesis"],
    }


# ---------------------------------------------------------------------
# 5. Fake evaluator
# ---------------------------------------------------------------------

def fake_evaluate(candidate: Dict[str, str], random_seed_offset: int = 0) -> Dict[str, object]:
    """
    Fake evaluation function.

    This is only for demonstrating the feedback loop.
    A real system would replace this with external simulation/check results.
    """
    random.seed(short_hash(candidate["candidate_expression"]) + str(random_seed_offset))

    tag_pair = candidate["tag_pair"]
    mode = candidate["mutation_mode"]

    base = 0.4

    if "price+volume" in tag_pair or "volume+price" in tag_pair:
        base += 0.30
    if "option" in tag_pair:
        base += 0.25
    if "fundamental" in tag_pair:
        base += 0.18
    if "news" in tag_pair or "analyst" in tag_pair:
        base += 0.12

    if mode in ["weak_gate_hybrid", "regime_hybrid"]:
        base += 0.18
    if mode == "dataset_substitution":
        base -= 0.05

    sharpe = round(random.gauss(base, 0.45), 3)
    fitness = round(sharpe * random.uniform(0.5, 1.8), 3)
    turnover = round(random.uniform(0.02, 0.65), 3)

    failed_checks = []

    if sharpe < 0.75:
        failed_checks.append("LOW_SHARPE")
    if fitness < 0.60:
        failed_checks.append("LOW_FITNESS")
    if turnover > 0.55:
        failed_checks.append("HIGH_TURNOVER")

    # Simulate correlation traps for some overly common combinations.
    if tag_pair in ["price+volume", "volume+price"] and random.random() < 0.20:
        failed_checks.append("SELF_CORRELATION")

    status = "passed" if not failed_checks else "failed"

    return {
        "sharpe": sharpe,
        "fitness": fitness,
        "turnover": turnover,
        "status": status,
        "failed_checks": "; ".join(failed_checks),
    }


# ---------------------------------------------------------------------
# 6. End-to-end demo
# ---------------------------------------------------------------------

def run_demo() -> pd.DataFrame:
    print("Building synthetic seed pool...")
    seeds = build_seed_pool(SEED_POOL)

    seed_df = pd.DataFrame([s.__dict__ for s in seeds])
    print("\nSeed families:")
    print(seed_df[["seed_id", "tag", "family_hash", "score", "expression"]].to_string(index=False))

    print("\nSampling diverse A-B pairs...")
    pairs = sample_diverse_pairs(seeds, n_pairs=18)

    pair_df = pd.DataFrame(
        [
            {
                "pair_id": p.pair_id,
                "tag_pair": p.tag_pair,
                "A": p.a.seed_id,
                "B": p.b.seed_id,
                "A_score": p.a.score,
                "B_score": p.b.score,
            }
            for p in pairs
        ]
    )

    print("\nSelected pairs:")
    print(pair_df.to_string(index=False))

    print("\nGenerating candidates...")
    candidates = [generate_candidate(pair) for pair in pairs]

    print("Evaluating candidates with fake evaluator...")
    rows = []

    for candidate in candidates:
        result = fake_evaluate(candidate)
        rows.append({**candidate, **result})

    result_df = pd.DataFrame(rows)

    print("\nCandidate results:")
    print(
        result_df[
            [
                "candidate_name",
                "tag_pair",
                "mutation_mode",
                "sharpe",
                "fitness",
                "turnover",
                "status",
                "failed_checks",
            ]
        ].to_string(index=False)
    )

    print("\nSummary:")
    print(result_df["status"].value_counts().to_string())

    print("\nFailed checks:")
    failed = result_df[result_df["failed_checks"] != ""]
    if failed.empty:
        print("No failed checks.")
    else:
        print(failed["failed_checks"].value_counts().to_string())

    print("\nBest candidates:")
    print(
        result_df.sort_values(["status", "fitness", "sharpe"], ascending=[False, False, False])
        .head(5)[
            [
                "candidate_name",
                "tag_pair",
                "mutation_mode",
                "sharpe",
                "fitness",
                "turnover",
                "status",
                "candidate_expression",
            ]
        ]
        .to_string(index=False)
    )

    return result_df


if __name__ == "__main__":
    run_demo()
