from os import path
from pathlib import Path
from app.util import Utility

thispath = path.abspath(path.dirname(__file__))

def run_kscalc(context, *args, **kwargs):
    from app import app
    arguments = context.parse_args('KSCalc', 'coge', *args, **kwargs)
    outdir = context.normalize(context.makeuniquedir(context.createoutdir()))
    
    stem = Path(arguments["data"]).stem
    db = path.join(outdir, stem + ".sqlite")
    ks = path.join(outdir, stem  + ".ks")
    context.bash_run(path.join(thispath, 'kscalc.sh'), arguments['data'], db, ks)
    return db,ks