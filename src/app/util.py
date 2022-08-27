import os
from os import path
from flask import g

from app.io.fileop import HadoopFileSystem, GalaxyFileSystem, HttpFileSystem, SciDataFileSystem
from dsl.fileop import PosixFileSystem
from app.managers.datamgr import datamanager

class Utility:
    @staticmethod
    def ValueOrNone(val):
        try:
            return int(val)
        except ValueError:
            return 0
        
    @staticmethod
    def get_rootdir(datasource_id):
        datasource =  datamanager.get_datasource(id = datasource_id)
        if datasource_id == 1:
            return path.join(datasource.url, datasource.root)
        if datasource_id == 2:
            return datasource.url
        if datasource_id == 3:
            return path.join(datasource.url, '/')
        return ""
    
    # @staticmethod
    # def get_fullpath(data):
    #     #print(str(data_id), file=sys.stderr)
    #     if data is None:
    #         return ''
    #     return path.join(Utility.get_rootdir(data.datasource_id), data.url)
    
    @staticmethod
    def get_quota_path(path, username):
        if not path:
            path = 'public'
        elif username and not path.startswith('public'):
            path = os.path.join(username, path)
        return path

    @staticmethod
    def create_fs(ds):
        
        if 'fs' not in g:
            g.fs = {}
            
        if ds.type in g.fs:
            return g.fs[ds.type]
        
        fs = None
        if ds.type == 'hdfs':
            g.fs[ds.type] = HadoopFileSystem(ds.url, ds.root, ds.temp, ds.user)
        elif ds.type == 'posix':
            g.fs[ds.type] = PosixFileSystem(ds.url, ds.public, ds.temp, ds.name)
        elif ds.type == 'scidata':
            g.fs[ds.type] = SciDataFileSystem(ds.url, ds.public, ds.temp, ds.prefix)
        elif ds.type == 'gfs':
            g.fs[ds.type] = GalaxyFileSystem(ds.url, ds.password)
        
        return g.fs[ds.type]
    
    @staticmethod
    def ds_by_prefix_or_root(path):
        if not path:
            return None
        path = str(path)
        dsdb = None
        datasources = datamanager.get_datasources()
        for ds in datasources:
            if ds.prefix and path.startswith(ds.prefix):
                return ds
                
            if ds.url and path.startswith(ds.url):
                return dsdb
                
    @staticmethod
    def ds_by_prefix(path):
        if not path:
            return None
        path = str(path)
        datasources = datamanager.get_datasources()
        for ds in datasources:
            if ds.prefix:
                if path.startswith(ds.prefix):
                    return ds
                
            if ds.url:
                if path.startswith(ds.url):
                    return ds
    
    @staticmethod
    def fs_type_by_prefix_or_default(path):
        ds = Utility.ds_by_prefix(path)
        return ds.type if ds else 'posix'
    
    @staticmethod
    def fs_type_by_prefix(path):
        ds = Utility.ds_by_prefix(path)
        path = str(path)
        return ds.type if ds else "posix" if path.startswith(os.sep) else None
            
    @staticmethod
    def fs_by_prefix(path):
        ds = Utility.ds_by_prefix(path)
        if ds:
            return Utility.create_fs(ds)
    
    @staticmethod
    def fs_by_prefix_or_none(path):
        ds = Utility.ds_by_prefix(path)
        if ds:
            return Utility.create_fs(ds)
        
    @staticmethod
    def fs_by_prefix_or_guess(path):
        ds = Utility.ds_by_prefix(path)

        if not ds:
            if path.startswith('http://') or path.startswith('https://'):
                return HttpFileSystem(path)
            else:
                return Utility.fs_by_typename("posix")
        else:
            return Utility.create_fs(ds)
   
    @staticmethod
    def fs_by_typename(typename):
        ds = datamanager.get_datasource(type = typename)
        return Utility.create_fs(ds)
    
    @staticmethod
    def copyfile(src, dest):
        srctype = Utility.fs_type_by_prefix_or_default(src)
        desttype = Utility.fs_type_by_prefix_or_default(dest)
        
        fssrc = Utility.fs_type_by_prefix_or_default(src)
        src = str(src)
        dest = dest(src)
        if srctype != desttype:
            fsdest = Utility.fs_type_by_prefix_or_default(dest)
            content = fssrc.read(src)
            fsdest.write(dest, content)
        else:
            return fssrc.copyfile(src, dest)
        
        
    @staticmethod
    def get_normalized_path(path):
        fs = Utility.fs_by_prefix_or_guess(path)
        return fs.normalize_path(str(path))
    
    @staticmethod
    def strip_root(path):
        fs = Utility.fs_by_prefix_or_guess(path)
        return fs.strip_root(str(path))