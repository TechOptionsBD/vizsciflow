from os import path
thispath = path.abspath(path.dirname(__file__))

def demo_service(context, *args, **kwargs):
	arguments = context.parse_args('SumInDocker', 'demo', *args, **kwargs)   
	out, _ = context.docker_run('bigclonebench', 'python', 'sum.py', arguments['data'], cwd='/root/commands')
	return int(out) # exception is raised if program doesn't stdout numeric values
