from bioblend.galaxy import GalaxyInstance
from bioblend.galaxy.histories import HistoryClient
from bioblend.galaxy.tools import ToolClient
from bioblend.galaxy.jobs import JobsClient

from urllib.parse import urlparse, urlunparse
import urllib.request
import shutil
import json
import uuid
import tempfile
from ftplib import FTP
from collections import namedtuple
import os
import time

from app.util import Utility
from app.biowl.ssh import ssh_command
from app.biowl.fileop import GalaxyFileSystem

#gi = GalaxyInstance(url='http://sr-p2irc-big8.usask.ca:8080', key='7483fa940d53add053903042c39f853a')
#  r = toolClient.run_tool('a799d38679e985db', 'toolshed.g2.bx.psu.edu/repos/devteam/fastq_groomer/fastq_groomer/1.0.4', params)
srlab_galaxy = 'http://sr-p2irc-big8.usask.ca:8080'
srlab_key='7483fa940d53add053903042c39f853a'

galaxies = {}

#workflow      
def get_workflow_ids(*args, **kwargs):
    gi = create_galaxy_instance_context(**kwargs)
    wf = gi.workflows.get_workflows()
    wf_ids = []
    for j in wf:
        #yield j.name
        wf_ids.append(j['id'])
    return wf_ids

def get_workflow_info(*args, **kwargs):
    gi = create_galaxy_instance_context(**kwargs)
    workflow_info = gi.workflows.show_workflow(args[0])
    return workflow_info

def run_workflow(*args, **kwargs):
    history_id = get_or_create_history_context(**kwargs)
    gi = create_galaxy_instance_context(**kwargs)
    
    if len(args) < 1:
        raise ValueError("Parameter for workflow id is missing.")
    workflow_id = args[0]
    
    datamap = dict()
    for k,v in kwargs.items():
        if v:
            values = v.split("=")
            if len(values) == 2:
                datamap[k] = { 'src': str(values[0]), 'id':str(values[1]) }
                continue 
        datamap[k] = v
    
    return gi.workflows.run_workflow(workflow_id, dataset_map=datamap, history_id=history_id)

#history    
def get_history_ids(*args, **kwargs):
    gi = create_galaxy_instance_context(**kwargs)
    histories = gi.histories.get_histories()
    history_ids = []
    for h in histories:
        #yield j.name
        history_ids.append(h['id'])
    return history_ids

def get_history_info(*args, **kwargs):
    gi = create_galaxy_instance_context(**kwargs)
    histories = gi.histories.get_histories(history_id = args[0])
    return histories[0] if histories else None
  
def get_most_recent_history(*args, **kwargs):
    gi = create_galaxy_instance_context(**kwargs)
    hi = gi.histories.get_most_recently_used_history()
    return hi['id']
        
def history_id_to_name(*args, **kwargs):
    info = get_history_info(*args, **kwargs)
    if info:
        return info['name']

def history_name_to_ids(*args, **kwargs):
    gi = create_galaxy_instance_context(**kwargs)
    histories = gi.histories.get_histories(name = args[0])
    history_ids = []
    for history in histories:
        history_ids.append(history['id'])
    return history_ids

#tool        
def get_tool_ids(*args, **kwargs):
    gi = create_galaxy_instance_context(**kwargs)
    tools = gi.tools.get_tools()
    tool_ids = []
    for t in tools:
        #yield j.name
        tool_ids.append(t['id'])
    return tool_ids
   
def get_tool_info(*args, **kwargs):
    gi = create_galaxy_instance_context(**kwargs)
    tools = gi.tools.get_tools(tool_id = args[0])
    if tools:
        return tools[0]

def tool_id_to_name(*args, **kwargs):
    tool = get_tool_info(*args, **kwargs)
    if tool:
        return tool['name']
                             
def get_tool_params(*args, **kwargs):
    gi = create_galaxy_instance_context(**kwargs)
    ts = gi.tools.show_tool(tool_id = args[0], io_details=True)
    return ts[args[1]] if len(args) > 1 else ts
 
# dataset                                       
def get_history_datasets(*args, **kwargs):
    gi = create_galaxy_instance_context(**kwargs)
    historyid = args[0] if len(args) > 0 else get_most_recent_history(gi)
    name = args[1] if len(args) > 1 else None

    datasets = gi.histories.show_matching_datasets(historyid, name)
    ids = []
    for dataset in datasets:
        ids.append(dataset['id'])
    return ids
                          
def dataset_id_to_name(*args, **kwargs):
    gi = create_galaxy_instance_context(**kwargs)
    t = args[1] if len(args) > 1 else 'hda'
    info = gi.datasets.show_dataset(dataset_id = args[0], hda_ldda = t)
    if info:
        return info['name']

def dataset_name_to_ids(*args, **kwargs):
    gi = create_galaxy_instance_context(**kwargs)
    h = HistoryClient(gi)
    historyid = args[1] if len(args) > 1 else get_most_recent_history(gi)
    ds_infos = h.show_matching_datasets(historyid, args[0])
    ids = []
    for info in ds_infos:
        ids.append(info['id'])
    return ids
    
def upload_to_library_from_url(*args, **kwargs):
    gi = create_galaxy_instance_context(**kwargs)
    d = gi.libraries.upload_file_from_url(args[1], args[0])
    return d["id"]

