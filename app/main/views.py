from __future__ import print_function

import os
import sys
from os import path
import json
import mimetypes
import math
import time

from flask import Flask, render_template, redirect, url_for, abort, flash, request, \
    current_app, make_response
from flask import send_from_directory, jsonify
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy import and_

from . import main
from .. import db
from ..decorators import admin_required, permission_required

from ..models import Permission, Role, User, Post, Comment, Workflow, DataSource, WorkflowAccess, DataSourceAllocation, AccessRights, Visualizer, MimeType, DataAnnotation, DataType, DataVisualizer, DataMimeType, DataProperty, Filter, FilterHistory
from ..util import Utility
from ..biowl.fileop import FilterManager
from .forms import EditProfileForm, EditProfileAdminForm, PostForm, CommentForm

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
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
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
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
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
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash('Your comment has been published.')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['PHENOPROC_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['PHENOPROC_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)

@main.route('/workflow/<int:id>', methods=['GET', 'POST'])
def workflow(id):
    workflow = Workflow.query.get_or_404(id)
    return render_template('workflow.html', workflows=[workflow])
                           
@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
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
    user = User.query.filter_by(username=username).first()
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
    user = User.query.filter_by(username=username).first()
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
    user = User.query.filter_by(username=username).first()
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
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['PHENOPROC_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments,
                           pagination=pagination, page=page)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields
    
        return json.JSONEncoder.default(self, obj)

@main.route('/tasklogs', methods=['POST'])
@login_required
def translate():
    workflow_id = request.form['text'] #request.args.get('workflow_id')
    workflow_id = Utility.ValueOrNone(workflow_id)
    if workflow_id is not None and Workflow.query.get(workflow_id) is not None:
        sql = 'SELECT workitems.id, MAX(time), taskstatus.name as status FROM workitems LEFT JOIN tasks ON workitems.id=tasks.workitem_id LEFT JOIN tasklogs ON tasklogs.task_id=tasks.id LEFT JOIN taskstatus ON tasklogs.status_id = taskstatus.id WHERE workitems.workflow_id=' + str(workflow_id) + ' GROUP BY workitems.id'
        result = db.engine.execute(sql)
        return json.dumps([dict(r) for r in result], cls=AlchemyEncoder)

def load_data_sources_biowl(recursive):
     # construct data source tree
    datasources = DataSource.query.filter_by(active = True)
    datasource_tree = []
    for ds in datasources:
        try:
            fs = Utility.create_fs(ds)
            if not fs:
                continue
            if not fs or fs.typename() != 'posix': # temporary code
                continue
            datasource = { 'path': ds.url, 'text': ds.name, 'type': 'folder', 'children': [], 'loaded': True}
            if current_user.is_authenticated:
                if not fs.exists(current_user.username):
                    fs.makedirs(current_user.username)
                    
                if fs.exists(current_user.username):
                    datasource['children'].append(fs.make_json_r(os.sep + current_user.username) if recursive else fs.make_json(os.sep + current_user.username))
                        
            if ds.public and fs.exists(ds.public):
                datasource['children'].append(fs.make_json_r(ds.public) if recursive else fs.make_json(ds.public))

            datasource_tree.append(datasource)
        except:
            pass
        
    return datasource_tree

def download_biowl(path):
    # construct data source tree
    path = path.strip()
    fs = Utility.fs_by_prefix_or_default(path)
    fullpath = fs.download(path)
    if not fullpath:
        abort(422)
    mime = mimetypes.guess_type(fullpath)[0]
    return send_from_directory(os.path.dirname(fullpath), os.path.basename(fullpath), mimetype=mime, as_attachment = mime is None )

def upload_biowl(file, request):
    
    fullpath = request.form['path'] 
    fs = Utility.fs_by_prefix_or_default(fullpath)
    saved_path = fs.save_upload(file, fullpath)
    if not fs.isfile(saved_path):
        return saved_path
    
    if request.form.get('filename'):
        newpath = fs.join(fs.dirname(saved_path), request.form['filename'])
        saved_path = fs.rename(saved_path, newpath)

    ds = Utility.ds_by_prefix_or_default(saved_path)
    if not ds:
        return saved_path
       
    data_alloc = DataSourceAllocation.add(current_user.id, ds.id, saved_path, AccessRights.Owner)
        
    if request.form.get('visualizer'):
        dbvisualizer = None
        if request.form.get('visualizer'):
            visualizer = json.loads(request.form['visualizer'])
            for k,v in visualizer.items():
                dbvisualizer = Visualizer.add(k, v)
                if dbvisualizer:
                    DataVisualizer.add(data_alloc.id, dbvisualizer.id)
        
    if request.form.get('annotations'):
        annotations = request.form['annotations']
        annotations = annotations.split(',')
        for annotation in annotations:
            DataAnnotation.add(data_alloc.id, annotation)
            
    if request.form.get('mimetype'):
        dbmimetype = None
        if request.form.get('mimetype'):
            mimetype = json.loads(request.form['mimetype'])
            for k,v in mimetype.items():
                dbmimetype = MimeType.add(k, v)
                if dbmimetype:
                    DataMimeType.add(data_alloc.id, dbmimetype.id)
    
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
    
    ds = Utility.ds_by_prefix_or_default(path)
    if not ds:
        return None # data source not added to the system
    
    # user must have at least read access
    DataSourceAllocation.check_access_rights(current_user.id, path, AccessRights.Read)

    # sysprops
    fs = Utility.create_fs(ds)
    if not fs:
        return None
    
    datatype = "DataType.File" if fs.isfile(path) else "DataType.Folder"
    if not path.startswith('/'):
        path = '/' + path
    
    # access rights in string
    accessRights = DataSourceAllocation.access_rights_to_string(current_user.id, path)

    if not accessRights:
