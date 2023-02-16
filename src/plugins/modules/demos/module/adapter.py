from os import path
thispath = path.abspath(path.dirname(__file__))
from .sum import sum

def demo_service(context, *args, **kwargs):
	arguments = context.parse_args('SumInModule', 'demo', *args, **kwargs)
	out = sum(arguments["data"])
	return out