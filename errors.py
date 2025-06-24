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

class PVZInvalidLevelFormatError(PVZInvalidInputError):
	'''Raise when an input is incorrectly formatted.'''
	pass
