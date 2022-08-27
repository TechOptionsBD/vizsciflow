from os import path
from pathlib import Path

thispath = path.dirname(__file__)

def demo_service(context, *args, **kwargs):
	blast_to_raw = path.join(thispath, 'bin', 'scripts', 'blast_to_raw.py')
	
	# parse user arguments
	arguments = context.parse_args('BlastToRaw', 'blast', *args, **kwargs)
	blastfile = arguments.pop("blast")
	
	# prepare output directories
	outdir = context.createoutdir()
	blaststem = Path(blastfile).stem

	qdups = path.join(outdir, blaststem +'.q.localdups')
	qnodups = path.join(outdir, blaststem +'.q.nolocaldups.bed')
	
	sdups = path.join(outdir, blaststem +'.s.localdups')
	snodups = path.join(outdir, blaststem +'.s.nolocaldups.bed')
	
	out = path.join(outdir, "{0}.tdd{1}.cs{2}.filtered".format(blaststem, arguments['tandem_Nmax'], arguments['cscore']))

	# run tool
	cmdargs = ["--localdups"] + ["=".join(["--"+key, str(arguments[key])]) for key in arguments.keys()]
	stdout, log = context.pyvenv_run(thispath, "python2", blast_to_raw, blastfile, *cmdargs)


	if log:
		# display log report
		context.out.append("BlastToRaw log:\n" + str(log))

	with open(out, "w") as file:
		# write stdout to output file
		file.write(stdout)
	
	return [qdups, qnodups, sdups, snodups, out]