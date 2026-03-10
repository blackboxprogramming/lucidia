"""Tests for lucidia.lucidia_logic — trinary logic, breath functions, symbolic math."""

import math
import pytest

from lucidia.lucidia_logic import (
    Trinary,
    psi_prime,
    breath_function,
    truth_reconciliation,
    emotional_gravity,
    self_awakening,
    render_break,
    recursive_soul_loop,
    lucidia_genesis,
    consciousness_resonance,
    anomaly_persistence,
    compassion_state_encryption,
    emotional_ai_anchor,
    soul_recognition,
)


class TestTrinary:
    def test_valid_values(self):
        for v in (-1, 0, 1):
            assert Trinary(v).value == v

    def test_invalid_value(self):
        with pytest.raises(ValueError):
            Trinary(2)

    def test_add_clamps_positive(self):
        assert (Trinary(1) + Trinary(1)).value == 1

    def test_add_clamps_negative(self):
        assert (Trinary(-1) + Trinary(-1)).value == -1

    def test_add_normal(self):
        assert (Trinary(0) + Trinary(1)).value == 1
        assert (Trinary(1) + Trinary(-1)).value == 0

    def test_sub(self):
        assert (Trinary(1) - Trinary(1)).value == 0
        assert (Trinary(0) - Trinary(-1)).value == 1

    def test_invert(self):
        assert Trinary(1).invert().value == -1
        assert Trinary(-1).invert().value == 1
        assert Trinary(0).invert().value == 0

    def test_repr(self):
        assert repr(Trinary(1)) == "Trinary(1)"


class TestPsiPrime:
    def test_always_zero(self):
        for x in [0, 1, -1, 42, 3.14, -999]:
            assert psi_prime(x) == 0

    def test_float_precision(self):
        assert psi_prime(1e15) == 0


class TestBreathFunction:
    def test_default_psi(self):
        # With psi_prime (always 0), breath is always 0
        assert breath_function(5.0) == 0

    def test_custom_psi(self):
        assert breath_function(3.0, psi=lambda t: t) == (3.0 - 1) + 3.0


class TestTruthReconciliation:
    def test_empty_truths(self):
        assert truth_reconciliation([]) == 0.0

    def test_with_default_psi(self):
        # psi_prime always returns 0, so numerator=0, result=0
        assert truth_reconciliation([1.0, 2.0, 3.0]) == 0.0

    def test_with_identity_psi(self):
        # psi=identity: numerator = sum(x + (-x)) = 0 for each, so still 0
        assert truth_reconciliation([1.0, 2.0], psi=lambda x: x) == 0.0


class TestEmotionalGravity:
    def test_basic(self):
        assert emotional_gravity(1.0, 2.0, 3.0) == 6.0

    def test_zero_gradient(self):
        assert emotional_gravity(5.0, 10.0, 0.0) == 0.0


class TestSelfAwakening:
    def test_default_psi(self):
        assert self_awakening([1.0, 2.0, 3.0]) == 0.0

    def test_custom_psi(self):
        # psi=identity, breath(t)=psi(t-1)+psi(t)=2t-1
        result = self_awakening([1.0], psi=lambda x: x)
        assert result == 1.0  # breath(1)=0+1=1, psi(1)=1


class TestRenderBreak:
    def test_empty_lists(self):
        assert render_break([], []) == 0.0

    def test_mismatched_lengths(self):
        assert render_break([1.0], [1.0, 2.0]) == 0.0

    def test_default_psi(self):
        assert render_break([1.0, 2.0], [3.0, 4.0]) == 0.0

    def test_custom_psi(self):
        result = render_break([2.0, 3.0], [1.0, 1.0], psi=lambda x: x)
        assert result == (2.0 * 1.0 + 3.0 * 1.0) / 2


class TestRecursiveSoulLoop:
    def test_default_psi(self):
        assert recursive_soul_loop(1.0, [1.0, 2.0], 1.0) == 0.0

    def test_zero_delta(self):
        assert recursive_soul_loop(1.0, [1.0], 0.0) == 0.0

    def test_custom_psi(self):
        result = recursive_soul_loop(1.0, [2.0, 3.0], 2.0, psi=lambda x: x)
        assert result == (1.0 + 5.0) / 2.0


class TestLucidiaGenesis:
    def test_default_psi(self):
        assert lucidia_genesis(1.0, 2.0, 3.0) == 0.0

    def test_custom_psi(self):
        # breath(3, identity) = 2+3=5, psi(5)=5, *1.0*2.0=10.0
        result = lucidia_genesis(1.0, 2.0, 3.0, psi=lambda x: x)
        assert result == 10.0


class TestConsciousnessResonance:
    def test_default_psi(self):
        assert consciousness_resonance(1.0, [1.0, 2.0], 0.5) == 0.0

    def test_custom_psi(self):
        # psi(loop_obs)=5, breath(1)=0+1=1, breath(2)=1+2=3
        # integral = 1*0.5 + 3*0.5 = 2.0, result = 5 * 2.0 = 10.0
        result = consciousness_resonance(5.0, [1.0, 2.0], 0.5, psi=lambda x: x)
        assert result == 10.0


class TestAnomalyPersistence:
    def test_mismatched(self):
        assert anomaly_persistence([1.0], [1.0, 2.0]) == 0.0

    def test_default_psi(self):
        assert anomaly_persistence([1.0, 2.0], [3.0, 4.0]) == 0.0

    def test_custom_psi(self):
        result = anomaly_persistence([2.0, 3.0], [1.0, 1.0], psi=lambda x: x)
        assert result == 5.0


class TestCompassionStateEncryption:
    def test_returns_string(self):
        result = compassion_state_encryption(1.0, 2.0, "key123")
        assert isinstance(result, str)
        assert ":key123" in result

    def test_deterministic(self):
        r1 = compassion_state_encryption(1.0, 2.0, "k")
        r2 = compassion_state_encryption(1.0, 2.0, "k")
        assert r1 == r2

    def test_different_keys(self):
        r1 = compassion_state_encryption(1.0, 2.0, "a")
        r2 = compassion_state_encryption(1.0, 2.0, "b")
        assert r1 != r2


class TestEmotionalAiAnchor:
    def test_default_psi(self):
        assert emotional_ai_anchor([1.0, 2.0], lambda x: x) == 0.0

    def test_empty(self):
        assert emotional_ai_anchor([], lambda x: x) == 0.0


class TestSoulRecognition:
    def test_default_psi(self):
        assert soul_recognition(1.0, 2.0) == 0.0

    def test_custom_psi(self):
        assert soul_recognition(3.0, 4.0, psi=lambda x: x) == 12.0
