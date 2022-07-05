from os import path
from pathlib import Path

thispath = path.dirname(__file__)

def demo_service(context, *args, **kwargs):
	blast_to_raw = path.join(thispath, 'quota-alignment', 'scripts', 'blast_to_raw.py')
	
	arguments = context.parse_args('BlastToRaw', 'blast', *args, **kwargs)
	
	outdir = context.createoutdir()
	
	blaststem = Path(arguments['blast']).stem
	qdups = path.join(outdir, blaststem +'.q.localdups')
	qnodups = path.join(outdir, blaststem +'.q.nolocaldups.bed')
	
	sdups = path.join(outdir, blaststem +'.s.localdups')
	snodups = path.join(outdir, blaststem +'.s.nolocaldups.bed')
	
	out = path.join(outdir, "{0}.tdd{1}.cs{2}.filtered".format(blaststem, arguments['tandem_Nmax'], arguments['cscore']))
	
	cmdargs = [arguments['blast'], "--localdups --qbed=" + arguments['qbed'], "--sbed="+ arguments['sbed'], "--tandem_Nmax={0}".format(arguments['tandem_Nmax']), "--cscore={0}".format(arguments['cscore']), ">", out]
	log, err = context.pyvenv_run(thispath, "python2", blast_to_raw, *cmdargs)
	
	return [qdups, qnodups, sdups, snodups, out]
