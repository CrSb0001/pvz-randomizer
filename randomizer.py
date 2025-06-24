from __future__ import annotations

import abc
import atexit
import math
import os
import platform
import random
import traceback

from dataclasses import dataclass
from idlelib.tooltip import Hovertip
from inspect import signature
from statistics import mean, median
from tkinter import *
from tkinter import ttk

# move to file called errors.py later.
######################################
# Errors related to importing PvZ or
# reading or writing data to PvZ

class MemoryAllocationError(Exception):
	'''Raise when memory fails to be allocated'''
	pass

class PVZImportError(ImportError):
	'''Raise when `pvz` cannot be imported'''
	pass

class PVZFileError(Exception):
	'''Raise when memory cannot be read or cannot be written to'''
	pass

class PVZNotFoundError(PVZFileError):
	'''Raise when file `pvz` cannot be found'''
	pass

class ReadMemoryError(PVZFileError):
	'''Raise when file memory cannot be read'''
	pass

class WriteMemoryError(PVZFileError):
	'''Raise when file memory cannot be written to'''
	pass

# Errors related to invalid input formats

class PVZInvalidInputError(Exception):
	'''Raise when input format is invalid'''
	def __init__(
		self,
		msg: str | None = None
	) -> None:
		self.msg = msg or 'Input is invalid'
	
	def __repr__(self) -> str:
		return self.msg

class PVZInvalidLevelFormatError(PVZInvalidInputError):
	'''Raise when an input is incorrectly formatted.'''
	pass

######################################

class MockMemoryLock:
	def acquire():
		pass
	
	def release():
		pass

