from app import blogapp
from flask_socketio import SocketIO, emit

socketio = SocketIO(blogapp)
if __name__=="__main__":
    socketio.run(blogapp,debug=True)
    # blogapp.run(debug=False)
    