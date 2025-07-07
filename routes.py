# ✅ Cleaned and Fixed routes.py

from flask import request, jsonify
from flask_restful import Resource,reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from uuid import uuid4
from flask.views import MethodView  
from flask_cors import core,cross_origin
import traceback  # ✅ Needed for debugging
from datetime import datetime
from models import User, db, Reminder, Workout
from utils import generate_token, decode_token
import secrets



# ✅ Register Endpoint
class RegisterAPI(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('firstName', required=True)
        parser.add_argument('lastName', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('phone', required=True)
        parser.add_argument('address')
        parser.add_argument('city')
        parser.add_argument('state')
        parser.add_argument('zip')
        parser.add_argument('birthdate', required=True)
        parser.add_argument('gender', required=True)
        parser.add_argument('password', required=True)
        parser.add_argument('confirmPassword', required=True)
        parser.add_argument('plan', required=True)
        parser.add_argument('planType')
        parser.add_argument('selectedPaymentMethod')

        data = parser.parse_args()

        # Password match check
        if data['password'] != data['confirmPassword']:
            return {'error': 'Passwords do not match!'}, 400

        # Email uniqueness check
        if User.select().where(User.email == data['email']).exists():
            return {'error': 'Email already registered.'}, 400

        try:
            user = User.create(
                first_name=data['firstName'],
                last_name=data['lastName'],
                email=data['email'],
                phone=data['phone'],
                address=data['address'],
                city=data['city'],
                state=data['state'],
                zip=data['zip'],
                birthdate=data['birthdate'],
                gender=data['gender'],
                password=generate_password_hash(data['password']),
                plan=data['plan'],
                plan_type=data['planType'] if data['plan'] == 'paid' else None,
                payment_method=data['selectedPaymentMethod'] if data['plan'] == 'paid' else None
            )

            # ✅ Only this part is updated
            return {
                'message': f"Welcome {user.first_name}, you’ve been registered successfully!",
                'user': {
                    'first_name': user.first_name,
                    'email': user.email,
                }
            }, 201

        except Exception as e:
            return {'error': str(e)}, 500

class ProtectedAPI(Resource):
    def get(self):
        api_key = request.headers.get('x-api-key')
        user = User.get_or_none(User.api_key == api_key)

        if not user:
            return {'error': 'Invalid or missing API key'}, 401

        return {'message': 'Access granted ✅', 'user_email': user.email}


# ✅ Delete User by ID
class DeleteUserAPI(Resource):
    def delete(self):
        user_id = request.args.get('id')
        user = User.get_or_none(User.id == user_id)
        if user:
            user.delete_instance()
            return {"message": "User deleted ✅"}, 200
        return {"message": "User not found"}, 404


# ✅ Create Reminder
class ReminderAPI(Resource):
    def post(self):
        data = request.get_json()

        category = data.get('category')
        task = data.get('task')
        interval = data.get('interval')
        unit = data.get('unit')

        if not category or not task or not interval or not unit:
            return {'error': 'Please fill in all fields.'}, 400

        try:
            reminder = Reminder.create(
                category=category,
                task=task,
                interval=int(interval),
                unit=unit
            )

            return {
                'message': 'Reminder set successfully ✅',
                'reminder': model_to_dict(reminder)
            }, 201

        except ValueError:
            return {'error': 'Interval must be a valid number.'}, 400

        except Exception as e:
            traceback.print_exc()
            return {'error': f'Internal server error: {str(e)}'}, 500


# ✅ Login API
class LoginAPI(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help='Email is required')
        parser.add_argument('password', type=str, required=True, help='Password is required')
        args = parser.parse_args()

        email = args['email']
        password = args['password']

        try:
            user = User.get(User.email == email)
        except User.DoesNotExist:
            return {'error': 'Invalid email or password'}, 401

        if not user.check_password(password):
            return {'error': 'Invalid email or password'}, 401

        # Generate token (replace with JWT in production)
        token = secrets.token_hex(16)

        return {
            'message': 'Login successful',
            'token': token,
            'api_key': user.api_key if hasattr(user, 'api_key') else 'demo_key',
            'user': {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': user.phone,
                'address': user.address,
                'city': user.city,
                'state': user.state,
                'zip': user.zip,
                'birthdate': str(user.birthdate),
                'gender': user.gender,
                'plan': user.plan,
                'plan_type': user.plan_type,
                'payment_method': user.payment_method,
                'registered_at': str(user.registered_at)
            }
        }, 200

# ✅ Forgot Password API
class ForgotPasswordAPI(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        new_password = data.get('new_password')

        if not email or not new_password:
            return {'error': 'Email and new password are required'}, 400

        user = User.get_or_none(User.email == email)
        if not user:
            return {'error': 'Email not found'}, 404

        user.password = generate_password_hash(new_password)
        user.save()

        return {'message': 'Password reset successfully ✅'}, 200

# ✅ Workout Create & Fetch

class WorkoutAPI(Resource):
    @cross_origin(origins='https://my-fronted-git-main-divyas-projects-031f9126.vercel.app', supports_credentials=True)
    def post(self):
        data = request.get_json()
        user_email = data.get('user_email')

        if not user_email:
            return {'error': 'Missing user email'}, 400

        required_fields = ['type', 'name', 'sets', 'reps', 'duration', 'calories']
        missing = [f for f in required_fields if not data.get(f)]

        if missing:
            return {'error': f'Missing fields: {", ".join(missing)}'}, 400

        try:
            with db.atomic():
                workout = Workout.create(
                    user_email=user_email,
                    type=data['type'],
                    name=data['name'],
                    sets=int(data['sets']),
                    reps=int(data['reps']),
                    duration=int(data['duration']),
                    calories=int(data['calories'])
                )

            return {
                'message': 'Workout saved successfully ✅',
                'workout': model_to_dict(workout)
            }, 201

        except Exception as e:
            return {'error': f'Internal error: {str(e)}'}, 500

    @cross_origin(origins='https://my-fronted-git-main-divyas-projects-031f9126.vercel.app', supports_credentials=True)
    def get(self):
        email = request.args.get('email')
        print(f"📩 Fetching workouts for: {email}")

        if not email:
            return {'error': 'Missing email parameter'}, 400

        try:
            workouts = Workout.select().where(Workout.user_email == email).order_by(Workout.created_at.desc())
            return {
                'workouts': [model_to_dict(w) for w in workouts]
            }, 200
        except Exception as e:
            return {'error': f'Failed to fetch workouts: {str(e)}'}, 500
# Workout Delete API
class WorkoutDeleteAPI(MethodView):
    @cross_origin(origins='https://my-fronted-git-main-divyas-projects-031f9126.vercel.app')
    def delete(self, workout_id):
        try:
            workout = Workout.get_or_none(Workout.id == workout_id)
            if workout:
                workout.delete_instance()
                return jsonify({'message': 'Workout deleted'}), 200
            return jsonify({'error': 'Workout not found'}), 404
        except Exception as e:
            return jsonify({'error': f'Error deleting workout: {str(e)}'}), 500
