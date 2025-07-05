from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from workout_api import WorkoutAPI,WorkoutDeleteAPI,WorkoutListAPI
from models import db
from routes import RegisterAPI, ProtectedAPI, DeleteUserAPI, ReminderAPI, LoginAPI, ForgotPasswordAPI

app = Flask(__name__)

# Enable CORS for SvelteKit frontend
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)



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
    app.run(debug=True)
