"""
Read/write vectors of correlated data from/to a csv file.

These data are stored in a dictionary, whose values are numpy arrays
with elements which may be strings, floats, or floats with associated uncertainties
as defined in the [uncertainties](https://pypi.org/project/uncertainties) library.
"""


__author__    = 'Mathieu Daëron'
__contact__   = 'mathieu@daeron.fr'
__copyright__ = 'Copyright (c) 2024 Mathieu Daëron'
__license__   = 'MIT License - https://opensource.org/licenses/MIT'
__date__      = '2024-10-09'
__version__   = '1.1.0'


import os as _os
import numpy as _np
import uncertainties as _uc


class uarray(_np.ndarray):

    __doc__ = """
    1-D [ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html)
    of [ufloat](https://pypi.org/project/uncertainties) values
    """

    def __new__(cls, a):
        obj = _np.asarray(a).view(cls)
        return obj
    
    n = property(fget = _np.vectorize(lambda x : x.n))
    """Return the array of nominal values (read-only)."""

    s = property(fget = _np.vectorize(lambda x : x.s))
    """Return the array of standard errors (read-only)"""

    correl = property(fget = lambda x: _np.array(_uc.correlation_matrix(x)))
    """Return the correlation matrix of the array elements (read-only)"""

    covar = property(fget = lambda x: _np.array(_uc.covariance_matrix(x)))
    """Return the covariance matrix of the array elements (read-only)"""

    nv = n
    "Alias for `uarray.nv`"

    se = s
    "Alias for `uarray.s`"

    cor = correl
    "Alias for `uarray.correl`"

    cov = covar
    "Alias for `uarray.covar`"    


def is_symmetric_positive_semidefinite(M: _np.ndarray) -> bool:
	'''
	Test whether 2-D array `M` is symmetric and positive semidefinite.
	'''
	return _np.all(_np.linalg.eigvals(M) >= 0) and _np.all(M - M.T == 0)


def smart_type(x: str):
	'''
	Tries to convert string `x` to a float if it includes a decimal point, or
	to an integer if it does not. If both attempts fail, return the original
	string unchanged.
	'''
	try:
		y = float(x)
	except ValueError:
		return x
	if y % 1 == 0 and '.' not in x:
		return int(y)
	return y


