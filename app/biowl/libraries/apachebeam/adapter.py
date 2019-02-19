import os
from os import path
from pathlib import Path
import uuid

from ...exechelper import func_exec_run
from ...fileop import PosixFileSystem
from ....util import Utility
from ....models import Runnable, User
from ...ssh import ssh_hadoop_command, scp_get, scp_put

# cluster = '206.12.102.75'
# user = 'hadoop'
# password = 'spark#2018'

cluster = '206.12.89.124'
user = 'hadoop'
password = 'sr-hadoop'
keyfile = '/home/phenodoop/.ssh/bananikey.pem'


cluster_big1 = 'sr-p2irc-big3.usask.ca'
user_big1 = 'spark'
password_big1 = 'sr-hadoop'


cluster_hdfs = 'hdfs://sr-p2irc-big1.usask.ca:8020'
spark_submit_app = 'spark-submit'
jar = "/home/phenodoop/phenoproc/app/biowl/libraries/apachebeam/lib/beamflows-bundled-spark.jar"


# {
#            "org": "SRLAB",
#            "package": "beam",
#            "module": "app.biowl.libraries.apachebeam.adapter",
#            "group": "Texts",
#            "level": "1",
#            "name":"CountWords",
#            "internal":"count_words",
#            "params":[  
#             {  
#                "name":"input",
#                "type":"string"
#             },
#             {  
#                "name":"output",
#                "type":"string"
#             } 
#             ],
#            "desc": "Count number of individual words in a document.",
#            "example": "beam.CountWords(input='/public/doc.txt', output='/public/counts')",
#            "runmode": "local"
#        },
# def count_words(*args, **kwargs):
#     
#     paramindex = 0
#     if 'input' in kwargs.keys():
#         inputfile = kwargs['input']
#     else:
#         if len(args) == paramindex:
#             raise ValueError("Argument 'input' missing.")
#         inputfile = args[paramindex]
#         paramindex +=1
#     
#     if 'output' in kwargs.keys():
#         output = kwargs['output']
#     else:
#         if len(args) == paramindex:
#             raise ValueError("Argument 'output' missing.")
#         output = args[paramindex]
#         paramindex +=1
#     
#     inputfile = Utility.get_normalized_path(inputfile)
#     output = Utility.get_normalized_path(output)
#     
#     args = ['-m', 'apache_beam.examples.wordcount', inputfile, output]
#     
#     _err, _ = run_apachebeam(args)
#     
#     fs = PosixFileSystem(Utility.get_rootdir(2))
#     stripped_path = fs.strip_root(output)
#     if not os.path.exists(output):
#         raise ValueError("CountWords could not generate the file " + stripped_path + " due to error: " + _err)
#     
#     return stripped_path

def copy_posix_file_to_cluster(data):
    # copy the data to cluster if it is a local file. HDFS file will be accessed by cluster directly
    if (Utility.fs_type_by_prefix(data) != 'hdfs'):
        raise ValueError("Apache beam works only on hdfs files.")
        
    if (Utility.fs_type_by_prefix(data) == 'posix'):
        data = Utility.get_normalized_path(data)
        remotepath = os.path.join('/home/phenodoop/phenoproc/storage/public/', os.path.basename(data))
        scp_put(cluster, user, password, data, remotepath)
        data = remotepath
    return data
        
def get_username(**kwargs):
    try:
        if 'context' in kwargs.keys():
            runnable_id = kwargs['context'].runnable
            runnable = Runnable.query.get(runnable_id)
            return User.query.get(runnable.user_id).username
    except:
        pass

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

