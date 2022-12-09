from __future__ import print_function

import io
import logging
import os
import sys
from os import path
import json
import mimetypes
import math
import time

from flask import Flask, render_template, redirect, url_for, abort, flash, request, \
    current_app, make_response
from flask import send_from_directory, jsonify, send_file
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from sqlalchemy import and_, or_

from . import main
from .. import db
from ..decorators import admin_required, permission_required

#from ..models import AlchemyEncoder, Post, Comment, Visualizer, MimeType, DataAnnotation, DataVisualizer, DataMimeType, DataProperty, Filter, FilterHistory, Dataset
from ..util import Utility
from dsl.fileop import FilterManager
from .forms import EditProfileForm, EditProfileAdminForm, PostForm, CommentForm
from app.system.exechelper import func_exec_stdout
from app.managers.usermgr import usermanager
from app.managers.workflowmgr import workflowmanager
from app.managers.datamgr import datamanager
from app.managers.filtermgr import filtermanager
from app.objectmodel.common import Permission, AccessRights, convert_to_safe_json
from app.userloader import *

app = Flask(__name__)
basedir = os.path.dirname(os.path.abspath(__file__))

@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['PHENOPROC_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response


@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'

@main.route('/user/<username>')
def user(username):
    user = usermanager.get_by_username(username)
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.paginate(
        page, per_page=current_app.config['PHENOPROC_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts,
                           pagination=pagination)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = usermanager.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = usermanager.get_role(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    return json.dumps('')
#     post = Post.query.get_or_404(id)
#     form = CommentForm()
#     if form.validate_on_submit():
#         comment = Comment(body=form.body.data,
#                           post=post,
#                           author=current_user._get_current_object())
#         db.session.add(comment)
#         flash('Your comment has been published.')
#         return redirect(url_for('.post', id=post.id, page=-1))
#     page = request.args.get('page', 1, type=int)
#     if page == -1:
#         page = (post.comments.count() - 1) // \
#             current_app.config['PHENOPROC_COMMENTS_PER_PAGE'] + 1
#     pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
#         page, per_page=current_app.config['PHENOPROC_COMMENTS_PER_PAGE'],
#         error_out=False)
#     comments = pagination.items
#     return render_template('post.html', posts=[post], form=form,
#                            comments=comments, pagination=pagination)

@main.route('/workflow/<int:id>', methods=['GET', 'POST'])
def workflow(id):
    workflow = workflowmanager.get_or_404(id)
    return render_template('workflow.html', workflows=[workflow])
                           
@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    return json.dumps('')

#     post = Post.query.get_or_404(id)
#     if current_user != post.author and \
#             not current_user.can(Permission.ADMINISTER):
#         abort(403)
#     form = PostForm()
#     if form.validate_on_submit():
#         post.body = form.body.data
#         db.session.add(post)
#         flash('The post has been updated.')
#         return redirect(url_for('.post', id=post.id))
#     form.body.data = post.body
#     return render_template('edit_post.html', form=form)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user =  usermanager.get_by_username(username)
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    flash('You are now following %s.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user =  usermanager.get_by_username(username)
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user =  usermanager.get_by_username(username)
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['PHENOPROC_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed-by/<username>')
def followed_by(username):
    user =  usermanager.get_by_username(username)
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['PHENOPROC_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    return json.dumps('')
#     page = request.args.get('page', 1, type=int)
#     pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
#         page, per_page=current_app.config['PHENOPROC_COMMENTS_PER_PAGE'],
#         error_out=False)
#     comments = pagination.items
#     return render_template('moderate.html', comments=comments,
#                            pagination=pagination, page=page)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    return json.dumps('')
#     comment = Comment.query.get_or_404(id)
#     comment.disabled = False
#     db.session.add(comment)
#     return redirect(url_for('.moderate',
#                             page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    return json.dumps('')
    
#     comment = Comment.query.get_or_404(id)
#     comment.disabled = True
#     db.session.add(comment)
#     return redirect(url_for('.moderate',
#                             page=request.args.get('page', 1, type=int)))

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

# @main.route('/tasklogs', methods=['POST'])
# @login_required
# def translate():
#     workflow_id = request.form['text'] #request.args.get('workflow_id')
#     workflow_id = Utility.ValueOrNone(workflow_id)
#     if workflow_id is not None and Workflow.query.get(workflow_id) is not None:
#         sql = 'SELECT workitems.id, MAX(time), taskstatus.name as status FROM workitems LEFT JOIN tasks ON workitems.id=tasks.workitem_id LEFT JOIN tasklogs ON tasklogs.task_id=tasks.id LEFT JOIN taskstatus ON tasklogs.status_id = taskstatus.id WHERE workitems.workflow_id=' + str(workflow_id) + ' GROUP BY workitems.id'
#         result = db.engine.execute(sql)
#         return json.dumps([dict(r) for r in result], cls=AlchemyEncoder)

def get_data_item_from_tree(root, parents):
    if len(parents) == 1:
        return root
    for r in root['children']:
        if r.text == parents[0]:
            return get_data_item_from_tree(r, parents[1:])

def load_child_data_sources(parent, recursive = False):
    fs = Utility.fs_type_by_prefix_or_default(parent)

    parents = os.path.split(parent)
    parents = [p for p in parents if p]

    datasource_tree = load_default_data_sources()
    if fs.prefix not in datasource_tree.keys():
        raise ValueError("Storage doesn't exist in the system.")

    root = datasource_tree[fs.prefix]
    if parents[0] == fs.prefix:
        parents = parents[1:]

    root = get_data_item_from_tree(root, parents)
    return fs.make_json_item_r(parent[-1]) if recursive else fs.make_json_item(parent[-1])

def load_default_data_sources():
     # construct data source tree
    datasources = datamanager.get_datasources(active = True)
    datasource_tree = []
    for ds in datasources:
        try:
            if ds.type != 'posix': # temporary code
                continue
            fs = Utility.create_fs(ds)
            if not fs:
                continue
            datasource = fs.make_json_item(ds.url)# { 'path': ds.url, 'text': ds.name, 'type': 'folder', 'children': []}
            if ds.user and current_user.is_authenticated:
                user_folder = fs.join(ds.user, current_user.username)
                if not fs.exists(user_folder):
                    fs.makedirs(user_folder)
                    
                if fs.exists(user_folder):
                    users_json = fs.make_json_item(ds.user)
                    if 'children' in datasource.keys() and not isinstance(datasource['children'], list):
                        datasource['children'] = [] # switch children from boolean to list
                    datasource['children'].append(users_json)
                    if 'children' in users_json.keys() and not isinstance(users_json['children'], list):
                        users_json['children'] = [] # switch children from boolean to list
                    users_json['children'].append(fs.make_json(user_folder))
                        
            if ds.public and fs.exists(ds.public):
                if 'children' in datasource.keys() and not isinstance(datasource['children'], list):
                    datasource['children'] = [] # switch children from boolean to list    
                datasource['children'].append(fs.make_json(ds.public))

            if ds.temp and not fs.exists(ds.temp):
                fs.makedirs(ds.temp)

            datasource_tree.append(datasource)
        except Exception as e:
            logging.error("Filesystem {0} load fails with error: {1}".format(ds.name, str(e)))
        
    return datasource_tree

def load_data_sources_biowl(recursive):
    if not recursive:
        return load_default_data_sources()

     # construct data source tree
    datasources = datamanager.get_datasources(active = True)
    datasource_tree = []
    for ds in datasources:
        try:
            if ds.type != 'posix': # temporary code
                continue
            fs = Utility.create_fs(ds)
            if not fs:
                continue
            datasource = fs.make_json_item(ds.url)# { 'path': ds.url, 'text': ds.name, 'type': 'folder', 'children': []}
            if ds.user and current_user.is_authenticated:
                user_folder = fs.join(ds.user, current_user.username)
                if not fs.exists(user_folder):
                    fs.makedirs(user_folder)
                    
                if fs.exists(user_folder):
                    users_json = fs.make_json_item(ds.user)
                    datasource['children'].append(users_json)
                    users_json['children'].append(fs.make_json_r(user_folder) if recursive else fs.make_json(user_folder))
                        
            if ds.public and fs.exists(ds.public):
                datasource['children'].append(fs.make_json_r(ds.public) if recursive else fs.make_json(ds.public))

            if ds.temp and not fs.exists(ds.temp):
                fs.makedirs(ds.temp)

            datasource_tree.append(datasource)
        except Exception as e:
            logging.error("Filesystem {0} load fails with error: {1}".format(ds.name, str(e)))
        
    return datasource_tree

def download_biowl(path):
    # construct data source tree
    path = path.strip()
    fs = Utility.fs_by_prefix_or_guess(path)
    fullpath = fs.download(path)
    if not fullpath:
        abort(422)
    mime = mimetypes.guess_type(fullpath)[0]
    return send_from_directory(os.path.dirname(fullpath), os.path.basename(fullpath), mimetype=mime, as_attachment = mime is None )

def get_filecontent(path):
    # construct data source tree
    path = path.strip()
    fs = Utility.fs_by_prefix_or_guess(path)
    image_binary = fs.read(path)

    mime = datamanager.get_mimetype(path)
    if not mime:
        mime = mimetypes.guess_type(path)[0]
    return send_file(io.BytesIO(image_binary), mimetype=mime, as_attachment=True, attachment_filename=fs.basename(path))

def get_filedata(path):
    # construct data source tree
    path = path.strip()
    with open(path, 'rb') as reader:
        file_binary = reader.read()
        mime = datamanager.get_mimetype(path)
        if not mime:
            mime = mimetypes.guess_type(path)[0]
        return send_file(io.BytesIO(file_binary), mimetype=mime, as_attachment=True, attachment_filename=os.path.basename(path))

def upload_biowl(file, request):
    
    fullpath = request.form['path'] 
    fs = Utility.fs_by_prefix_or_guess(fullpath)
    saved_path = fs.save_upload(file, fullpath)
    if not fs.isfile(saved_path):
        return saved_path
    
    if request.form.get('filename'):
        newpath = fs.join(fs.dirname(saved_path), request.form['filename'])
        saved_path = fs.rename(saved_path, newpath)

    ds = Utility.ds_by_prefix_or_root(saved_path)
    if not ds:
        return saved_path
       
    data_alloc = datamanager.add_allocation(current_user.id, ds.id, saved_path, AccessRights.Owner)
        
    # if request.form.get('visualizer'):
    #     dbvisualizer = None
    #     if request.form.get('visualizer'):
    #         visualizer = json.loads(request.form['visualizer'])
    #         for k,v in visualizer.items():
    #             dbvisualizer = Visualizer.add(k, v)
    #             if dbvisualizer:
    #                 DataVisualizer.add(data_alloc.id, dbvisualizer.id)
        
    # if request.form.get('annotations'):
    #     annotations = request.form['annotations']
    #     annotations = annotations.split(',')
    #     for annotation in annotations:
    #         DataAnnotation.add(data_alloc.id, annotation)
            
    # if request.form.get('mimetype'):
    #     dbmimetype = None
    #     if request.form.get('mimetype'):
    #         mimetype = json.loads(request.form['mimetype'])
    #         for k,v in mimetype.items():
    #             dbmimetype = MimeType.add(k, v)
    #             if dbmimetype:
    #                 DataMimeType.add(data_alloc.id, dbmimetype.id)
    
    return saved_path
    
@main.route('/biowl', methods=['GET', 'POST'])
@main.route('/', methods = ['GET', 'POST'])
#@login_required
def index():
    return render_template('biowl.html', username= current_user.username if current_user.is_authenticated else "")

def sizeof_fmt(num, suffix='B'):
    magnitude = int(math.floor(math.log(num, 1024)))
    val = num / math.pow(1024, magnitude)
    if magnitude > 7:
        return '{:.1f}{}{}'.format(val, 'Yi', suffix)
    return '{:3.1f}{}{}'.format(val, ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi'][magnitude], suffix)

def load_metadataproperties():
    visualizers = {'browsers': 'all'}
    
    datamimetypes = {}
    for m in mimetypes.types_map.items():
        datamimetypes[m[0]] = m[1]
    
    return { 'visualizers': visualizers, 'mimetypes': datamimetypes}

def load_metadata(path):
    metadata = {}
    
    # user must have at least read access
    datamanager.check_access_rights(current_user.id, path, AccessRights.Read)

    # sysprops
    fs = Utility.fs_by_prefix_or_guess(path)
    if not fs:
        return None
    
    datatype = "DataType.File" if fs.isfile(path) else "DataType.Folder"
    if not path.startswith('/'):
        path = '/' + path
    
    # access rights in string
    accessRights = datamanager.access_rights_to_string(current_user.id, path)

    if not accessRights:
#         if path.startswith('/' + current_user.username):
#             rights = AccessRights.Owner
#             ds = Utility.ds_by_prefix_or_default(path)
#             data_alloc = datamanager.add(current_user.id, ds.id, path, rights)
#         elif
        if path.startswith(ds.public):
            user =  usermanager.get_by_id(current_user.id)
            if user.is_administrator():
                rights = AccessRights.Write
            else:
                rights = AccessRights.Read
    
        if rights == AccessRights.NotSet:
            return None
    
    statinfo = os.stat(fs.normalize_path(path))
        
    metadata['sysprops'] = {'Name': fs.basename(path), 'Path': fs.dirname(path), 'Type': datatype, 'Size': sizeof_fmt(statinfo.st_size), 'Accessed on': time.ctime(statinfo.st_atime), 'Modified on': time.ctime(statinfo.st_mtime), 'Created on': time.ctime(statinfo.st_ctime), 'Permissions': accessRights}
    
    data_alloc = datamanager.add_allocation(current_user.id, ds.id, path, AccessRights.Read)
            
    metadata['mimetypes'] = {}
    if data_alloc:
        metadatadb = data_alloc.visualizers
        visualizers = {}
        for m in metadatadb:
            visualizers.update({ m.name: m.desc })
        metadata['visualizers'] = visualizers
        
        metadatadb = data_alloc.annotations
        annotations = {}
        index = 1
        for m in metadatadb:
            annotations.update({ str(index): m.tag})
            index += 1
        metadata['annotations'] = annotations
        
        metadatadb = data_alloc.mimetypes
        dbmimetypes = {}
        for m in metadatadb:
            dbmimetypes.update({ m.name: m.desc })
        
        if not dbmimetypes:
            for g in mimetypes.guess_type(path):
                dbmimetypes.update({ g: g })
                          
        metadata['mimetypes'] = dbmimetypes
        
        metadatadb = data_alloc.properties
        properties = {}
        for m in metadatadb:
            properties.update({ m.key: m.value })
        metadata['properties'] = properties
    
    return metadata
    
# def save_metadata(request):
#     path = request.form.get('save')
#     newname = request.form.get('filename')
    
#     ds = Utility.ds_by_prefix_or_default(path)
#     data = datamanager.get_allocation_by_url(ds.id, path)
    
#     fs = Utility.fs_by_prefix_or_guess(path)
#     if not fs:
#         raise ValueError("path not found")
#     newpath = fs.rename(path, newname)
#     if path != newpath:
#         data.update_url(newpath)
#         path = newpath    

#     datamanager.check_access_rights(current_user.id, path, AccessRights.Read)
    
#     if request.form.get('visualizers'):    
#         visualizers = json.loads(request.form.get('visualizers'))
#         for name, desc in visualizers.items():
#             visualizer = Visualizer.add(name, desc)
#             if visualizer:
#                 DataVisualizer.add(data.id, visualizer.id)
    
#     if request.form.get('annotations'):    
#         annotations = json.loads(request.form.get('annotations'))
#         for name, desc in annotations.items():
#             DataAnnotation.add(data.id, desc)
    
#     if request.form.get('mimetypes'):    
#         mimetypes = json.loads(request.form.get('mimetypes'))
#         for name, desc in mimetypes.items():
#             mimetype = MimeType.add(name, desc)
#             if mimetype:
#                 DataMimeType.add(data.id, mimetype.id)
                
#     if request.form.get('properties'):    
#         properties = json.loads(request.form.get('properties'))
#         for name, desc in properties.items():
#             DataProperty.add(data.id, name, desc)

def search_and_filter(filters, path):
    filters = json.loads(filters)
    filters = filters if not filters or type(filters) is list else [filters]
    selected_filters = [f for f in filters if f["selected"]]
    filtermanager.add_history(current_user.id, json.dumps(selected_filters))
    
    fs = Utility.fs_by_prefix_or_guess(path)
    return FilterManager.listdirR(fs, path, filters)

def load_filter_history():
    filters = filtermanager.get_history(user_id = current_user.id)
    return jsonify(histories = [f.to_json_info() for f in filters])

def load_filters():
    filters = filtermanager.get(user_id = current_user.id)
    return jsonify(histories = [f.to_json_info() for f in filters])

def load_filter_tip(filter_id):
    return filtermanager.get(id = filter_id).to_json_tooltip()

def load_script_from_filter(filter_id, path):
    return filtermanager.make_script(filter_id, path)

def save_filters(name, filters):
    return filtermanager.add(user_id = current_user.id, name = name, value = json.loads(filters))

def delete_filter(filter_id):
    filtermanager.remove(filter_id)

# def load_datasets():
#     datasets = Dataset.query.all()
#     jsondatasets = []
#     for d in datasets:
#         jsondatasets.append(d.to_json())
        
#     return jsonify(datasets = jsondatasets)

# def save_datasets(schema):
#     schema = json.loads(schema)
#     #schemadic = {}
#     #for s in schema:
#      #   schemadic.update({s['name']: s['value']})
            
#     dataset = Dataset.add(schema)
#     return jsonify(dataset = dataset.to_json())

# def delete_datasets(dataset_id):
#     Dataset.remove(dataset_id)
#     return json.dumps({})

# def update_datasets(dataset_id, schema):
#     schema = json.loads(schema)
#     Dataset.update(dataset_id, schema)
#     return json.dumps({})

@main.route('/filters', methods=['GET', 'POST'])
@login_required
def filters():
    return json.dumps('')
    if request.args.get('filterhistory'):
        return load_filter_history()
    elif request.args.get('filters'):
        return load_filters()
    elif request.args.get("savefilters"):
        return json.dumps(save_filters(request.args.get("name"), request.args.get("savefilters")))
    elif request.args.get('filtertip'):
        return json.dumps(load_filter_tip(request.args.get('filtertip')))
    elif request.args.get('filterforscript'):
        return jsonify(script = load_script_from_filter(request.args.get('filterforscript'), request.args.get('path')))
    elif request.args.get('applyfilters'):
        return json.dumps({'datasources': search_and_filter(request.args.get('applyfilters'), request.args.get('root')) })
    elif request.args.get('delete'):
        return json.dumps(delete_filter(request.args.get('delete')))

@main.route('/datasets', methods=['GET', 'POST'])
@login_required
def datasets():
    return json.dumps('')
    
#     if request.args.get("save"):
#         return save_datasets(request.args.get("save"))
#     elif request.args.get("delete"):
#         return delete_datasets(request.args.get("delete"))
#     elif request.args.get("update"):
#         return update_datasets(request.args.get("update_id"), request.args.get("update"))
    
#     return load_datasets()

@main.route('/metadata', methods=['GET', 'POST'])
@login_required
def metadata():
    return json.dumps({})
#     if request.args.get('load'):
#         return json.dumps(load_metadata(request.args.get('load')))
#     elif request.args.get('properties'):
#         return json.dumps(load_metadataproperties())
#     elif request.form.get('save'):
#         return json.dumps(save_metadata(request))

def get_mimetype(path):
    return datamanager.get_mimetype(path)

@main.route('/datasources', methods=['GET', 'POST'])
@login_required
def datasources():
    try:
        if request.form.get('download'):
            return download_biowl(request.form['download'])
        elif 'mimetype' in request.args:
            return json.dumps({'mimetype': get_mimetype(request.args.get('mimetype'))})
        elif 'filecontent' in request.args:
            return get_filecontent(request.args.get('filecontent'))
        elif 'file_data' in request.args:
            return get_filedata(request.args.get('file_data'))    
        elif request.files and request.files['upload']:
            return json.dumps({'path' : upload_biowl(request.files['upload'], request)})
        elif request.args.get('addfolder'):
            path = request.args['addfolder']
            fileSystem = Utility.fs_by_prefix_or_guess(path)
            parent = path if fileSystem.isdir(path) else fileSystem.dirname(path)
            unique_filename = fileSystem.unique_fs_name(parent, 'newfolder', '')
            dirpath = fileSystem.strip_root(fileSystem.makedirs(unique_filename))
            return json.dumps({'text': fileSystem.basename(unique_filename), 'path' : dirpath, 'type': 'folder'})
        elif request.args.get('delete'):
            path = request.args['delete']
            fileSystem = Utility.fs_by_prefix_or_guess(path)
            return json.dumps({'path' : fileSystem.remove(fileSystem.strip_root(path))})
        elif request.args.get('rename'):
            fileSystem = Utility.fs_by_prefix_or_guess(request.args['oldpath'])
            oldpath = fileSystem.strip_root(request.args['oldpath'])
            newpath = os.path.join(os.path.dirname(oldpath), request.args['rename'])
            return json.dumps({'path' : fileSystem.rename(oldpath, newpath)})
        elif request.args.get('load'):
            fs = Utility.fs_by_prefix_or_guess(request.args['load'])
            return json.dumps(fs.make_json_r(request.args['load']) if request.args.get('recursive') and str(request.args.get('recursive')).lower()=='true' else fs.make_json(request.args['load']))
        elif 'children' in request.args:
            return json.dumps(load_child_data_sources(request.args['children']))
            
        return json.dumps({'datasources': load_data_sources_biowl(request.args.get('recursive') and request.args.get('recursive').lower() == 'true') })
    except Exception as e:
        return make_response(jsonify(err=str(e)), 500)

class Samples():
    @staticmethod
    def load_samples_recursive_for_user(samples_dir, access):
        all_samples = []
        for f in os.listdir(samples_dir):
            fsitem = os.path.join(samples_dir, f)
            if os.path.isdir(fsitem) and f == 'users':
                for fuser in os.listdir(fsitem):
                    userPath = os.path.join(fsitem, fuser)
                    samples = Samples.load_samples_recursive(userPath, fuser, access)
                    if samples:
                        all_samples.extend(samples if isinstance(samples, list) else [samples])
            else:
                samples = Samples.load_samples_recursive(fsitem, None, access)
                if samples:
                    all_samples.extend(samples if isinstance(samples, list) else [samples])
            #all_samples = {**all_samples, **samples}
        return all_samples
    
    @staticmethod
    def load_samples_recursive(library_def_file, user, access):
        if os.path.isfile(library_def_file):
            return Samples.load_samples(library_def_file, user, access)
        
        all_samples = []
        for f in os.listdir(library_def_file):
            samples = Samples.load_samples_recursive(os.path.join(library_def_file, f), user, access)
            all_samples.extend(samples if isinstance(samples, list) else [samples])
            #all_samples = {**all_samples, **samples}
        return all_samples
       
    @staticmethod
    def load_samples(sample_def_file, user, access):
        samples = []
        if not os.path.isfile(sample_def_file) or not sample_def_file.endswith(".json"):
            return samples
        try:
            with open(sample_def_file, 'r') as json_data:
                ds = json.load(json_data)
                if ds.get("samples"):
                    for d in ds:
                        sample_access = d.get("access") if d.get("access") else 0
                        if sample_access == access:
                            samples.append(d)
                else:
                    if not ds.get("access"):
                        ds["access"] = 2 if user else 0
                    if ds.get("access") == access:
                        if access != 2 or not user or user == current_user.username:
                            samples.append(ds)
        finally:
            return samples
    
    
    @staticmethod
    def make_fn(path, prefix, ext, suffix):
        path = os.path.join(path, '{0}'.format(prefix))
        if suffix:
            path = '{0}_{1}'.format(path, suffix)
        if ext:
            path = '{0}.{1}'.format(path, ext)
        return path
    
    @staticmethod
    def unique_filename(path, prefix, ext):
        uni_fn = Samples.make_fn(path, prefix, ext, '')
        if not os.path.exists(uni_fn):
            return uni_fn
        for i in range(1, sys.maxsize):
            uni_fn = Samples.make_fn(path, prefix, ext, i)
            if not os.path.exists(uni_fn):
                return uni_fn
    
    @staticmethod
    def jsonify_script(script):
        return script
        #return script.replace("\\n", "\n").replace("\r\n", "\n").replace("\"", "\'").split("\n") #TODO: double quote must be handled differently to allow  "x='y'"

    @staticmethod
    def create_workflow(user, id, name, desc, script, params, returns, publicaccess, users, temp, derived = 0):
        access = 9
        if id:
            workflow = workflowmanager.first(id = id)
            if workflow:
                return workflow.update(user_id=user, name=name, desc=desc, script=script, params=params, returns=returns, access=access, users=users, temp=temp, derived=derived)
            
        if script and name:
            if publicaccess == 'true':
                access = 0
                users = False 
            else:
                if users:
                    access = 1
                else:
                    access = 2
                    users = False
            return workflowmanager.create(user_id=user, name=name, desc=desc if desc else '', script=script, params=params, returns=returns, access=access, users=users, temp=temp, derived=derived)

    @staticmethod
    def add_workflow(user, id, name, desc, script, params, returns, access, users, temp):
        workflow = Samples.create_workflow(user, id, name, desc, script, params, returns, access, users, temp, 0)
        info = workflow.to_json()
        info["is_owner"] = info["user"] == current_user.username
        info["access"] = access
        return json.dumps(info)

'''
Used for saving workflow into the filesystem instead of in the database
    @staticmethod
    def add_sample(sample, name, desc, shared):
        this_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(this_path) #set dir of this file to current directory
        samplesdir = os.path.normpath(os.path.join(this_path, '../biowl/samples'))

        try:
            if sample and name:
                new_path = os.path.join(samplesdir, 'users', current_user.username)
                new_path = os.path.normpath(new_path)    
                if not os.path.isdir(new_path):
                    os.makedirs(new_path)
                
                path = Samples.unique_filename(new_path, name, 'json')
                
                access = 1 if shared and shared.lower() == 'true' else 2
                        
                with open(path, 'w') as fp:
                    fp.write("{\n")
                    fp.write('{0}"name":"{1}",\n'.format(" " * 4, name))
                    fp.write('{0}"desc":"{1}",\n'.format(" " * 4, desc))
                    fp.write('{0}"access":{1},\n'.format(" " * 4, access))
                    fp.write('{0}"sample":[\n'.format(" " * 4))
                    sample = sample.replace("\\n", "\n").replace("\r\n", "\n").replace("\"", "\'")
                    lines = sample.split("\n")
                    for line in lines[0:-1]:
                        fp.write('{0}"{1}",\n'.format(" " * 8, line))
                    fp.write('{0}"{1}"\n'.format(" " * 8, lines[-1]))
                    fp.write("{0}]\n}}".format(" " * 4))
#                json.dump(samples, fp, indent=4, separators=(',', ': '))
        finally:
            return json.dumps({ 'out': '', 'err': ''})
'''

def workflow_compare(workflow1, workflow2):
    try:
        from ..jobs import generate_graph_from_workflow
        from app.objectmodel.provmod.provobj import View, Run
        from ..managers.runmgr import runnablemanager
        from difflib import ndiff
        
        graph1 = generate_graph_from_workflow(workflow1)
        graph2 = generate_graph_from_workflow(workflow2)
        view = {"graph": [graph1, graph2] }
        
        workflow = workflowmanager.first(id=workflow1)
        wf_script1 = workflow.script
        node1 = runnablemanager.create_runnable(current_user.id, workflow1, wf_script1, provenance=True, args=None)
        
        workflow = workflowmanager.first(id=workflow2)
        wf_script2 = workflow.script
        node2 = runnablemanager.create_runnable(current_user.id, workflow2, wf_script2, provenance=True, args=None)
        view['compare'] = [View.compare(Run(runItem = node1), Run(runItem = node2))]
        
        diff = ndiff(wf_script1, wf_script2)              
        diff = '\n'.join(list(diff))
        view['textcompare'] = [diff]
        
        return json.dumps({"view": view})
    except Exception as e:
        return make_response(jsonify(err=str(e)), 500)
    
def workflow_rev_compare(request):
    try:
        from ..jobs import generate_graph
        from app.objectmodel.provmod.provobj import View
        
        workflow = workflowmanager.get_or_404(request.args.get('revcompare'))
        
        revision1_script = workflow.revision_by_commit(request.args.get('revision1'))
        revision2_script = workflow.revision_by_commit(request.args.get('revision2'))
        graph1 = generate_graph(workflow.id, workflow.name, revision1_script)
        graph2 = generate_graph(workflow.id, workflow.name, revision2_script)
        return json.dumps(View.compare(graph1, graph2))
    except Exception as e:
        return make_response(jsonify(err=str(e)), 500)
    
@main.route('/samples', methods=['GET', 'POST'])
@login_required
def samples():
    try:
        if request.form.get('sample'):
            return Samples.add_workflow(current_user.id, request.form.get('id'), request.form.get('name'), request.form.get('desc'), request.form.get('sample'), request.form.get('params'), request.form.get('returns'), request.form.get('publicaccess') if request.form.get('publicaccess') else False, request.form.get('sharedusers'), False)
        elif request.args.get('sample_id'):
            workflow = workflowmanager.get_or_404(request.args.get('sample_id'))
            return json.dumps(workflow.to_json())
        elif request.args.get('revision'):
            workflow = workflowmanager.get_or_404(request.args.get('revision'))
            return json.dumps(workflow.revision_by_commit(request.args.get('hexsha')))
        elif request.args.get('compare'):
            return workflow_compare(int(request.args.get('compare')), int(request.args.get('with')))
        elif request.args.get('revcompare'):
            return workflow_rev_compare(request)
        elif request.args.get('revisions'):
            workflow = workflowmanager.get_or_404(request.args.get('revisions'))
            return json.dumps(workflow.revisions)
        elif request.args.get('tooltip'):
            workflow = workflowmanager.get_or_404(request.args.get('tooltip'))
            return json.dumps(workflow.to_json_tooltip())   
        elif 'workflow_id' in request.args:
            workflow_id = request.args.get("workflow_id")
            if 'confirm' in request.args:
                if request.args.get("confirm") == "true":
                    workflowmanager.remove(current_user.id, workflow_id)
                    return json.dumps({'return':'deleted'})
            else:
                shared_Workflow_check = workflowmanager.check(workflow_id) 
                if shared_Workflow_check:  
                    return json.dumps({'return':'shared'})
                else:
                    return json.dumps({'return':'not_shared'})
            return json.dumps({'return':'error'})
        
        access = int(request.args.get('access')) if request.args.get('access') else 0
        return json.dumps({'samples': convert_to_safe_json(workflowmanager.get_workflows_as_list(access, current_user))})
    except Exception as e :
        logging.error(str(e))
        return make_response(jsonify(err=str(e)), 500)

@main.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # project folder
    target = os.path.dirname(os.path.dirname(basedir))
    # git folder location, usually .git subfolder inside project folder
    gitdir = os.path.join(target, '.git')
    # branch name to checkout
    branch = 'master'
    
    func_exec_stdout(os.path.join(target, 'pullwebhook.sh'), '{0} {1} {2} '.format(target, gitdir, branch))
    return json.dumps({})

def load_listview_datasets(user_id, page, no_of_item):
    """
    Load list view of Datasets with basic information  
    
    """
    return datamanager.load_listview_datasets(user_id, page, no_of_item)

def load_plugin_datasets(request):
    """
    Load plugin Datasets. 
    
    """
    try:
        page = int(request.args.get("pageNum")) if request.args.get("pageNum") else 1
        no_of_item = int(request.args.get("numOfItems")) if request.args.get("numOfItems") else 20000

        return load_listview_datasets(current_user.id, page, no_of_item)
    except Exception as e:
        return {'data': [], 'hasMore': False, 'itemCount': 0, 'pageNum': '0'}


@main.route('/api/plugin/datasets', methods=['GET'])
def loadPluginInfo():
    return load_plugin_datasets(request)

import datetime

def custom_date_serializer(obj):
    """Custom json serializer"""
    if isinstance(obj, (datetime)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))
    
def load_plugin_data(dataset_id, data_id, page_num):
    """
    Load plugin data for VizSciFlow. 
    
    """
    try:
        data =  datamanager.load_dataset_data_for_plugin(dataset_id, data_id, page_num)
        return json.dumps(data, default=custom_date_serializer)
    except Exception as e:
        return {'data': [], 'hasMore': False, 'itemCount': 0, 'pageNum': '0'}

@main.route('/api/plugin/dataset/data', methods=['GET'])
def loadPlugeinData():
    return load_plugin_data(request.args.get("dataset_id"), request.args.get("data_id"), int(request.args.get("page_num")))
