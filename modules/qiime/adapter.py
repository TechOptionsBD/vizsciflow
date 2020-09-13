import os
from pathlib import Path
from app.util import Utility
from app.biowl.exechelper import func_exec_bash_stdout


activate = 'source /home/phenodoop/miniconda3/bin/activate /home/phenodoop/miniconda3/envs/qiime2-2018.11;'
qiime_runner = "/home/phenodoop/phenoproc/app/biowl/modules/qiime/conda_service.sh"

# def run_qiime2(*args):
#     return func_exec_bash_stdout(qiime_service, *args)

def get_input_from_args(paramindex, keyname, *args, **kwargs):
    
    barcode = ''
    if keyname in kwargs.keys():
        barcode = kwargs[keyname]
    else:
        if len(args) == paramindex:
            raise ValueError("Argument {0} missing error in function call.".format(keyname))
        barcode = args[paramindex]
        paramindex +=1
    
    return paramindex, barcode
      
def get_input_from_args_optional(paramindex, keyname, default, *args, **kwargs):
    
    barcode = default
    if keyname in kwargs.keys():
        barcode = kwargs[keyname]
    else:
        if len(args) > paramindex:
            barcode = args[paramindex]
            paramindex +=1
            
    return paramindex, barcode

def get_output_filename_from_args(paramindex, fs, data, keyname, defaultname, ext, *args, **kwargs):
    repseqs=''
    if keyname in kwargs.keys():
        repseqs = kwargs[keyname]
    else:
        if len(args) > paramindex:
            repseqs = args[paramindex]
            paramindex +=1
    
    outputName = defaultname if defaultname else Path(os.path.basename(data)).stem
    if not outputName:
        outputName = keyname
    if ext:
        outputName += '.' + ext

    if not repseqs:
        repseqs = fs.join(os.path.dirname(data), outputName)
    else:
        if fs.isdir(repseqs):
            repseqs = fs.join(repseqs, outputName)

    if fs.exists(repseqs):
        repseqs = fs.unique_filename(os.path.dirname(data), repseqs, ext)
    
    return paramindex, fs.normalize_path(repseqs)

def get_output_path_from_args(paramindex, fs, data, keyname, default, *args, **kwargs):
    repseqs=default
    if keyname in kwargs.keys():
        repseqs = kwargs[keyname]
    else:
        if len(args) > paramindex:
            repseqs = args[paramindex]
            paramindex +=1
    
    if not repseqs:
        repseqs = fs.join(os.path.dirname(data), repseqs)
        
    if fs.exists(repseqs):
        repseqs =  fs.make_unique_dir(os.path.dirname(repseqs))
    
    return paramindex, fs.normalize_path(repseqs)

def run_qiime_demux_single(context, *args, **kwargs):
    paramindex = 0

    paramindex, data = get_input_from_args(paramindex, 'data', *args, **kwargs)
    paramindex, barcode = get_input_from_args(paramindex, 'barcode', *args, **kwargs)
    paramindex, barcodeCol = get_input_from_args(paramindex, 'barcodeCol', *args, **kwargs)
    
    fs = Utility.fs_by_prefix_or_default(data)
    data = fs.normalize_path(data)
    barcode = fs.normalize_path(barcode)
    
    paramindex, output = get_output_filename_from_args(paramindex, fs, data, 'output', 'demux', 'qza', *args, **kwargs)

    cmdargs = ['demux', 'emp-single', '--i-seqs {0}'.format(data), '--m-barcodes-file {0}'.format(barcode), '--m-barcodes-column {0}'.format(barcodeCol), '--o-per-sample-sequences {0}'.format(output)]
    # add if you have any extra parameters, must be in same format as to be sent to qiime in command line.
    for arg in args[paramindex + 1:]:
        cmdargs.append(arg)
    
    return check_output_file_exists(fs, output, cmdargs, "qiime demux emp-single could not generate the file {0} due to error {1}")

def run_qiime_demux_summarize(context, *args, **kwargs):
    paramindex = 0
    paramindex, data = get_input_from_args(paramindex, 'data', *args, **kwargs)
    fs = Utility.fs_by_prefix_or_default(data)
    data = fs.normalize_path(data)
    
    paramindex, output = get_output_filename_from_args(paramindex, fs, data, 'output', Path(os.path.basename(data)).stem, 'qzv', *args, **kwargs)
        
    cmdargs = ['demux', 'summarize', '--i-data {0}'.format(data), '--o-visualization {0}'.format(output)]
    # add if you have any extra parameters, must be in same format as to be sent to qiime in command line.
    for arg in args[paramindex + 1:]:
        cmdargs.append(arg)
    
    return check_output_file_exists(fs, output, cmdargs, "qiime demux summarize could not generate the file {0} due to error {1}")