def run_beam_quality(*args, **kwargs):
    paramindex = 0
    paramindex, data = get_input_from_args(paramindex, 'data', *args, **kwargs)
    if not data.startswith('hdfs://'):
        raise ValueError("Apache beam service runs only on HDFS file system.")

    outdir = ''
    if 'outdir' in kwargs.keys():
        outdir = kwargs['outdir']
    else:
        if len(args) > paramindex:
            outdir = args[paramindex]
            paramindex +=1
    
    if not outdir or not outdir.startswith('hdfs://'):
        username = get_username(**kwargs)
        outdir = os.path.join(os.path.dirname(data), username,  str(uuid.uuid4()))
                   
    runner = 'spark'
    if 'runner' in kwargs.keys():
        runner = kwargs['runner']
    else:
        if len(args) > paramindex:
            runner = args[paramindex]
            paramindex +=1

    outpath = outdir
    ext = Path(data).suffix
    # is it a filename
    if ext and (ext == '.fq' or ext == '.fastq'):
        outpath = os.path.join(outdir, Path(data).stem + "_fastqc.html")

    ssh_cmd = ''
    if runner == 'spark':
        ssh_cmd = "spark-submit --class edu.usask.srlab.biowl.beam.CheckQ --master yarn --deploy-mode cluster --driver-memory 4g --executor-memory 4g --executor-cores 4 {0} --inputFile={1} --outDir={2} --runner=SparkRunner".format(jar, data, outdir)
    else:
        #ssh_cmd = "mvn compile exec:java -Dexec.mainClass=edu.usask.srlab.biowl.beam.CheckQ -Dexec.args='--inputFile={0} {1}' -Pdirect-runner".format(data, cmd_outdir)
        ssh_cmd = "java -cp /home/phenodoop/phenoproc/app/biowl/libraries/apachebeam/lib/beamflows-bundled-spark.jar edu.usask.srlab.biowl.beam.CheckQ --inputFile={0} {1}".format(data, outdir)
    
    ssh_hadoop_command(cluster, user, keyfile, ssh_cmd)
           
    return outpath


