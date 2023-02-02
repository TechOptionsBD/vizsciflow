import logging
import os
import json
import pathlib
from app.objectmodel.common import isiterable

class Loader:
    
    @staticmethod
    def get_datasources():
        from app import app

        return [{
            'name':'HDFS', 'type':'hdfs', 'url':'hdfs://206.12.102.75:54310/', 'root':'/user', 'user':'hadoop', 'password':'spark#2018', 'public':'/public', 'prefix':'HDFS'
        },{
            'name':'LocalFS', 'type':'posix', 'url':app.config['DATA_DIR'], 'root':'/', 'user':'users', 'public':'/public'
        },{
            'name':'GalaxyFS', 'type':'gfs', 'url':'http://sr-p2irc-big8.usask.ca:8080', 'root':'/', 'password':'7483fa940d53add053903042c39f853a', 'prefix':'GalaxyFS'
        },{
            'name':'HDFS-BIG', 'type':'hdfs', 'url':'http://sr-p2irc-big1.usask.ca:50070', 'root':'/user', 'user':'hdfs', 'public': '/public', 'prefix': 'GalaxyFS'
        },{
            'name':'COPERNICUS', 'type':'scidata', 'url':'/copernicus', 'root':'/', 'prefix':'https://p2irc-data-dev.usask.ca/api'
        }
        ]

    @staticmethod
    def load_funcs_recursive_flat(library_def_file, with_users = True):
        funcs = Loader.load_funcs_recursive(library_def_file)
        funclist = []
        for f in funcs.values():
            funclist.extend(f)
        
        if not with_users:
            from app import app

            funclist = [func for func in funclist if not func['module'].startswith(app.config['MODULE_PACKAGE'] + '.users')]

        return funclist

    @staticmethod
    def load_funcs_recursive(library_def_file):
        if os.path.isfile(library_def_file):
            return Loader.load_funcs(library_def_file)
        
        all_funcs = {}
        for f in os.listdir(library_def_file):
            funcs = Loader.load_funcs_recursive(os.path.join(library_def_file, f))
            for k,v in funcs.items():
                if k in all_funcs:
                    all_funcs[k].extend(v)
                else:
                    all_funcs[k] = v if isinstance(v, list) else [v]
        return all_funcs
       
    @staticmethod
    def load_funcs(library_def_file):
        from app import app

        funcs = {}
        try:
            if not os.path.isfile(library_def_file) or not library_def_file.endswith(".json"):
                return funcs
            
            with open(library_def_file, 'r') as json_data:
                d = json.load(json_data)
                libraries = d["functions"] if "functions" in d else d
                libraries = sorted(libraries, key = lambda k : k['package'].lower()) if isinstance(libraries, list) else [libraries]

                module = os.path.realpath(json_data.name)
                module_dir = os.path.dirname(module)
                if os.path.commonpath([app.config['ROOT_DIR']]) == os.path.commonpath([app.config['ROOT_DIR'], module_dir]):
                    module = str(pathlib.Path(module_dir).relative_to(app.config['ROOT_DIR']))
                else:
                    logging.warning(f"Module path {module_dir} is not a child path of system's modules folder.")
                module = module.replace('/', '.') + '.adapter'

                for f in libraries:
                    org = f["org"] if f.get("org") else ""
                    name = f["name"] if f.get("name") else f["internal"]
                    internal = f["internal"] if f.get("internal") else f["name"]
                    package = f["package"] if f.get("package") else ""
                    example = f["example"] if f.get("example") else ""
                    desc = f["desc"] if f.get("desc") else ""
                    #runmode = f["runmode"] if f.get("runmode") else ""
                    #level = int(f["level"]) if f.get("level") else 0
                    group = f["group"] if f.get("group") else ""
                    href = f["href"] if f.get("href") else ""
                    public = bool(f["public"]) if f.get("public") else True

                    params = []
                    if f.get("params"):
                        for p in f["params"]:
                            param = {}
                            if p.get("name"):
                                param["name"] = p["name"]
                            if p.get("default"):
                                param["default"] = p["default"]
                            if p.get("type"):
                                param["type"] = p["type"]
                            if p.get("desc"):
                                param["desc"] = p["desc"]
                            params.append(param)
                            
                    returns = []
                    if f.get("returns"):
                        rs = f["returns"]

                        if not isinstance(rs, list):
                            rs = [rs]

                        for p in rs:
                            param = {}
                            if p.get("name"):
                                param["name"] = p["name"]
                            if p.get("type"):
                                param["type"] = p["type"]
                            if p.get("desc"):
                                param["desc"] = p["desc"]
                            returns.append(param)

                    func = {
                        "org": org,
                        "name": name, 
                        "internal": internal,
                        "package":package, 
                        "module": module,
                        "params": params, 
                        "example": example,
                        "desc": desc,
                        "group": group,
                        "returns": returns,
                        "public": public
                        }
                    pipenvflag = f.get("pipenv") and (f.get("pippkgs") or f.get("reqfile"))
                    if pipenvflag:
                        if f.get("pippkgs") and f["pippkgs"]:
                            func.update({"pippkgs": f["pippkgs"]})
                        if f.get("reqfile") and f["reqfile"]:
                            func.update({"reqfile": f["reqfile"]})
                        func.update({"pipenv": f["pipenv"]})

                    if name.lower() in funcs:
                        funcs[name.lower()].extend([func])
                    else:
                        funcs[name.lower()] = [func]
        except Exception as e:
            logging.error("Error occurred during module loading:" + str(e))
        finally:
            return funcs
    
    @staticmethod
    def load_samples_recursive(library_def_file):

        if os.path.isfile(library_def_file):
            try:
                samples = Loader.load_samples(library_def_file)
                return [sample for sample in samples if "script" in sample]
            except:
                return []
        
        all_samples = []
        for f in os.listdir(library_def_file):
            all_samples.extend(Loader.load_samples_recursive(os.path.join(library_def_file, f)))
        return all_samples
       
    @staticmethod
    def load_samples(sample_def_file):
        samples = []
        if os.path.isfile(sample_def_file) and sample_def_file.endswith(".json"):
            with open(sample_def_file, 'r') as json_data:
                ds = json.load(json_data)
                if ds.get("workflows"):
                    samples.extend(ds["workflows"])
                else:
                    samples.append(ds)
        return samples