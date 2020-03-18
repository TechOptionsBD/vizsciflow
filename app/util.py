from __future__ import print_function

import os
from os import path
from .models import DataSource

from app.biowl.fileop import HadoopFileSystem, GalaxyFileSystem
from dsl.fileop import PosixFileSystem

class Utility:
    @staticmethod
    def ValueOrNone(val):
        try:
            return int(val)
        except ValueError:
            return 0
        
    @staticmethod
    def get_rootdir(datasource_id):
        datasource = DataSource.query.get(datasource_id)
        if datasource_id == 1:
            return path.join(datasource.url, datasource.root)
        if datasource_id == 2:
            return datasource.url
        if datasource_id == 3:
            return path.join(datasource.url, '/')
        return ""
    
    @staticmethod
    def get_fullpath(data):
        #print(str(data_id), file=sys.stderr)
        if data is None:
            return ''
        return path.join(Utility.get_rootdir(data.datasource_id), data.url)
    
    @staticmethod
    def get_quota_path(path, username):
        if not path:
            path = 'public'
        elif username and not path.startswith('public'):
            path = os.path.join(username, path)
        return path
    
    @staticmethod
    def create_fs(ds):
        if ds.type == 'hdfs':
            return HadoopFileSystem(ds.url, ds.root, ds.user)
        elif ds.type == 'posix':
            return PosixFileSystem(ds.url, ds.public, ds.name)
        elif ds.type == 'gfs':
            return GalaxyFileSystem(ds.url, ds.password)
    
    @staticmethod
    def ds_by_prefix_or_default(path):
        if not path:
            return None
        path = str(path)
        dsdb = None
        datasources = DataSource.query.all()
        for ds in datasources:
            if ds.prefix:
                if path.startswith(ds.prefix):
                    dsdb = ds
                    break
                
            if ds.url:
                if path.startswith(ds.url):
                    dsdb = ds
                    break
        if not dsdb:
            dsdb = DataSource.query.filter_by(type = "posix").first()
        return dsdb
                
    @staticmethod
    def ds_by_prefix(path):
        if not path:
            return None
        path = str(path)
        datasources = DataSource.query.all()
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
    def fs_by_prefix_or_default(path):
        ds = Utility.ds_by_prefix(path)
        return Utility.create_fs(ds) if ds else Utility.fs_by_typename("posix")
    
    @staticmethod
    def fs_by_typename(typename):
        ds = DataSource.query.filter_by(type = typename).first()
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
        fs = Utility.fs_by_prefix_or_default(path)
        return fs.normalize_path(str(path))
    
    @staticmethod
    def strip_root(path):
        fs = Utility.fs_by_prefix_or_default(path)
        return fs.strip_root(str(path))