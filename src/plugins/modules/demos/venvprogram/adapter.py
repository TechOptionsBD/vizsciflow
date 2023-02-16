from os import path
thispath = path.abspath(path.dirname(__file__))

def demo_service(context, *args, **kwargs):
	arguments = context.parse_args('SumInVenv', '', *args, **kwargs)
	# run in python 2 virtual environment
	out, err = context.pyvenv_run_at_venv(thispath, "python", '.venvpy2', path.join(thispath, 'sum.py'), arguments["data"])
	if err:
		raise(f"Tool SumInVenv exited with error: {err}")
	return int(out) # exception is raised if sum.py doesn't write valid numeric values in stdout