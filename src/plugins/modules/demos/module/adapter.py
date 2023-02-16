from os import path
thispath = path.abspath(path.dirname(__file__))
from .sum import demo_sum

def demo_service(context, *args, **kwargs):
	arguments = context.parse_args('demo_sum7', '', *args, **kwargs)
	out = demo_sum(arguments["data"])
	print(out)
	return out