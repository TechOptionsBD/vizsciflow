import logging
from flask_socketio import join_room, leave_room, rooms, send, emit, SocketIO
from flask_login import current_user
from app.managers.chatmgr import chatmanager
from app import app

socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('joinchat')
def handle_join(data):
    # workflow_id = data['workflow_id']
    JoinChatRoom(data)
    # emit('status', {'msg': f'{current_user.username} has entered the room.'}, to=workflow_id)

@socketio.on('leavechat')
def handle_leave(data):
    # workflow_id = data['workflow_id']
    LeaveChatRoom(data)
    # emit('status', {'msg': f'{current_user.username} has left the room.'}, to=workflow_id)

@socketio.on('message')
def handle_message(data):
    workflow_id = data['workflow_id']
    message = data['message']
    SendChatMessage(workflow_id, message)
    # emit('message', {'message': message, 'user': current_user.username}, to=workflow_id)

def JoinChatRoom(workflow_id):
    try:
        # leave from all rooms in this session. Session is managed by python-socketio
        # for room in rooms():
        #     LeaveChatRoom(room)
        join_room(workflow_id)
        logging.info(f'Joined room {workflow_id}')
    except Exception as e:
        logging.error(str(e))

def LeaveChatRoom(workflow_id):
    try:
        if workflow_id in rooms():
            leave_room(workflow_id)
            logging.info(f'Left room {workflow_id}')
    except Exception as e:
        logging.error(str(e))

def SendChatMessage(workflow_id, message):
    try:
        # emit(<event>, message, to=workflow_id)
        if not workflow_id in rooms():
            JoinChatRoom(workflow_id)
        emit('message', {'message': message, 'user': current_user.username}, to=workflow_id)
        # insert into database -> workflow_id, user_id, session_id, message, timestamp
        chatmanager.add(user_id = current_user.id, workflow_id = workflow_id, message = message)
    except Exception as e:
        logging.error(str(e))
    return {}

def GetMessages(workflow_id):
    return chatmanager.get(workflow_id = workflow_id)