def http_to_local_file(remote_name, destfile):
    with urllib.request.urlopen(remote_name) as response, open(destfile, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

def wait_for_job_completion(gi, job_id):
    jc = JobsClient(gi)
    state = jc.get_state(job_id)
    while state != 'error' and state != 'ok':
        time.sleep(0.5)
        state = jc.get_state(job_id)
        
    if state == 'error':
        raise ValueError("Error occurred during a Galaxy tool execution.")
    
    return jc.show_job(job_id)  
        
def ftp_download(u, destfile):       
    ftp = FTP(u.netloc)
    ftp.login()
    ftp.cwd(os.path.dirname(u.path))
    ftp.retrbinary("RETR " + os.path.basename(u.path), open(destfile, 'wb').write)

def temp_file_from_urlpath(u):
    filename = os.path.basename(u.path)   
    destfile = os.path.join(tempfile.gettempdir(), filename)
    if os.path.exists(destfile):
        os.remove(destfile)
    return destfile
    
def ssh_download(src, dest):
    wget_cmd = 'wget ' + src + ' -P ' + dest
    return ssh_command('sr-p2irc-big8.usask.ca', 'phenodoop', 'sr-hadoop', wget_cmd)

def get_installed_datatypes(*args, **kwargs):
    gi = create_galaxy_instance_context(**kwargs)
    return gi.datatypes.get_datatypes()

def get_installed_sniffers(*args, **kwargs):
    gi = create_galaxy_instance_context(**kwargs)
    return gi.datatypes.get_sniffers()

def get_op(prefix, opindex, argcount, *args, **kwargs):
    if prefix + str(opindex) in kwargs.keys():
        return kwargs[prefix + str(opindex)]
    else:
        if len(args) > argcount:
            return args[argcount]
        
def get_galaxy_server_context(dci):
    return dci[0] if len(dci) > 0 and dci[0] else srlab_galaxy

def get_galaxy_key_context(dci):
    return dci[1] if len(dci) > 1 and dci[1] else srlab_key

def get_galaxy_instance_context(server, key):
    if (server, key) in galaxies:
        return galaxies[(server, key)]
    
    gi = GalaxyInstance(server, key)
    galaxies[(server, key)] = gi
    return gi

def create_galaxy_instance_context_local(dci):
    return get_galaxy_instance_context(get_galaxy_server_context(dci), get_galaxy_key_context(dci))

def create_galaxy_instance_context(**kwargs):
    return create_galaxy_instance_context_local(kwargs['dci'] if 'dci' in kwargs.keys() else None)

def create_history(*args, **kwargs):
    gi = create_galaxy_instance_context(**kwargs)
    historyName = args[0] if len(args) > 0 else str(uuid.uuid4())
    h = gi.histories.create_history(historyName)    
    if 'context' in kwargs.keys():
        kwargs['context'].add_var('history_id', h["id"])       
    return h["id"]

def create_history_context(**kwargs):
    gi = create_galaxy_instance_context(**kwargs)
    historyName = str(uuid.uuid4())
    h = gi.histories.create_history(historyName)
    return h["id"]

def get_or_create_history_context(**kwargs):
    history_id = ''
    
    if 'history_id' in kwargs.keys():
        history_id = kwargs['history_id']
    else:
        context = kwargs['context'] if 'context' in kwargs.keys() else None
        if context and context.var_exists('history_id'):
            history_id = context.get_var('history_id')
        else:
            history_id = create_history_context(**kwargs)
            if context:
                context.add_var('history_id', history_id)
    
    return history_id

def fs_upload_context(local_file, **kwargs):
    gi = create_galaxy_instance_context(**kwargs)

    if 'library_id' in kwargs.keys() and kwargs['library_id'] is not None:
        return gi.libraries.upload_file_from_local_path(kwargs['library_id'], local_file)
    else:
        if 'history_id' in kwargs.keys() and kwargs['history_id'] is not None:
            history_id = kwargs['history_id']
        else:
            history_id = get_or_create_history_context(**kwargs)
            
        return gi.tools.upload_file(local_file, history_id) # waits till the update finis

def classic_ftp_upload_context(u, **kwargs):
    destfile = temp_file_from_urlpath(u)
    ftp_download(u, destfile)
    fs_upload_context(destfile, **kwargs)
        
def ftp_upload_context(u, **kwargs):
    src = urlunparse(list(u))
    #destDir = '/home/phenodoop/galaxy_import/' + str(uuid.uuid4())
    destDir = '/hadoop/galaxy/galaxy_import/' + str(uuid.uuid4())
    status = ssh_download(src, destDir)
    if status != 0:
        raise ValueError("ssh download failed.")
#     srcFTP = FTP(u.netloc)
#     srcFTP.login()
#     srcFTP.cwd(os.path.dirname(u.path))
#     srcFTP.voidcmd('TYPE I')
#     
#     destDir = str(uuid.uuid4())
    try:
#         destFTP = FTP("sr-p2irc-big8.usask.ca", 'phenodoop', 'sr-hadoop')
#         #destFTP.login()
#         
#         destFTP.cwd("galaxy_import")
#         destFTP.mkd(destDir)
#         destFTP.cwd(destDir)
#         destFTP.voidcmd('TYPE I')
#         
#         from_Sock = srcFTP.transfercmd("RETR " + os.path.basename(u.path))
#         to_Sock = destFTP.transfercmd("STOR " + os.path.basename(u.path))
#         
#         state = 0
#         while 1:
#             block = from_Sock.recv(1024)
#             if len(block) == 0:
#                 break
#             state += len(block)
#             while len(block) > 0:
#                 sentlen = to_Sock.send(block)
#                 block = block[sentlen:]     
#         
#         from_Sock.close()
#         to_Sock.close()
#         srcFTP.quit()
#         destFTP.quit()
        gi = create_galaxy_instance_context(**kwargs)
        if 'library_id' in kwargs.keys() and kwargs['library_id'] is not None:
            return gi.libraries.upload_file_from_server(kwargs['library_id'], destDir)
        else:
            # get/create a history first
            if 'history_id' in kwargs.keys() and kwargs['history_id'] is not None:
                history_id = kwargs['history_id']
            else:
                history_id = get_or_create_history_context(**kwargs)
            # get the import_dir library 
            libs = gi.libraries.get_libraries(name='import_dir')
            lib = libs[0] if libs else gi.libraries.create_library(name='import_dir')
            d = gi.libraries.upload_file_from_server(lib['id'], destDir)
            if d:
                dataset = gi.histories.upload_dataset_from_library(history_id, d[0]['id'])
                return dataset['id']
    except:
        return classic_ftp_upload_context(u, **kwargs)

def local_upload(*args, **kwargs):
    history_id = get_or_create_history_context(**kwargs)
    if not 'history_id' in kwargs.keys():
        kwargs['history_id'] = history_id

    paramindex = 0
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("No input dataset given.")
        data = args[paramindex]
 
    data_id = local_upload_context(data, **kwargs)
    return GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, data_id)
        
def local_upload_context(data, **kwargs):
    
    job = None
    fs_type = Utility.fs_type_by_prefix(data)
    if not fs_type:
        u = urlparse(data)
        
        if u.scheme:
            if u.scheme.lower() == 'http' or u.scheme.lower() == 'https':
                tempfile = temp_file_from_urlpath(u)
                http_to_local_file(data, tempfile)
                job = fs_upload_context(tempfile, **kwargs)
                return job['outputs'][0]['id']
            elif u.scheme.lower() == 'ftp':
                return ftp_upload_context(u, **kwargs) if get_galaxy_server_context(kwargs['dci'] if 'dci' in kwargs.keys() else None) == srlab_galaxy else classic_ftp_upload_context(u, **kwargs)
            else:
                raise ValueError('No http(s) or ftp addresses given.')

    fs = Utility.fs_by_prefix_or_guess(data)
    job = fs_upload_context(fs.normalize_path(data), **kwargs)
    return job['outputs'][0]['id']
    
def get_dataset_context(data, **kwargs):
    
    if Utility.fs_type_by_prefix(data) == "gfs":
        fs = Utility.fs_by_prefix_or_guess(data)
        hda_ldda = 'ldda' if fs.islibrarydata(data) else 'hda'
        return hda_ldda, os.path.basename(data)
    else:
        return 'hda', local_upload_context(data, **kwargs)

def local_run_tool_context(tool_id, inputs, **kwargs):
    gi = create_galaxy_instance_context(**kwargs)
    toolClient = ToolClient(gi)
    d = toolClient.run_tool(history_id=kwargs['history_id'], tool_id=tool_id, tool_inputs=inputs)
    job_info = wait_for_job_completion(gi, d['jobs'][0]['id'])
    return job_info#['outputs']['output_file']['id']
    
#{"tool_id":"toolshed.g2.bx.psu.edu/repos/devteam/fastqc/fastqc/0.70","tool_version":"0.70",
#"inputs":{"input_file":{"values":[{"src":"hda","name":"FASTQ Groomer on data 1","tags":[],"keep":false,"hid":26,"id":"d343a822bd747ee4"}],"batch":false},"contaminants":null,"limits":null}}
def run_fastqc(*args, **kwargs):    
    history_id = get_or_create_history_context(**kwargs)
    if not 'history_id' in kwargs.keys():
        kwargs['history_id'] = history_id
    
    paramindex = 0
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("No input dataset given.")
        data = args[paramindex]
        
    src, data_id = get_dataset_context(data, **kwargs)
    if data_id is None:
        raise ValueError("No dataset given. Give a dataset path")

    inputs = {
        "contaminants":'null',
        "limits":'null',
        "input_file":{
            "values":[{
                "src":src, 
                "id":data_id
                }]
            }
        }
    
    tool_id = 'toolshed.g2.bx.psu.edu/repos/devteam/fastqc/fastqc/0.72' #tool_name_to_id('FastQC')
    output = local_run_tool_context(tool_id, inputs, **kwargs)
    return GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, output['outputs']['html_file']['id'])