def run_beam_align(*args, **kwargs):
    
    paramindex = 0
    ref = ''
    if 'ref' in kwargs.keys():
        ref = kwargs['ref']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument error")
        ref = args[paramindex]
        paramindex +=1
    
    fs = None
    destpath = None
    if Utility.fs_type_by_prefix(ref) != 'hdfs':
        fssrc = Utility.fs_by_prefix_or_default(ref)
        fs = Utility.fs_by_prefix(cluster_hdfs)
        username = get_username(**kwargs)
        destpath = fs.makedirs(os.path.join(username, str(uuid.uuid4())))
        srcpath = ref
        ref = fs.join(destpath, os.path.basename(ref))
        fs.write(ref, fssrc.read(srcpath))
    else:
        fs = Utility.fs_by_prefix(ref)
    
    data1 = ''
    if 'data1' in kwargs.keys():
        data1 = kwargs['data1']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument error")
        data1 = args[paramindex]
        paramindex +=1
    
    if Utility.fs_type_by_prefix(data1) != 'hdfs':
        fssrc = Utility.fs_by_prefix_or_default(data1)
        if not destpath:
            username = get_username(**kwargs)
            destpath = fs.makedirs(os.path.join(username, str(uuid.uuid4())))
        srcpath = data1
        data1 = fs.join(destpath, os.path.basename(data1))
        fs.write(data1, fssrc.read(srcpath))
    
    output = ''
    data2 = ''
    if fs.isfile(data1):
        
        if 'data2' in kwargs.keys():
            data2 = kwargs['data2']
        else:
            if len(args) > paramindex:
                data2 = args[paramindex]
                paramindex +=1
          
        if data2 and Utility.fs_type_by_prefix(data2) != 'hdfs':
            fssrc = Utility.fs_by_prefix_or_default(data2)
            if not destpath:
                username = get_username(**kwargs)
                destpath = fs.makedirs(os.path.join(username, str(uuid.uuid4())))
            srcpath = data2
            data2 = fs.join(destpath, os.path.basename(data2))
            fs.write(data2, fssrc.read(srcpath))
            
        if 'output' in kwargs.keys():
            output = kwargs['output']
        else:
            if len(args) > paramindex:
                output = args[paramindex]
                paramindex +=1
    
        outdir = ''
        if not output or Utility.fs_type_by_prefix(output) != 'hdfs':
            if destpath:
                outdir = destpath
            else:
                username = get_username(**kwargs)
                outdir = os.path.join(username,  str(uuid.uuid4()))
        else:
            if fs.isdir(output):
                outdir = output
                output = ''
    
        if outdir and not fs.exists(outdir):
            fs.makedirs(outdir)
        
        if outdir:
            output = os.path.join(outdir, Path(data1).stem + ".sam")        
    else:
        if 'output' in kwargs.keys():
            output = kwargs['output']
        else:
            if len(args) > paramindex:
                output = args[paramindex]
                paramindex +=1
    
        if not output or Utility.fs_type_by_prefix(output) != 'hdfs':
            if destpath:
                output = destpath
            else:
                username = get_username(**kwargs)
                output = os.path.join(username,  str(uuid.uuid4()))
    
        if output and not fs.exists(output):
            fs.makedirs(output)
            
    ref = fs.normalize_fullpath(ref)
    data1 = fs.normalize_fullpath(data1)
    if data2:
        data2 = fs.normalize_fullpath(data2)
    output = fs.normalize_fullpath(output)

    runner = 'spark'
    if 'runner' in kwargs.keys():
        runner = kwargs['runner']
    else:
        if len(args) > paramindex:
            runner = args[paramindex]
            paramindex +=1

    ssh_cmd = ''
    if runner == 'spark':
        if data2:
            ssh_cmd = "spark-submit --class edu.usask.srlab.biowl.beam.Alignment --master yarn --deploy-mode cluster --driver-memory 4g --executor-memory 4g  --executor-cores 4 {0} --referenceFile={1} --input1File={2} --input2File={3} --output={4} --runner=SparkRunner".format(jar, ref, data1, data2, output)
        else:
            ssh_cmd = "spark-submit --class edu.usask.srlab.biowl.beam.Alignment --master yarn --deploy-mode cluster --driver-memory 4g --executor-memory 4g  --executor-cores 4 {0} --referenceFile={1} --input1File={2} --output={3}  --runner=SparkRunner".format(jar, ref, data1, output)
    else:
        ssh_cmd = "mvn compile exec:java -Dexec.mainClass=edu.usask.srlab.biowl.beam.Alignment -Dexec.args='--inputFile={0} {1}' -Pdirect-runner".format(ref, data1, data2, output)
    
    kwargs['context'].out.append(ssh_cmd)
    ssh_hadoop_command(cluster, user, password, ssh_cmd)
    
    stripped_path = output
    if not fs.exists(stripped_path):
        raise ValueError("Apache beam could not generate the .sam file: " + stripped_path)
    
    return stripped_path

