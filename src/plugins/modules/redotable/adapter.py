from os import path

def demo_service(context, *args, **kwargs):
	redotable = path.join(context.getnormdir(__file__), 'redotable_v1.1', 'redotable')
	output = path.join(context.createoutdir(), args[0].split("/")[-1].split('.')[0] + '-'+ args[1].split("/")[-1].split('.')[0] + '_dotplot.png')

	context.exec_run(redotable, "--png", args[0], args[1], output)
	return output