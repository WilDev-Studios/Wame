from __future__ import annotations

import pygame

KEYS:dict[tuple[int, int], str] = {
    (pygame.K_a, pygame.KMOD_SHIFT | pygame.KMOD_CAPS): 'A',
    (pygame.K_b, pygame.KMOD_SHIFT | pygame.KMOD_CAPS): 'B',
    (pygame.K_c, pygame.KMOD_SHIFT | pygame.KMOD_CAPS): 'C',
    (pygame.K_d, pygame.KMOD_SHIFT | pygame.KMOD_CAPS): 'D',
    (pygame.K_e, pygame.KMOD_SHIFT | pygame.KMOD_CAPS): 'E',
    (pygame.K_f, pygame.KMOD_SHIFT | pygame.KMOD_CAPS): 'F',
    (pygame.K_g, pygame.KMOD_SHIFT | pygame.KMOD_CAPS): 'G',
    (pygame.K_h, pygame.KMOD_SHIFT | pygame.KMOD_CAPS): 'H',
    (pygame.K_i, pygame.KMOD_SHIFT | pygame.KMOD_CAPS): 'I',
    (pygame.K_j, pygame.KMOD_SHIFT | pygame.KMOD_CAPS): 'J',
    (pygame.K_k, pygame.KMOD_SHIFT | pygame.KMOD_CAPS): 'K',
    (pygame.K_l, pygame.KMOD_SHIFT | pygame.KMOD_CAPS): 'L',
    (pygame.K_m, pygame.KMOD_SHIFT | pygame.KMOD_CAPS): 'M',
    (pygame.K_n, pygame.KMOD_SHIFT | pygame.KMOD_CAPS): 'N',
    (pygame.K_o, pygame.KMOD_SHIFT | pygame.KMOD_CAPS): 'O',
    (pygame.K_p, pygame.KMOD_SHIFT | pygame.KMOD_CAPS): 'P',
    (pygame.K_q, pygame.KMOD_SHIFT | pygame.KMOD_CAPS): 'Q',
    (pygame.K_r, pygame.KMOD_SHIFT | pygame.KMOD_CAPS): 'R',
    (pygame.K_s, pygame.KMOD_SHIFT | pygame.KMOD_CAPS): 'S',
    (pygame.K_t, pygame.KMOD_SHIFT | pygame.KMOD_CAPS): 'T',
    (pygame.K_u, pygame.KMOD_SHIFT | pygame.KMOD_CAPS): 'U',
    (pygame.K_v, pygame.KMOD_SHIFT | pygame.KMOD_CAPS): 'V',
    (pygame.K_w, pygame.KMOD_SHIFT | pygame.KMOD_CAPS): 'W',
    (pygame.K_x, pygame.KMOD_SHIFT | pygame.KMOD_CAPS): 'X',
    (pygame.K_y, pygame.KMOD_SHIFT | pygame.KMOD_CAPS): 'Y',
    (pygame.K_z, pygame.KMOD_SHIFT | pygame.KMOD_CAPS): 'Z',

    (pygame.K_a, pygame.KMOD_NONE): 'a',
    (pygame.K_b, pygame.KMOD_NONE): 'b',
    (pygame.K_c, pygame.KMOD_NONE): 'c',
    (pygame.K_d, pygame.KMOD_NONE): 'd',
    (pygame.K_e, pygame.KMOD_NONE): 'e',
    (pygame.K_f, pygame.KMOD_NONE): 'f',
    (pygame.K_g, pygame.KMOD_NONE): 'g',
    (pygame.K_h, pygame.KMOD_NONE): 'h',
    (pygame.K_i, pygame.KMOD_NONE): 'i',
    (pygame.K_j, pygame.KMOD_NONE): 'j',
    (pygame.K_k, pygame.KMOD_NONE): 'k',
    (pygame.K_l, pygame.KMOD_NONE): 'l',
    (pygame.K_m, pygame.KMOD_NONE): 'm',
    (pygame.K_n, pygame.KMOD_NONE): 'n',
    (pygame.K_o, pygame.KMOD_NONE): 'o',
    (pygame.K_p, pygame.KMOD_NONE): 'p',
    (pygame.K_q, pygame.KMOD_NONE): 'q',
    (pygame.K_r, pygame.KMOD_NONE): 'r',
    (pygame.K_s, pygame.KMOD_NONE): 's',
    (pygame.K_t, pygame.KMOD_NONE): 't',
    (pygame.K_u, pygame.KMOD_NONE): 'u',
    (pygame.K_v, pygame.KMOD_NONE): 'v',
    (pygame.K_w, pygame.KMOD_NONE): 'w',
    (pygame.K_x, pygame.KMOD_NONE): 'x',
    (pygame.K_y, pygame.KMOD_NONE): 'y',
    (pygame.K_z, pygame.KMOD_NONE): 'z',

    (pygame.K_1, pygame.KMOD_SHIFT): '!',
    (pygame.K_2, pygame.KMOD_SHIFT): '@',
    (pygame.K_3, pygame.KMOD_SHIFT): '#',
    (pygame.K_4, pygame.KMOD_SHIFT): '$',
    (pygame.K_5, pygame.KMOD_SHIFT): '%',
    (pygame.K_6, pygame.KMOD_SHIFT): '^',
    (pygame.K_7, pygame.KMOD_SHIFT): '&',
    (pygame.K_8, pygame.KMOD_SHIFT): '*',
    (pygame.K_9, pygame.KMOD_SHIFT): '(',
    (pygame.K_0, pygame.KMOD_SHIFT): ')',

    (pygame.K_1, pygame.KMOD_NONE): '1',
    (pygame.K_2, pygame.KMOD_NONE): '2',
    (pygame.K_3, pygame.KMOD_NONE): '3',
    (pygame.K_4, pygame.KMOD_NONE): '4',
    (pygame.K_5, pygame.KMOD_NONE): '5',
    (pygame.K_6, pygame.KMOD_NONE): '6',
    (pygame.K_7, pygame.KMOD_NONE): '7',
    (pygame.K_8, pygame.KMOD_NONE): '8',
    (pygame.K_9, pygame.KMOD_NONE): '9',
    (pygame.K_0, pygame.KMOD_NONE): '0',

    (pygame.K_BACKQUOTE, pygame.KMOD_SHIFT): '~',
    (pygame.K_MINUS, pygame.KMOD_SHIFT): '_',
    (pygame.K_EQUALS, pygame.KMOD_SHIFT): '+',
    (pygame.K_LEFTBRACKET, pygame.KMOD_SHIFT): '{',
    (pygame.K_RIGHTBRACKET, pygame.KMOD_SHIFT): '}',
    (pygame.K_BACKSLASH, pygame.KMOD_SHIFT): '|',
    (pygame.K_SEMICOLON, pygame.KMOD_SHIFT): ':',
    (pygame.K_QUOTE, pygame.KMOD_SHIFT): '"',
    (pygame.K_COMMA, pygame.KMOD_SHIFT): '<',
    (pygame.K_PERIOD, pygame.KMOD_SHIFT): '>',
    (pygame.K_SLASH, pygame.KMOD_SHIFT): '?',

    (pygame.K_BACKQUOTE, pygame.KMOD_NONE): '`',
    (pygame.K_MINUS, pygame.KMOD_NONE): '-',
    (pygame.K_EQUALS, pygame.KMOD_NONE): '=',
    (pygame.K_LEFTBRACKET, pygame.KMOD_NONE): '[',
    (pygame.K_RIGHTBRACKET, pygame.KMOD_NONE): ']',
    (pygame.K_BACKSLASH, pygame.KMOD_NONE): '\\',
    (pygame.K_SEMICOLON, pygame.KMOD_NONE): ';',
    (pygame.K_QUOTE, pygame.KMOD_NONE): '\'',
    (pygame.K_COMMA, pygame.KMOD_NONE): ',',
    (pygame.K_PERIOD, pygame.KMOD_NONE): '.',
    (pygame.K_SLASH, pygame.KMOD_NONE): '/',
}
'''Mapping of `(KEYCODE, MODIFIERS)` -> `KEY`'''

