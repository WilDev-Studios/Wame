# Utilities
Contains commonly used functionality that many developers would need at some point. `Wame` takes care of this for you.

## Keys
Defined in `wame.utils.keys`:
- `KEYS`: A `keycode: modifiers` (`KC: MOD`) mapping of keyboard keys.
- Conditional Methods:
    - `is_char`: Checks if the provided `KC: MOD` mapping equates to a character on the common `WASD` keyboard.
    - `is_letter`: Checks if the provided `KC: MOD` mapping equates to any (lower, upper)case letter.
    - `is_lower`: Checks if the provided `KC: MOD` mapping equates to a lowercase letter.
    - `is_number`: Checks if the provided `KC: MOD` mapping equates to a number.
    - `is_symbol`: Checks if the provided `KC: MOD` mapping equates to a symbol (non-letter/number) character.
    - `is_upper`: Checks if the provided `KC: MOD` mapping equates to a uppercase letter.

The `KEYS` mapping is particularly helpful with text input. It takes any `keycode: modifiers` combination and returns the appropriate, correct character typed, without unnecessary, bloated `if` or `match` statements.

## OTHER FEATURES
Defined in `wame.utils._____`:
- ...

## Example Programs
```python
# Check if the character typed equals uppercase a ('A')
# Provided keycode: int, modifiers: int

# Old, bloated method
return keycode == pygame.K_a and modifiers in (pygame.KMOD_SHIFT, pygame.KMOD_CAPS)

# Better, easy method
return KEYS[(keycode, modifiers)] == 'A'
```
```python
# If you are trying to figure out which key was typed
if keycode == pygame.K_a and modifiers in (pygame.KMOD_SHIFT, pygame.KMOD_CAPS):
    return 'A'
elif keycode == pygame.K_a and modifiers == pygame.KMOD_NONE:
    return 'a'
elif keycode == pygame.K_b and modifiers in (pygame.KMOD_SHIFT, pygame.KMOD_CAPS):
    return 'B'
# etc. etc.

# Just do this:
return KEYS[(keycode, modifiers)]
# Just be aware, if it doesn't exist on the common `WASD` keyboard, you will get a `KeyError`, so keep it in mind
```
```python
# Check if the key is an uppercase letter
return is_upper(keycode, modifiers)

# Check if the key is a symbol
return is_symbol(keycode, modifiers)

# Etc.
```