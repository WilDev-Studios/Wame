import pytest
import pygame

from wame.utils import KEYS, is_char, is_letter, is_upper, is_lower, is_number, is_symbol

@pytest.mark.parametrize("key, mods, expected", [
    (pygame.K_a, pygame.KMOD_NONE, 'a'),
    (pygame.K_a, pygame.KMOD_SHIFT | pygame.KMOD_CAPS, 'A'),
    (pygame.K_1, pygame.KMOD_NONE, '1'),
    (pygame.K_1, pygame.KMOD_SHIFT, '!'),
    (pygame.K_BACKQUOTE, pygame.KMOD_NONE, '`'),
    (pygame.K_BACKQUOTE, pygame.KMOD_SHIFT, '~'),
])
def test_keys_mapping(key, mods, expected):
    assert KEYS.get((key, mods)) == expected

@pytest.mark.parametrize("key, mods, expected", [
    (pygame.K_a, pygame.KMOD_NONE, True),
    (pygame.K_z, pygame.KMOD_SHIFT | pygame.KMOD_CAPS, True),
    (pygame.K_1, pygame.KMOD_NONE, True),
    (pygame.K_1, pygame.KMOD_SHIFT, True),
    (pygame.K_TAB, pygame.KMOD_NONE, False),
])
def test_is_char(key, mods, expected):
    assert is_char(key, mods) == expected

@pytest.mark.parametrize("key, mods, expected", [
    (pygame.K_a, pygame.KMOD_NONE, True),
    (pygame.K_z, pygame.KMOD_SHIFT | pygame.KMOD_CAPS, True),
    (pygame.K_1, pygame.KMOD_NONE, False),
])
def test_is_letter(key, mods, expected):
    assert is_letter(key, mods) == expected

@pytest.mark.parametrize("key, mods, expected", [
    (pygame.K_a, pygame.KMOD_NONE, True),
    (pygame.K_z, pygame.KMOD_NONE, True),
    (pygame.K_z, pygame.KMOD_SHIFT | pygame.KMOD_CAPS, False),
])
def test_is_lower(key, mods, expected):
    assert is_lower(key, mods) == expected

@pytest.mark.parametrize("key, mods, expected", [
    (pygame.K_a, pygame.KMOD_SHIFT | pygame.KMOD_CAPS, True),
    (pygame.K_z, pygame.KMOD_SHIFT | pygame.KMOD_CAPS, True),
    (pygame.K_z, pygame.KMOD_NONE, False),
])
def test_is_upper(key, mods, expected):
    assert is_upper(key, mods) == expected

@pytest.mark.parametrize("key, mods, expected", [
    (pygame.K_1, pygame.KMOD_NONE, True),
    (pygame.K_0, pygame.KMOD_NONE, True),
    (pygame.K_a, pygame.KMOD_NONE, False),
])
def test_is_number(key, mods, expected):
    assert is_number(key, mods) == expected

@pytest.mark.parametrize("key, mods, expected", [
    (pygame.K_1, pygame.KMOD_SHIFT, True),  # '!'
    (pygame.K_BACKQUOTE, pygame.KMOD_SHIFT, True),  # '~'
    (pygame.K_EQUALS, pygame.KMOD_SHIFT, True),  # '+'
    (pygame.K_a, pygame.KMOD_NONE, False),
])
def test_is_symbol(key, mods, expected):
    assert is_symbol(key, mods) == expected