#===============================================================================
# run_bwa
# {"tool_id":"toolshed.g2.bx.psu.edu/repos/devteam/bwa/bwa/0.7.15.2","tool_version":"0.7.15.2",
# "inputs":{
#     "reference_source|reference_source_selector":"history",
#     "reference_source|ref_file":{
#         "values":[{
#             "src":"hda",
#             "name":"all.cDNA",
#             "tags":[],
#             "keep":false,
#             "hid":2,
#             "id":"0d72ca01c763d02d"}],
#         "batch":false},
#         "reference_source|index_a":"auto",
#         "input_type|input_type_selector":"paired",
#         "input_type|fastq_input1":{
#             "values":[{
#                 "src":"hda",
#                 "name":"FASTQ Groomer on data 1",
#                 "tags":[],
#                 "keep":false,
#                 "hid":10,
#                 "id":"4eb81b04b33684fd"}],
#             "batch":false
#         },
#     "input_type|fastq_input2":{
#         "values":[{
#             "src":"hda",
#             "name":"FASTQ Groomer on data 1",
#             "tags":[],
#             "keep":false,
#             "hid":11,
#             "id":"5761546ab79a71f2"}],
#         "batch":false
#     },
#     "input_type|adv_pe_options|adv_pe_options_selector":"do_not_set",
#     "rg|rg_selector":"do_not_set",
#     "analysis_type|analysis_type_selector":"illumina"
#     }
#===============================================================================
def run_bwa(*args, **kwargs):
    
    history_id = get_or_create_history_context(**kwargs)
    if not 'history_id' in kwargs.keys():
        kwargs['history_id'] = history_id

    paramindex = 0
    ref = ''
    if 'ref' in kwargs.keys():
        ref = kwargs['ref']
    else:
        if len(args) <= paramindex:
            raise ValueError("No dataset given for reference data. Give a dataset path.")
        ref = args[paramindex]
        paramindex +=1
            
    refsrc, refdata_id = get_dataset_context(ref, **kwargs)
    if not refdata_id:
        raise ValueError("No dataset given for reference data. Give a dataset path.")
    
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("No dataset given for read1 data. Give a dataset path.")
        data = args[paramindex]
        paramindex +=1
    datasrc, data_id = get_dataset_context(data, **kwargs)
    if not data_id:
        raise ValueError("No dataset given for read1 data. Give a dataset path.")
    
    data2 = ''
    if 'data2' in kwargs.keys():
        data2 = kwargs['data2']
    else:
        if len(args) > paramindex:
            data2 = args[paramindex]
            paramindex +=1
    
    data2src = ''
    data2_id = ''
    if data2:
        data2src, data2_id = get_dataset_context(data2, **kwargs)
        
    input_type = "paired" if data2_id else "single"
    
    input_name1 = "input_type|bam_input1" if 'datatype' in kwargs.keys() and kwargs['datatype'] == 'bam' else "input_type|fastq_input1"
    input_name2 = "input_type|bam_input2" if 'datatype' in kwargs.keys() and kwargs['datatype'] == 'bam' else "input_type|fastq_input2"
    
    inputs = {
     "reference_source|reference_source_selector":"history",
     "reference_source|ref_file":{
         "values":[{
             "src":refsrc,
#              "name":"all.cDNA",
             "tags":[],
#             "keep":False,
#              "hid":2,
             "id":refdata_id
             }],
         "batch":False
         },
        "reference_source|index_a":"auto",
         "input_type|input_type_selector":input_type,
         input_name1:{
             "values":[{
                 "src":datasrc,
#                 "name":"FASTQ Groomer on data 1",
                 "tags":[],
#                 "keep":False,
#                  "hid":10,
                 "id": data_id
                 }],
             "batch":False
         },
     "input_type|adv_pe_options|adv_pe_options_selector":"do_not_set",
     "rg|rg_selector":"do_not_set",
     "analysis_type|analysis_type_selector":"illumina"
     }
    
    if data2_id:
        inputs[input_name2] = {
         "values":[{
             "src":data2src,
#             "name":"FASTQ Groomer on data 1",
             "tags":[],
#             "keep":False,
#              "hid":11,
             "id": data2_id
             }],
         "batch":False
         }
    
    tool_id = 'toolshed.g2.bx.psu.edu/repos/devteam/bwa/bwa/0.7.15.2' #tool_name_to_id('Map with BWA')
    output = local_run_tool_context(tool_id, inputs, **kwargs)
    return GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, output['outputs']['bam_output']['id'])

#{"tool_id":"toolshed.g2.bx.psu.edu/repos/iuc/pear/iuc_pear/0.9.6.1","tool_version":"0.9.6.1",
def run_merge_pear(*args, **kwargs):
    
    history_id = get_or_create_history_context(**kwargs)
    if not 'history_id' in kwargs.keys():
        kwargs['history_id'] = history_id

    paramindex = 0
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("No dataset given for forward fastq  data. Give a dataset path.")
        data = args[paramindex]
        paramindex +=1
        
    datasrc, data_id = get_dataset_context(data, **kwargs)
    if not data_id:
        raise ValueError("No dataset given for forward fastq data. Give a dataset path.")
    
    data2 = ''
    if 'data2' in kwargs.keys():
        data2 = kwargs['data2']
    else:
        if len(args) <= paramindex:
            raise ValueError("No dataset given for reverse fastq  data. Give a dataset path.")
        data2 = args[paramindex]
        paramindex +=1
    
    data2src, data2_id = get_dataset_context(data2, **kwargs)
    if not data2_id:
        raise ValueError("No dataset given for reverse fastq  data. Give a dataset path.")
       
    inputs = {
    "library|type":"paired",
    "library|forward":{
        "values":[{
            "src":datasrc,
#             "name":"ex_min_reads.fq",
            "tags":[],
#             "keep":False,
#             "hid":1,
            "id":data_id
            }],
        "batch":False
        },
    "library|reverse":{
        "values":[{
            "src":data2src,
#            "name":"ex_min_reads.fq",
            "tags":[],
#            "keep":False,
#            "hid":1,
            "id":data2_id
            }],
        "batch":False
        },
    "pvalue":0.01,
    "min_overlap":10,
    "max_assembly_length":0,
    "min_assembly_length":50,
    "min_trim_length":1,
    "quality_threshold":0,
    "max_uncalled_base":1,
    "cap":40,
    "test_method":"1",
    "empirical_freqs":"false",
    "nbase":"false",
    "score_method":"2",
    "outputs":["assembled"]
    }
    
    tool_id = 'toolshed.g2.bx.psu.edu/repos/iuc/pear/iuc_pear/0.9.6.1' #tool_name_to_id('Map with BWA')
    output = local_run_tool_context(tool_id, inputs, **kwargs)
    return GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, output['outputs']['assembled_reads']['id'])
#{"outputs": [{"misc_blurb": "queued", "peek": "<table cellspacing=\"0\" cellpadding=\"3\"><\/table>", "update_time": "2018-08-30T18:55:33.682122", "data_type": "galaxy.datatypes.sequence.FastqSanger", "tags": [], "deleted": false, "s": null, "history_id": "92b83968e0b52980", "visible": true, "genome_build": "?", "create_time": "2018-08-30T18:55:33.539822", "hid": 34, "file_size": 0, "metadata_data_lines": null, "file_ext": "fastqsanger", "id": "1c35dae9a1f78ad6", "misc_info": null, "hda_ldda": "hda", "a": null, "history_content_type": "dataset", "name": "Pear on data 1: Assembled reads", "g": null, "uuid": "5f74e1f0-8b8b-4296-9866-14d4dd92349f", "metadata_sequences": null, "state": "new", "t": null, "model_class": "HistoryDatasetAssociation", "metadata_dbkey": "?", "output_name": "assembled_reads", "purged": false}], "implicit_collections": [], "jobs": [{"tool_id": "toolshed.g2.bx.psu.edu/repos/iuc/pear/iuc_pear/0.9.6.1", "update_time": "2018-08-30T18:55:33.677809", "exit_code": null, "state": "new", "create_time": "2018-08-30T18:55:33.677803", "model_class": "Job", "id": "1e1b36f0c148bdb9"}], "output_collections": []}

#{"tool_id":"toolshed.g2.bx.psu.edu/repos/devteam/bam_to_sam/bam_to_sam/2.0.1","tool_version":"2.0.1","inputs":{"input1":{"values":[{"src":"hda","name":"FastqToSam on data 2: reads as unaligned BAM","tags":[],"keep":false,"hid":4,"id":"1587e0955a89debb"}],"batch":false},"header":"-h"}}
def run_bam_to_sam(*args, **kwargs):
        
    history_id = get_or_create_history_context(**kwargs)
    if not 'history_id' in kwargs.keys():
        kwargs['history_id'] = history_id

    paramindex = 0
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("No input bam dataset given.")
        data = args[paramindex]
        paramindex +=1
        
    datasrc, data_id = get_dataset_context(data, **kwargs)
    if not data_id:
        raise ValueError("No input bam dataset given.")
    
    inputs = {
        "header":"-h",
        "input1":{
            "values":[{
                "src":datasrc, 
                "id":data_id
                }]
            }
        }
    
    tool_id = "toolshed.g2.bx.psu.edu/repos/devteam/bam_to_sam/bam_to_sam/2.0.1" #tool_name_to_id('FastQC')
    output = local_run_tool_context(tool_id, inputs, **kwargs)
    return GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, output['outputs']['output1']['id'])

#{"tool_id":"toolshed.g2.bx.psu.edu/repos/devteam/sam_to_bam/sam_to_bam/2.1.1","tool_version":"2.1.1","inputs":{"source|index_source":"history","source|input1":{"values":[{"src":"hda","name":"BAM-to-SAM on data 4: converted SAM","tags":[],"keep":false,"hid":5,"id":"c903e9d706700fc8"}],"batch":false},"source|ref_file":{"values":[{"src":"hda","name":"Chr1.cdna","tags":[],"keep":false,"hid":3,"id":"b7c1d0811979026c"}],"batch":false}}}
def run_sam_to_bam(*args, **kwargs):
    history_id = get_or_create_history_context(**kwargs)
    if not 'history_id' in kwargs.keys():
        kwargs['history_id'] = history_id

    paramindex = 0
    ref = ''
    if 'ref' in kwargs.keys():
        ref = kwargs['ref']
    else:
        if len(args) <= paramindex:
            raise ValueError("No dataset given for reference data. Give a dataset path.")
        ref = args[paramindex]
        paramindex +=1
            
    refsrc, refdata_id = get_dataset_context(ref, **kwargs)
    if not refdata_id:
        raise ValueError("No dataset given for reference data. Give a dataset path.")
    
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("No dataset given for read1 data. Give a dataset path.")
        data = args[paramindex]
        paramindex +=1
    datasrc, data_id = get_dataset_context(data, **kwargs)
    if not data_id:
        raise ValueError("No dataset given for read1 data. Give a dataset path.")
    
    inputs = {
        "source|index_source":"history",
        "source|input1":{
            "values":[{
                "src":datasrc,
                "id":data_id
                }]
            },
        "source|ref_file":{
            "values":[{
                "src":refsrc,
                "id":refdata_id
                }]
            }
        }

    tool_id = "toolshed.g2.bx.psu.edu/repos/devteam/sam_to_bam/sam_to_bam/2.1.1"
    output = local_run_tool_context(tool_id, inputs, **kwargs)
    return GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, output['outputs']['output1']['id'])
    #return output#['outputs']#['output1']['id']
    