def run_qiime_metadata_tabulate(context, *args, **kwargs):
    paramindex = 0
    paramindex, data = get_input_from_args(paramindex, 'data', *args, **kwargs)
    fs = Utility.fs_by_prefix_or_default(data)
    data = fs.normalize_path(data)
    
    paramindex, output = get_output_filename_from_args(paramindex, fs, data, 'output', Path(os.path.basename(data)).stem, 'qzv', *args, **kwargs)
        
    cmdargs = ['metadata', 'tabulate', '--m-input-file {0}'.format(data), '--o-visualization {0}'.format(output)]
    # add if you have any extra parameters, must be in same format as to be sent to qiime in command line.
    for arg in args[paramindex + 1:]:
        cmdargs.append(arg)
    
    return check_output_file_exists(fs, output, cmdargs, "qiime metadata tabulate could not generate the file {0} due to error {1}")    

def run_qiime_deblur_visualize_stats(context, *args, **kwargs):
    paramindex = 0
    paramindex, data = get_input_from_args(paramindex, 'data', *args, **kwargs)
    fs = Utility.fs_by_prefix_or_default(data)
    data = fs.normalize_path(data)
    
    paramindex, output = get_output_filename_from_args(paramindex, fs, data, 'output', Path(os.path.basename(data)).stem, 'qzv', *args, **kwargs)
        
    cmdargs = ['deblur', 'visualize-stats', '--i-deblur-stats {0}'.format(data), '--o-visualization {0}'.format(output)]
    # add if you have any extra parameters, must be in same format as to be sent to qiime in command line.
    for arg in args[paramindex + 1:]:
        cmdargs.append(arg)
    
    return check_output_file_exists(fs, output, cmdargs, "qiime deblur visualize stats could not generate the file {0} due to error {1}")

def run_qiime_feature_table_summarize(context, *args, **kwargs):
    paramindex = 0
    paramindex, data = get_input_from_args(paramindex, 'data', *args, **kwargs)
    fs = Utility.fs_by_prefix_or_default(data)
    data = fs.normalize_path(data)
    
    paramindex, metadata = get_input_from_args(paramindex, 'metadata', *args, **kwargs)
    metadata = fs.normalize_path(metadata)
    
    paramindex, output = get_output_filename_from_args(paramindex, fs, data, 'output', Path(os.path.basename(data)).stem, 'qzv', *args, **kwargs)
        
    cmdargs = ['feature-table', 'summarize', '--i-table {0}'.format(data), '--o-visualization {0}'.format(output), '--m-sample-metadata-file {0}'.format(metadata)]
    # add if you have any extra parameters, must be in same format as to be sent to qiime in command line.
    for arg in args[paramindex + 1:]:
        cmdargs.append(arg)
        
    return check_output_file_exists(fs, output, cmdargs, "qiime feature-table summarize could not generate the file {0} due to error {1}")

def run_qiime_feature_table_tabulate_seqs(context, *args, **kwargs):
    paramindex = 0
    paramindex, data = get_input_from_args(paramindex, 'data', *args, **kwargs)
    fs = Utility.fs_by_prefix_or_default(data)
    data = fs.normalize_path(data)
    
    paramindex, output = get_output_filename_from_args(paramindex, fs, data, 'output', Path(os.path.basename(data)).stem, 'qzv', *args, **kwargs)
        
    cmdargs = ['feature-table', 'tabulate-seqs', '--i-data {0}'.format(data), '--o-visualization {0}'.format(output)]
    # add if you have any extra parameters, must be in same format as to be sent to qiime in command line.
    for arg in args[paramindex + 1:]:
        cmdargs.append(arg)
    
    return check_output_file_exists(fs, output, cmdargs, "qiime feature-table tabulate-seqs could not generate the file {0} due to error {1}")

