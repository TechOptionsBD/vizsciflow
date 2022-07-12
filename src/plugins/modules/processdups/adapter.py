import numpy as np
from os import path

def process_dups(context, *args, **kwargs):
    """
    Read in a file containing tandem duplicates and generate CoGe links to FeatList, GEvo, and FastaView
    for further analysis

    filepath: path to file containing tandem duplicates
    return: file containing generated links
    """
    arguments = context.parse_args('ProcessDups', 'CoGe', *args, **kwargs)
    infile = arguments["data"]

    with open(infile, "r") as fp:
        # read in input file
        lines = [line.split("\t") for line in fp.read().splitlines()][1:]
        
    baseurl = np.full(3, ["https://genomevolution.org/coge/"])
    tools = np.array(["FeatList.pl?", "GEvo.pl?", "FastaView.pl?"])
    links = np.char.add(baseurl, tools)
    
    outpath = context.createoutdir() + path.basename(infile) + ".tandems"

    with open(outpath, "w") as fp:
        # write header
        print("#FeatList_link	GEvo_link	FastaView_link	chr||start||stop||name||strand||type||database_id||gene_order", file=fp)
        
        # write to new file with links prepended
        for line in lines:
            num_seqs = len(line)
            fids = ";".join(["fid="+l.split("||")[6] for l in line])
            urls = np.char.add(links, np.array(fids))

            # process GeVo link by appending number after every fid and num_seqs
            fid_num = np.arange(1, num_seqs+1).astype("str")
            split_gevo = urls[1].split("fid")

            # insert numbers from 1 to num_seqs behind every fid
            urls[1] = split_gevo[0] + "".join(np.char.add(np.full(num_seqs, "fid"), np.char.add(fid_num, np.array(split_gevo[1:]))))
        
            # convert urls to list of strings
            urls = urls.astype("str").tolist()

            # append num_seqs to GEvo
            urls[1] += ";num_seqs="+ str(num_seqs)
            
            # write output to file
            prepend = "	".join(urls)
            print(prepend + "	" + "	".join(line), file=fp)
            
    return outpath