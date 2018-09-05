from __future__ import print_function

import os
from os.path import join
import pathlib
import shutil
import sys
import tempfile
from urllib.parse import urlunparse, urlsplit, urljoin
import uuid


__author__ = "Mainul Hossain"
__date__ = "$Dec 10, 2016 2:23:14 PM$"


try:
    from hdfs import InsecureClient
except:
    pass

try:
    from bioblend.galaxy import GalaxyInstance
except:
    pass

class PosixFileSystem():
    
    def __init__(self, root, prefix = None):
        
        self.localdir = root
        if not os.path.exists(self.localdir):
            os.makedirs(self.localdir)
        self.prefix = prefix
        
    def normalize_path(self, path):
        path = os.path.normpath(path)
        if self.prefix:
            path = self.strip_prefix(path)
        if path.startswith(self.localdir):
            return path
        while path and path[0] == os.sep:
            path = path[1:]    
        return os.path.join(self.localdir, path)
    
    def makedirs(self, path):
        os.makedirs(self.normalize_path(path))
    
    def unique_fs_name(self, path, prefix, ext):
        return IOHelper.unique_filename(self, path, prefix, ext)
                    
    def make_prefix(self, path):
        if not self.prefix:
            return path     
        if path.startswith(self.prefix):
            return path
        if path.startswith(self.localdir):
            path = path[len(self.localdir):]
        if not path.startswith(os.sep):
            path = os.sep + path
        return self.prefix + path
    
    def strip_prefix(self, path):      
        return path[len(self.prefix):] if self.prefix and path.startswith(self.prefix) else path
        
    def strip_root(self, path):
        path = self.strip_prefix(path)
        return path[len(self.localdir):] if path.startswith(self.localdir) else path
            
    def mkdirs(self, path):
        path = self.normalize_path(path)
        if not os.path.exists(path):
            os.makedirs(path) 
        return self.make_prefix(path)
    
    def remove(self, path):
        path = self.normalize_path(path)
        dirpath = os.path.dirname(path)
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)
        return self.make_prefix(dirpath)
               
    def rename(self, oldpath, newpath):
        oldpath = self.normalize_path(oldpath)
        newpath = self.normalize_path(newpath)
        os.rename(oldpath, newpath)
        return self.make_prefix(newpath)
    
    def get_files(self, path):
        path = self.normalize_path(path)
        return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    
    def get_folders(self, path):
        path = self.normalize_path(path)
        return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    
    def listdir(self, path):
        path = self.normalize_path(path)
        return os.listdir(path)
            
    def read(self, path):
        path = self.normalize_path(path)
        with open(path) as reader:
            return reader.read().decode('utf-8')
        
    def write(self, path, content):
        path = self.normalize_path(path)
        with open(path, 'w') as writer:
            return writer.write(content)
        
    def unique_filename(self, path, prefix, ext):
        make_fn = lambda i: os.path.join(self.normalize_path(path), '{0}_{1}.{2}'.format(prefix, i, ext))

        for i in range(1, sys.maxsize):
            uni_fn = make_fn(i)
            if not self.exists(uni_fn):
                return uni_fn
    
    def make_unique_dir(self, path):
        unique_dir = self.join(path, str(uuid.uuid4()))
        os.makedirs(unique_dir)
        return unique_dir
            
    def exists(self, path):
        return os.path.exists(self.normalize_path(path))
        
    def isdir(self, path):
        return os.path.isdir(self.normalize_path(path))
    
    def isfile(self, path):
        return os.path.isfile(self.normalize_path(path))
    
    def join(self, path1, path2):
        path1 = self.normalize_path(path1)
        return os.path.join(path1, path2)
    
    def make_json_item(self, path):
        data_json =  { 'path': self.make_prefix(path), 'text': os.path.basename(path) }
        if self.isdir(path):
            data_json['nodes'] = []
        return data_json
        
    def make_json(self, path):
        data_json = self.make_json_item(path)
        
        if self.isdir(path):
            data_json['nodes'] = [self.make_json_item(os.path.join(path, fn)) for fn in os.listdir(self.normalize_path(path))]
            data_json['loaded'] = True
        return data_json
    
    def make_json_r(self, path):
        normalized_path = self.normalize_path(path)
        data_json = { 'path': self.make_prefix(path), 'text': os.path.basename(path) }
        data_json['folder'] = os.path.isdir(normalized_path)
        
        if os.path.isdir(normalized_path):
            data_json['nodes'] = [self.make_json_r(os.path.join(path, fn)) for fn in os.listdir(normalized_path)]
        return data_json

    def save_upload(self, file, path):
        path = self.normalize_path(path)
        if self.isfile(path):
            path = os.path.dirname(path)
        elif not os.path.exists(path):
            os.makedirs(path)
        file.save(os.path.join(path, file.filename))
        return self.make_prefix(os.path.join(path, file.filename))
    
    def download(self, path):
        path = self.normalize_path(path)
        if os.path.isfile(path):
            return path
        else:
            return None
                                   
