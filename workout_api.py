from flask_restful import Resource, reqparse
from models import db, Workout

class WorkoutAPI(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('type', required=True)
            parser.add_argument('name', required=True)
            parser.add_argument('sets', type=int, required=True)
            parser.add_argument('reps', type=int, required=True)
            parser.add_argument('duration', type=int, required=True)
            parser.add_argument('calories', type=int, required=True)
            data = parser.parse_args()

            workout = Workout.create(
                type=data['type'],
                name=data['name'],
                sets=data['sets'],
                reps=data['reps'],
                duration=data['duration'],
                calories=data['calories']
            )

            return {'message': 'Workout added', 'id': workout.id}, 201
        except Exception as e:
            return {'error': str(e)}, 500

class WorkoutListAPI(Resource):
    def get(self):
        try:
            workouts = Workout.select()
            return [{
                'id': w.id,
                'type': w.type,
                'name': w.name,
                'sets': w.sets,
                'reps': w.reps,
                'duration': w.duration,
                'calories': w.calories
            } for w in workouts], 200
        except Exception as e:
            return {'error': str(e)}, 500

class WorkoutDeleteAPI(Resource):
    def delete(self, id):
        try:
            workout = Workout.get_or_none(Workout.id == id)
            if workout:
                workout.delete_instance()
                return {'message': 'Workout deleted'}, 200
            else:
                return {'error': 'Workout not found'}, 404
        except Exception as e:
            return {'error': str(e)}, 500
