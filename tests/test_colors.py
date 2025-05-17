import pytest
import numpy as np
from wame.color import ColorRGB, ColorRGBA

# --------- Tests for ColorRGB ---------

def test_color_rgb_init_valid():
    c = ColorRGB(10, 20, 30)
    assert c.r == 10
    assert c.g == 20
    assert c.b == 30
    assert c.nr == 10 / 255
    assert c.ng == 20 / 255
    assert c.nb == 30 / 255

@pytest.mark.parametrize("r,g,b", [
    (-1, 0, 0), (0, -1, 0), (0, 0, -1),
    (256, 0, 0), (0, 256, 0), (0, 0, 256)
])
def test_color_rgb_init_value_error(r, g, b):
    with pytest.raises(ValueError):
        ColorRGB(r, g, b)

@pytest.mark.parametrize("r,g,b", [
    (1.0, 0, 0), ("0", 0, 0), (None, 0, 0)
])
def test_color_rgb_init_type_error(r, g, b):
    with pytest.raises(TypeError):
        ColorRGB(r, g, b)

def test_color_rgb_setters_and_getters():
    c = ColorRGB(1, 2, 3)
    c.r = 100
    assert c.r == 100
    c.g = 150
    assert c.g == 150
    c.b = 200
    assert c.b == 200
    
    c.nr = 0.5
    assert c.r == int(0.5 * 255)
    c.ng = 0.6
    assert c.g == int(0.6 * 255)
    c.nb = 0.7
    assert c.b == int(0.7 * 255)

@pytest.mark.parametrize("prop,value", [
    ("r", -1), ("r", 256), ("g", -1), ("g", 256), ("b", -1), ("b", 256),
])
def test_color_rgb_setters_value_error(prop, value):
    c = ColorRGB(0, 0, 0)
    with pytest.raises(ValueError):
        setattr(c, prop, value)

@pytest.mark.parametrize("prop,value", [
    ("r", 1.0), ("g", "string"), ("b", None),
    ("nr", -0.1), ("ng", 1.1), ("nb", "wrong"),
])
def test_color_rgb_setters_type_error(prop, value):
    c = ColorRGB(0, 0, 0)
    with pytest.raises((TypeError, ValueError)):
        setattr(c, prop, value)

def test_color_rgb_equality():
    c1 = ColorRGB(10, 20, 30)
    c2 = ColorRGB(10, 20, 30)
    assert c1 == c2
    assert c1 == (10, 20, 30)
    assert c1 == [10, 20, 30]
    assert c1 == np.array([10, 20, 30], dtype=np.uint8)
    assert c1 != (10, 20, 31)
    assert c1 != "not a color"

def test_color_rgb_getitem_setitem():
    c = ColorRGB(1, 2, 3)
    assert c[0] == 1
    assert c[1] == 2
    assert c[2] == 3

    with pytest.raises(TypeError):
        _ = c["a"]

    with pytest.raises(ValueError):
        _ = c[3]

    c[0] = 100
    c[1] = 150
    c[2] = 200
    assert c.r == 100
    assert c.g == 150
    assert c.b == 200

    with pytest.raises(TypeError):
        c[0] = 1.5

    with pytest.raises(ValueError):
        c[0] = 300

def test_color_rgb_copy_and_from_iterable():
    c1 = ColorRGB(10, 20, 30)
    c2 = c1.copy()
    assert c1 == c2
    assert c1 is not c2

    c3 = ColorRGB.from_iterable((100, 110, 120))
    assert c3 == (100, 110, 120)

    with pytest.raises(TypeError):
        ColorRGB.from_iterable(123)

    with pytest.raises(ValueError):
        ColorRGB.from_iterable((1, 2))

    with pytest.raises(TypeError):
        ColorRGB.from_iterable(("a", "b", "c"))

