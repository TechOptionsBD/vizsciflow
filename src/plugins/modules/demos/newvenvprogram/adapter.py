from os import path
thispath = path.abspath(path.dirname(__file__))

def demo_service(context, *args, **kwargs):
	arguments = context.parse_args('SumInNewVenv', 'demo', *args, **kwargs)
	# run in new virtual environment
	out, err = context.pyvenv_run_at_venv(thispath, "python", 'newvenvprogram', path.join(thispath, 'sum.py'), arguments["data"])
	if err:
		raise ValueError(f"Tool SumInNewVenv exited with error: {err}")
	return int(out) # exception is raised if sum.py doesn't write valid numeric values in stdout