def run_qiime_phylogeny_tree(context, *args, **kwargs):
    paramindex = 0
    paramindex, data = get_input_from_args(paramindex, 'data', *args, **kwargs)
    fs = Utility.fs_by_prefix_or_default(data)
    data = fs.normalize_path(data)
    
    paramindex, alignedSeqs = get_output_filename_from_args(paramindex, fs, data, 'alignseqs', 'alignseqs', 'qza', *args, **kwargs)
    paramindex, maskedAlignedSeqs = get_output_filename_from_args(paramindex, fs, data, 'maskseqs', 'maskseqs', 'qza', *args, **kwargs)
    paramindex, unrootedTree = get_output_filename_from_args(paramindex, fs, data, 'unrooted', 'unrooted', 'qza', *args, **kwargs)
    paramindex, rootedTree = get_output_filename_from_args(paramindex, fs, data, 'rooted', 'rooted', 'qza', *args, **kwargs)
        
    cmdargs = ['phylogeny', 'align-to-tree-mafft-fasttree', '--i-sequences {0}'.format(data), '--o-alignment {0}'.format(alignedSeqs), '--o-masked-alignment {0}'.format(maskedAlignedSeqs),'--o-tree {0}'.format(unrootedTree),'--o-rooted-tree {0}'.format(rootedTree)]
    # add if you have any extra parameters, must be in same format as to be sent to qiime in command line.
    for arg in args[paramindex + 1:]:
        cmdargs.append(arg)
    
    return check_output_file_exists(fs, [alignedSeqs, maskedAlignedSeqs, unrootedTree, rootedTree], cmdargs, "qiime phylogeny align-to-tree-mafft-fasttree could not generate the file {0} due to error {1}")

def run_qiime_diversity_core_metrics(context, *args, **kwargs):
    paramindex = 0
    paramindex, data = get_input_from_args(paramindex, 'data', *args, **kwargs)
    fs = Utility.fs_by_prefix_or_default(data)
    data = fs.normalize_path(data)
    
    paramindex, table = get_input_from_args(paramindex, 'table', *args, **kwargs)
    table = fs.normalize_path(table)
    
    paramindex, metadata = get_input_from_args(paramindex, 'metadata', *args, **kwargs)
    metadata = fs.normalize_path(metadata)
    
    paramindex, samplingdepth = get_input_from_args_optional(paramindex, 'sampling', str(1109), *args, **kwargs)
    samplingdepth = str(samplingdepth)
    
    paramindex, output = get_output_path_from_args(paramindex, fs, data, 'outpath', os.path.join(os.path.dirname(data), 'core-metrics-results'), *args, **kwargs)
        
    cmdargs = ['diversity ', 'core-metrics-phylogenetic', '--i-phylogeny {0}'.format(data), '--i-table {0}'.format(table), '--m-metadata-file {0}'.format(metadata), '--p-sampling-depth {0}'.format(samplingdepth), '--output-dir {0}'.format(output)]
    # add if you have any extra parameters, must be in same format as to be sent to qiime in command line.
    for arg in args[paramindex + 1:]:
        cmdargs.append(arg)
    return check_output_file_exists(fs, output, cmdargs, "qiime diversity core metrics could not generate the file {0} due to error {1}")

def run_qiime_diversity_alpha_significance(context, *args, **kwargs):
    paramindex = 0
    paramindex, data = get_input_from_args(paramindex, 'data', *args, **kwargs)
    fs = Utility.fs_by_prefix_or_default(data)
    data = fs.normalize_path(data)
    
    paramindex, metadata = get_input_from_args(paramindex, 'metadata', *args, **kwargs)
    metadata = fs.normalize_path(metadata)
    
    paramindex, output = get_output_filename_from_args(paramindex, fs, data, 'output', Path(os.path.basename(data)).stem + "-group-significance", 'qzv', *args, **kwargs)
        
    cmdargs = ['diversity ', 'alpha-group-significance', '--i-alpha-diversity {0}'.format(data), '--m-metadata-file {0}'.format(metadata), '--o-visualization {0}'.format(output)]
    # add if you have any extra parameters, must be in same format as to be sent to qiime in command line.
    for arg in args[paramindex + 1:]:
        cmdargs.append(arg)
    return check_output_file_exists(fs, output, cmdargs, "qiime diversity alpha-group-significance could not generate the file {0} due to error {1}")
    

