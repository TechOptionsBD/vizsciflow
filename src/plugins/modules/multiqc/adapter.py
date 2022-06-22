from os import path
thispath = path.dirname(__file__)

def demo_service(context, *args, **kwargs):
	arguments = context.parse_args('MultiQC', 'fastqc', *args, **kwargs)
	outdir = context.createoutdir()
	context.pyvenv_run(thispath, 'multiqc', ' '.join(arguments['data']), "-o " + outdir)
	
	output = path.join(outdir, 'multiqc_report.html')
	if not path.exists(output):
		raise ValueError("MultiQC could not generate the result file")

	return output