from __future__ import print_function

import os
from os import path
from .models import DataSource
import sys
from app.biowl.fileop import PosixFileSystem, HadoopFileSystem, GalaxyFileSystem
from flask_login import current_user

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
            return PosixFileSystem(ds.url)
        elif ds.type == 'gfs':
            return GalaxyFileSystem(ds.url, ds.user)
    
    @staticmethod
    def ds_by_prefix(path):
        if path:
            #path = os.path.normpath(path)
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
        if ds:
            return ds.type
            
    @staticmethod
    def fs_by_prefix(path):
        ds = Utility.ds_by_prefix(path)
        if ds:
            return Utility.create_fs(ds)
    
    @staticmethod
    def fs_by_prefix_or_default(path):
        ds = Utility.ds_by_prefix(path)
        if not ds:
            ds = DataSource.query.filter_by(type = 'posix').first()
        return Utility.create_fs(ds)
    
    @staticmethod
    def get_normalized_path(path):
        fs = Utility.fs_by_prefix_or_default(path)
        path = fs.strip_root(path)
        username = current_user.username if current_user.is_authenticated else ''
        path = Utility.get_quota_path(path, username)
        return fs.normalize_path(path)