try:
	if plaform.system() == 'Windows':
		WINDOWS = True
		LINUX = False
		
		# use `pip install pvz` in the shell
		from pvz import *
		from pvz.extra import *
		
		write_memory = WriteMemory # PEP008
		read_memory = ReadMemory
		virtual_free_ex = VirtualFreeEx
		
		def dealloc_rng_memory() -> None:
			write_memory(
				'unsigned int',
				0x00000006,
				0x5A9936
			)
			write_Mmemory(
				'unsigned int',
				0xFFFFFEFB,
				0x5A9A41
			)
			write_memory(
				'unsigned int',
				0xFFFFFED5,
				0x5A9A67
			)
			try:
				virtual_free_ex(
					pvz_handler,
					rng_addr,
					0,
					0x8000
				)
			
			except:
				raise MemoryAllocationError('Could not deallocate rng memory.')
	
	else:
		WINDOWS = False
		LINUX = True
		
		memory_lock = MockMemoryLock()
		
		import ctypes, struct, time
		from os import listdir
		libc = ctpyes.CDLL('libc.so.6', use_errno = True)
		
		from ctypes import c_int     as INT
		from ctypes import c_uint    as UINT
		from ctypes import c_ulong   as ULONG
		from ctypes import c_char_p  as CHARP
		from ctypes import c_void_p  as VOIDP
		from ctypes import c_size_t  as SIZE_T
		from ctypes import c_ssize_t as SSIZE_T
		
		pwrite          = libc.pwrite
		pwrite.argtypes = [INT, VOIDP, SIZE_T, VOIDP]
		pwrite.restype  = SSIZE_T
		
		pread          = libc.pread
		pread.argtypes = [INT, VOIDP, SIZE_T, VOIDP]
		pread.restype  = INT
		
		c_open          = libc.open
		c_open.argtypes = [CHARP, INT, UINT]
		c_open.restype  = INT
		
		cpp_typename = {
			'char': 'b',
			'signed char': 'b',
			'int8_t': 'b',
			'unsigned char': 'B',
			'byte': 'B',
			'uint8_t': 'B',
			'bool': '?',
			'short': 'h',
			'int16_t': 'h',
			'unsigned short': 'h',
			'uint16_t': 'H',
			'int': 'i',
			'int32_t': 'i',
			'intptr_t': 'i',
			'unsigned int': 'I',
			'uint32_t': 'I',
			'uintptr_t': 'I',
			'size_t': 'I',
			'long': 'l',
			'unsigned long': 'L',
			'long long': 'q',
			'int64_t': 'q',
			'intmax_t': 'q',
			'unsigned long long': 'Q',
			'uint64_t': 'Q',
			'uintmax_t': 'Q',
			'float': 'f',
			'double': 'd'
		}
		
		def open_PVZ():
			PROCFILES = listdir('/proc/')
			PROCESSES = []
			
			for i in PROCFILES:
				if i.isdigit():
					PROCESSES += [i]
			
			PVZ_PROC = None
			for i in PROCESSES:
				with open('/proc/' + i + '/comm', 'rb') as namefile:
					name = namefile.read()
				
				if name == b'popcapgame1.exe\n':
					PVZ_PROC = i
				
				elif name == b'PlantsVsZombies\n':
					if not PVZ_PROC:
						PVZ_PROC = i
			
			if not PVZ_PROC:
				raise PVZImportError(
					'PvZ not found. Try importing it using `pip install pvz` in the shell.'
				)
			
			print(PVZ_PROC)
			pvz_memfd = c_open(b'/proc/' + bytes(PVZ_PROC, 'utf-8') + b'/mem', 0x01B6, 0)
			
			return pvz_memfd
		
		pvz_memfd = open_PVZ()
		
		def read_memory(data_type, *addr, array = 1):
			level      = len(addr)
			offset     = VOIDP()
			buffer     = UINT()
			bytes_read = ULONG()
			
			for i in range(level):
				offset.value = buffer.value + addr[i]
				
				if level - i - 1:
					size = ctypes.sizeof(buffer)
					bytes_read.value = pread(
						pvz_memfd,
						ctypes.byref(buffer),
						size,
						offset
					)
					if bytes_read.value != size:
						raise ReadMemoryError(f'ERRNO: {-cytes.get_errno()}')
				
				else:
					fmt_str = f'<{array}{cpp_typename[data_type]}'
					size = struct.calcsize(fmt_str)
					buff = ctypes.create_string_buffer(size)
					bytes_read.value = pread(
						pvz_memfd,
						ctypes.byref(buff),
						size,
						offset
					)
					if bytes_read.value != size:
						raise ReadMemoryError(f'ERRNO: {-cytes.get_errno()}')
					
					result = struct.unpack(fmt_str, buff.raw)
			
			if array == 1:
				return result[0]
			
			return result
		
		def write_memory(data_type, values, *addr) -> None:
			if not isinstance(values, (tuple, list)):
				values = [values]
			
			level         = len(addr)
			offset        = VOIDP()
			buffer        = UINT()
			bytes_read    = ULONG()
			bytes_written = ULONG()
			
			for i in range(level):
				offset.value = buffer.value + addr[i]
				
				if level - i - 1:
					size = ctypes.sizeof(buffer)
					bytes_read.value = pread(
						pvz_memfd,
						ctypes.byref(buffer),
						size,
						offset
					)
					if bytes_read.value != size:
						raise WriteMemoryError(f'ERRNO: {-cytes.get_errno()}')
				
				else:
					array = len(values)
					fmt_str = f'<{array}{cpp_typename[data_type]}'
					size = struct.calcsize(fmt_str)
					buff = ctypes.create_string_buffer(size)
					buff.value = struct.pack(fmt_str, *values)
					bytes_written.value = pwrite(
						pvz_memfd,
						ctypes.byref(buff),
						size,
						offset
					)
					if bytes_written.value != size:
						raise WriteMemoryError(f'ERRNO: {-cytes.get_errno()}')
		
		def sleep_(time_cs):
			if time_cs > 0.0:
				time.sleep(time_cs / 100)
			
			elif time_cs == 0.0:
				pass
			
			else:
				error('The thread sleep time cannot be less than 0.0')
		
		def game_ui():
			return read_memory('int', 0x6A9EC0, 0x07FC)

except Exception as err:
	raise PVZNotFoundError(
		f'PvZ not found!\n\t\t\t\t  Windows: {WINDOWS}\n\t\t\t\t  {traceback.format_exc()}'
	)

