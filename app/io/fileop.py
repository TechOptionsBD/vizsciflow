import os
from os.path import join
import pathlib
import shutil
import sys
import tempfile
from urllib.parse import urlparse, urlunparse, urlsplit, urljoin
import uuid
import urllib
import re
from dsl.fileop import PosixFileSystem
import requests

__author__ = "Mainul Hossain"
__date__ = "$Dec 10, 2016 2:23:14 PM$"

urllib.parse.uses_relative.append('hdfs')
urllib.parse.uses_netloc.append('hdfs')

try:
    import pyarrow
except:
    pass

try:
    from bioblend.galaxy import GalaxyInstance
except:
    pass
                                  
class HadoopFileSystem():
    timeout = 20 # 100s timeout
    def __init__(self, url, root, user, temp, prefix = None):
        u = urlsplit(url)
        if u.scheme != 'http' and u.scheme != 'https' and u.scheme != 'hdfs':
            raise ValueError("Invalid name node address")
        
        parsedurl = urlparse(url)
        self.client = pyarrow.hdfs.connect(host=parsedurl.hostname, port=parsedurl.port, user=user, driver='libhdfs')
        self.url = urlunparse((u.scheme, u.netloc, '', '', '', ''))
        self._localdir = root
        self.prefix = prefix
        self.temp = temp
    
    def typename(self):
        return "hdfs"
    
    def normalize_path(self, path):
        if self.prefix:
            path = self.strip_prefix(path)
            
        if self.url and path.startswith(self.url):
            path = path[len(self.url):]
            if not path.startswith(os.sep):
                path = os.sep + path
        
        if self._localdir and path.startswith(self._localdir):
            return path
 
        while path and path[0] == os.sep:
            path = path[1:]
        return os.path.join(self._localdir, path)
    
    def normalize_fullpath(self, path):
        return urljoin(self.url, self.normalize_path(path))
    
    def strip_prefix(self, path):
        return path[len(self.prefix):] if self.prefix and path.startswith(self.prefix) else path
    
    def strip_root(self, path):
        path = self.strip_prefix(path)
        if path.startswith(self.url):
            path = path[len(self.url):]
            if not path.startswith(self._localdir):
                raise 'Invalid hdfs path. It must start with the root directory'
        return path[len(self._localdir):] if path.startswith(self._localdir) else path
    
    def makedirs(self, path):
        path = self.normalize_path(path)
        if self.exists(path):
            return path
        dirnames = self.strip_root(path).split(os.sep)
        done = ''
        for dirname in dirnames:
            done = os.path.join(done, dirname)
            self.mkdir(done)
        return path
        
    def mkdir(self, path):
        path = self.normalize_path(path)
        self.client.mkdir(path)
        return path
    
    def unique_fs_name(self, path, prefix, ext):
        return IOHelper.unique_fs_name(self, path, prefix, ext)
    
    def remove(self, path):
        try: 
            path = self.normalize_path(path)
            if not self.client.exists(path):
                self.client.rm(path, True)
        except Exception as e:
            print(e)
           
    def rename(self, oldpath, newpath):
        try:
            oldpath = self.normalize_path(oldpath)
            newpath = self.normalize_path(newpath)
            self.client.rename(oldpath, newpath)
            return self.strip_root(newpath)
        except Exception as e:
            print(e)
    
    def get_files(self, path):
        path = self.normalize_path(path)
        files = []
        for f in self.client.ls(path):
            if self.client.isfile(join(path, f)):
                files.append(f)
        return files
    
    def get_folders(self, path):
        path = self.normalize_path(path)
        folders = []
        for f in self.client.list(path):
            if self.client.isdir(join(path, f)):
                folders.append(f)
        return folders
    
    def copyfile(self, src, dst):
        content = self.read(src)
        if self.isdir(dst):
            dst = os.path.join(dst, os.path.basename(src))
        self.write(dst, content)
        return self.normalize_fullpath(dst)
    
    def listdir(self, path):
        path = self.normalize_path(path)
        for f in self.client.ls(path):
            yield f
    
    def unique_filename(self, path, prefix, ext):
        stem = pathlib.Path(prefix).stem
        if not ext:
            ext = pathlib.Path(prefix).suffix
        make_fn = lambda i: self.join(path, '{0}_{1}.{2}'.format(stem, i, ext) if ext else '{0}_{1}'.format(stem, i))

        for i in range(1, sys.maxsize):
            uni_fn = make_fn(i)
            if not self.exists(uni_fn):
                return uni_fn
    
    def make_unique_dir(self, path):
        unique_dir = self.join(path, str(uuid.uuid4()))
        self.makedirs(unique_dir)
        return unique_dir
    
    def exists(self, path):
        path = self.normalize_path(path)
        return self.client.exists(path)
        
    def isdir(self, path):
        path = self.normalize_path(path)
        return self.client.isdir(path)
    
    def isfile(self, path):
        path = self.normalize_path(path)
        return self.client.isfile(path)
    
    def join(self, path1, path2):
        path1 = self.normalize_path(path1)
        return os.path.join(path1, path2)
    
    def read(self, path):
        path = self.normalize_path(path)
        with self.client.open(path, 'rb') as reader:
            return reader.read()
    
    def write(self, path, content):
        path = self.normalize_path(path)
        with self.client.open(path, 'wb') as writer:
            return writer.write(content)
    
    def make_json_item(self, path):
        data_json = { 'path': urljoin(self.url, self.normalize_path(path)), 'text': os.path.basename(path) }
        if self.isdir(path):
            data_json['nodes'] = []
        return data_json
        
    def make_json(self, path):
        data_json = self.make_json_item(path)
        
        if self.isdir(path):
            data_json['nodes'] = [self.make_json_item(os.path.join(path, fn)) for fn in self.listdir(self.normalize_path(path))]
            data_json['loaded'] = True
        return data_json
    
    def make_json_r(self, path):
        data_json = self.make_json_item(path)
        if self.isdir(path):
            data_json['nodes'] = [self.make_json_r(os.path.join(path, fn)) for fn in self.listdir(self.normalize_path(path))]
            data_json['loaded'] = True
        return data_json
     
    def save_upload(self, file, path):       
        localpath = os.path.join(tempfile.gettempdir(), os.path.basename(file.filename))
            
        if os.path.exists(localpath):
            fs = PosixFileSystem('/')
            unique_dir = fs.make_unique_dir(os.path.dirname(localpath))
            localpath = os.path.join(unique_dir, os.path.basename(file.filename))
            
        try:
            file.save(localpath)
            if self.isfile(path):
                path = os.path.dirname(path)
            
            with open(localpath, 'rb') as reader:
                self.write(path, reader.read())
        except:
            pass
        
    def download(self, path):
        path = self.normalize_path(path)
        if self.client.isfile(path):
            localpath = os.path.join(tempfile.gettempdir(), os.path.basename(path))
            if os.path.exists(localpath):
                fs = PosixFileSystem('/')
                unique_dir = fs.make_unique_dir(os.path.dirname(localpath))
                localpath = os.path.join(unique_dir, os.path.basename(path))
            
            with open(localpath, "wb") as writer:
                writer.write(self.read(path))
            return localpath