def run_qiime_diversity_beta_significance(context, *args, **kwargs):
    paramindex = 0
    paramindex, data = get_input_from_args(paramindex, 'data', *args, **kwargs)
    fs = Utility.fs_by_prefix_or_default(data)
    data = fs.normalize_path(data)
    
    paramindex, metadata = get_input_from_args(paramindex, 'metadata', *args, **kwargs)
    metadata = fs.normalize_path(metadata)
    paramindex, metadataCol = get_input_from_args(paramindex, 'metadataCol', *args, **kwargs)
    
    paramindex, output = get_output_filename_from_args(paramindex, fs, data, 'output', "{0}_{1}_{2}".format(Path(os.path.basename(data)).stem, metadataCol, "significance"), 'qzv', *args, **kwargs)
        
    cmdargs = ['diversity ', 'beta-group-significance', '--i-distance-matrix {0}'.format(data), '--m-metadata-file {0}'.format(metadata), '--m-metadata-column {0}'.format(metadataCol), '--p-pairwise', '--o-visualization {0}'.format(output)]
    # add if you have any extra parameters, must be in same format as to be sent to qiime in command line.
    for arg in args[paramindex + 1:]:
        cmdargs.append(arg)
    return check_output_file_exists(fs, output, cmdargs, "qiime diversity beta-group-significance could not generate the file {0} due to error {1}")

def run_qiime_emperor_plot(context, *args, **kwargs):
    paramindex = 0
    paramindex, data = get_input_from_args(paramindex, 'data', *args, **kwargs)
    fs = Utility.fs_by_prefix_or_default(data)
    data = fs.normalize_path(data)
    
    paramindex, metadata = get_input_from_args(paramindex, 'metadata', *args, **kwargs)
    metadata = fs.normalize_path(metadata)
    paramindex, customAxes = get_input_from_args(paramindex, 'customAxes', *args, **kwargs)
    
    paramindex, output = get_output_filename_from_args(paramindex, fs, data, 'output', "{0}_{1}_{2}".format(Path(os.path.basename(data)).stem, "emperor", customAxes), 'qzv', *args, **kwargs)
        
    cmdargs = ['emperor', 'plot', '--i-pcoa {0}'.format(data), '--m-metadata-file {0}'.format(metadata), '--p-custom-axes {0}'.format(customAxes), '--o-visualization {0}'.format(output)]
    # add if you have any extra parameters, must be in same format as to be sent to qiime in command line.
    for arg in args[paramindex + 1:]:
        cmdargs.append(arg)
    
    return check_output_file_exists(fs, output, cmdargs, "qiime emperor plot could not generate the file {0} due to error {1}")

def run_qiime_diversity_alpha_rarefaction(context, *args, **kwargs):
    paramindex = 0
    paramindex, data = get_input_from_args(paramindex, 'data', *args, **kwargs)
    fs = Utility.fs_by_prefix_or_default(data)
    data = fs.normalize_path(data)
    
    paramindex, table = get_input_from_args(paramindex, 'table', *args, **kwargs)
    table = fs.normalize_path(table)
    paramindex, metadata = get_input_from_args(paramindex, 'metadata', *args, **kwargs)
    metadata = fs.normalize_path(metadata)
    paramindex, maxDepth = get_input_from_args(paramindex, 'maxDepth', *args, **kwargs)
    paramindex, minDepth = get_input_from_args_optional(paramindex, 'minDepth', None, *args, **kwargs)
    
    paramindex, output = get_output_filename_from_args(paramindex, fs, data, 'output', '{0}-{1}'.format(Path(os.path.basename(data)).stem, 'alpha-rarefaction'), 'qzv', *args, **kwargs)

    cmdargs = ['diversity ', 'alpha-rarefaction', '--i-phylogeny {0}'.format(data), '--i-table {0}'.format(table), '--p-max-depth {0}'.format(maxDepth), '--m-metadata-file {0}'.format(metadata), '--o-visualization {0}'.format(output)]
    if minDepth:
        cmdargs.append('--p-min-depth {0}'.format(minDepth))
        
    # add if you have any extra parameters, must be in same format as to be sent to qiime in command line.
    for arg in args[paramindex + 1:]:
        cmdargs.append(arg)
    
    return check_output_file_exists(fs, output, cmdargs, "qiime diversity alpha-rarefaction could not generate the file {0} due to error {1}")