#{"tool_id":"toolshed.g2.bx.psu.edu/repos/devteam/fastq_to_fasta/cshl_fastq_to_fasta/1.0.2","tool_version":"1.0.2",
#"inputs":{"input":{"values":[{"src":"hda","name":"F3D8_S196_L001_R2_001.fastq","tags":[],"keep":false,"hid":2,"id":"f82be65594961f87"}],"batch":false},"SKIPN":"","RENAMESEQ":"-r"}}
def run_fastq_to_fasta(*args, **kwargs):
        
    history_id = get_or_create_history_context(**kwargs)
    if not 'history_id' in kwargs.keys():
        kwargs['history_id'] = history_id

    paramindex = 0
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("No input fastq dataset given.")
        data = args[paramindex]
        paramindex +=1
        
    datasrc, data_id = get_dataset_context(data, **kwargs)
    if not data_id:
        raise ValueError("No input fastq dataset given.")
    
    inputs = {
        "input":{
            "values":[{
                "src":datasrc, 
                "id":data_id
                }]
            },
        "SKIPN":"",
        "RENAMESEQ":"-r"
    }
    
    tool_id = "toolshed.g2.bx.psu.edu/repos/devteam/fastq_to_fasta/cshl_fastq_to_fasta/1.0.2" #tool_name_to_id('FastQC')
    output = local_run_tool_context(tool_id, inputs, **kwargs)
    return GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, output['outputs']['output1']['id'])

# {"tool_id":"toolshed.g2.bx.psu.edu/repos/artbio/yac_clipper/yac/2.0.1","tool_version":"2.0.1","inputs":{"input":{"values":[{"src":"hda","name":"Select first on data 33","tags":[],"keep":false,"hid":53,"id":"b735ed9e5e005602"}],"batch":false},"min":15,"max":36,"out_format":"fasta","Nmode":"accept","clip_source|clip_source_list":"prebuilt","clip_source|clip_sequence":"TGGAATTCTCGGGTGCCAAG"}}
def run_clip_adapter(*args, **kwargs):
    
    history_id = get_or_create_history_context(**kwargs)
    if not 'history_id' in kwargs.keys():
        kwargs['history_id'] = history_id

    paramindex = 0
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("No input dataset given.")
        data = args[paramindex]
        paramindex +=1
        
    datasrc, data_id = get_dataset_context(data, **kwargs)
    if not data_id:
        raise ValueError("No input dataset given.")
    
    mininum = 0    
    if 'min' in kwargs.keys():
        mininum = kwargs['min']
    else:
        if len(args) > paramindex:
            mininum = args[paramindex]
            paramindex +=1
    
    maximum = 15        
    if 'max' in kwargs.keys():
        maximum = kwargs['max']
    else:
        if len(args) > paramindex:
            maximum = args[paramindex]
            paramindex +=1

    dataformat = 'q'
    if 'format' in kwargs.keys():
        dataformat = kwargs['format']
    else:
        if len(args) > paramindex:
            dataformat = args[paramindex]
            paramindex +=1
            
    nmode = kwargs['nmode'] if 'nmode' in kwargs.keys() else "accept"    
    adapter = kwargs['adapter'] if 'adapter' in kwargs.keys() else "TGGAATTCTCGGGTGCCAAG"
    source = kwargs['src'] if 'src' in kwargs.keys() else None
    
    inputs = {
        "min": mininum,
        "max":maximum,
        "out_format": "fastq" if dataformat=="q" else "fasta",
        "Nmode":nmode,
        "clip_source|clip_source_list":"prebuilt",
        "clip_source|clip_sequence":adapter,
        "input":{
            "values":[{
                "src":datasrc,
                "id":data_id
                }]
        }
     }
    
    if source:
        inputs["clip_source|clip_source_list"] = "user"
        inputs["clip_source|clip_sequence"] = source

    tool_id = 'toolshed.g2.bx.psu.edu/repos/artbio/yac_clipper/yac/2.0.1' #tool_name_to_id('Clip adapter')
    output = local_run_tool_context(tool_id, inputs, **kwargs)
    return GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, output['outputs']['output']['id'])

# {
#     "tool_id":"trimmer",
#     "tool_version":"0.0.1",
#     "inputs":{
#         "input1":{
#             "values":
#             [{
#                 "src":"hda",
#                 "name":"SRR034608.fastq",
#                 "tags":[],
#                 "keep":false,
#                 "hid":39,
#                 "id":"f2f5db583bb871d6"
#                 }],
#                   "batch":false},
#               "col":0,"start":1,"end":0,"fastq":"","ignore":["62","64","43","60","42","45","61","124","63","36","46","58","38","37","94","35"]
#               }
#               }
def run_trim(*args, **kwargs):

    history_id = get_or_create_history_context(**kwargs)
    if not 'history_id' in kwargs.keys():
        kwargs['history_id'] = history_id

    paramindex = 0
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("No input dataset given.")
        data = args[paramindex]
        paramindex +=1
        
    datasrc, data_id = get_dataset_context(data, **kwargs)
    if not data_id:
        raise ValueError("No input dataset given.")
    
    col = 0    
    if 'col' in kwargs.keys():
        col = kwargs['col']
    else:
        if len(args) > paramindex:
            col = args[paramindex]
            paramindex +=1
    
    start = 1        
    if 'start' in kwargs.keys():
        start = kwargs['start']
    else:
        if len(args) > paramindex:
            start = args[paramindex]
            paramindex +=1

    end = 0        
    if 'end' in kwargs.keys():
        start = kwargs['end']
    else:
        if len(args) > paramindex:
            end = args[paramindex]
            paramindex +=1

    ignore = '>@+<*-=|?$.:&%^#'   
    if 'ignore' in kwargs.keys():
        start = kwargs['ignore']
    else:
        if len(args) > paramindex:
            ignore = args[paramindex]
            paramindex +=1
            
    if ignore:
        ignore = [ord(x) for x in ignore]#.split(",")]
    
    inputs = {
        "input1":{
            "values":[{
                "src":datasrc,
                "id":data_id
                }]
            },
        "col":col,
        "start":start,
        "end":end,
        "fastq":"",
        "ignore":ignore
    }
    
    tool_id = 'trimmer' #tool_name_to_id('Trim')
    output = local_run_tool_context(tool_id, inputs, **kwargs)
    return GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, output['outputs']['out_file1']['id'])

#===============================================================================
# run_fastq_groomer
# {"tool_id":"toolshed.g2.bx.psu.edu/repos/devteam/fastq_groomer/fastq_groomer/1.0.4",
# "tool_version":"1.0.4",
# "inputs":{"input_file":{"values":[{"src":"hda","name":"SRR034608.fastq","tags":[],"keep":false,"hid":1,"id":"c9468fdb6dc5c5f1"}],"batch":false},
# "input_type":"sanger","options_type|options_type_selector":"basic"}}
#===============================================================================
def run_fastq_groomer(*args, **kwargs):
    
    history_id = get_or_create_history_context(**kwargs)
    if not 'history_id' in kwargs.keys():
        kwargs['history_id'] = history_id

    paramindex = 0
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("No input dataset given.")
        data = args[paramindex]
        
    datasrc, data_id = get_dataset_context(data, **kwargs)
    if not data_id:
        raise ValueError("No input dataset given.")

    inputs = {
        "input_file":{
            "values":[{
                "src":datasrc, "id":data_id
                }]
            }
        }
    
    tool_id = 'toolshed.g2.bx.psu.edu/repos/devteam/fastq_groomer/fastq_groomer/1.0.4' #tool_name_to_id('FASTQ Groomer')
    output = local_run_tool_context(tool_id, inputs, **kwargs)
    return GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, output['outputs']['output_file']['id'])