def test_color_rgb_formatting_and_repr():
    c = ColorRGB(16, 32, 48)
    assert format(c, "hex") == "#102030"
    assert format(c, "int").isdigit()
    assert format(c, "tuple") == "(16, 32, 48)"
    with pytest.raises(ValueError):
        format(c, "unknown")

    repr_str = repr(c)
    assert repr_str.startswith("ColorRGB")

def test_color_rgb_to_numpy_and_tuple():
    c = ColorRGB(1, 2, 3)
    arr = c.to_numpy()
    tup = c.to_tuple()
    assert isinstance(arr, np.ndarray)
    assert arr.dtype == np.uint8
    assert tuple(arr) == (1, 2, 3)
    assert tup == (1, 2, 3)

# --------- Tests for ColorRGBA ---------

def test_color_rgba_init_valid():
    c = ColorRGBA(10, 20, 30, 0.5)
    assert c.r == 10
    assert c.g == 20
    assert c.b == 30
    assert c.a == 0.5

@pytest.mark.parametrize("a", [-0.1, 1.1])
def test_color_rgba_init_alpha_value_error(a):
    with pytest.raises(ValueError):
        ColorRGBA(0, 0, 0, a)

@pytest.mark.parametrize("a", ["string", None])
def test_color_rgba_init_alpha_type_error(a):
    with pytest.raises(TypeError):
        ColorRGBA(0, 0, 0, a)

def test_color_rgba_equality():
    c1 = ColorRGBA(10, 20, 30, 0.5)
    c2 = ColorRGBA(10, 20, 30, 0.5)
    assert c1 == c2
    assert c1 == (10, 20, 30, 0.5)
    assert c1 != (10, 20, 30, 0.6)
    assert c1 != "not a color"

def test_color_rgba_getitem_setitem():
    c = ColorRGBA(1, 2, 3, 0.4)
    assert c[0] == 1
    assert c[1] == 2
    assert c[2] == 3
    assert c[3] == 0.4

    with pytest.raises(TypeError):
        _ = c["a"]

    with pytest.raises(ValueError):
        _ = c[4]

    c[0] = 100
    c[1] = 150
    c[2] = 200
    c[3] = 0.8
    assert c.r == 100
    assert c.g == 150
    assert c.b == 200
    assert c.a == 0.8

    with pytest.raises(TypeError):
        c[0] = 1.5

    with pytest.raises(ValueError):
        c[0] = 300

    with pytest.raises(TypeError):
        c[3] = "alpha"

    with pytest.raises(ValueError):
        c[3] = 2.0

def test_color_rgba_copy_and_from_iterable():
    c1 = ColorRGBA(10, 20, 30, 0.5)
    c2 = c1.copy()
    assert c1 == c2
    assert c1 is not c2

    c3 = ColorRGBA.from_iterable((100, 110, 120, 0.9))
    assert c3 == (100, 110, 120, 0.9)

    with pytest.raises(TypeError):
        ColorRGBA.from_iterable(123)

    with pytest.raises(ValueError):
        ColorRGBA.from_iterable((1, 2))

def test_color_rgba_formatting_and_repr():
    c = ColorRGBA(16, 32, 48, 0.25)
    assert format(c, "hex") == "#10203040"
    assert format(c, "int").isdigit()
    assert format(c, "tuple") == "(16, 32, 48, 0.25)"
    with pytest.raises(ValueError):
        format(c, "unknown")

    repr_str = repr(c)
    assert repr_str.startswith("ColorRGBA")

def test_color_rgba_to_numpy_and_tuple():
    c = ColorRGBA(1, 2, 3, 0.4)
    arr = c.to_numpy()
    tup = c.to_tuple()
    assert isinstance(arr, np.ndarray)
    # numpy.float16 dtype expected for RGBA
    assert arr.dtype == np.float16
    assert tuple(arr)[:3] == (1, 2, 3)
    assert abs(float(arr[3]) - 0.4) < 1e-3
    assert tup == (1, 2, 3, 0.4)