def run_beam_sam_to_bam(*args, **kwargs):
    
    paramindex = 0
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument missing error in sam2bam.")
        data = args[paramindex]
        paramindex +=1
        
    fs = None
    destpath = None
    if Utility.fs_type_by_prefix(data) != 'hdfs':
        fssrc = Utility.fs_by_prefix_or_default(data)
        fs = Utility.fs_by_prefix(cluster_hdfs)
        username = get_username(**kwargs)
        destpath = fs.makedirs(os.path.join(username, str(uuid.uuid4())))
        srcpath = data
        data = fs.join(destpath, os.path.basename(data))
        fs.write(data, fssrc.read(srcpath))
    else:
        fs = Utility.fs_by_prefix(data)
    
    output = ''
    if 'output' in kwargs.keys():
        output = kwargs['output']
    else:
        if len(args) > paramindex:
            output = args[paramindex]
            paramindex +=1

    outdir = ''
    if not output or Utility.fs_type_by_prefix(output) != 'hdfs':
        if destpath:
            outdir = destpath
        else:
            username = get_username(**kwargs)
            outdir = os.path.join(username,  str(uuid.uuid4()))
    else:
        if fs.isdir(output):
            outdir = output
            output = ''

    if outdir and not fs.exists(outdir):
        fs.makedirs(outdir)
    
    if fs.isfile(data):
        if outdir:
            output = os.path.join(outdir, Path(data).stem + ".bam")
    else:
        if outdir:
            output = outdir
        elif output:
            if not fs.exists(output):
                fs.makedirs(output)
            elif fs.isfile(output):
                output = os.path.dirname(output)
        else:
            raise ValueError("Output path can't be found.")
            
    data = fs.normalize_fullpath(data)
    output = fs.normalize_fullpath(output)
    
    runner = 'spark'
    if 'runner' in kwargs.keys():
        runner = kwargs['runner']
    else:
        if len(args) > paramindex:
            runner = args[paramindex]
            paramindex +=1
    
    ssh_cmd = ''                   
    if runner == 'spark':
        ssh_cmd = "spark-submit --class edu.usask.srlab.biowl.beam.Convert --master yarn --deploy-mode cluster --driver-memory 4g --executor-memory 4g  --executor-cores 4 {0} --input={1} --output={2} --convertType=sam2bam --runner=SparkRunner".format(jar, data, output)
    
    ssh_hadoop_command(cluster, user, password, ssh_cmd)
    
    stripped_path = output
    if not fs.exists(stripped_path):
        raise ValueError("Apache beam could not generate the .bam  " + stripped_path)
    
    return stripped_path

def run_beam_pear(*args, **kwargs):
    
    paramindex = 0
    data1 = ''
    if 'data' in kwargs.keys():
        data1 = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("Argument missing error in apache beam merge: data.")
        data1 = args[paramindex]
        paramindex +=1
    
    fs = None
    destpath = None
    if Utility.fs_type_by_prefix(data1) != 'hdfs':
        fssrc = Utility.fs_by_prefix_or_default(data1)
        username = get_username(**kwargs)
        fs = Utility.fs_by_prefix(cluster_hdfs)
        destpath = fs.makedirs(os.path.join(username, str(uuid.uuid4())))
        srcpath = data1
        data1 = fs.join(destpath, os.path.basename(data1))
        fs.write(data1, fssrc.read(srcpath))
    else:
        fs = Utility.fs_by_prefix(data1)
            
    data2 = ''
    if 'data2' in kwargs.keys():
        data2 = kwargs['data2']
    else:
        if len(args) <= paramindex:
            raise ValueError("Argument missing error in apache beam merge: data2.")
        data2 = args[paramindex]
        paramindex +=1
      
    if Utility.fs_type_by_prefix(data2) != 'hdfs':
        fssrc = Utility.fs_by_prefix_or_default(data2)
        if not destpath:
            username = get_username(**kwargs)
            destpath = fs.makedirs(os.path.join(username, str(uuid.uuid4())))
        srcpath = data2
        data2 = fs.join(destpath, os.path.basename(data2))
        fs.write(data2, fssrc.read(srcpath))
        
    output = ''
    if 'output' in kwargs.keys():
        output = kwargs['output']
    else:
        if len(args) > paramindex:
            output = args[paramindex]
            paramindex +=1

    outdir = ''
    if not output or Utility.fs_type_by_prefix(output) != 'hdfs':
        if destpath:
            outdir = destpath
        else:
            username = get_username(**kwargs)
            outdir = os.path.join(username,  str(uuid.uuid4()))
    else:
        if fs.isdir(output):
            outdir = output
            output = ''

    if outdir and not fs.exists(outdir):
        fs.makedirs(outdir)
        
    data1_path = Path(os.path.basename(data1))
    output = os.path.join(outdir, data1_path.stem)    
        
    assembled_output = output + ".assembled" + data1_path.suffix
    if fs.exists(assembled_output):
        fs.remove(assembled_output)
    
    data1 = fs.normalize_fullpath(data1)
    data2 = fs.normalize_fullpath(data2)
    output = fs.normalize_fullpath(output)
    
    runner = 'spark'
    if 'runner' in kwargs.keys():
        runner = kwargs['runner']
    else:
        if len(args) > paramindex:
            runner = args[paramindex]
            paramindex +=1
            
    if runner == 'spark':
        ssh_cmd = "spark-submit --class edu.usask.srlab.biowl.beam.Merge --master yarn --deploy-mode cluster --driver-memory 4g --executor-memory 4g  --executor-cores 4 {0} --input1File={1} --input2File={2} --output={3} --runner=SparkRunner".format(jar, data1, data2, output)
    
    ssh_hadoop_command(cluster, user, password, ssh_cmd)
    
    stripped_path = fs.normalize_fullpath(assembled_output)
    if not fs.exists(stripped_path):
        raise ValueError("Apache beam could not generate the merged file." + stripped_path)
    
    return stripped_path
     