#         if path.startswith('/' + current_user.username):
#             rights = AccessRights.Owner
#             ds = Utility.ds_by_prefix_or_default(path)
#             data_alloc = DataSourceAllocation.add(current_user.id, ds.id, path, rights)
#         elif
        if path.startswith(ds.public):
            user = User.query.get(current_user.id)
            if user.is_administrator():
                rights = AccessRights.Write
            else:
                rights = AccessRights.Read
    
        if rights == AccessRights.NotSet:
            return None
    
    statinfo = os.stat(fs.normalize_path(path))
        
    metadata['sysprops'] = {'Name': fs.basename(path), 'Path': fs.dirname(path), 'Type': datatype, 'Size': sizeof_fmt(statinfo.st_size), 'Accessed on': time.ctime(statinfo.st_atime), 'Modified on': time.ctime(statinfo.st_mtime), 'Created on': time.ctime(statinfo.st_ctime), 'Permissions': accessRights}
    
    #data_alloc = DataSourceAllocation.query.filter(and_(DataSourceAllocation.user_id == current_user.id, DataSourceAllocation.datasource_id == ds.id, DataSourceAllocation.url == path)).first()
    data_alloc = DataSourceAllocation.add(current_user.id, ds.id, path, AccessRights.Read)
            
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
            properties.update(m.keyvalue)
        metadata['properties'] = properties
    
    return metadata
    
def save_metadata(request):
    path = request.form.get('metadatasave')
    newname = request.form.get('filename')
    
    fs = Utility.fs_by_prefix_or_default(path)
    if fs.basename(path) != newname:
        fs.rename(path, newname)

    DataSourceAllocation.check_access_rights(current_user.id, path, AccessRights.Read)
    
    ds = Utility.ds_by_prefix_or_default(path)
    data = DataSourceAllocation.get_by_url(ds.id, path)
    
    if request.form.get('visualizers'):    
        visualizers = json.loads(request.form.get('visualizers'))
        for name, desc in visualizers.items():
            visualizer = Visualizer.add(name, desc)
            if visualizer:
                DataVisualizer.add(data.id, visualizer.id)
    
    if request.form.get('annotations'):    
        annotations = json.loads(request.form.get('annotations'))
        for name, desc in annotations.items():
            DataAnnotation.add(data.id, desc)
    
    if request.form.get('mimetypes'):    
        mimetypes = json.loads(request.form.get('mimetypes'))
        for name, desc in mimetypes.items():
            mimetype = MimeType.add(name, desc)
            if mimetype:
                DataMimeType.add(data.id, mimetype.id)
                
    if request.form.get('properties'):    
        properties = json.loads(request.form.get('properties'))
        for name, desc in properties.items():
            DataProperty.add(data.id, name, desc)

def search_and_filter(path, filters):
    filters = json.loads(filters)
    filters = filters if not filters or type(filters) is list else [filters]
    selected_filters = []
    for f in filters:
        if f["selected"]:
            selected_filters.append(f)
    
    FilterHistory.add(current_user.id, json.dumps(selected_filters))
    
    fs = Utility.fs_by_prefix_or_default(path)
    return FilterManager.listdirR(fs, path, filters);

def load_filter_history():
    filters = FilterHistory.query.filter(Filter.user_id == current_user.id)
    histories = []
    for f in filters:
        histories.append(f.to_json_info())
        
    return jsonify(histories = histories)

def load_filters():
    filters = Filter.query.filter(Filter.user_id == current_user.id)
    histories = []
    for f in filters:
        histories.append(f.to_json_info())
        
    return jsonify(histories = histories)

def load_filter_tip(filter_id):
    return Filter.query.get(filter_id).to_json_tooltip()

def load_script_from_filter(path, filter_id):
    filterjson = json.loads(Filter.query.get(filter_id).value)
    filterjson = [f for f in filterjson if f["selected"] ]
    script = "data = GetFiles('{0}', {1})".format(path, filterjson)
    return script
     