class GalaxyFileSystem():
    urlKey = 0
    hlddTitleKey = 1
    hlddKey = 2
    folderKey = 3
    hdaKey = 3
    lddaKey = 4
    
    def __init__(self, url, user):
        u = urlsplit(url)
        if u.scheme != 'http' and u.scheme != 'https':
            raise ValueError("Invalid name node address")
        
        self.url = urlunparse((u.scheme, u.netloc, '', '', '', ''))
        self._localdir = ""
        self.prefix = 'GalaxyFS'
        self.lddaprefix = 'Libraries'
        self.hdaprefix = 'Histories'
        self.client = GalaxyInstance(self.url, user)
    
    def typename(self):
        return "gfs"
    
    def strip_prefix(self, path):
        return path[len(self.prefix):] if self.prefix and path.startswith(self.prefix) else path
    
    def normalize_path(self, path):
        if self.prefix:
            path = self.strip_prefix(path)
            
        if self.url and path.startswith(self.url):
            return path
        
        if not self._localdir or path.startswith(self._localdir):
                return os.path.join(self.url, path)
 
        while path and path[0] == os.sep:
            path = path[1:]
        return os.path.join(self.url, self._localdir, path)

    def normalize_fullpath(self, path):
        return self.normalize_path(path)
    
    def strip_root(self, path):
        path = self.strip_prefix(path)
        if path.startswith(self.url):
            path = path[len(self.url):]
            if not path.startswith(self._localdir):
                raise 'Invalid hdfs path. It must start with the root directory'
        return path[len(self._localdir):] if path.startswith(self._localdir) else path
    
    def make_fullpath(self, path):
        path = self.normalize_path(path)
        return os.path.join(self.prefix, path)
     
    def makedirs(self, path):
        return self.mkdir(path)
        
    def mkdir(self, path):
        try:
            path = self.normalize_path(path)
            parts = self.path_parts(path)
            
            if len(parts) > 4 or len(parts) < 3:
                return "" #raise ValueError("Galaxy path may have maximum 4 parts.")
            hd_ldd = ''
            if len(parts) == 3:
                hd_ldd = self.client.libraries.create_library(parts[-1]) if self.islibrary(parts[GalaxyFileSystem.hlddTitleKey]) else self.client.histories.create_history(parts[-1])
            elif len(parts) == 4:
                if not self.islibrary(parts[GalaxyFileSystem.hlddTitleKey]):
                    return ""
                hd_ldd = self.client.libraries.create_folder(parts[GalaxyFileSystem.lddaKey], parts[-1])
                
            parts[-1] = hd_ldd['id']
            
            return os.sep.join(parts['id'])
        except:
            return None
    
    def unique_fs_name(self, path, prefix, ext):
        return os.path.join(path, prefix + "_" + str(uuid.uuid4()) + ext)
    
    def remove(self, path):
        try:
            path = self.normalize_path(path)
            parts = self.path_parts(path)
            if len(parts) > 4:
                raise ValueError("Galaxy path may have maximum 4 parts.")
            if self.islibrary(parts[GalaxyFileSystem.hlddTitleKey]):
                self.client.libraries.delete_library(library_id = parts[-1])
            else:
                self.client.histories.delete_history(history_id = parts[-1])
        except Exception as e:
            print(e)
           
    def rename(self, oldpath, newpath):
        try:
            oldpath = self.normalize_path(oldpath)
            newpath = self.normalize_path(newpath)
            self.client.rename(oldpath, newpath)
            return self.strip_root(newpath)
        except Exception as e:
            print(e)
    
    def copyfile(self, src, dst):
        if self.islibrarydata(src) and not self.islibrarydata(dst):
            parts = self.path_parts(self.normalize_path(src))
            self.client.libraries.copy_from_dataset(parts[GalaxyFileSystem.hlddKey], self.id_from_path(dst), parts[GalaxyFileSystem.folderKey])
        elif not self.islibrary(parts[GalaxyFileSystem.hlddTitleKey]) and self.islibrarydata(dst):
            parts = self.path_parts(self.normalize_path(dst))
            self.client.histories.upload_dataset_from_library(parts[GalaxyFileSystem.hdaKey], self.id_from_path(src))
        else:
            content = self.read(src)
            if self.isdir(dst):
                dst = os.path.join(dst, os.path.basename(src))
                self.write(dst, content)
        return self.normalize_fullpath(dst)
    
    def get_files(self, path):
        path = self.normalize_path(path)
        files = []
        for f in self.client.list(path):
            status = self.client.status(join(path, f), False)
            if status['type'] != "DIRECTORY":
                files.append(f)
        return files
    
    def get_folders(self, path):
        try:
            normalized_path = self.normalize_path(path)
            parts = self.path_parts(normalized_path)
            if len(parts) > 4:
                raise ValueError("Galaxy path may have maximum 4 parts.")

            parts[-1] = self.client.libraries.create_library(parts[-1]) if self.islibrary(parts[GalaxyFileSystem.hlddTitleKey]) else self.client.histories.create_history(parts[-1])
            
            path = os.sep.join(parts)
            return self.make_fullpath(path)
        except:
            return []
        return path       
    
    def exists(self, path):
        return self.isdir(path) or self.isfile(path)
     
    def islibrary(self, name):
        return name == self.lddaprefix
    
    def islibrarydata(self, path):
        normalized_path = self.normalize_path(path)
        parts = self.path_parts(normalized_path)
        return self.islibrary(parts[GalaxyFileSystem.hlddTitleKey])
       
    def isdir(self, path):
        normalized_path = self.normalize_path(path)
        parts = self.path_parts(normalized_path)
        return len(parts) <= GalaxyFileSystem.lddaKey if self.islibrary(parts[GalaxyFileSystem.hlddTitleKey]) else len(parts) <= GalaxyFileSystem.hdaKey
    
    def isfile(self, path):
        return not self.isdir(path) and self.name_from_id(path) != ""
    
    def join(self, path1, path2):
        path1 = self.normalize_path(path1)
        return os.path.join(path1, path2)
    
    def make_unique_dir(self, path):
        unique_dir = self.join(path, str(uuid.uuid4()))
        self.makedirs(unique_dir)
        return unique_dir
        
    def read(self, path):
        path = self.normalize_path(path)
        with self.client.read(path, 'rb') as reader:
            return reader.read()
    
    def write(self, path, content):
        path = self.normalize_path(path)
        self.client.write(path, content)
    
    def id_from_path(self, path):
        normalized_path = self.normalize_path(path)
        parts = self.path_parts(normalized_path)
        if len(parts) <= GalaxyFileSystem.urlKey + 1:
            return ""
        elif len(parts) == GalaxyFileSystem.hlddTitleKey + 1:#Histories/Libraries
            return parts[GalaxyFileSystem.hlddTitleKey] 
        elif len(parts) == GalaxyFileSystem.hlddKey + 1: #library-name/history-name
            info = self.client.libraries.get_libraries(library_id = parts[GalaxyFileSystem.hlddKey])[0] if parts[GalaxyFileSystem.hlddTitleKey] == self.lddaprefix else self.client.histories.get_histories(history_id = parts[GalaxyFileSystem.hlddKey])[0]
            return info['id']
        elif len(parts) == GalaxyFileSystem.folderKey + 1: #Folder(library)/Dataset(history)
            if parts[GalaxyFileSystem.hlddTitleKey] == self.lddaprefix:
                folder = self.client.folders.show_folder(parts[3], False)
                return folder['id']
            else:
                info = self.client.datasets.show_dataset(dataset_id = parts[GalaxyFileSystem.hdaKey], hda_ldda = 'hda')
                return info['id']
        elif len(parts) == GalaxyFileSystem.lddaKey + 1:
            info = self.client.datasets.show_dataset(dataset_id = parts[GalaxyFileSystem.lddaKey], hda_ldda = 'ldda')
            return info['id']
    
    def path_parts(self, path):
        parts = []
        if path.startswith(self.prefix):
            parts.append(self.prefix)
            if len(path) > len(self.prefix):
                path = path[len(self.prefix) + 1:]
        elif path.startswith(self.url):
            parts.append(self.url)
            if len(path) > len(self.url):
                path = path[len(self.url) + 1:]
            
        parts.extend(pathlib.Path(path).parts)
        return parts
              
    def name_from_id(self, path):
        normalized_path = self.normalize_path(path)
        parts = self.path_parts(normalized_path)
        if len(parts) <= GalaxyFileSystem.urlKey + 1:
            return ""
        elif len(parts) == GalaxyFileSystem.hlddTitleKey + 1:#Histories/Libraries
            return parts[GalaxyFileSystem.hlddTitleKey] 
        elif len(parts) == GalaxyFileSystem.hlddKey + 1: #library-name/history-name
            info = self.client.libraries.get_libraries(library_id = parts[GalaxyFileSystem.hlddKey])[0] if self.islibrary(parts[GalaxyFileSystem.hlddTitleKey]) else self.client.histories.get_histories(history_id = parts[GalaxyFileSystem.hlddKey])[0]
            return info['name']
        elif len(parts) == GalaxyFileSystem.folderKey + 1: #Folder(library)/Dataset(history)
            if parts[GalaxyFileSystem.hlddTitleKey] == self.lddaprefix:
                folder = self.client.folders.show_folder(parts[GalaxyFileSystem.folderKey], False)
                return folder['name']
            else:
                info = self.client.datasets.show_dataset(dataset_id = parts[GalaxyFileSystem.hdaKey], hda_ldda = 'hda')
                return info['name']
        elif len(parts) == GalaxyFileSystem.lddaKey + 1:
            info = self.client.datasets.show_dataset(dataset_id = parts[GalaxyFileSystem.lddaKey], hda_ldda = 'ldda')
            return info['name']
    
    def make_json_item(self, path):
        data_json = { 'path': self.normalize_path(path), 'text': "{0}(id:{1})".format(self.name_from_id(path), self.id_from_path(path)) }
        if self.isdir(path):
            data_json['nodes'] = []
        return data_json
        
    def make_json(self, path):
        normalized_path = self.normalize_path(path)
        if not normalized_path or normalized_path == self.url:
            return [self.make_json_item(urljoin(self.url, self.lddaprefix)), self.make_json_item(urljoin(self.url, self.hdaprefix))]
        else:
            data_json = self.make_json_item(path)
            parts = self.path_parts(normalized_path)
            if self.islibrary(parts[GalaxyFileSystem.hlddTitleKey]):
                if len(parts) == GalaxyFileSystem.hlddTitleKey + 1:
                    libraries = self.client.libraries.get_libraries()
                    data_json['nodes'] = [self.make_json_item(os.path.join(path, fn['id'])) for fn in libraries]
                elif len(parts) == GalaxyFileSystem.hlddKey + 1:
                    folders = self.client.libraries.get_folders(library_id = parts[GalaxyFileSystem.hlddKey])
                    data_json['nodes'] = [self.make_json_item(os.path.join(path, fn['id'])) for fn in folders]
                elif len(parts) == GalaxyFileSystem.folderKey + 1:
                    folder = self.client.folders.show_folder(parts[GalaxyFileSystem.folderKey], True)
                    data_json['nodes'] = [self.make_json_item(os.path.join(path, fn['id'])) for fn in folder['folder_contents']]
            else:
                if len(parts) == GalaxyFileSystem.hlddTitleKey + 1:
                    histories = self.client.histories.get_histories()
                    data_json['nodes'] = [self.make_json_item(os.path.join(path, fn['id'])) for fn in histories]
                elif len(parts) == GalaxyFileSystem.hlddKey + 1:
                    datasets = self.client.histories.show_matching_datasets(parts[GalaxyFileSystem.hlddKey])
                    data_json['nodes'] = [self.make_json_item(os.path.join(path, fn['id'])) for fn in datasets]
            
            data_json['loaded'] = True
            return data_json
    
    @staticmethod    
    def get_history_path(url, history_id, data_id):
        return urljoin(url, os.path.join('Histories', history_id, data_id))
            
    def make_json_r(self, path):
        normalized_path = self.normalize_path(path)
        if not normalized_path or normalized_path == self.url:
            return [self.make_json_r(urljoin(self.url, self.lddaprefix)), self.make_json_r(urljoin(self.url, self.hdaprefix))]
        else:
            data_json = self.make_json_item(path)
            parts = self.path_parts(normalized_path)
            if self.islibrary(parts[GalaxyFileSystem.hlddTitleKey]):
                if len(parts) == GalaxyFileSystem.hlddTitleKey + 1:
                    libraries = self.client.libraries.get_libraries()
                    data_json['nodes'] = [self.make_json_r(os.path.join(path, fn['id'])) for fn in libraries]
                elif len(parts) == GalaxyFileSystem.hlddKey + 1:
                    folders = self.client.libraries.get_folders(library_id = parts[GalaxyFileSystem.hlddKey])
                    data_json['nodes'] = [self.make_json_r(os.path.join(path, fn['id'])) for fn in folders]
                elif len(parts) == GalaxyFileSystem.folderKey + 1:
                    folder = self.client.folders.show_folder(parts[GalaxyFileSystem.folderKey], True)
                    data_json['nodes'] = [self.make_json_item(os.path.join(path, fn['id'])) for fn in folder['folder_contents']]
            else :
                if len(parts) == GalaxyFileSystem.hlddTitleKey + 1:
                    histories = self.client.histories.get_histories()
                    data_json['nodes'] = [self.make_json_r(os.path.join(path, fn['id'])) for fn in histories]
                elif len(parts) == GalaxyFileSystem.hlddKey + 1:
                    datasets = self.client.histories.show_matching_datasets(parts[GalaxyFileSystem.hlddKey])
                    data_json['nodes'] = [self.make_json_item(os.path.join(path, fn['id'])) for fn in datasets]
                    
            data_json['loaded'] = True
            return data_json
     
    def save_upload(self, file, path):
        if self.isfile(path):
            path = os.path.dirname(path)
        elif not self.isdir(path):
            return ""
        parts = self.path_parts(path)
        if not parts or len(parts) < 3:
            return ""
        
        localpath = os.path.join(tempfile.gettempdir(), os.path.basename(file.filename))
            
        if os.path.exists(localpath):
            fs = PosixFileSystem('/')
            unique_dir = fs.make_unique_dir(os.path.dirname(localpath))
            localpath = os.path.join(unique_dir, os.path.basename(file.filename))
            
        try:
            file.save(localpath)
            
            dataset = ''        
            if self.islibrary(parts[1]):
                dataset = self.client.libraries.upload_file_from_local_path(parts[2], localpath, folder_id=parts[3] if len(parts) > 3 else None)
            else:
                dataset = self.client.tools.upload_file(localpath, parts[2])
            
            if dataset:
                return os.path.join(path, dataset['id']);
        except:
            pass
                
    def download(self, path):
        path = self.normalize_path(path)
        if self.isdir(path):
            return None
        
        dataset = self.client.datasets.show_dataset(dataset_id = os.path.basename(path), hda_ldda = 'ldda' if self.islibrarydata(path) else 'hda')
        name = dataset['name']
        if not pathlib.Path(name).suffix and dataset['file_ext']:
            name += '.' + dataset['file_ext']
        
        localpath = os.path.join(tempfile.gettempdir(), name)
            
        if os.path.exists(localpath):
            fs = PosixFileSystem('/')
            unique_dir = fs.make_unique_dir(os.path.dirname(localpath))
            localpath = os.path.join(unique_dir, name)
        
        self.client.datasets.download_dataset(os.path.basename(path), file_path = localpath, use_default_filename=False)
        return localpath

