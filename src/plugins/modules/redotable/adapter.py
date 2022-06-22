from os import path
from pathlib import Path

def demo_service(context, *args, **kwargs):
	redotable = path.join(context.getnormdir(__file__), 'redotable_v1.1', 'redotable')

	arguments = context.parse_args('reDOTable', 'redotable', *args, **kwargs)
	outdir = context.createoutdir()
	output = path.join(outdir, "{0}-{1}_{2}".format(Path(arguments['x_seq']).stem, Path(arguments['y_seq']).stem, '_dotplot.png'))

	_, err = context.exec_run(redotable, "--png", arguments['x_seq'], arguments['y_seq'], output)
	
	if not path.exists(output):
		raise ValueError("reDOTable could not generate the result file.: " + err)

	return output