def run_beam_quality_big1(*args, **kwargs):
    
    paramindex = 0
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument missing error in FastQC.")
        data = args[paramindex]
        paramindex +=1
    
    fs = None
    destpath = None
    if Utility.fs_type_by_prefix(data) != 'hdfs':
        fssrc = Utility.fs_by_prefix_or_default(data)
        fs = Utility.fs_by_prefix(cluster_hdfs)
        username = get_username(**kwargs)
        destpath = fs.makedirs(os.path.join(username, str(uuid.uuid4())))
        srcpath = data
        data = fs.join(destpath, os.path.basename(data))
        fs.write(data, fssrc.read(srcpath))
    else:
        fs = Utility.fs_by_prefix(data)

    outdir = ''
    if 'outdir' in kwargs.keys():
        outdir = kwargs['outdir']
    else:
        if len(args) > paramindex:
            outdir = args[paramindex]
            paramindex +=1
    
    if not outdir or Utility.fs_type_by_prefix(outdir) != 'hdfs':
        if destpath:
            outdir = destpath
        else:
            username = get_username(**kwargs)
            outdir = os.path.join(username,  str(uuid.uuid4()))
        
    if not fs.exists(outdir):
        fs.makedirs(outdir)
            
    runner = 'spark'
    if 'runner' in kwargs.keys():
        runner = kwargs['runner']
    else:
        if len(args) > paramindex:
            runner = args[paramindex]
            paramindex +=1

    data = fs.normalize_fullpath(data)
    outdir = fs.normalize_fullpath(outdir)

    outpath = outdir
    if fs.isfile(data):
        outpath = Path(data).stem + "_fastqc.html"
        outpath = fs.join(outdir, os.path.basename(outpath))
        if fs.exists(outpath):
            fs.remove(outpath)

    ssh_cmd = ''    
    if runner == 'spark':
        ssh_cmd = "spark-submit --class edu.usask.srlab.biowl.beam.CheckQ --master yarn --deploy-mode cluster --driver-memory 4g --executor-memory 4g --executor-cores 4 {0} --inputFile={1} --outDir={2} --runner=SparkRunner".format(jar, data, outdir)
    else:
        #ssh_cmd = "mvn compile exec:java -Dexec.mainClass=edu.usask.srlab.biowl.beam.CheckQ -Dexec.args='--inputFile={0} {1}' -Pdirect-runner".format(data, cmd_outdir)
        ssh_cmd = "java -cp /home/phenodoop/phenoproc/app/biowl/libraries/apachebeam/lib/beamflows-bundled-spark.jar edu.usask.srlab.biowl.beam.CheckQ --inputFile={0} {1}".format(data, outdir)
    
    ssh_hadoop_command(cluster, user, password, ssh_cmd)
           
    if not fs.exists(outpath):
        raise ValueError("Check quality beam could not generate the file: " + outpath)
    
    # #     if (Utility.fs_type_by_prefix(data) == 'posix'):
