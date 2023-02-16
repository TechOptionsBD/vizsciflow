from os import path
thispath = path.abspath(path.dirname(__file__))

def sum(numbers):
    sum = 0
    for i in range(len(numbers)):
        sum = sum + numbers[i]
    return sum

def demo_service(context, *args, **kwargs):
	arguments = context.parse_args('SumInFunction', 'demo', *args, **kwargs)
	out = sum(arguments["data"])
	return out