def read_data(data: str, sep: str = ',', validate_covar: bool = True):
	'''
	Read correlated data from a CSV-like string.
	
	Column names are interpreted in the following way:
	* In most cases, each columns is converted to a dict value, with the corresponding
	dict key being the column's label.
	* Columns whose label starts with `SE` are interpreted as specifying the standard
	error for the latest preceding data column.
	* Columns whose label starts with `correl` are interpreted as specifying the
	correlation matrix for the latest preceding data column. In that case, column labels
	are ignored for the rest of the columns belonging to this matrix.
	* Columns whose label starts with `covar` are interpreted as specifying the
	covariance matrix for the latest preceding data column. In that case, column labels
	are ignored for the rest of the columns belonging to this matrix.
	* `SE`, `correl`, and `covar` may be specified for any arbitrary variable other than
	the latest preceding data column, by adding an underscore followed by the variable's
	label (ex: `SE_foo`, `correl_bar`, `covar_baz`).
	* `correl`, and `covar` may also be specified for any pair of variable, by adding an
	underscore followed by the two variable labels, joined by a second underscore
	(ex: `correl_foo_bar`, `covar_X_Y`). The elements of the first and second variables
	correspond, respectively, to the lines and columns of this matrix.
	* Exceptions will be raised, for any given variable:
		- when specifying both `covar` and any combination of (`SE`, `correl`)
		- when specifying `correl` without `SE`

	**Arguments**
	- `data`: a CSV-like string
	- `sep`: the CSV separator
	- `validate_covar`: whether to check that the overall covariance matrix
	is symmetric and positive semidefinite. Specifying `validate_covar = False`
	bypasses this computationally expensive step.
	
	**Example**
	```py
	import correldata
	data  = """
	Sample, Tacid,  D47,   SE,         correl,,,  D48, covar,,,          correl_D47_D48
	   FOO,   90., .245, .005,      1, 0.5, 0.5, .145,  4e-4, 1e-4, 1e-4, 0.5,   0,   0
	   BAR,   90., .246, .005,    0.5,   1, 0.5, .146,  1e-4, 4e-4, 1e-4,   0, 0.5,   0
	   BAZ,   90., .247, .005,    0.5, 0.5,   1, .147,  1e-4, 1e-4, 4e-4,   0,   0, 0.5
	"""[1:-1]
	print(correldata.read_data(data))
	
	# yields:
	# 
	# > {
	#     'Sample': array(['FOO', 'BAR', 'BAZ'], dtype='<U3'),
	#     'Tacid': array([90., 90., 90.]),
	#     'D47': uarray([0.245+/-0.004999999999999998, 0.246+/-0.004999999999999997, 0.247+/-0.005], dtype=object),
	#     'D48': uarray([0.145+/-0.019999999999999993, 0.146+/-0.019999999999999993, 0.147+/-0.019999999999999997], dtype=object)
	#   }
	```
	'''

	data = [[smart_type(e.strip()) for e in l.split(sep)] for l in data.split('\n')]
	N = len(data) - 1

	values, se, correl, covar = {}, {}, {}, {}
	j = 0
	while j < len(data[0]):
		field = data[0][j]
		if not (
			field.startswith('SE_')
			or field.startswith('correl_')
			or field.startswith('covar_')
			or field == 'SE'
			or field == 'correl'
			or field == 'covar'
			or len(field) == 0
		):
			values[field] = _np.array([l[j] for l in data[1:]])
			j += 1
			oldfield = field
		elif field.startswith('SE_'):
			se[field[3:]] = _np.array([l[j] for l in data[1:]])
			j += 1
		elif field == 'SE':
			se[oldfield] = _np.array([l[j] for l in data[1:]])
			j += 1
		elif field.startswith('correl_'):
			correl[field[7:]] = _np.array([l[j:j+N] for l in data[1:]])
			j += N
		elif field == 'correl':
			correl[oldfield] = _np.array([l[j:j+N] for l in data[1:]])
			j += N
		elif field.startswith('covar_'):
			covar[field[6:]] = _np.array([l[j:j+N] for l in data[1:]])
			j += N
		elif field == 'covar':
			covar[oldfield] = _np.array([l[j:j+N] for l in data[1:]])
			j += N

	nakedvalues = {}
	for k in [_ for _ in values]:
		if (
			k not in se
			and k not in correl
			and k not in covar
		):
			nakedvalues[k] = values.pop(k)

	for x in values:
		if x in covar:
			if x in se:
				raise KeyError(f'Too much information: both SE and covar are specified for variable "{x}".')
			if x in correl:
				raise KeyError(f'Too much information: both correl and covar are specified for variable "{x}".')
		if x in correl:
			if x not in se:
				raise KeyError(f'Not enough information: correl is specified without SE for variable "{x}".')

	for x in correl:
		if x in values:
			covar[x] = _np.diag(se[x]) @ correl[x] @ _np.diag(se[x])
		else:
			for x1 in values:
				for x2 in values:
					if x == f'{x1}_{x2}':
						if x1 in se:
							se1 = se[x1]
						else:
							if x1 in covar:
								se1 = _np.diag(covar[x1])**0.5
							else:
								raise KeyError(f'Not enough information: correl_{x} is specified without SE for variable "{x1}".')
						if x2 in se:
							se2 = se[x2]
						else:
							if x2 in covar:
								se2 = _np.diag(covar[x2])**0.5
							else:
								raise KeyError(f'Not enough information: correl_{x} is specified without SE for variable "{x1}".')

						covar[x] = _np.diag(se1) @ correl[x] @ _np.diag(se2)

	for x in se:
		if x in values and x not in correl:
			covar[x] = _np.diag(se[x]**2)

	for k in [_ for _ in covar]:
		if k not in values:
			for j1 in values:
				for j2 in values:
					if k == f'{j1}_{j2}':
						covar[f'{j2}_{j1}'] = covar[f'{j1}_{j2}'].T

	X = _np.array([_ for k in values for _ in values[k]])
	CM = _np.zeros((X.size, X.size))
	for i, vi in enumerate(values):
		for j, vj in enumerate(values):
			if vi == vj:
				if vi in covar:
					CM[N*i:N*i+N,N*j:N*j+N] = covar[vi]
			else:
				if f'{vi}_{vj}' in covar:
					CM[N*i:N*i+N,N*j:N*j+N] = covar[f'{vi}_{vj}']

	if validate_covar and not is_symmetric_positive_semidefinite(CM):
		raise _np.linalg.LinAlgError('The complete covariance matrix is not symmetric positive-semidefinite.')

	corvalues = uarray(_uc.correlated_values(X, CM))

	allvalues = nakedvalues

	for i, x in enumerate(values):
		allvalues[x] = corvalues[i*N:i*N+N]

	return allvalues