class HadoopFileSystem():
    def __init__(self, url, root, user, prefix = None):
        u = urlsplit(url)
        if u.scheme != 'http' and u.scheme != 'https' and u.scheme != 'hdfs':
            raise ValueError("Invalid name node address")
        
        self.url = urlunparse((u.scheme, u.netloc, '', '', '', ''))
        self.client = InsecureClient(self.url, user=user, timeout=100)
        self.localdir = root
        self.prefix = prefix
    
    def normalize_path(self, path):
        if self.prefix:
            path = self.strip_prefix(path)
            
        if self.url and path.startswith(self.url):
            path = path[len(self.url):]
            if not path.startswith(os.sep):
                path = os.sep + path
        
        if self.localdir and path.startswith(self.localdir):
            return path
 
        while path and path[0] == os.sep:
            path = path[1:]
        return os.path.join(self.localdir, path)
    
    def strip_prefix(self, path):
        return path[len(self.prefix):] if self.prefix and path.startswith(self.prefix) else path
    
    def strip_root(self, path):
        path = self.strip_prefix(path)
        if path.startswith(self.url):
            path = path[len(self.url):]
            if not path.startswith(self.localdir):
                raise 'Invalid hdfs path. It must start with the root directory'
        return path[len(self.localdir):] if path.startswith(self.localdir) else path
        
    def mkdirs(self, path):
        try:
            path = self.normalize_path(path)
            self.client.makedirs(path)
        except:
            return None
        return path
    
    def unique_fs_name(self, path, prefix, ext):
        return IOHelper.unique_filename(self, path, prefix, ext)
    
    def remove(self, path):
        try: 
            path = self.normalize_path(path)
            if self.client.status(path, False) is not None:
                self.client.delete(path, True)
        except Exception as e:
            print(e)
           
    def rename(self, oldpath, newpath):
        try:
            oldpath = self.normalize_path(oldpath)
            newpath = self.normalize_path(newpath)
            self.client.rename(oldpath, newpath)
        except Exception as e:
            print(e)
    
    def get_files(self, path):
        path = self.normalize_path(path)
        files = []
        for f in self.client.list(path):
            status = self.client.status(join(path, f), False)
            if status['type'] != "DIRECTORY":
                files.append(f)
        return files
    
    def get_folders(self, path):
        path = self.normalize_path(path)
        folders = []
        for f in self.client.list(path):
            status = self.client.status(join(path, f), False)
            if status['type'] == "DIRECTORY":
                folders.append(f)
        return folders
    
    def listdir(self, path):
        path = self.normalize_path(path)
        for f in self.client.list(path):
            yield f
    
    def unique_filename(self, path, prefix, ext):
        make_fn = lambda i: os.path.join(self.normalize_path(path), '{0}_{1}.{2}'.format(prefix, i, ext))

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
        status = self.client.status(path, False)
        return not (status is None)
        
    def isdir(self, path):
        path = self.normalize_path(path)
        status = self.client.status(path, False)
        return status['type'] == "DIRECTORY"
    
    def isfile(self, path):
        path = self.normalize_path(path)
        status = self.client.status(path, False)
        return status['type'] == "FILE"
    
    def join(self, path1, path2):
        path1 = self.normalize_path(path1)
        return os.path.join(path1, path2)
    
    def read(self, path):
        path = self.normalize_path(path)
        with self.client.read(path) as reader:
            return reader.read().decode('utf-8')
    
    def write(self, path, content):
        path = self.normalize_path(path)
        self.client.write(path, content)
    
    def make_json_item(self, path):
        data_json = { 'path': urljoin(self.url, self.normalize_path(path)), 'text': os.path.basename(path) }
        if self.isdir(path):
            data_json['nodes'] = []
        return data_json
        
    def make_json(self, path):
        data_json = self.make_json_item(path)
        
        if self.isdir(path):
            data_json['nodes'] = [self.make_json_item(os.path.join(path, fn)) for fn in self.client.list(self.normalize_path(path))]
            data_json['loaded'] = True
        return data_json
    
    def make_json_r(self, path):
        normalized_path = self.normalize_path(path)
        data_json = { 'path': urljoin(self.url, normalized_path), 'text': os.path.basename(path) }
        status = self.client.status(normalized_path, False)

        if status is not None:
            data_json['folder'] = status['type'] == "DIRECTORY"
            if status['type'] == "DIRECTORY":
                data_json['nodes'] = [self.make_json_r(os.path.join(path, fn)) for fn in self.client.list(normalized_path)]
        #print(json.dumps(data_json))
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
            self.client.upload(self.normalize_path(path), localpath, True)
        except:
            pass
        
    def download(self, path):
        path = self.normalize_path(path)
        status = self.client.status(path, False)
        if status is not None and status['type'] == "FILE":
            localpath = os.path.join(tempfile.gettempdir(), os.path.basename(path))
            return self.client.download(path, localpath, True)
        else:
            return None

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
        self.localdir = ""
        self.prefix = 'GalaxyFS'
        self.lddaprefix = 'Libraries'
        self.hdaprefix = 'Histories'
        self.client = GalaxyInstance(self.url, user)
    
    def strip_prefix(self, path):
        return path[len(self.prefix):] if self.prefix and path.startswith(self.prefix) else path
    
    def normalize_path(self, path):
        if self.prefix:
            path = self.strip_prefix(path)
            
        if self.url and path.startswith(self.url):
            suffix = path[len(self.url):]
            while suffix and suffix[0] == os.sep:
                suffix = suffix[1:]
            return os.path.join(self.url, suffix)
        
        if self.localdir and path.startswith(self.localdir):
            return path
 
        while path and path[0] == os.sep:
            path = path[1:]
        return os.path.join(self.localdir, path)

    def strip_root(self, path):
        if path.startswith(self.url):
            path = path[len(self.url):]
            if not path.startswith(self.localdir):
                raise ValueError("Invalid hdfs path. It must start with the root directory")
      
        if not path.startswith(self.localdir):
            return path
        
        return path[len(self.localdir):]
    
    def make_fullpath(self, path):
        path = self.normalize_path(path)
        return os.path.join(self.prefix, path)
        
    def mkdirs(self, path):
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
        except Exception as e:
            print(e)
    
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
        with self.client.read(path) as reader:
            return reader.read().decode('utf-8')
    
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
        data_json = { 'path': self.normalize_path(path), 'text': self.name_from_id(path) }
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
        if not normalized_path:
            return [self.make_json_r(self.lddaprefix), self.make_json_r(self.hdaprefix)]
        else:
            data_json = { 'path': urljoin(self.url, normalized_path), 'text': self.name_from_id(path) }
            parts = self.path_parts(normalized_path)
            if self.islibrary(parts[GalaxyFileSystem.hlddTitleKey]):
                if len(parts) == 1:
                    data_json['folder'] = True
                    libraries = self.client.libraries.get_libraries()
                    data_json['nodes'] = [self.make_json_r(os.path.join(path, fn['id'])) for fn in libraries]
                elif len(parts) == 2:
                    data_json['folder'] = True
                    folders = self.client.libraries.get_folders(library_id = parts[1])
                    data_json['nodes'] = [self.make_json_r(os.path.join(path, fn['id'])) for fn in folders]
                elif len(parts) == 3:
                    data_json['folder'] = True
                    folder = self.client.folders.show_folder(parts[2], True)
                    data_json['nodes'] = [self.make_json_r(os.path.join(path, fn['id'])) for fn in folder['folder_contents']]
            else :
                if len(parts) == 1:
                    data_json['folder'] = True
                    histories = self.client.histories.get_histories()
                    data_json['nodes'] = [self.make_json_r(os.path.join(path, fn['id'])) for fn in histories]
                elif len(parts) == 2:
                    data_json['folder'] =  True
                    datasets = self.client.histories.show_matching_datasets(parts[1])
                    data_json['nodes'] = [self.make_json_r(os.path.join(path, fn['id'])) for fn in datasets]
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
        
        localpath = os.path.join(tempfile.gettempdir(), name)
            
        if os.path.exists(localpath):
            fs = PosixFileSystem('/')
            unique_dir = fs.make_unique_dir(os.path.dirname(localpath))
            localpath = os.path.join(unique_dir, name)
        
        self.client.datasets.download_dataset(os.path.basename(path), file_path = localpath, use_default_filename=False)
        return localpath
        
class IOHelper():
    @staticmethod
    def getFileSystem(url):
        try:
            u = urlsplit(url)
            if u.scheme == 'http' or u.scheme == 'https':
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
    def mkdirs(path):
        filesystem = IOHelper.getFileSystem(path)
        return filesystem.mkdirs(path)
    
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
