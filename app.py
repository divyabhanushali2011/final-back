from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from workout_api import WorkoutAPI,WorkoutDeleteAPI,WorkoutListAPI
from models import db
from routes import RegisterAPI, ProtectedAPI, DeleteUserAPI, ReminderAPI, LoginAPI, ForgotPasswordAPI
import os
app = Flask(__name__)

# Enable CORS for SvelteKit frontend
CORS(app, resources={r"/api/*": {"origins": "https://my-fronted-git-main-divyas-projects-031f9126.vercel.app"}}, supports_credentials=True)



api = Api(app)

# API endpoints
api.add_resource(RegisterAPI, '/api/register')
api.add_resource(LoginAPI, '/api/login')
api.add_resource(ForgotPasswordAPI, '/api/forgot')
api.add_resource(DeleteUserAPI, '/api/delete_user')
api.add_resource(ProtectedAPI, '/api/protected')
api.add_resource(ReminderAPI, '/api/reminder')
api.add_resource(WorkoutAPI, '/api/workout')
api.add_resource(WorkoutListAPI, '/api/workouts')
api.add_resource(WorkoutDeleteAPI, '/api/workout/<int:id>')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
