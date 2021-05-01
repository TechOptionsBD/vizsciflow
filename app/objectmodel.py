import os
import json
import logging

class ObjectModel:
    
    @staticmethod
    def get_datasources():
        basedir = os.path.dirname(os.path.abspath(__file__))
        storagedir = os.path.abspath(os.path.join(basedir, '../storage'))

        return [{
            'name':'HDFS', 'type':'hdfs', 'url':'hdfs://206.12.102.75:54310/', 'root':'/user', 'user':'hadoop', 'password':'spark#2018', 'public':'/public', 'prefix':'HDFS'
        },{
            'name':'LocalFS', 'type':'posix', 'url':storagedir, 'root':'/', 'public':'/public'
        },{
            'name':'GalaxyFS', 'type':'gfs', 'url':'http://sr-p2irc-big8.usask.ca:8080', 'root':'/', 'password':'7483fa940d53add053903042c39f853a', 'prefix':'GalaxyFS'
        },{
            'name':'HDFS-BIG', 'type':'hdfs', 'url':'http://sr-p2irc-big1.usask.ca:50070', 'root':'/user', 'user':'hdfs', 'public': '/public', 'prefix': 'GalaxyFS'
        }
        ]

    @staticmethod
    def load_funcs_recursive_flat(library_def_file):
        funcs = ObjectModel.load_funcs_recursive(library_def_file)
        funclist = []
        for f in funcs.values():
            funclist.extend(f)
        return funclist

    @staticmethod
    def load_funcs_recursive(library_def_file):
        if os.path.isfile(library_def_file):
            return ObjectModel.load_funcs(library_def_file)
        
        all_funcs = {}
        for f in os.listdir(library_def_file):
            funcs = ObjectModel.load_funcs_recursive(os.path.join(library_def_file, f))
            for k,v in funcs.items():
                if k in all_funcs:
                    all_funcs[k].extend(v)
                else:
                    all_funcs[k] = v if isinstance(v, list) else [v]
        return all_funcs
       
    @staticmethod
    def load_funcs(library_def_file):
        funcs = {}
        try:
            if not os.path.isfile(library_def_file) or not library_def_file.endswith(".json"):
                return funcs
            
            with open(library_def_file, 'r') as json_data:
                d = json.load(json_data)
                libraries = d["functions"]
                libraries = sorted(libraries, key = lambda k : k['package'].lower())
                for f in libraries:
                    org = f["org"] if f.get("org") else ""
                    name = f["name"] if f.get("name") else f["internal"]
                    internal = f["internal"] if f.get("internal") else f["name"]
                    module = f["module"] if f.get("module") else None
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
                            pname = p["name"] if p.get("name") else ""
                            pvalue = p["default"] if p.get("default") else ""
                            ptype = p["type"] if p.get("type") else ""
                            pdesc = p["desc"] if p.get("desc") else ""
                            params.append({"name": pname, "default": pvalue, "desc": pdesc, "type": ptype})
                            
                    returns = []
                    if f.get("returns"):
                        rs = f["returns"]
                        if not isinstance(rs, list):
                            rs = [rs]

                        for p in rs:
                            pname = p["name"] if p.get("name") else ""
                            ptype = p["type"] if p.get("type") else ""
                            pdesc = p["desc"] if p.get("desc") else ""
                            returns.append({"name": pname, "desc": pdesc, "type": ptype})

                    func = {
                        "org": org,
                        "name": name, 
                        "internal": internal,
                        "package":package, 
                        "module": module,
                        "params": params, 
                        "example": example,
                        "desc": desc,
                        #"runmode": runmode,
                        #"level": level, 
                        "group": group,
                        "returns": returns,
                        "public": public
                        }
                    if name.lower() in funcs:
                        funcs[name.lower()].extend([func])
                    else:
                        funcs[name.lower()] = [func]
        finally:
            return funcs
    
    @staticmethod
    def load_samples_recursive(library_def_file):

        if os.path.isfile(library_def_file):
            try:
                samples = ObjectModel.load_samples(library_def_file)
                return [sample for sample in samples if "script" in sample]
            except:
                return []
        
        all_samples = []
        for f in os.listdir(library_def_file):
            all_samples.extend(ObjectModel.load_samples_recursive(os.path.join(library_def_file, f)))
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