def run_qiime_feature_classifier_classify_sklearn(context, *args, **kwargs):
    paramindex = 0
    paramindex, data = get_input_from_args(paramindex, 'data', *args, **kwargs)
    fs = Utility.fs_by_prefix_or_default(data)
    data = fs.normalize_path(data)
    
    paramindex, classifier = get_input_from_args(paramindex, 'classifier', *args, **kwargs)
    classifier = fs.normalize_path(classifier)
    
    paramindex, output = get_output_filename_from_args(paramindex, fs, data, 'output', 'taxonomy', 'qza', *args, **kwargs)

    cmdargs = ['feature-classifier', 'classify-sklearn', '--i-reads {0}'.format(data), '--i-classifier {0}'.format(classifier), '--o-classification {0}'.format(output)]
    # add if you have any extra parameters, must be in same format as to be sent to qiime in command line.
    for arg in args[paramindex + 1:]:
        cmdargs.append(arg)
    
    return check_output_file_exists(fs, output, cmdargs, "qiime feature-classifier classify-sklearn could not generate the file {0} due to error {1}")

def run_qiime_taxa_barplot(context, *args, **kwargs):
    paramindex = 0
    paramindex, data = get_input_from_args(paramindex, 'data', *args, **kwargs)
    fs = Utility.fs_by_prefix_or_default(data)
    data = fs.normalize_path(data)
    
    paramindex, table = get_input_from_args(paramindex, 'table', *args, **kwargs)
    table = fs.normalize_path(table)
    paramindex, metadata = get_input_from_args(paramindex, 'metadata', *args, **kwargs)
    metadata = fs.normalize_path(metadata)
    
    paramindex, output = get_output_filename_from_args(paramindex, fs, data, 'output',  Path(os.path.basename(data)).stem + "-bar-plots", 'qzv', *args, **kwargs)

    cmdargs = ['taxa', 'barplot ', '--i-taxonomy {0}'.format(data), '--i-table {0}'.format(table), '--m-metadata-file {0}'.format(metadata), '--o-visualization {0}'.format(output)]
    # add if you have any extra parameters, must be in same format as to be sent to qiime in command line.
    for arg in args[paramindex + 1:]:
        cmdargs.append(arg)
        
    return check_output_file_exists(fs, output, cmdargs, "qiime taxa barplot could not generate the file {0} due to error {1}")

def run_qiime_taxa_collapse(context, *args, **kwargs):
    paramindex = 0
    paramindex, data = get_input_from_args(paramindex, 'data', *args, **kwargs)
    fs = Utility.fs_by_prefix_or_default(data)
    data = fs.normalize_path(data)
    
    paramindex, table = get_input_from_args(paramindex, 'table', *args, **kwargs)
    table = fs.normalize_path(table)
    paramindex, level = get_input_from_args(paramindex, 'level', *args, **kwargs)
    
    paramindex, output = get_output_filename_from_args(paramindex, fs, data, 'output', "{0}-{1}".format(Path(os.path.basename(data)).stem, level),'qza', *args, **kwargs)

    cmdargs = ['taxa', 'collapse ', '--i-taxonomy {0}'.format(data), '--i-table {0}'.format(table), '--p-level {0}'.format(level), '--o-collapsed-table {0}'.format(output)]
    # add if you have any extra parameters, must be in same format as to be sent to qiime in command line.
    for arg in args[paramindex + 1:]:
        cmdargs.append(arg)
    return check_output_file_exists(fs, output, cmdargs, "qiime taxa collapse could not generate the file {0} due to error {1}")

def run_qiime_feature_table_filter_samples(context, *args, **kwargs):
    paramindex = 0
    paramindex, data = get_input_from_args(paramindex, 'data', *args, **kwargs)
    fs = Utility.fs_by_prefix_or_default(data)
    data = fs.normalize_path(data)
    
    paramindex, metadata = get_input_from_args(paramindex, 'metadata', *args, **kwargs)
    metadata = fs.normalize_path(metadata)
    paramindex, where = get_input_from_args(paramindex, 'where', *args, **kwargs)
    
    paramindex, output = get_output_filename_from_args(paramindex, fs, data, 'output', Path(os.path.basename(data)).stem + "-filtered", 'qza', *args, **kwargs)

    cmdargs = ['feature-table', 'filter-samples', '--i-table {0}'.format(data), '--m-metadata-file {0}'.format(metadata), '--p-where {0}'.format(where), '--o-filtered-table {0}'.format(output)]
    # add if you have any extra parameters, must be in same format as to be sent to qiime in command line.
    for arg in args[paramindex + 1:]:
        cmdargs.append(arg)
    return check_output_file_exists(fs, output, cmdargs, "qiime feature-table filter-samples could not generate the file {0} due to error {1}")