#galaxy.datatypes.tabular:Vcf
#galaxy.datatypes.binary:TwoBit
#galaxy.datatypes.binary:Bam
#galaxy.datatypes.binary:Sff
#galaxy.datatypes.xml:Phyloxml
#galaxy.datatypes.xml:GenericXml
#galaxy.datatypes.sequence:Maf
#galaxy.datatypes.sequence:Lav
#galaxy.datatypes.sequence:csFasta
def get_datatype(*args, **kwargs):
    
    history_id = get_or_create_history_context(**kwargs)
    if not 'history_id' in kwargs.keys():
        kwargs['history_id'] = history_id

    paramindex = 0
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("No input dataset given.")
        data = args[paramindex]
        
    datasrc, data_id = get_dataset_context(data, **kwargs)
    if not data_id:
        raise ValueError("No input dataset given.")
    
    gi = create_galaxy_instance_context(**kwargs)
    info = gi.datasets.show_dataset(dataset_id = data_id, hda_ldda = datasrc)
    return info['data_type']

# {"tool_id":"toolshed.g2.bx.psu.edu/repos/devteam/picard/picard_FastqToSam/2.7.1.0","tool_version":"2.7.1.0","inputs":{"input_type|input_type_selector":"se","input_type|fastq":{"values":[{"src":"hda","name":"FASTQ Groomer on data 1","tags":[],"keep":false,"hid":26,"id":"d343a822bd747ee4"}],"batch":false},"quality_format":"Standard","read_group_name":"A","sample_name":"sample-a","library_name":"","platform_unit":"","platform":"","sequencing_center":"","predicted_insert_size":"","comment":"","description":"","run_date":"","min_q":0,"max_q":93,"strip_unpairied_mate_number":"false","allow_and_ignore_empty_lines":"false","validation_stringency":"LENIENT"}}
# {"tool_id":"toolshed.g2.bx.psu.edu/repos/devteam/picard/picard_FastqToSam/1.136.0","tool_version":"1.136.0","inputs":{"input_type|input_type_selector":"se","input_type|fastq":{"values":[{"src":"hda","name":"SP1.fq","tags":[],"keep":false,"hid":2,"id":"cff44749a1f216fe"}],"batch":false},"quality_format":"Standard","read_group_name":"A","sample_name":"sample-a","library_name":"","platform_unit":"","platform":"","sequencing_center":"","predicted_insert_size":"","comment":"","description":"","run_date":"","min_q":0,"max_q":93,"strip_unpairied_mate_number":"false","allow_and_ignore_empty_lines":"false","validation_stringency":"LENIENT"}}
# {"tool_id":"toolshed.g2.bx.psu.edu/repos/devteam/picard/picard_FastqToSam/1.136.0","tool_version":"1.136.0","inputs":{"input_type|input_type_selector":"pe","input_type|fastq":{"values":[{"src":"hda","name":"SP1.fq","tags":[],"keep":false,"hid":2,"id":"cff44749a1f216fe"}],"batch":false},"input_type|fastq2":{"values":[{"src":"hda","name":"SP1.fq","tags":[],"keep":false,"hid":2,"id":"cff44749a1f216fe"}],"batch":false},"quality_format":"Standard","read_group_name":"A","sample_name":"sample-a","library_name":"","platform_unit":"","platform":"","sequencing_center":"","predicted_insert_size":"","comment":"","description":"","run_date":"","min_q":0,"max_q":93,"strip_unpairied_mate_number":"false","allow_and_ignore_empty_lines":"false","validation_stringency":"LENIENT"}}
def run_fastq_to_sam(*args, **kwargs):    
    
    history_id = get_or_create_history_context(**kwargs)
    if not 'history_id' in kwargs.keys():
        kwargs['history_id'] = history_id

    paramindex = 0
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("No input dataset given.")
        data = args[paramindex]
        
    datasrc, data_id = get_dataset_context(data, **kwargs)
    if not data_id:
        raise ValueError("No input dataset given.")
    
    inputs = {
        "input_type|input_type_selector":"se",
        "input_type|fastq":{
            "values":[{
                "src":datasrc, 
                "id":data_id
                }]
            },
        "quality_format":"Standard",
        "read_group_name":"A",
        "sample_name":"sample-a",
        "library_name":"",
        "platform_unit":"",
        "platform":"",
        "sequencing_center":"",
        "predicted_insert_size":"",
        "comment":"",
        "description":"",
        "run_date":"",
        "min_q":0,
        "max_q":93,
        "strip_unpairied_mate_number":"false",
        "allow_and_ignore_empty_lines":"false",
        "validation_stringency":"LENIENT"
    }
    
    tool_id = 'toolshed.g2.bx.psu.edu/repos/devteam/picard/picard_FastqToSam/2.7.1.0' #tool_name_to_id('FastqToSam') # 
    output = local_run_tool_context(tool_id, inputs, **kwargs)
    return GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, output['outputs']['outFile']['id'])

#{"tool_id":"toolshed.g2.bx.psu.edu/repos/devteam/sam2interval/sam2interval/1.0.1","tool_version":"1.0.1","inputs":{"input1":{"values":[{"src":"hda","name":"BAM-to-SAM on data 114: converted SAM","tags":[],"keep":false,"hid":115,"id":"c0279aab05812500"}],"batch":false},"print_all":"-p"}}
def run_sam_to_interval(*args, **kwargs):
    
    history_id = get_or_create_history_context(**kwargs)
    if not 'history_id' in kwargs.keys():
        kwargs['history_id'] = history_id

    paramindex = 0
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("No input dataset given.")
        data = args[paramindex]
        
    datasrc, data_id = get_dataset_context(data, **kwargs)
    if not data_id:
        raise ValueError("No input dataset given.")

    inputs = {
        "print_all":"-p",
        "input1":{
            "values":[{
                "src":datasrc, 
                "id":data_id
                }]
            }
        }
    
    tool_id = "toolshed.g2.bx.psu.edu/repos/devteam/sam2interval/sam2interval/1.0.1" #tool_name_to_id('FastQC')
    output = local_run_tool_context(tool_id, inputs, **kwargs)
    return GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, output['outputs']['out_file1']['id'])

#{"tool_id":"toolshed.g2.bx.psu.edu/repos/devteam/join/gops_join_1/1.0.0","tool_version":"1.0.0","inputs":{"input1":{"values":[{"src":"hda","name":"Converted Interval","tags":[],"keep":false,"hid":116,"id":"e037fdb493429c2a"}],"batch":false},"input2":{"values":[{"src":"hda","name":"Converted Interval","tags":[],"keep":false,"hid":116,"id":"e037fdb493429c2a"}],"batch":false},"min":1,"fill":"none"}}
def run_join_interval(*args, **kwargs):
    
    history_id = get_or_create_history_context(**kwargs)
    if not 'history_id' in kwargs.keys():
        kwargs['history_id'] = history_id

    paramindex = 0
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("No dataset given for forward fastq  data. Give a dataset path.")
        data = args[paramindex]
        paramindex +=1
        
    datasrc, data_id = get_dataset_context(data, **kwargs)
    if not data_id:
        raise ValueError("No dataset given for forward fastq data. Give a dataset path.")
    
    data2 = ''
    if 'data2' in kwargs.keys():
        data2 = kwargs['data2']
    else:
        if len(args) <= paramindex:
            raise ValueError("No dataset given for reverse fastq  data. Give a dataset path.")
        data2 = args[paramindex]
        paramindex +=1
    
    data2src, data2_id = get_dataset_context(data2, **kwargs)
    if not data2_id:
        raise ValueError("No dataset given for reverse fastq  data. Give a dataset path.")
    
    minimum = 1    
    if 'min' in kwargs.keys():
        minimum = kwargs['min']
    else:
        if len(args) > paramindex:
            minimum = args[paramindex]
            
    inputs = {
        "min":str(minimum),
        "fill":"none",
        "input1":{
            "values":[{
                "src":datasrc,
                "id":data_id
                }]
            },
        "input2":{
            "values":[{
                "src":data2src,
                "id":data2_id
                }]
            }
    }
    
    tool_id = "toolshed.g2.bx.psu.edu/repos/devteam/join/gops_join_1/1.0.0"
    output = local_run_tool_context(tool_id, inputs, **kwargs)
    return GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, output['outputs']['output']['id'])

# {"tool_id":"Grouping1","tool_version":"2.1.1",
#"inputs":
#{"input1":{"values":[{"src":"hda","name":"Cut on data 43","tags":[],"keep":false,"hid":44,"id":"1c84aa7fc4490e6d"}],"batch":false},
#"groupcol":"1","ignorecase":"false","ignorelines":null,
#"operations_0|optype":"mean","operations_0|opcol":"1","operations_0|opround":"no","operations_1|optype":"mean","operations_1|opcol":"1","operations_1|opround":"yes"}}

