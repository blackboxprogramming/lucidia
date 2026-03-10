"""Tests for lucidia.substrate_performance_optimizer."""

import pytest

from lucidia.substrate_performance_optimizer import optimize_substrate_selection


class TestOptimizeSubstrateSelection:
    def setup_method(self):
        self.task = {"complexity": 0.9}
        self.energy = {"chemical": 1.2, "quantum": 0.7, "electronic": 1.0}
        self.time = {"chemical": 2.0, "quantum": 1.1, "electronic": 1.3}
        self.switch = {"chemical": 0.4, "quantum": 0.2, "electronic": 0.1}

    def test_selects_lowest_cost(self):
        best, cost = optimize_substrate_selection(
            self.task, self.energy, self.time, self.switch
        )
        assert best == "quantum"

    def test_cost_formula(self):
        _, cost = optimize_substrate_selection(
            self.task, self.energy, self.time, self.switch, lambda_weight=0.5
        )
        expected = 0.7 * 1.1 * (1 + 0.5 * 0.2)
        assert abs(cost - expected) < 1e-10

    def test_lambda_zero_ignores_penalty(self):
        best, cost = optimize_substrate_selection(
            self.task, self.energy, self.time, self.switch, lambda_weight=0.0
        )
        expected = 0.7 * 1.1 * 1.0
        assert abs(cost - expected) < 1e-10

    def test_high_lambda_penalizes_switching(self):
        best, _ = optimize_substrate_selection(
            self.task,
            {"a": 1.0, "b": 1.0},
            {"a": 1.0, "b": 1.0},
            {"a": 0.0, "b": 10.0},
            lambda_weight=1.0,
        )
        assert best == "a"

    def test_single_substrate(self):
        best, cost = optimize_substrate_selection(
            {}, {"only": 2.0}, {"only": 3.0}, {"only": 0.5}, lambda_weight=1.0
        )
        assert best == "only"
        assert abs(cost - 2.0 * 3.0 * 1.5) < 1e-10

    def test_equal_costs_returns_one(self):
        best, _ = optimize_substrate_selection(
            {}, {"a": 1.0, "b": 1.0}, {"a": 1.0, "b": 1.0}, {"a": 0.0, "b": 0.0}
        )
        assert best in ("a", "b")

    def test_returns_tuple(self):
        result = optimize_substrate_selection(
            self.task, self.energy, self.time, self.switch
        )
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], str)
        assert isinstance(result[1], float)
