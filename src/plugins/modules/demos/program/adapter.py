from os import path
thispath = path.abspath(path.dirname(__file__))

def demo_service(context, *args, **kwargs):
	arguments = context.parse_args('SumInProgram', 'demo', *args, **kwargs)
	out, err, _ = context.py_run(path.join(thispath, 'sum.py'), arguments["data"])
	if err:
		raise ValueError(f"Tool SumInProgram exited with error: {err}")
	return int(out) # exception is raised if python program doesn't stdout numeric values