#{"tool_id":"Grouping1","tool_version":"2.1.1","inputs":{"input1":{"values":[{"src":"hda","name":"Join two Datasets on data 44 and data 45","tags":[],"keep":false,"hid":47,"id":"13120e62d0fbb985"}],"batch":false},
#"groupcol":"1","ignorecase":"false","ignorelines":["62","64","43"],"operations_0|optype":"mean","operations_0|opcol":"1","operations_0|opround":"no"}}
def run_group(*args, **kwargs):

    history_id = get_or_create_history_context(**kwargs)
    if not 'history_id' in kwargs.keys():
        kwargs['history_id'] = history_id

    paramindex = 0
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("No input dataset given.")
        data = args[paramindex]
        paramindex += 1
        
    datasrc, data_id = get_dataset_context(data, **kwargs)
    if not data_id:
        raise ValueError("No input dataset given.")
    
    groupcol = 1
    if 'groupcol' in kwargs.keys():
        groupcol = kwargs['groupcol']
    else:
        if len(args) > paramindex:
            groupcol = args[paramindex]
            paramindex += 1
    
    opindex = 1
    opstr = {}
    while True:
        op = get_op('op', opindex, paramindex, *args, **kwargs)
        if not op:
            break
        else:
            if 'op{0}'.format(opindex) in kwargs.keys():
                paramindex += 1
                
            opitems = op.split('|')
            #"operations_0|optype":"mean","operations_0|opcol":"1","operations_0|opround":"no"
            opstr["operations_{0}|optype".format(opindex - 1)] = opitems[0] if len(opitems) > 0 and opitems[0] else "mean"
            opstr["operations_{0}|opcol".format(opindex - 1)] = opitems[1] if len(opitems) > 1 and opitems[1] else "1"
            opstr["operations_{0}|opround".format(opindex - 1)] = opitems[2] if len(opitems) > 2 and opitems[2] else "no"
            
            opindex += 1
    
    ignorecase = False
    if 'ignorecase' in kwargs.keys():
        ignorecase = kwargs['ignorecase']
    
    ignorelines = ""
    if 'ignorelines' in kwargs.keys():
        ignorelines = [ord(x) for x in kwargs['ignorelines'] ]
    
    inputs = {
        "input1":{
            "values":[{
                "src":datasrc,
                "id":data_id
                }]
            },
        "groupcol":str(groupcol),
        "ignorecase": "true" if ignorecase else "false",
        "ignorelines":ignorelines
    }
    
    for k, v in opstr.items():
        inputs[k] = v

    #tool_id = tool_name_to_id('Group') # 'Grouping1'
    output = local_run_tool_context('Grouping1', inputs, **kwargs)
    return GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, output['outputs']['out_file1']['id'])

#{"tool_id":"sort1","tool_version":"1.0.3","inputs":{"input":{"values":[{"src":"hda","name":"Cut on data 1","tags":[],"keep":false,"hid":45,"id":"fee08c51df578e3d"}],"batch":false},
# "column":"1","style":"num","order":"DESC","column_set_0|other_column":"2","column_set_0|other_style":"gennum","column_set_0|other_order":"ASC","column_set_1|other_column":"1","column_set_1|other_style":"alpha","column_set_1|other_order":"DESC"}}
def run_sort(*args, **kwargs):

    history_id = get_or_create_history_context(**kwargs)
    if not 'history_id' in kwargs.keys():
        kwargs['history_id'] = history_id

    paramindex = 0
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("No input dataset given.")
        data = args[paramindex]
        paramindex += 1
        
    datasrc, data_id = get_dataset_context(data, **kwargs)
    if not data_id:
        raise ValueError("No input dataset given.")
    
    opstr = {}    
    op = ""
    if 'col' in kwargs.keys():
        op = kwargs['col']
    else:
        if len(args) > paramindex:
            op = args[paramindex]
            paramindex += 1
    if op:
        opitems = op.split('|')
        opstr['column'] = opitems[0] if len(opitems[0]) > 0 and opitems[0] else None
        opstr['style'] = opitems[1].lower() if len(opitems) > 1 and opitems[1] else "num"
        opstr['order'] = opitems[2].upper() if len(opitems) > 2 and opitems[2] else "DESC"
        
    opindex = 1                        
    while True:
        op = get_op('col', opindex + 1, paramindex, *args, **kwargs)
        if not op:
            break
        else:
            if 'col{0}'.format(opindex + 1) in kwargs.keys():
                paramindex += 1
                
            opitems = op.split('|')
            
            opstr['column_set_{0}|other_column'.format(opindex - 1)] = opitems[0] if len(opitems) > 0 and opitems[0] else str(opindex + 1)
            opstr['column_set_{0}|other_style'.format(opindex - 1)] = opitems[1] if len(opitems) > 1 and opitems[1] else "num"
            opstr['column_set_{0}|other_order'.format(opindex - 1)] = opitems[2] if len(opitems) > 2 and opitems[2] else "DESC"
            
            opindex += 1

    inputs = {
        "input1":{
            "values":[{
                "src":datasrc,
                "id":data_id
                }]
            }
    }
    
    for k, v in opstr.items():
        inputs[k] = v
        
    #tool_id = tool_name_to_id('Sort') # 'sort1'
    output = local_run_tool_context('sort1', inputs, **kwargs)
    return GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, output['outputs']['out_file1']['id'])

#{"tool_id":"Show beginning1","tool_version":"1.0.0",
#"inputs":{"lineNum":10,
#"input":{"values":[{"src":"hda","name":"SRR034608.fastq","tags":[],"keep":false,"hid":33,"id":"bb7d1d57fc91145a"}],"batch":false}}}
def run_selectfirst(*args, **kwargs):

    history_id = get_or_create_history_context(**kwargs)
    if not 'history_id' in kwargs.keys():
        kwargs['history_id'] = history_id

    paramindex = 0
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("No input dataset given.")
        data = args[paramindex]
        paramindex += 1
        
    datasrc, data_id = get_dataset_context(data, **kwargs)
    if not data_id:
        raise ValueError("No input dataset given.")
    
    lines = 10
    if 'lines' in kwargs.keys():
        lines = kwargs['lines']
    else:
        if len(args) > paramindex:
            lines = args[paramindex]

    inputs = {
        "lineNum":int(lines),
        "input":{
            "values":[{
                "src":datasrc,
                "id":data_id
                }]
        }
     }
    
    #tool_id = tool_name_to_id('Select First') # 'Show beginning1'
    output = local_run_tool_context('Show beginning1', inputs, **kwargs)
    return GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, output['outputs']['out_file1']['id'])

#{"tool_id":"comp1","tool_version":"1.0.2",
#"inputs":
#{"input1":{"values":[{"src":"hda","name":"Cut on data 43","tags":[],"keep":false,"hid":44,"id":"1c84aa7fc4490e6d"}],"batch":false},
#"field1":"1",
#"input2":{"values":[{"src":"hda","name":"Sort on data 45","tags":[],"keep":false,"hid":52,"id":"7e1ddb768ae0c642"}],"batch":false},
#"field2":"1","mode":"N"}}
def run_compare(*args, **kwargs):

    history_id = get_or_create_history_context(**kwargs)
    if not 'history_id' in kwargs.keys():
        kwargs['history_id'] = history_id

    paramindex = 0
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("No dataset given for forward fastq  data. Give a dataset path.")
        data = args[paramindex]
        paramindex +=1
        
    datasrc, data_id = get_dataset_context(data, **kwargs)
    if not data_id:
        raise ValueError("No dataset given for forward fastq data. Give a dataset path.")
    
    data2 = ''
    if 'data2' in kwargs.keys():
        data2 = kwargs['data2']
    else:
        if len(args) <= paramindex:
            raise ValueError("No dataset given for reverse fastq  data. Give a dataset path.")
        data2 = args[paramindex]
        paramindex +=1
    
    data2src, data2_id = get_dataset_context(data2, **kwargs)
    if not data2_id:
        raise ValueError("No dataset given for reverse fastq  data. Give a dataset path.")
    
            
    field1 = 1
    if 'field1' in kwargs.keys():
        field1 = kwargs['field1']
    else:
        if len(args) > paramindex:
            field1 = args[paramindex]
            paramindex += 1
    
    field2 = 1
    if 'field2' in kwargs.keys():
        field2 = kwargs['field2']
    else:
        if len(args) > paramindex:
            field2 = args[paramindex]
            paramindex += 1
    
    mode = "N"
    if 'mode' in kwargs.keys():
        mode = kwargs['mode']
    else:
        if len(args) > paramindex:
            mode = args[paramindex]
            paramindex += 1
                    
    field1 = str(field1)
    field2 = str(field2)
            
    inputs = {
        "input1":{
            "values":[{
                "src":datasrc,
                "id":data_id
                }]
            },
        "field1":field1,
        "input2":{
            "values":[{
                "src":data2src,
                "id":data2_id
                }]
            },
        "field2":field2,
        "mode":mode,
    }

    #tool_id = tool_name_to_id('Compare two Datasets') # 'comp1'
    output = local_run_tool_context('comp1', inputs, **kwargs)
    return GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, output['outputs']['out_file1']['id'])