def run_qiime_composition_add_pseudocount(context, *args, **kwargs):
    paramindex = 0
    paramindex, data = get_input_from_args(paramindex, 'table', *args, **kwargs)
    fs = Utility.fs_by_prefix_or_default(data)
    data = fs.normalize_path(data)
        
    paramindex, output = get_output_filename_from_args(paramindex, fs, data, 'output', Path(os.path.basename(data)).stem + "-composition", 'qza', *args, **kwargs)

    cmdargs = ['composition', 'add-pseudocount', '--i-table {0}'.format(data), '--o-composition-table {0}'.format(output)]
    # add if you have any extra parameters, must be in same format as to be sent to qiime in command line.
    for arg in args[paramindex + 1:]:
        cmdargs.append(arg)
    
    return check_output_file_exists(fs, output, cmdargs, "qiime composition add-pseudocount could not generate the file {0} due to error {1}")

def run_qiime_composition_ancom(context, *args, **kwargs):
    paramindex = 0
    paramindex, data = get_input_from_args(paramindex, 'data', *args, **kwargs)
    fs = Utility.fs_by_prefix_or_default(data)
    data = fs.normalize_path(data)
    
    paramindex, metadata = get_input_from_args(paramindex, 'metadata', *args, **kwargs)
    metadata = fs.normalize_path(metadata)

    paramindex, metadataCol = get_input_from_args(paramindex, 'metadataCol', *args, **kwargs)
    paramindex, output = get_output_filename_from_args(paramindex, fs, data, 'output', "{0}-{1}".format(Path(os.path.basename(data)).stem, metadataCol), 'qzv', *args, **kwargs)

    cmdargs = ['composition', 'ancom', '--i-table {0}'.format(data), '--m-metadata-file {0}'.format(metadata), '--m-metadata-column {0}'.format(metadataCol), '--o-visualization {0}'.format(output)]
    # add if you have any extra parameters, must be in same format as to be sent to qiime in command line.
    for arg in args[paramindex + 1:]:
        cmdargs.append(arg)
    
    return check_output_file_exists(fs, output, cmdargs, "qiime composition ancom could not generate the file {0} due to error {1}")

def run_qiime_dada2_denoise_single(context, *args, **kwargs):
    paramindex = 0
    paramindex, data = get_input_from_args(paramindex, 'data', *args, **kwargs)
    fs = Utility.fs_by_prefix_or_default(data)
    data = fs.normalize_path(data) 

    paramindex, trimleft = get_input_from_args_optional(paramindex, 'trimleft', *args, **kwargs)
    paramindex, trunclen = get_input_from_args_optional(paramindex, 'trunclen', *args, **kwargs)  
    paramindex, repseqs = get_output_filename_from_args(paramindex, fs, data, 'seqs', 'dada2-seqs', 'qza', *args, **kwargs)        
    paramindex, table = get_output_filename_from_args(paramindex, fs, data, 'table', 'dada2-table', 'qza', *args, **kwargs)
    paramindex, stats = get_output_filename_from_args(paramindex, fs, data, 'stats', 'dada2-stats', 'qza', *args, **kwargs)
                
    cmdargs = ['dada2', 'denoise-single', '--i-demultiplexed-seqs {0}'.format(data), '--p-trim-left {0}'.format(trimleft), '--p-trunc-len {0}'.format(trunclen), '--o-representative-sequences {0}'.format(repseqs), '--o-table {0}'.format(table), '--o-denoising-stats {0}'.format(stats)]
    # add if you have any extra parameters, must be in same format as to be sent to qiime in command line.
    for arg in args[paramindex + 1:]:
        cmdargs.append(arg)
                
    return check_output_file_exists(fs, [repseqs, table, stats], cmdargs, "qiime dada2 denoise-single could not generate the file {0} due to error {1}")
     
