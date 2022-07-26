import os
from os import path
from pathlib import Path

def run_makeblastdb(context, *args, **kwargs):
    # locate executable in uploaded zip folder
    makedb = path.join(context.getnormdir(__file__), 'bin', 'makeblastdb')

    # parse input file and database type, as specified by user
    arguments = context.parse_args('CreateBlastDB', 'blast', *args, **kwargs)

    # create output directory where all files of database will be stored
    outpath = path.join(context.createoutdir(), Path(arguments["data"]).stem)
    cmdargs = ["-in", arguments["data"], "-dbtype", arguments["dbtype"], "-out", outpath]
   
    log, err = context.exec_run(makedb, *cmdargs)
    
    if err:
        raise ValueError(err)
    else:
        # display log report
        context.out.append("CreateBlastDB log:\n" + str(log))
        return outpath

def run_blast(blast, context, *args, **kwargs):
    """
    Blast a query sequence against a nucleotide/protein database
    User specifies the variant based on the data they are passing in
    And the algorithm they wish to use
    """

    toolpath = path.join(context.getnormdir(__file__), 'bin', blast.lower())
    arguments = context.parse_args(blast, 'blast', *args, **kwargs)

    # query and database are mandatory
    query, db = arguments.pop("query"), arguments.pop("db")

    outpath = path.join(context.createoutdir(), "{0}-{1}.{2}".format(Path(query).stem, Path(db).stem, blast.lower()))

    # the rest are optional arguments
    optargs = [["-"+key, str(arguments[key])] for key in arguments.keys() if arguments[key]]
    optargs = [a for arg in optargs for a in arg] # flatten 2D list into 1D
    
    log, err = context.exec_run(toolpath, "-query", query, "-db", db, *optargs, "-out", outpath)

    if err and not "Warning" in err:
        # report errors, but ignore warnings
        raise ValueError(err)
    if log:
        context.out.append(blast+" log:\n" + str(log))

        # Note: if Mainul can find way to display .txt output in output, then won't have to generate .html file
        # report = path.join(context.createoutdir(), "{0}-{1}.{2}.html".format(Path(arguments['query']).stem, Path(arguments['db']).stem, blast.lower()))

        # text = '<html><pre>' + out + '</pre></html>'
        # with open(report, "w") as file:
        #     file.write(text)
   
        # return report
    
    return outpath


# Below are variants of Blast

def run_blastn(context, *args, **kwargs):
    return run_blast("BlastN", context, *args, **kwargs)

def run_blastp(context, *args, **kwargs):
    return run_blast("BlastP", context, *args, **kwargs)

# Translated searches
def run_tblastn(context, *args, **kwargs):
    return run_blast("tBlastN", context, *args, **kwargs)

def run_blastx(context, *args, **kwargs):
    return run_blast("BlastX", context, *args, **kwargs)

def run_tblastx(context, *args, **kwargs):
    return run_blast("tBlastX", context, *args, **kwargs)