def run_download(*args, **kwargs):
    
    paramindex = 0
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("No dataset given. Give a dataset path.")
        data = args[paramindex]
        paramindex +=1
    
    outdir = None
    if 'outdir' in kwargs.keys():
        outdir = kwargs['outdir']
    else:
        if len(args) > paramindex:
            outdir = args[paramindex]
    
    fs_type = Utility.fs_type_by_prefix(data)            
    if not fs_type or fs_type != 'gfs':
        raise ValueError("Invalid dataset path.")
    
    fs = Utility.fs_by_prefix(data) 
    gi = create_galaxy_instance_context(**kwargs) 
    dataset = gi.datasets.show_dataset(dataset_id = os.path.basename(data), hda_ldda = 'ldda' if fs.islibrarydata(data) else 'hda')
    name = dataset['name']
    
    path = Utility.get_normalized_path(outdir)
    fullpath = os.path.join(path, name)
    gi.datasets.download_dataset(os.path.basename(data), file_path = fullpath, use_default_filename=False, wait_for_completion=True)
    fs = Utility.fs_by_prefix_or_guess(fullpath)       
    return fs.strip_root(fullpath)

#library       
def get_libraries_json_local(**kwargs):
    gi =  create_galaxy_instance_context(**kwargs)
    return gi.libraries.get_libraries()
    
def get_library_ids(**kwargs):
    wf = get_libraries_json_local(**kwargs)
    wf_ids = []
    for j in wf:
        #yield j.name
        wf_ids.append(j['id'])
    return wf_ids

def get_library_info(*args, **kwargs):
    paramindex = 0
    library_id = None
    if 'library_id' in kwargs.keys():
        library_id = kwargs['library_id']
    else:
        if len(args) > paramindex:
            library_id = args[paramindex]
        
    gi =  create_galaxy_instance_context(**kwargs)
    libraries = gi.libraries.get_libraries(library_id = library_id)
    return libraries[0] if libraries else None

def create_library(*args, **kwargs):
    paramindex = 0
    library_name = None
    if 'library_name' in kwargs.keys():
        library_name = kwargs['library_name']
    else:
        if len(args) > paramindex:
            library_name = args[paramindex]
            
    gi =  create_galaxy_instance_context(**kwargs)
    name = library_name if library_name else str(uuid.uuid4())
    library = gi.libraries.create_library(name)
    return library["id"]

# {
# "tool_id":"Cut1",
# "tool_version":"1.0.2",
# "inputs": {
#     "columnList":"c1,c2",
#     "delimiter":"T",
#     "input":{
#         "values":[{
#             "src":"hda",
#             "name":"SRR034608.fastq",
#             "tags":[],
#             "keep":false,
#             "hid":39,
#             "id":"f2f5db583bb871d6"
#             }],
#          "batch":false
#     }
#  }
# }
def run_cut(*args, **kwargs):

    history_id = get_or_create_history_context(**kwargs)
    if not 'history_id' in kwargs.keys():
        kwargs['history_id'] = history_id

    paramindex = 0
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("No input dataset given.")
        data = args[paramindex]
        paramindex += 1
        
    datasrc, data_id = get_dataset_context(data, **kwargs)
    if not data_id:
        raise ValueError("No input dataset given.")
    
    columns = 'c1'
    if 'columns' in kwargs.keys():
        columns = kwargs['columns']
    else:
        if len(args) > paramindex:
            columns = args[paramindex]
            paramindex +=1
    
    delimiter = 'Tab'
    if 'delimiter' in kwargs.keys():
        delimiter = kwargs['delimiter']
    else:
        if len(args) > paramindex:
            delimiter = args[paramindex]
            paramindex +=1

    inputs = {
        "columnList":columns,
        "delimiter":delimiter[:1],
        "input":{
            "values":[{
                "src":datasrc,
                "tags":[],
#                "keep":False,
                "id":data_id
                }]
#             "batch":False
        }
     }

    tool_id = 'Cut1' #tool_name_to_id('Cut')
    output = local_run_tool_context(tool_id, inputs, **kwargs)
    return GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, output['outputs']['out_file1']['id'])

#{"tool_id":"join1","tool_version":"2.0.2",
# "inputs":{"input1":{"values":[{"src":"hda","name":"Cut on data 1","tags":[],"keep":false,"hid":45,"id":"fee08c51df578e3d"}],"batch":false},"field1":"2","input2":{"values":[{"src":"hda","name":"Cut on data 43","tags":[],"keep":false,"hid":44,"id":"1c84aa7fc4490e6d"}],"batch":false},"field2":"1","unmatched":"-u","partial":"-p","fill_empty_columns|fill_empty_columns_switch":"no_fill"}}
def run_join(*args, **kwargs):

    history_id = get_or_create_history_context(**kwargs)
    if not 'history_id' in kwargs.keys():
        kwargs['history_id'] = history_id

    paramindex = 0
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("No dataset given for forward fastq  data. Give a dataset path.")
        data = args[paramindex]
        paramindex +=1
        
    datasrc, data_id = get_dataset_context(data, **kwargs)
    if not data_id:
        raise ValueError("No dataset given for forward fastq data. Give a dataset path.")
    
    data2 = ''
    if 'data2' in kwargs.keys():
        data2 = kwargs['data2']
    else:
        if len(args) <= paramindex:
            raise ValueError("No dataset given for reverse fastq  data. Give a dataset path.")
        data2 = args[paramindex]
        paramindex +=1
    
    data2src, data2_id = get_dataset_context(data2, **kwargs)
    if not data2_id:
        raise ValueError("No dataset given for reverse fastq  data. Give a dataset path.")
               
    field1 = 1
    if 'field1' in kwargs.keys():
        field1 = kwargs['field1']
    else:
        if len(args) > paramindex:
            field1 = args[paramindex]
            paramindex += 1
    
    field2 = 1
    if 'field2' in kwargs.keys():
        field2 = kwargs['field2']
    else:
        if len(args) > paramindex:
            field2 = args[paramindex]
            paramindex += 1
    
                
    inputs = {
        "input1":{
            "values":[{
                "src":datasrc,
                "id":data_id
                }]
            },
        "field1":str(field1),
        "input2":{
            "values":[{
                "src":data2src,
                "id":data2_id
                }]
            },
        "field2":str(field2),
        "unmatched":"", #-u",
        "partial":"", #"-p",
        "fill_empty_columns|fill_empty_columns_switch":"no_fill"
    }
    
    tool_id = 'join1' # tool_name_to_id('Join two Datasets')
    output = local_run_tool_context(tool_id, inputs, **kwargs)
    return GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, output['outputs']['out_file1']['id'])

#{"tool_id":"toolshed.g2.bx.psu.edu/repos/portiahollyoak/fastuniq/fastuniq/1.1","tool_version":"1.1",
#"inputs":{"fastq_R1":{"values":[{"src":"hda","name":"SRR034608.fastq","tags":[],"keep":false,"hid":30,"id":"b3a78854daef4a5a"}],"batch":false},
#"fastq_R2":{"values":[{"src":"hda","name":"FASTQ Groomer on data 37","tags":[],"keep":false,"hid":38,"id":"920c23ba6ef2e3da"}],"batch":false},
#"select_output_format":"f/q"}}
def run_fastuniq(*args, **kwargs):

    history_id = get_or_create_history_context(**kwargs)
    if not 'history_id' in kwargs.keys():
        kwargs['history_id'] = history_id

    paramindex = 0
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("No dataset given for forward fastq  data. Give a dataset path.")
        data = args[paramindex]
        paramindex +=1
        
    datasrc, data_id = get_dataset_context(data, **kwargs)
    if not data_id:
        raise ValueError("No dataset given for forward fastq data. Give a dataset path.")
    
    data2 = ''
    if 'data2' in kwargs.keys():
        data2 = kwargs['data2']
    else:
        if len(args) <= paramindex:
            raise ValueError("No dataset given for reverse fastq  data. Give a dataset path.")
        data2 = args[paramindex]
        paramindex +=1
    
    data2src, data2_id = get_dataset_context(data2, **kwargs)
    if not data2_id:
        raise ValueError("No dataset given for reverse fastq  data. Give a dataset path.")
            
    data_format = 'q'
    if 'format' in kwargs.keys():
        data_format = kwargs['format']
    else:
        if len(args) > paramindex:
            data_format = args[paramindex]
            paramindex += 1
            
    inputs = {
        "fastq_R1":{
            "values":[{
                "src":datasrc,
                "id":data_id
                }]
            },
        "fastq_R2":{
            "values":[{
                "src":data2src,
                "id":data2_id
                }]
            },
        "format":data_format,
    }

    tool_id = 'toolshed.g2.bx.psu.edu/repos/portiahollyoak/fastuniq/fastuniq/1.1' #tool_name_to_id('FastUniq')
    output = local_run_tool_context(tool_id, inputs, **kwargs)
    return GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, output['outputs']['fastq_R1_rmdup']['id']), GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, output['outputs']['fastq_R2_rmdup']['id'])

