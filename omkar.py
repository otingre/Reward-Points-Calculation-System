from copy import deepcopy
from collections import defaultdict

transactions = {
    "T1": {"merchant_code": "sportcheck", "amount_cents": 21000},
    "T2": {"merchant_code": "sportcheck", "amount_cents": 8700},
    "T3": {"merchant_code": "tim_hortons", "amount_cents": 323},
    "T4": {"merchant_code": "tim_hortons", "amount_cents": 1267},
    "T5": {"merchant_code": "tim_hortons", "amount_cents": 2116},
    "T6": {"merchant_code": "tim_hortons", "amount_cents": 2211},
    "T7": {"merchant_code": "subway", "amount_cents": 1853},
    "T8": {"merchant_code": "subway", "amount_cents": 2153},
    "T9": {"merchant_code": "sportcheck", "amount_cents": 7326},
    "T10": {"merchant_code": "tim_hortons", "amount_cents": 1321},
}

rules = {
    "R1": {
        "points": 500,
        "criteria": {"sportcheck": 75, "tim_hortons": 25, "subway": 25},
    },
    "R2": {"points": 300, "criteria": {"sportcheck": 75, "tim_hortons": 25}},
    "R3": {"points": 200, "criteria": {"sportcheck": 75}},
    "R4": {
        "points": 150,
        "criteria": {"sportcheck": 25, "tim_hortons": 10, "subway": 10},
    },
    "R5": {"points": 75, "criteria": {"sportcheck": 25, "tim_hortons": 10}},
    "R6": {"points": 75, "criteria": {"sportcheck": 20}},
    "R7": {"points": 1, "criteria": None},
}


def aggregate(transactions):
    agg_tx = defaultdict(int)
    for tx in transactions.values():
        agg_tx[tx["merchant_code"]] += tx["amount_cents"]
    return {
        f"T{i}": {"merchant_code": m, "amount_cents": a // 100} for i, (m, a) in enumerate(agg_tx.items(), 1)
    }


def points_with_rule(rule, transactions, deduct=False):
    if rule["criteria"] is None:
        return sum([tx["amount_cents"] * rule["points"] for tx in transactions.values()])
    mm = {m: 0 for m in rule["criteria"]}  # multiplier per merchant
    for tx in transactions.values():
        if tx["merchant_code"] in rule["criteria"]:
            mm[tx["merchant_code"]] = tx["amount_cents"] // rule["criteria"][tx["merchant_code"]]
    mm_min = min(mm.values())
    if deduct:  # deduct the points consumed
        for t in transactions.values():
            if t["merchant_code"] in rule["criteria"]:
                t["amount_cents"] -= mm_min * rule["criteria"][t["merchant_code"]]
    return mm_min * rule["points"]


def rank_rules(rules, transactions, truncate=False):
    rule_pts = {}
    for k, v in rules.items():
        merchant_code = points_with_rule(v, transactions)
        rule_pts[k] = merchant_code
    sorted_rule_pts = sorted(rule_pts.items(), key=lambda b: b[1], reverse=True)
    if truncate:  # remove rules that give zero points
        sorted_rule_pts = [rp for rp in sorted_rule_pts if rp[1] > 0]
    return sorted_rule_pts


def sort_rules(rules):
    sorted_rules = {}
    for rule, _ in rank_rules(rules, transactions, truncate=True):
        sorted_rules[rule] = rules[rule]
    return sorted_rules


def get_total(transactions, rule_num=1):
    if rule_num not in rule_map:
        return 0
    if sum([t["amount_cents"] for t in transactions.values()]) == 0:
        return 0
    rule = rule_map[rule_num]
    r_take = deepcopy(transactions)  # include rule
    r_not = deepcopy(transactions)  # dont
    return max(
        get_total(r_not, rule_num + 1),
        points_with_rule(rules[rule], r_take, deduct=True)
        + get_total(r_take, rule_num + 1),
    )


transactions = aggregate(transactions)
rules = sort_rules(rules)
print(transactions)
rule_map = {i: r for i, r in enumerate(rules.keys(), 1)}

print(get_total(transactions))