try:
	SAVE_FILE = open('saveFile.txt', 'r')

except:
	# if it doesn't work, open it in write mode, close it and try again
	SAVE_FILE = open('saveFile.txt', 'w')
	SAVE_FILE.close()
	SAVE_FILE = open('saveFile.txt', 'r')

HAS_SAVE = False
FILE_INFO = SAVE_FILE.readlines()
if len(FILE_INFO):
	HAS_SAVE = True

SAVE_FILE.close()
SAVE_POINT = -5

# Creates a window obj from the tkinter.Tk class
# `BooleanVar(value = True)` means that a restriction is applied by default.
# `BooleanVar(value = False)` or `StringVar(value = False)` means that a restriction is not applied by default.

# Effects of `NO_RESTRICTIONS`:
# * All `BooleanVar`s are set to True
# * All `StringVar`s are set to either of 'True' or 'On' where applicable.
# * All `IntVar`s are set to 100.
window = Tk()
window.title('Randomizer settings')
CHALLENGE_MODE                = BooleanVar(value = False)      #
SHOPLESS                      = BooleanVar(value = False)      # Shop is inaccessible to the player.
NO_RESTRICTIONS               = BooleanVar(value = False)      # All restrictions are set to maximum/True/False/On where applicable.
NO_AUTO_SLOTS                 = BooleanVar(value = True)       # Slots are not automatically set.
IMITATER                      = BooleanVar(value = False)      # Imitater plant
RANDOMIZE_PLANTS              = BooleanVar(value = True)       # Plants are given in a random order
SEEDED                        = BooleanVar(value = False)      #
UPGRADE_REWARDS               = BooleanVar(value = True)       #
RANDOM_WEIGHTS                = BooleanVar(value = False)      #
RENDER_WEIGHTS                = BooleanVar(value = False)      #
RANDOM_WAVE_POINTS            = StringVar(value = 'False')     #
RENDER_WAVE_POINTS            = BooleanVar(value = False)      #
SAVED                         = BooleanVar(value = False)      #
STARTING_WAVE                 = StringVar(value = '3')         # Wave that the level starts on.
RANDOM_COST                   = BooleanVar(value = False)      #
RANDOM_COOLDOWNS              = BooleanVar(value = False)      #
COST_TXT_TOGGLE               = BooleanVar(value = False)      #
COOLDOWN_COLORING             = StringVar(value = 'False')     #
RANDOM_ZOMBIES                = BooleanVar(value = False)      # Zombies are randomized based on wavepoints.
RANDOM_CONVEYORS              = StringVar(value = 'False')     # Plants on the conveyor belt are randomized.
ENABLE_CRAZY_DAVE             = StringVar(value = 'False')     # Enable Crazy Dave. Why is this an option? Because I'm crazy! Waby waboo.
DAVE_PLANTS_COUNT             = StringVar(value = '3')         # Number of plants Crazy Dave has in the shop.
RANDOM_VARS_CAT_ZOMBIE_HEALTH = StringVar(value = 'Off')       #
RANDOM_VARS_CAT_FIRE_RATE     = StringVar(value = 'Off')       #
LIMIT_PREVIEWS                = BooleanVar(value = False)      #
GAMEMODE                      = StringVar(value = 'adventure') # Gamemode that the user wants to play.
RANDOM_WAVE_COUNT             = StringVar(value = 'False')     #
RANDOM_WORLD                  = BooleanVar(value = False)      # The player starts in and is transported to a random world every level.
RANDOM_WORLD_CHANCE           = IntVar(value = 33)             # The (integral) percent chance that the player is transported to a randm world at the end of a level.
RANDOM_STUFF                  = BooleanVar(value = False)      #
RANDOM_SOUND                  = BooleanVar(value = False)      # Randomizes the sound files
RANDOM_SOUND_CHANCE           = IntVar(value = 3)              # The (integral) percent chance that a sound file is randomized.
RANDOM_PITCH                  = BooleanVar(value = False)      # Randomizes the pitch of sounds.

seed = random.randint(0x01, 0xFFFFFFFFFF)
