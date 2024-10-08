import pytest
import itg.utils.math as itg_math


def test_swsh():
    """Test spin_weighted_spherical_harmonics function"""
    assert itg_math.spin_weighted_spherical_harmonics(2, 2, 0.0, 0.0) == pytest.approx(
        0.6307831305050401 + 0j
    )
