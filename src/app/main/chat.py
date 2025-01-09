import logging
from flask_socketio import join_room, leave_room, rooms, emit
from flask_login import current_user
from app.managers.chatmgr import chatmanager

from ..extensions import socketio

@socketio.on('joinchat')
def handle_join(data):
    JoinChatRoom(data)

@socketio.on('leavechat')
def handle_leave(data):
    LeaveChatRoom(data)

@socketio.on('message')
def handle_message(data):
    workflow_id = data['workflow_id']
    message = data['message']
    SendChatMessage(workflow_id, message)

@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))

def JoinChatRoom(workflow_id):
    try:
        # leave from all rooms in this session. Session is managed by python-socketio
        join_room(workflow_id)
    except Exception as e:
        logging.error(str(e))
        raise

def LeaveChatRoom(workflow_id):
    try:
        if workflow_id in rooms():
            leave_room(workflow_id)
    except Exception as e:
        logging.error(str(e))
        raise

def SendChatMessage(workflow_id, message):
    try:
        # emit(<event>, message, to=workflow_id)
        if not workflow_id in rooms():
            JoinChatRoom(workflow_id)
        # insert into database -> workflow_id, user_id, session_id, message, timestamp
        chatmanager.add(user_id = current_user.id, workflow_id = workflow_id, message = message)
        emit('message', {'message': message, 'user': current_user.username, 'workflow': workflow_id}, to=workflow_id)
    except KeyError as ke:
        logging.error(f"Key Error: {str(ke)}")
        raise
    except Exception as e:
        logging.error(str(e))
        raise
    return {}

def GetChatHistory(workflow_id):
    chats = chatmanager.get(workflow_id = workflow_id)
    chatjson = []
    for chat in chats:
        chatjson.append({'message': chat.message, 'user': chat.user.username})
    return chatjson
