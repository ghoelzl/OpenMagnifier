# Copyright 2011-2013 Guenther Hoelzl (ghoelzl@gmail.com)
#
# This file is part of OpenMagnifier
#
# OpenMagnifier is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OpenMagnifier is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OpenMagnifier.  If not, see <http://www.gnu.org/licenses/>.

from pygame import *

KEYS_MOVE_LEFT = [K_LEFT, K_KP4, ord('h'), ord('H')]
KEYS_MOVE_RIGHT = [K_RIGHT, K_KP6, ord('l'), ord('L')]
KEYS_MOVE_UP = [K_UP, K_KP8, ord('k'), ord('K')]
KEYS_MOVE_DOWN = [K_DOWN, K_KP2, ord('j'), ord('J')]
KEYS_ZOOM_IN = [K_a, K_END, K_KP1, K_KP_PLUS, ord('+'), K_PAGEUP]
KEYS_ZOOM_OUT = [K_s, K_PAGEDOWN, K_KP3, K_KP_MINUS, ord('-')]
KEYS_TOGGLE_MODE = [K_KP_DIVIDE, K_KP0, ord(' ')]
KEYS_FOCUS_MINUS = [K_HOME, K_KP7] 
KEYS_FOCUS_PLUS = [K_PAGEUP, K_KP9]
KEYS_ENTER = [K_RETURN, ord('\r')]
KEYS_GREENRED = [K_KP_DIVIDE]
KEYS_CONTROL_MODE = [K_INSERT, K_KP0]
KEYS_CENTER = [K_HOME, K_KP5]
KEYS_AUTOFOCUS = [ord('a'), ord('A')]
KEYS_RESET = [ord('r'), ord('R')]
KEYS_FULLSCREEN = [K_HOME, K_KP7, ord('F'), ord('f')]
KEYS_QUIT = [K_ESCAPE, K_q]

