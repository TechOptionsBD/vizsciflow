from os import path
thispath = path.abspath(path.dirname(__file__))

def demo_service(context, *args, **kwargs):
	arguments = context.parse_args('demo_sum8', '', *args, **kwargs)
	out, err, _ = context.py_run(path.join(thispath, 'sum.py'), arguments["data"])
	if err:
		raise(f"Tool demo_sum8 existed with error: {err}")
	return int(out)