# #         if outdir:
# #             outdir = Utility.get_normalized_path(outdir)
# #         else:
# #             outdir = path.dirname(data)
# # 
# #         if not os.path.exists(outdir):
# #             os.makedirs(outdir)
# # 
# #         scp_get(cluster, user, password, outpath, outdir)
# #     
# #         fs = Utility.fs_by_prefix_or_default(outpath)
#         
#     stripped_path = fs.strip_root(outpath)

    return outpath


def run_beam_align_big1(*args, **kwargs):
    
    paramindex = 0
    ref = ''
    if 'ref' in kwargs.keys():
        ref = kwargs['ref']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument error")
        ref = args[paramindex]
        paramindex +=1
    
    fs = None
    destpath = None
    if Utility.fs_type_by_prefix(ref) != 'hdfs':
        fssrc = Utility.fs_by_prefix_or_default(ref)
        fs = Utility.fs_by_prefix(cluster_hdfs)
        username = get_username(**kwargs)
        destpath = fs.makedirs(os.path.join(username, str(uuid.uuid4())))
        srcpath = ref
        ref = fs.join(destpath, os.path.basename(ref))
        fs.write(ref, fssrc.read(srcpath))
    else:
        fs = Utility.fs_by_prefix(ref)
    
    data1 = ''
    if 'data1' in kwargs.keys():
        data1 = kwargs['data1']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument error")
        data1 = args[paramindex]
        paramindex +=1
    
    if Utility.fs_type_by_prefix(data1) != 'hdfs':
        fssrc = Utility.fs_by_prefix_or_default(data1)
        if not destpath:
            username = get_username(**kwargs)
            destpath = fs.makedirs(os.path.join(username, str(uuid.uuid4())))
        srcpath = data1
        data1 = fs.join(destpath, os.path.basename(data1))
        fs.write(data1, fssrc.read(srcpath))
    
    output = ''
    data2 = ''
    if fs.isfile(data1):
        
        if 'data2' in kwargs.keys():
            data2 = kwargs['data2']
        else:
            if len(args) > paramindex:
                data2 = args[paramindex]
                paramindex +=1
          
        if data2 and Utility.fs_type_by_prefix(data2) != 'hdfs':
            fssrc = Utility.fs_by_prefix_or_default(data2)
            if not destpath:
                username = get_username(**kwargs)
                destpath = fs.makedirs(os.path.join(username, str(uuid.uuid4())))
            srcpath = data2
            data2 = fs.join(destpath, os.path.basename(data2))
            fs.write(data2, fssrc.read(srcpath))
            
        if 'output' in kwargs.keys():
            output = kwargs['output']
        else:
            if len(args) > paramindex:
                output = args[paramindex]
                paramindex +=1
    
        outdir = ''
        if not output or Utility.fs_type_by_prefix(output) != 'hdfs':
            if destpath:
                outdir = destpath
            else:
                username = get_username(**kwargs)
                outdir = os.path.join(username,  str(uuid.uuid4()))
        else:
            if fs.isdir(output):
                outdir = output
                output = ''
    
        if outdir and not fs.exists(outdir):
            fs.makedirs(outdir)
        
        if outdir:
            output = os.path.join(outdir, Path(data1).stem + ".sam")        
    else:
        if 'output' in kwargs.keys():
            output = kwargs['output']
        else:
            if len(args) > paramindex:
                output = args[paramindex]
                paramindex +=1
    
        if not output or Utility.fs_type_by_prefix(output) != 'hdfs':
            if destpath:
                output = destpath
            else:
                username = get_username(**kwargs)
                output = os.path.join(username,  str(uuid.uuid4()))
    
        if output and not fs.exists(output):
            fs.makedirs(output)
            
    ref = fs.normalize_fullpath(ref)
    data1 = fs.normalize_fullpath(data1)
    if data2:
        data2 = fs.normalize_fullpath(data2)
    output = fs.normalize_fullpath(output)

    runner = 'spark'
    if 'runner' in kwargs.keys():
        runner = kwargs['runner']
    else:
        if len(args) > paramindex:
            runner = args[paramindex]
            paramindex +=1

    ssh_cmd = ''
    if runner == 'spark':
        if data2:
            ssh_cmd = "spark-submit --class edu.usask.srlab.biowl.beam.Alignment --master yarn --deploy-mode cluster --driver-memory 4g --executor-memory 4g  --executor-cores 4 {0} --referenceFile={1} --input1File={2} --input2File={3} --output={4} --runner=SparkRunner".format(jar, ref, data1, data2, output)
        else:
            ssh_cmd = "spark-submit --class edu.usask.srlab.biowl.beam.Alignment --master yarn --deploy-mode cluster --driver-memory 4g --executor-memory 4g  --executor-cores 4 {0} --referenceFile={1} --input1File={2} --output={3}  --runner=SparkRunner".format(jar, ref, data1, output)
    else:
        ssh_cmd = "mvn compile exec:java -Dexec.mainClass=edu.usask.srlab.biowl.beam.Alignment -Dexec.args='--inputFile={0} {1}' -Pdirect-runner".format(ref, data1, data2, output)
    
    kwargs['context'].out.append(ssh_cmd)
    ssh_hadoop_command(cluster, user, password, ssh_cmd)
    
    stripped_path = output
    if not fs.exists(stripped_path):
        raise ValueError("Apache beam could not generate the .sam file: " + stripped_path)
    
    return stripped_path