def read_data_from_file(filename: str | _os.PathLike, **kwargs):
	'''
	Read correlated data from a CSV file.

	**Arguments**
	- `filename`: `str` or path to the file to read from
	- `kwargs`: passed to correldata.read_data()
	'''
	with open(filename) as fid:
		return read_data(fid.read(), **kwargs)

def data_string(
	data: dict,
	sep: str = ',',
	float_fmt: str = 'zg',
	max_correl_precision: int = 9,
	fields: list = None,
	align: str = '>',
	atol: float = 1e-12,
	rtol: float = 1e-12,
):
	'''
	Generate CSV-like string from correlated data

	**Arguments**
	- `data`: dict of arrays with strings, floats or correlated data
	- `sep`: the CSV separator
	- `float_fmt`: formatting string for float values
	- `max_correl_precision`: number of post-decimal digits for correlation values
	- `fields`: subset of fields to write; if `None`, write all fields
	- `align`: right-align (`>`), left-align (`<`), or don't align (empty string) CSV values
	- `atol`: passed to _np.allclose(),
	- `rtol`: passed to [numpy.allclose()](https://numpy.org/doc/stable/reference/generated/numpy.allclose.html),
	'''
	if fields is None:
		fields = [_ for _ in data]
	cols, ufields = [], []
	for f in fields:
		if isinstance(data[f], uarray):
			ufields.append(f)
			N = data[f].size
			cols.append([f] + [f'{_.n:{float_fmt}}' for _ in data[f]])
			cols.append([f'SE_{f}'] + [f'{_.s:{float_fmt}}' for _ in data[f]])
			CM = _uc.correlation_matrix(data[f])
			if not _np.allclose(CM, _np.eye(N), atol = atol, rtol = rtol):
				for i in range(N):
					cols.append(['' if i else f'correl_{f}'] + [f'{CM[i,j] if abs(CM[i,j]) > atol else 0:z.{max_correl_precision}f}'.rstrip('0') for j in range(N)])

		else:
			cols.append([f] + [str(_) for _ in data[f]])

	for i in range(len(ufields)):
		for j in range(i):
			CM = _uc.correlation_matrix((*data[ufields[i]], *data[ufields[j]]))[:N,N:]
			if not _np.allclose(CM, _np.eye(N), atol = atol, rtol = rtol):
				for k in range(N):
					cols.append(['' if k else f'correl_{ufields[i]}_{ufields[j]}'] + [f'{CM[k,l] if abs(CM[k,l]) > atol else 0:z.{max_correl_precision}f}'.rstrip('0') for l in range(N)])

	lines = list(map(list, zip(*cols)))

	if align:
		lengths = [max([len(e) for e in l]) for l in cols]
		for l in lines:
			for k,ln in enumerate(lengths):
				l[k] = f'{l[k]:{align}{ln}s}'
		return '\n'.join([(sep+' ').join(l) for l in lines])

	return '\n'.join([sep.join(l) for l in lines])



def save_data_to_file(data, filename, **kwargs):
	'''
	Write correlated data to a CSV file.

	**Arguments**
	- `data`: dict of arrays with strings, floats or correlated data
	- `filename`: `str` or path to the file to read from
	- `kwargs`: passed to correldata.data_string()
	'''
	with open(filename, 'w') as fid:
		return fid.write(data_string(data, **kwargs))