class HttpFileSystem():
    timeout = 20 # 100s timeout
    def __init__(self, url, root = None, temp = None, prefix = None):
        u = urlsplit(url)
        if u.scheme != 'http' and u.scheme != 'https':
            raise ValueError("Invalid url address")
        
        self.url = url
        self._localdir = root
        self.prefix = prefix
        self.temp = temp
    
    def typename(self):
        return "http"
    
    def basename(self, path):
        u = urlsplit(path)
        path = urlunparse((u.scheme, u.netloc, u.path, '', '', ''))
        return os.path.basename(path)
        
    def normalize_path(self, path):
        if self.prefix:
            path = self.strip_prefix(path)
            
        if not self._localdir or path.startswith(self._localdir) or (self._localdir.endswith(os.sep) and path == self._localdir[:-1]):
            return path
        while path and path[0] == os.sep:
            path = path[1:]    
        return os.path.join(self._localdir, path)
    
    def normalize_fullpath(self, path):
        return urljoin(self.url, self.normalize_path(path))
    
    def strip_prefix(self, path):
        return path[len(self.prefix):] if self.prefix and path.startswith(self.prefix) else path
    
    def strip_root(self, path):
        path = self.strip_prefix(path)
        if path.startswith(self.url):
            path = path[len(self.url):]
        return path[len(self._localdir):] if path.startswith(self._localdir) else path
    
    def makedirs(self, path):
        raise NotImplementedError("makedirs")
        
    def mkdir(self, path):
        raise NotImplementedError("makedir")
    
    def unique_fs_name(self, path, prefix, ext):
        return IOHelper.unique_fs_name(self, path, prefix, ext)
    
    def remove(self, path):
        raise NotImplementedError("remove")
           
    def rename(self, oldpath, newpath):
        raise NotImplementedError("rename")
    
    def get_files(self, path):
        raise NotImplementedError("get_files")
    
    def get_folders(self, path):
        raise NotImplementedError("get_folders")
    
    def copyfile(self, src, dst):
        content = self.read(src)
        if self.isdir(dst):
            dst = os.path.join(dst, os.path.basename(src))
        self.write(dst, content)
        return self.normalize_fullpath(dst)
    
    def listdir(self, path):
        raise NotImplementedError("listdir")
    
    def unique_filename(self, path, prefix, ext):
        raise NotImplementedError("unique_filename")
    
    def make_unique_dir(self, path):
        raise NotImplementedError("make_unique_dir")
    
    def exists(self, path):
        response = requests.head(self.normalize_path(path))
        return response.status_code == 200
        
    def isdir(self, path):
        raise NotImplementedError("isdir")
    
    def isfile(self, path):
        return self.exists(path)
    
    def join(self, path1, path2):
        path1 = self.normalize_path(path1)
        return os.path.join(path1, path2)
    
    def read(self, path):
        path = self.normalize_path(path)
        r = requests.get(path, allow_redirects=True)
        return r.content
    
    def write(self, path, content):
        if not self.canwrite:
            raise ValueError("Read only file system")
    
    def make_json_item(self, path):
        raise NotImplementedError("make_json_item")
        
    def make_json(self, path):
        raise NotImplementedError("make_json")
    
    def make_json_r(self, path):
        raise NotImplementedError("make_json_r")
     
    def save_upload(self, file, path):       
        raise NotImplementedError("save_upload")
        
    def download(self, path):
        path = self.normalize_path(path)
        localpath = os.path.join(tempfile.gettempdir(), os.path.basename(path))
        if os.path.exists(localpath):
            fs = PosixFileSystem('/')
            unique_dir = fs.make_unique_dir(os.path.dirname(localpath))
            localpath = os.path.join(unique_dir, os.path.basename(path))
        
        with open(localpath, "wb") as writer:
            writer.write(self.read(path))
        return localpath