@main.route('/datasources', methods=['GET', 'POST'])
@login_required
def datasources():
    if request.form.get('download'):
        return download_biowl(request.form['download'])
    elif request.files and request.files['upload']:
        upload_biowl(request.files['upload'], request)
    elif request.args.get('addfolder'):
        path = request.args['addfolder']
        fileSystem = Utility.fs_by_prefix_or_default(path)
        parent = path if fileSystem.isdir(path) else fileSystem.dirname(path)
        unique_filename = fileSystem.unique_fs_name(parent, 'newfolder', '')
        dirpath = fileSystem.strip_root(fileSystem.makedirs(unique_filename))
        return json.dumps({'text': fileSystem.basename(unique_filename), 'path' : dirpath, 'type': 'folder'})
    elif request.args.get('delete'):
        path = request.args['delete']
        fileSystem = Utility.fs_by_prefix_or_default(path)
        return json.dumps({'path' : fileSystem.remove(fileSystem.strip_root(path))})
    elif request.args.get('rename'):
        fileSystem = Utility.fs_by_prefix_or_default(request.args['oldpath'])
        oldpath = fileSystem.strip_root(request.args['oldpath'])
        newpath = os.path.join(os.path.dirname(oldpath), request.args['rename'])
        return json.dumps({'path' : fileSystem.rename(oldpath, newpath)})
    elif request.args.get('load'):
        fs = Utility.fs_by_prefix_or_default(request.args['load'])
        return json.dumps(fs.make_json_r(request.args['load']) if request.args.get('recursive') and str(request.args.get('recursive')).lower()=='true' else fs.make_json(request.args['load']))
    elif request.args.get('metadataload'):
        return json.dumps(load_metadata(request.args.get('metadataload')))
    elif request.args.get('metadataproperties'):
        return json.dumps(load_metadataproperties())
    elif request.form.get('metadatasave'):
        return json.dumps(save_metadata(request))                
    elif request.args.get('filters'):
        return json.dumps({'datasources': search_and_filter(request.args.get('root'), request.args.get('filters')) })
    elif request.args.get('filterhistory'):
        return load_filters()
    elif request.args.get('filtertip'):
        return json.dumps(load_filter_tip(request.args.get('filtertip')))
    elif request.args.get('filtertforscript'):
        return jsonify(script = load_script_from_filter(request.args.get('path'), request.args.get('filtertforscript')))
        
    return json.dumps({'datasources': load_data_sources_biowl(request.args.get('recursive') and request.args.get('recursive').lower() == 'true') })

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
    def get_samples_as_list(access):
        workflows = []
        if access == 0:
            workflows = Workflow.query.filter(Workflow.public == True)
            #workflows=Workflow.query.join(User).filter(User.role != None).join(Role).filter(and_(Role.permissions != None, Role.permissions.op('&')(Permission.ADMINISTER) == Permission.ADMINISTER)).filter(Workflow.accesses.any(WorkflowAccess.user_id.is_(None)))
        elif access == 1:
            workflows = Workflow.query.filter(Workflow.public != True).filter(Workflow.accesses.any(and_(WorkflowAccess.user_id == current_user.id, Workflow.user_id != current_user.id))) # TODO: Do we need or_ operator here? 
        else:
            workflows = Workflow.query.filter(and_(Workflow.public != True, Workflow.user_id == current_user.id)).filter(Workflow.accesses.any(WorkflowAccess.user_id != current_user.id) != True)
        
        samples = []
        for workflow in workflows:
            samples.append(workflow.to_json_info())
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
    def create_workflow(user, name, desc, script, access, users, temp, derived = 0):
        if script and name:
            users = users.split(";") if users else []
            return Workflow.create(user, name, desc if desc else '', script, 2 if not access else int(access), users, temp, derived)

    @staticmethod
    def add_workflow(user, name, desc, script, access, users, temp):
        try:
            workflow = Samples.create_workflow(user, name, desc, script, access, users, temp)
            return json.dumps(workflow.to_json_info());
        except:
            return json.dumps({})
                
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
    
    
@main.route('/samples', methods=['GET', 'POST'])
@login_required
def samples():
    if request.form.get('sample'):
        return Samples.add_workflow(current_user.id, request.form.get('name'), request.form.get('desc'), request.form.get('sample'), request.form.get('access'), request.form.get('users'), False)
    elif request.args.get('sample_id'):
        workflow = Workflow.query.filter_by(id = request.args.get('sample_id')).first_or_404()
        return json.dumps(workflow.to_json())
    elif request.args.get('tooltip'):
        workflow = Workflow.query.filter_by(id = request.args.get('tooltip')).first_or_404()
        return json.dumps(workflow.to_json_tooltip())
               
    access = int(request.args.get('access')) if request.args.get('access') else 0
    return json.dumps({'samples': Samples.get_samples_as_list(access)})