#{"tool_id":"Filter1","tool_version":"1.1.0","inputs":{"input":{"values":[{"src":"hda","name":"all.cDNA (as tabular)","tags":[],"keep":false,"hid":3,"id":"7ef8021ae23ac2fc"}],"batch":false},"cond":"c1=='chr22'","header_lines":0}}
def run_filter(*args, **kwargs):    

    history_id = get_or_create_history_context(**kwargs)
    if not 'history_id' in kwargs.keys():
        kwargs['history_id'] = history_id

    paramindex = 0
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("No input dataset given.")
        data = args[paramindex]
        paramindex += 1
        
    datasrc, data_id = get_dataset_context(data, **kwargs)
    if not data_id:
        raise ValueError("No input dataset given.")

    condition = ''
    if 'condition' in kwargs.keys():
        condition = kwargs['condition']
    else:
        if len(args) <= paramindex:
            raise ValueError("No filtering condition is given.")
        condition = args[paramindex]
            
    inputs = {
        "cond":condition,
        "input":{
            "values":[{
                "src":datasrc, 
                "id":data_id
                }]
            }
        }
    
    #tool_id = tool_name_to_id('Filter') # Filter1
    output = local_run_tool_context('Filter1', inputs, **kwargs)
    return GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, output['outputs']['output_file']['id'])

#{"tool_id":"Convert characters1","tool_version":"1.0.0","inputs":{"convert_from":"Dt","input":{"values":[{"src":"hda","name":"Filter on data 3","tags":[],"keep":false,"hid":57,"id":"4eb3d2698c4eef35"}],"batch":false},"strip":"true","condense":"true"}}
def run_convert_to_tab(*args, **kwargs):    
    
    history_id = get_or_create_history_context(**kwargs)
    if not 'history_id' in kwargs.keys():
        kwargs['history_id'] = history_id

    paramindex = 0
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("No input dataset given.")
        data = args[paramindex]
        paramindex += 1
        
    datasrc, data_id = get_dataset_context(data, **kwargs)
    if not data_id:
        raise ValueError("No input dataset given.")
    
    delimiter = "T"
    if 'delimiter' in kwargs.keys():
        delimiter = kwargs['delimiter']
    else:
        if len(args) > paramindex:
            delimiter = args[paramindex]
            
    if 'delimeter' == ' ':
        delimeter = 's'
    elif 'delimeter' == '.':
        delimeter = 'Dt'
    elif 'delimeter' == '.':
        delimeter = 'C'
    elif 'delimeter' == '-':
        delimeter = 'D'
    elif 'delimeter' == '_':
        delimeter = 'U'
    elif 'delimeter' == '.':
        delimeter = 'Dt'
    elif 'delimeter' == '|':
        delimeter = 'P'
    elif 'delimeter' == ':':
        delimeter = 'Co'
    elif 'delimeter' == ';':
        delimeter = 'Sc'
    else:
        delimeter = 'T'
            
    inputs = {
        "convert_from":delimiter,
        "strip":"true",
        "condense":"true",
        "input":{
            "values":[{
                "src":datasrc, 
                "id":data_id
                }]
            }
        }
    
    #tool_id = tool_name_to_id('Filter') # Convert characters1
    output = local_run_tool_context('Convert characters1', inputs, **kwargs)
    return GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, output['outputs']['out_file1']['id'])



#{"tool_id":"toolshed.g2.bx.psu.edu/repos/slegras/sickle_1_33/sickle/1.33","tool_version":"1.33",
#"inputs":{"readtype|single_or_paired":"se","readtype|input_single":{"values":[{"src":"hda","name":"SRR034608.fastq","tags":[],"keep":false,"hid":33,"id":"bb7d1d57fc91145a"}],"batch":false},
#"qual_threshold":20,"length_threshold":20,"no_five_prime":"false","trunc_n":"false"}}

#{"tool_id":"toolshed.g2.bx.psu.edu/repos/slegras/sickle_1_33/sickle/1.33","tool_version":"1.33",
#"inputs":{"readtype|single_or_paired":"pe_sep","readtype|input_paired1":{"values":[{"src":"hda","name":"SRR034608.fastq","tags":[],"keep":false,"hid":30,"id":"b3a78854daef4a5a"}],"batch":false},
#"readtype|input_paired2":{"values":[{"src":"hda","name":"FASTQ Groomer on data 37","tags":[],"keep":false,"hid":38,"id":"920c23ba6ef2e3da"}],"batch":false},
#"qual_threshold":20,"length_threshold":20,"no_five_prime":"true","trunc_n":"true"}}

#{"tool_id":"toolshed.g2.bx.psu.edu/repos/slegras/sickle_1_33/sickle/1.33","tool_version":"1.33",
#"inputs":{"readtype|single_or_paired":"pe_combo","readtype|input_combo":{"values":[{"src":"hda","name":"SRR034608.fastq","tags":[],"keep":false,"hid":39,"id":"f2f5db583bb871d6"}],"batch":false},"readtype|output_n":"false","qual_threshold":20,"length_threshold":20,"no_five_prime":"true","trunc_n":"true"}}
def run_sickle(*args, **kwargs):

    history_id = get_or_create_history_context(**kwargs)
    if not 'history_id' in kwargs.keys():
        kwargs['history_id'] = history_id

    paramindex = 0
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("No dataset given for forward fastq  data. Give a dataset path.")
        data = args[paramindex]
        paramindex +=1
        
    datasrc, data_id = get_dataset_context(data, **kwargs)
    if not data_id:
        raise ValueError("No dataset given for forward fastq data. Give a dataset path.")
    
    data2 = ''
    if 'data2' in kwargs.keys():
        data2 = kwargs['data2']
    else:
        if len(args) > paramindex:
            data2 = args[paramindex]
            paramindex +=1
    
    data2src = ''
    data2_id = ''
    if data2:
        data2src, data2_id = get_dataset_context(data2, **kwargs)            
    
    mode = 'se'        
    if 'mode' in kwargs.keys():
        mode = kwargs['mode']
    else:
        if len(args) > paramindex:
            mode = args[paramindex]
            paramindex +=1
        else:
            mode = 'pe_sep' if data2_id else 'se'

    quality = 20
    if 'quality' in kwargs.keys():
        quality = kwargs['quality']
    else:
        if len(args) > paramindex:
            quality = args[paramindex]
            paramindex +=1
    
    length = 20
    if 'length' in kwargs.keys():
        length = kwargs['length']
    else:
        if len(args) > paramindex:
            length = args[paramindex]
            paramindex +=1
           
    inputs = {
        "qual_threshold":quality,
        "length_threshold":length,
        "no_five_prime":"true",
        "trunc_n":"true",
        "readtype|single_or_paired":mode
    }
    
    if mode == "se":
        inputs["readtype|input_single"] = {
         "values":[{
             "src":datasrc,
             "id": data_id
             }]
         }
    elif mode == "pe_sep":
        inputs["readtype|input_paired1"] = {
         "values":[{
             "src":datasrc,
             "id": data_id
             }]
         }
        inputs["readtype|input_paired2"] = {
         "values":[{
             "src":data2src,
             "id": data2_id
             }]
         }
    else:
        inputs["readtype|input_combo"] = {
         "values":[{
             "src":datasrc,
             "id": data_id
             }]
         }
        inputs["readtype|output_n"] = "false"
    
    tool_id = 'toolshed.g2.bx.psu.edu/repos/iuc/sickle/sickle/1.33.1' #tool_name_to_id('Sickle')
    output = local_run_tool_context(tool_id, inputs, **kwargs)
    return GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, output['outputs']['out_file1']['id'])
    if mode == 'se':
        return [GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, output['outputs']['output_single']['id'])]
    elif mode == 'pe_sep':
        return [GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, output['outputs']['output_paired1']['id']), GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, output['outputs']['output_paired2']['id'], output['outputs']['output_paired_single']['id']) ]
    else:
        return [ GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, output['outputs']['output_paired']['id']), GalaxyFileSystem.get_history_path(srlab_galaxy, history_id, output['outputs']['output_paired_single']['id']) ]