def run_beam_sam_to_bam_big1(*args, **kwargs):
    
    paramindex = 0
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument missing error in sam2bam.")
        data = args[paramindex]
        paramindex +=1
        
    fs = None
    destpath = None
    if Utility.fs_type_by_prefix(data) != 'hdfs':
        fssrc = Utility.fs_by_prefix_or_default(data)
        fs = Utility.fs_by_prefix(cluster_hdfs)
        username = get_username(**kwargs)
        destpath = fs.makedirs(os.path.join(username, str(uuid.uuid4())))
        srcpath = data
        data = fs.join(destpath, os.path.basename(data))
        fs.write(data, fssrc.read(srcpath))
    else:
        fs = Utility.fs_by_prefix(data)
    
    output = ''
    if 'output' in kwargs.keys():
        output = kwargs['output']
    else:
        if len(args) > paramindex:
            output = args[paramindex]
            paramindex +=1

    outdir = ''
    if not output or Utility.fs_type_by_prefix(output) != 'hdfs':
        if destpath:
            outdir = destpath
        else:
            username = get_username(**kwargs)
            outdir = os.path.join(username,  str(uuid.uuid4()))
    else:
        if fs.isdir(output):
            outdir = output
            output = ''

    if outdir and not fs.exists(outdir):
        fs.makedirs(outdir)
    
    if fs.isfile(data):
        if outdir:
            output = os.path.join(outdir, Path(data).stem + ".bam")
    else:
        if outdir:
            output = outdir
        elif output:
            if not fs.exists(output):
                fs.makedirs(output)
            elif fs.isfile(output):
                output = os.path.dirname(output)
        else:
            raise ValueError("Output path can't be found.")
            
    data = fs.normalize_fullpath(data)
    output = fs.normalize_fullpath(output)
    
    runner = 'spark'
    if 'runner' in kwargs.keys():
        runner = kwargs['runner']
    else:
        if len(args) > paramindex:
            runner = args[paramindex]
            paramindex +=1
    
    ssh_cmd = ''                   
    if runner == 'spark':
        ssh_cmd = "spark-submit --class edu.usask.srlab.biowl.beam.Convert --master yarn --deploy-mode cluster --driver-memory 4g --executor-memory 4g  --executor-cores 4 {0} --input={1} --output={2} --convertType=sam2bam --runner=SparkRunner".format(jar, data, output)
    
    ssh_hadoop_command(cluster, user, password, ssh_cmd)
    
    stripped_path = output
    if not fs.exists(stripped_path):
        raise ValueError("Apache beam could not generate the .bam  " + stripped_path)
    
    return stripped_path