def run_qiime_deblur_denoise_16s(context, *args, **kwargs):
    paramindex, data = get_input_from_args(0, 'data', *args, **kwargs)
    fs = Utility.fs_by_prefix_or_default(data)
    data = fs.normalize_path(data)
        
    paramindex, trimlen = get_input_from_args_optional(paramindex, 'trimlen', *args, **kwargs)
    trimlen = str(trimlen)
    
    paramindex, repseqs = get_output_filename_from_args(paramindex, fs, data, 'seqs', 'deblur-seqs', 'qza', *args, **kwargs)        
    paramindex, table = get_output_filename_from_args(paramindex, fs, data, 'table', 'deblur-table', 'qza', *args, **kwargs)
    paramindex, stats = get_output_filename_from_args(paramindex, fs, data, 'stats', 'deblur-stats', 'qza', *args, **kwargs)
                    
    #cmdargs = ['deblur', 'denoise-16S', '--i-demultiplexed-seqs {0}'.format(data), '--p-trim-length {0}'.format(trimlen), '--o-representative-sequences {0}'.format(repseqs), '--o-table {0}'.format(table), '--p-sample-stats', '--o-stats {0}'.format(stats)]
    cmdargs = ['deblur', 'denoise-16S', '--i-demultiplexed-seqs', data, '--p-trim-length', trimlen, '--o-representative-sequences', repseqs, '--o-table', table, '--p-sample-stats', '--o-stats', stats]
    # add if you have any extra parameters, must be in same format as to be sent to qiime in command line.
    for arg in args[paramindex + 1:]:
        cmdargs.append(arg)

    return check_output_file_exists(fs, [repseqs, table, stats], cmdargs, "qiime deblur denoise-16S could not generate the file {0} due to error {1}")    

def run_qiime_quality_qscore(context, *args, **kwargs):
    paramindex, data = get_input_from_args(0, 'data', *args, **kwargs)
    fs = Utility.fs_by_prefix_or_default(data)
    data = fs.normalize_path(data)
    
    paramindex, repseqs = get_output_filename_from_args(paramindex, fs, data, 'seqs', 'filtered-seqs', 'qza', *args, **kwargs)
    paramindex, stats = get_output_filename_from_args(paramindex, fs, data, 'stats', 'filter-stats', 'qza', *args, **kwargs)
    
    cmdargs = ['quality-filter', 'q-score', '--i-demux {0}'.format(data), '--o-filtered-sequences {0}'.format(repseqs), '--o-filter-stats {0}'.format(stats)]
    # add if you have any extra parameters, must be in same format as to be sent to qiime in command line.
    for arg in args[paramindex + 1:]:
        cmdargs.append(arg)
    
    return check_output_file_exists(fs, [repseqs, stats], cmdargs, "qiime quality-filter q-score could not generate the file {0} due to error {1}")

def check_output_file_exists(fs, output, cmdargs, msg):
    _,err = func_exec_bash_stdout(qiime_runner, *cmdargs)
    if not output:
        return True
    if isinstance(output, list):
        stripped_paths = []
        for o in output:
            stripped_path = fs.strip_root(o)
            if not fs.exists(o):
                raise ValueError(msg.format(stripped_path, err))
            stripped_paths.append(stripped_path)
        return stripped_paths
    else:
        stripped_path = fs.strip_root(output)
        if not fs.exists(output):
            raise ValueError(msg.format(stripped_path, err))
        return stripped_path

def run_qiime_import(context, *args, **kwargs):
    paramindex, data = get_input_from_args(0, 'data', *args, **kwargs)
    fs = Utility.fs_by_prefix_or_default(data)
    data = fs.normalize_path(data)
    
    paramindex, data_type = get_input_from_args_optional(paramindex, 'type', 'EMPSingleEndSequences', *args, **kwargs)            
    paramindex, output = get_output_filename_from_args(paramindex, fs, data, 'output', '', 'qza', *args, **kwargs)
    
    cmdargs = ['tools', 'import', '--type {0}'.format(data_type), '--input-path {0}'.format(data), '--output-path {0}'.format(output)]
    # add if you have any extra parameters, must be in same format as to be sent to qiime in command line.
    for arg in args[paramindex + 1:]:
        cmdargs.append(arg)
    return check_output_file_exists(fs, output, cmdargs, "qiime import could not generate the file {0} due to error {1}")
    

def run_qiime_import_types(context, *args, **kwargs):
    cmdargs = ['tools', 'import', '--show-importable-types']
    out,_ = func_exec_bash_stdout(qiime_runner, *cmdargs)
    return out