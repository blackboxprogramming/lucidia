"""Substrate performance optimizer — selects optimal compute substrate."""


def optimize_substrate_selection(
    task: dict,
    energy_costs: dict,
    time_costs: dict,
    switching_costs: dict,
    lambda_weight: float = 0.5,
) -> tuple:
    """Select the substrate with the lowest weighted cost.

    cost = energy * time * (1 + lambda_weight * switching_cost)
    """
    best_name = None
    best_cost = float("inf")

    for name in energy_costs:
        e = energy_costs[name]
        t = time_costs[name]
        s = switching_costs[name]
        cost = e * t * (1 + lambda_weight * s)
        if cost < best_cost:
            best_cost = cost
            best_name = name

    return (best_name, float(best_cost))
