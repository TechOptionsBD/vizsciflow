from __future__ import print_function

import os
from os import path
from .models import DataSource
import sys
from app.biowl.fileop import PosixFileSystem, HadoopFileSystem, GalaxyFileSystem

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
            return path.join(datasource.root)
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
        elif not path.startswith('public'):
            path = os.path.join(username, path)
        return path
    
    @staticmethod
    def create_fs(ds):
        if ds.type == 'hdfs':
            return HadoopFileSystem(ds.url, ds.root, ds.user)
        elif ds.type == 'posix':
            return PosixFileSystem(ds.url, ds.name)
        elif ds.type == 'gfs':
            return GalaxyFileSystem(ds.url, ds.password)
    
    @staticmethod
    def fs_type_by_prefix(path):
        if path:
            #path = os.path.normpath(path)
            datasources = DataSource.query.all()
            for ds in datasources:
                if ds.prefix:
                    if path.startswith(ds.prefix):
                        return ds.type
                    
                if ds.url:
                    if path.startswith(ds.url):
                        return ds.type
                    
        return 'posix'
            
    @staticmethod
    def fs_by_prefix(path):
        fs_type = Utility.fs_type_by_prefix(path)
        ds = DataSource.query.filter_by(type = fs_type).first()
        return Utility.create_fs(ds.url)
    
    @staticmethod
    def get_normalized_path(path):
        fs = Utility.fs_by_prefix(path)
        path = fs.strip_root(path)
        path = Utility.get_quota_path(path)
        return fs.normalize_path(path)