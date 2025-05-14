# Vectors
Game engines usually include 2D/3D vector array objects that developers can interact with. `Wame` is no different.
- Vectors are created to simplify access and math that is usually associated with XY, XYZ, etc. coordinates.
- All of these vector objects are able to add and subtract from each other, even with regular `tuple` objects or `numpy` arrays of the same dimension. Vectors are natively hashable and can be compared to one another.

As vectors sit right now, these objects are mostly unnecessary for developers to use, as they are provided by the engine internally. If you wish to use vectors with optimized arithmetic, consider using commonly used modules supported by `3D` libraries like `OpenGL`.

## 2D Vectors
Defined in the `wame.vector.xy` program:
- `FloatVector2`: Stores `x` and `y` internally, but can be `int` or `float`. This is generally recommended for 2D game scenes, not UI (as it's pixel/integer based).
- `IntVector2`: Similar to `FloatVector2` but can only be `int`. This is generally recommended for 2D game UIs.

## 3D Vectors
Defined in the `wame.vector.xyz` program:
- `FloatVector3`: Stores `x`, `y`, and `z` internally, but can be `int` or `float`. This is generally recommended for 3D game scenes; the `Z` parameter is useless in UI-contexts.
- `IntVector3`: Similar to `FloatVector3` but can only be `int`.

These 3D vectors come with special methods, like `normalize` and `cross`, which are frequently necessary when developing 3D games, especially with `OpenGL`.

## Example Programs
```python
# Adding/Subtracting Two Vectors
vector1: IntVector2 = IntVector2(1, 1)
vector2: IntVector2 = IntVector2(1, 1)
vector3: IntVector2 = vector1 + vector2
vector4: IntVector2 = vector1 - vector2

print(vector3.x, vector3.y)
print(vector4.x, vector4.y)

# Vectors can also be directly printed if needed
print(vector1)
```
```
>>> 2 2
>>> 0 0
>>> X: 1, Y: 1
```
```python
# Generating Vectors from Tuples
vector1: IntVector2 = IntVector2.from_iterable((1, 1))
vector2: IntVector2 = IntVector2.from_iterable((1000, -1))

print(vector1.x, vector1.y)
print(vector2.x, vector2.y)

# And exporting to tuples and `numpy` arrays
tuple_: tuple[int, int] = vector1.to_tuple()
array: numpy.ndarray[numpy.int32] = vector2.to_numpy()

print(tuple_)
print(array)
```
```
>>> 1 1
>>> 1000 -1
>>> (1, 1)
>>> [1000, -1]
```