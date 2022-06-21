from os import path
thispath = path.dirname(__file__)

def demo_service(context, *args, **kwargs):
	output = context.createoutdir()
	context.pyvenv_run(thispath, 'multiqc', ' '.join([context.normalize(arg) for arg in args]), "-o " + output)
	
	return context.denormalize(output + '/multiqc_report.html')