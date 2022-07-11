from ast import arguments
from os import path
from pathlib import Path

def demo_service(context, *args, **kwargs):
	blast2bed = path.join(context.getnormdir(__file__), 'bin', 'blast2bed.pl')
	
	arguments = context.parse_args("Blast2Bed", "blast", *args, **kwargs)
	data = arguments["data"]
	
	outdir = context.createoutdir()
	
	outfile1 = path.join(outdir, Path(data).stem +'.q.bed')
	outfile2 = path.join(outdir, Path(data).stem +'.s.bed')
	
	cmdargs = ["-infile", data, "-outfile1", outfile1, "-outfile2", outfile2]
	out, err = context.exec_run(blast2bed, *cmdargs)

	if err:
		raise ValueError("Blast2Bed could not generate {0}, {1} due to error: {2}".format(outfile1, outfile2, err))
	
	return [outfile1, outfile2]