def is_char(key:int, mods:int) -> bool:
    '''
    Check to see if this key/mods combination equates to a character on the keyboard
    
    Parameters
    ----------
    key : int
        The raw `pygame` key code
    mods : int
        The raw `pygame` key mods
    
    Returns
    -------
    bool
        If this key/mods combination equates to a character on the keyboard
    '''

    if not KEYS.get((key, mods), None):
        return False

    return True

def is_letter(key:int, mods:int) -> bool:
    '''
    Check to see if this key/mods combination equates to a letter
    
    Parameters
    ----------
    key : int
        The raw `pygame` key code
    mods : int
        The raw `pygame` key mods
    
    Returns
    -------
    bool
        If this key/mods combination equates to a letter
    '''

    return is_upper(key, mods) or is_lower(key, mods)

def is_lower(key:int, mods:int) -> bool:
    '''
    Check to see if this key/mods combination equates to a lowercase letter
    
    Parameters
    ----------
    key : int
        The raw `pygame` key code
    mods : int
        The raw `pygame` key mods
    
    Returns
    -------
    bool
        If this key/mods combination equates to a lowercase letter
    '''

    return KEYS.get((key, mods), None) in [
        'a', 'b', 'c', 'd', 'e', 'f', 'g',
        'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u',
        'v', 'w', 'x', 'y', 'z'
    ]

def is_number(key:int, mods:int) -> bool:
    '''
    Check to see if this key/mods combination equates to a number/digit
    
    Parameters
    ----------
    key : int
        The raw `pygame` key code
    mods : int
        The raw `pygame` key mods
    
    Returns
    -------
    bool
        If this key/mods combination equates to a number/digit
    '''

    return KEYS.get((key, mods), None) in [
        '1', '2', '3', '4', '5',
        '6', '7', '8', '9', '0'
    ]

def is_symbol(key:int, mods:int) -> bool:
    '''
    Check to see if this key/mods combination equates to a symbol
    
    Parameters
    ----------
    key : int
        The raw `pygame` key code
    mods : int
        The raw `pygame` key mods
    
    Returns
    -------
    bool
        If this key/mods combination equates to a symbol
    '''

    return KEYS.get((key, mods), None) in [
        '~', '`', '!', '@', '#', '$', '%', '^',
        '&', '*', '(', ')', '_', '-', '+', '=',
        '{', '[', '}', ']', ':', ';', '"', '\'',
        '|', '\\', '<', ',', '>', '.', '?', '/'
    ]

def is_upper(key:int, mods:int) -> bool:
    '''
    Check to see if this key/mods combination equates to an uppercase letter
    
    Parameters
    ----------
    key : int
        The raw `pygame` key code
    mods : int
        The raw `pygame` key mods
    
    Returns
    -------
    bool
        If this key/mods combination equates to an uppercase letter
    '''

    return KEYS.get((key, mods), None) in [
        'A', 'B', 'C', 'D', 'E', 'F', 'G',
        'H', 'I', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U',
        'V', 'W', 'X', 'Y', 'Z'
    ]