class IOHelper():
    @staticmethod
    def getFileSystem(url):
        try:
            u = urlsplit(url)
            if u.scheme == 'http' or u.scheme == 'https' or u.scheme == 'hdfs':
                return HadoopFileSystem(url, 'hdfs')
        except:
            pass
        return PosixFileSystem()
    
    @staticmethod
    def get_files(path):
        filesystem = IOHelper.getFileSystem(path)
        return filesystem.get_files(path)
    
    @staticmethod
    def get_folders(path):
        filesystem = IOHelper.getFileSystem(path)
        return filesystem.get_folders(path)
    
    @staticmethod
    def remove(path):
        filesystem = IOHelper.getFileSystem(path)
        filesystem.remove(path)
        
    @staticmethod
    def makedirs(path):
        filesystem = IOHelper.getFileSystem(path)
        return filesystem.makedirs(path)
    
    @staticmethod
    def rename(oldpath, newpath):
        filesystem = IOHelper.getFileSystem(oldpath)
        filesystem.rename(oldpath, newpath)
        
    @staticmethod
    def read(path):
        filesystem = IOHelper.getFileSystem(path)
        return filesystem.read(path)
    
    @staticmethod
    def normalize_path(path):
        filesystem = IOHelper.getFileSystem(path)
        return filesystem.normalize_path(path)
    
    @staticmethod
    def write(path, content):
        filesystem = IOHelper.getFileSystem(path)
        return filesystem.write(path, content)
    
    @staticmethod
    def unique_fs_name(filesystem, path, prefix, ext):

        make_fn = lambda i: os.path.join(path, '{0}({1}){2}'.format(prefix, i, ext))

        for i in range(1, sys.maxsize):
            uni_fn = make_fn(i)
            if not filesystem.exists(uni_fn):
                return uni_fn

    @staticmethod
    def unique_filename(path, prefix, ext):
        filesystem = IOHelper.getFileSystem(path)
        return IOHelper.unique_fs_name(filesystem, path, prefix, ext)


                        
if __name__ == "__main__":
    print("Hello World")