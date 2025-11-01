
from flask import Flask, request, jsonify
from functools import wraps
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mydatabase import create_database, Event, User
from organizerInterface import OrganizerInterface
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

DATABASE_URL = 'sqlite:///test_levem.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
API_KEY = "levem_api_key_2024"

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != API_KEY:
            return jsonify({'error': 'Unauthorized - Invalid or missing API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

def get_db_session():
    return Session()

def event_to_dict(event):
    return {
        'event_id': event.event_id,
        'organizer_id': event.organizer_id,
        'title': event.title,
        'description': event.description,
        'start_date': event.start_date.isoformat() if event.start_date else None,
        'end_date': event.end_date.isoformat() if event.end_date else None,
        'location': event.location
    }

@app.route('/api/events', methods=['POST'])
@require_api_key
def create_event():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'JSON data is required'}), 400
        
        required_fields = ['organizer_id', 'title', 'description', 'start_date', 'end_date', 'location']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Field {field} is required'}), 400
        
        session = get_db_session()
        org_interface = OrganizerInterface(session)
        
        success = org_interface.create_event(
            organizer_id=data['organizer_id'],
            title=data['title'],
            description=data['description'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            location=data['location']
        )
        
        if not success:
            session.close()
            return jsonify({'error': 'Failed to create event'}), 500
        
        event = session.query(Event).order_by(Event.event_id.desc()).first()
        session.close()
        
        return jsonify({
            'message': 'Event created successfully',
            'event': event_to_dict(event)
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Failed to create event: {str(e)}'}), 500

@app.route('/api/events', methods=['GET'])
@require_api_key
def get_all_events():
    try:
        session = get_db_session()
        events = session.query(Event).all()
        session.close()
        
        return jsonify({
            'events': [event_to_dict(event) for event in events],
            'total': len(events)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get events: {str(e)}'}), 500

@app.route('/api/events/<int:event_id>', methods=['DELETE'])
@require_api_key
def delete_event(event_id):
    try:
        data = request.get_json()
        if not data or 'user_id' not in data:
            return jsonify({'error': 'user_id is required in JSON body'}), 400
        
        session = get_db_session()
        org_interface = OrganizerInterface(session)
        
        success = org_interface.delete_event(
            user_id=data['user_id'],
            event_id=event_id
        )
        
        session.close()
        
        if not success:
            return jsonify({'error': 'Event not found or access denied'}), 404
        
        return jsonify({'message': 'Event deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to delete event: {str(e)}'}), 500

@app.route('/api/events/my/<int:user_id>', methods=['GET'])
@require_api_key
def get_user_events(user_id):
    try:
        session = get_db_session()
        org_interface = OrganizerInterface(session)
        
        events = org_interface.view_my_events(user_id)
        session.close()
        
        return jsonify({
            'events': [event_to_dict(event) for event in events],
            'total': len(events)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get user events: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'Levem API is running',
        'timestamp': datetime.utcnow().isoformat(),
        'project': 'Levem - Event Management System',
        'endpoints': {
            'create_event': 'POST /api/events',
            'get_all_events': 'GET /api/events',
            'get_user_events': 'GET /api/events/my/{user_id}',
            'delete_event': 'DELETE /api/events/{event_id}',
            'health_check': 'GET /api/health'
        }
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    try:
        create_database('sqlite:///test_levem.db')
    except:
        pass
    
    print("Levem API запущен на http://localhost:5000")
    print("Используйте API-ключ: levem_api_key_2024")
    print("Доступные эндпоинты:")
    print("- POST /api/events - создание мероприятия")
    print("- GET /api/events - получение всех мероприятий")
    print("- GET /api/events/my/{user_id} - получение мероприятий пользователя")
    print("- DELETE /api/events/{id} - удаление мероприятия (нужен user_id в JSON)")
    print("- GET /api/health - проверка состояния")
    
    app.run(debug=True, host='0.0.0.0', port=5000)