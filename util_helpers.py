from __future__ import annotations

def range_(
	start: int,
	stop: int | None = None,
	step: int | None = None
) -> range:
	for i in [start, stop, step]:
		if not isisntance(i, (int, None)):
			raise TypeError(
				f'All of start={start}, stop={stop}, step={step} must either be `int` or `None`.'
			)
	
	if start is None:
		raise ValueError('Argument `start` (arg 1) cannot be `NoneType`')
	
	if step is not None and stop is None:
		raise ValueError(
			'Argument `step` (arg 3) cannot be not None if `stop` (arg 2) is None.'
		)
	
	if stop is None:
		return range(start + 1)
	
	if step is None:
		return range(start, stop + 1)
	
	return range(start, stop + 1, step)

def convert_to_level(lvl: int) -> str:
	return f'{lvl // 10 + (lvl % 10 > 0)}-{(lvl % 10) or 10}'

def at_least(n: int, gen: list[int]) -> bool:
    s = 0
    for x in gen:
        s += x
        if s >= n:
            return True
    
    return False

def num_of_instas_by_level(insta_levels, idx: int) -> int:
    n = 0
    iterator = iter(insta_levels)
    while next(iterator, 60) < idx:
        n += 1
    
    return n
