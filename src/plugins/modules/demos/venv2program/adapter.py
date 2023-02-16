from os import path
thispath = path.abspath(path.dirname(__file__))

def demo_service(context, *args, **kwargs):
	arguments = context.parse_args('demo_sum10', '', *args, **kwargs)
	out, err = context.pyvenv_run(thispath, "python", path.join(thispath, 'sum.py'), arguments["data"])
	if err:
		raise(f"Tool demo_sum10 existed with error: {err}")
	return int(out)