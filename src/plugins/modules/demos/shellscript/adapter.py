from os import path
thispath = path.abspath(path.dirname(__file__))

def demo_service(context, *args, **kwargs):
	arguments = context.parse_args('SumInBashScript', 'demo', *args, **kwargs)
	out, err, _ = context.bash_run_out_err_exit(path.join(thispath, "sum.sh"),  arguments["data"])
	if err:
		raise ValueError(f"Tool SumInBashScript exited with error: {err}")
	return int(out) # exception is raised if bash script doesn't echo numeric values