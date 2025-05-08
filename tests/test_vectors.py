import math
import numpy as np
import pytest
from wame.vector import FloatVector2, FloatVector3, IntVector2, IntVector3

# Creation & Initialization
def test_vector_creation():
    assert FloatVector2(3.0, 4.0) == FloatVector2(3.0, 4.0)
    assert IntVector2(3, 4) == IntVector2(3, 4)
    assert FloatVector3(3.0, 4.0, 5.0) == FloatVector3(3.0, 4.0, 5.0)
    assert IntVector3(3, 4, 5) == IntVector3(3, 4, 5)

# Add
def test_vector_addition():
    assert FloatVector2(1, 2) + FloatVector2(3, 4) == FloatVector2(4, 6)
    assert IntVector2(1, 2) + IntVector2(3, 4) == IntVector2(4, 6)
    assert FloatVector3(1, 2, 3) + FloatVector3(4, 5, 6) == FloatVector3(5, 7, 9)
    assert IntVector3(1, 2, 3) + IntVector3(4, 5, 6) == IntVector3(5, 7, 9)

# Subtract
def test_vector_subtraction():
    assert FloatVector2(1, 2) - FloatVector2(3, 4) == FloatVector2(-2, -2)
    assert IntVector2(3, 4) - IntVector2(1, 2) == IntVector2(2, 2)
    assert FloatVector3(4, 5, 6) - FloatVector3(1, 2, 3) == FloatVector3(3, 3, 3)
    assert IntVector3(4, 5, 6) - IntVector3(1, 2, 3) == IntVector3(3, 3, 3)

# Multiplication & Division
def test_scalar_multiplication_and_division():
    assert FloatVector2(1, 2) * 5 == FloatVector2(5, 10)
    assert IntVector2(1, 2) * 5 == IntVector2(5, 10)
    assert FloatVector3(1, 2, 3) * 5 == FloatVector3(5, 10, 15)
    assert IntVector3(1, 2, 3) * 5 == IntVector3(5, 10, 15)

    assert FloatVector2(10, 20) / 5 == FloatVector2(2, 4)
    assert IntVector2(10, 20) / 5 == FloatVector2(2.0, 4.0)
    assert FloatVector3(10, 20, 30) / 5 == FloatVector3(2, 4, 6)
    assert IntVector3(10, 20, 30) / 5 == FloatVector3(2.0, 4.0, 6.0)

    assert FloatVector2(10, 20) // 5 == FloatVector2(2, 4)
    assert IntVector2(10, 20) // 5 == IntVector2(2, 4)
    assert FloatVector3(10, 20, 30) // 5 == FloatVector3(2, 4, 6)
    assert IntVector3(10, 20, 30) // 5 == IntVector3(2, 4, 6)

# Magnitude / Normalize
def test_magnitude_and_normalization():
    assert FloatVector2(3, 4).magnitude() == 5
    assert IntVector2(3, 4).magnitude() == 5

    fn = FloatVector2(3.0, 4.0).normalize()
    assert abs(fn.magnitude() - 1.0) < 1e-9
    in_ = IntVector2(3, 4).normalize()
    assert abs(in_.magnitude() - 1.0) < 1e-9

    with pytest.raises(ZeroDivisionError):
        FloatVector2(0.0, 0.0).normalize()

# Dot / Cross
def test_dot_product():
    assert FloatVector2(1, 2).dot(FloatVector2(3, 4)) == 11
    assert IntVector2(1, 2).dot(IntVector2(3, 4)) == 11
    assert FloatVector3(1, 2, 3).dot(FloatVector3(4, 5, 6)) == 32
    assert IntVector3(1, 2, 3).dot(IntVector3(4, 5, 6)) == 32

def test_cross_product():
    a = FloatVector3(1, 0, 0)
    b = FloatVector3(0, 1, 0)
    c = a.cross(b)
    assert c == FloatVector3(0, 0, 1)

    ai = IntVector3(1, 0, 0)
    bi = IntVector3(0, 1, 0)
    ci = ai.cross(bi)
    assert ci == IntVector3(0, 0, 1)

# Type Errors
def test_invalid_initialization():
    with pytest.raises(ValueError):
        FloatVector2("h", 2)
    with pytest.raises(ValueError):
        IntVector2("i", 3.0)
    with pytest.raises(ValueError):
        FloatVector3("h", "i", 3)
    with pytest.raises(ValueError):
        IntVector3("l", 0.1, "l")

def test_invalid_operations():
    with pytest.raises(TypeError):
        _ = FloatVector2(1, 2) + "bad"
    with pytest.raises(TypeError):
        _ = IntVector2(1, 2) + "bad"
    with pytest.raises(TypeError):
        _ = FloatVector3(1, 2, 3) + "bad"
    with pytest.raises(TypeError):
        _ = IntVector3(1, 2, 3) + "bad"

# Edge & NumPy Support
def test_close_and_numpy():
    a = FloatVector2(0.3000000001, 0.4)
    b = FloatVector2(0.3, 0.4)
    assert math.isclose(a.x, b.x, rel_tol=1e-8)
    np.testing.assert_array_equal(FloatVector3(1, 2, 3)._array, np.array([1.0, 2.0, 3.0]))

def test_nan_and_inf():
    a = FloatVector2(float("nan"), 1.0)
    b = FloatVector2(float("inf"), 1.0)
    assert math.isnan(a.x)
    assert math.isinf(b.x)