def run_beam_pear_big1(*args, **kwargs):
    
    paramindex = 0
    data1 = ''
    if 'data' in kwargs.keys():
        data1 = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("Argument missing error in apache beam merge: data.")
        data1 = args[paramindex]
        paramindex +=1
    
    fs = None
    destpath = None
    if Utility.fs_type_by_prefix(data1) != 'hdfs':
        fssrc = Utility.fs_by_prefix_or_default(data1)
        username = get_username(**kwargs)
        fs = Utility.fs_by_prefix(cluster_hdfs)
        destpath = fs.makedirs(os.path.join(username, str(uuid.uuid4())))
        srcpath = data1
        data1 = fs.join(destpath, os.path.basename(data1))
        fs.write(data1, fssrc.read(srcpath))
    else:
        fs = Utility.fs_by_prefix(data1)
            
    data2 = ''
    if 'data2' in kwargs.keys():
        data2 = kwargs['data2']
    else:
        if len(args) <= paramindex:
            raise ValueError("Argument missing error in apache beam merge: data2.")
        data2 = args[paramindex]
        paramindex +=1
      
    if Utility.fs_type_by_prefix(data2) != 'hdfs':
        fssrc = Utility.fs_by_prefix_or_default(data2)
        if not destpath:
            username = get_username(**kwargs)
            destpath = fs.makedirs(os.path.join(username, str(uuid.uuid4())))
        srcpath = data2
        data2 = fs.join(destpath, os.path.basename(data2))
        fs.write(data2, fssrc.read(srcpath))
        
    output = ''
    if 'output' in kwargs.keys():
        output = kwargs['output']
    else:
        if len(args) > paramindex:
            output = args[paramindex]
            paramindex +=1

    outdir = ''
    if not output or Utility.fs_type_by_prefix(output) != 'hdfs':
        if destpath:
            outdir = destpath
        else:
            username = get_username(**kwargs)
            outdir = os.path.join(username,  str(uuid.uuid4()))
    else:
        if fs.isdir(output):
            outdir = output
            output = ''

    if outdir and not fs.exists(outdir):
        fs.makedirs(outdir)
        
    data1_path = Path(os.path.basename(data1))
    output = os.path.join(outdir, data1_path.stem)    
        
    assembled_output = output + ".assembled" + data1_path.suffix
    if fs.exists(assembled_output):
        fs.remove(assembled_output)
    
    data1 = fs.normalize_fullpath(data1)
    data2 = fs.normalize_fullpath(data2)
    output = fs.normalize_fullpath(output)
    
    runner = 'spark'
    if 'runner' in kwargs.keys():
        runner = kwargs['runner']
    else:
        if len(args) > paramindex:
            runner = args[paramindex]
            paramindex +=1
            
    if runner == 'spark':
        ssh_cmd = "spark-submit --class edu.usask.srlab.biowl.beam.Merge --master yarn --deploy-mode cluster --driver-memory 4g --executor-memory 4g  --executor-cores 4 {0} --input1File={1} --input2File={2} --output={3} --runner=SparkRunner".format(jar, data1, data2, output)
    
    ssh_hadoop_command(cluster, user, password, ssh_cmd)
    
    stripped_path = fs.normalize_fullpath(assembled_output)
    if not fs.exists(stripped_path):
        raise ValueError("Apache beam could not generate the merged file." + stripped_path)
    
    return stripped_path