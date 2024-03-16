import json
from flask import Blueprint, redirect, render_template, request, jsonify, session, url_for
from approval_service.database import *
from datetime import datetime
from record_service import record

approval_bp = Blueprint('approval', __name__)

# Route to retrieve all unapproved events
@approval_bp.route('/get_unapproved_events', methods=['GET'])
def get_unapproved_events_route():
    unapproved_events = get_unapproved_events()  # Assuming you have a function to retrieve unapproved events
    
    for event in unapproved_events:
        event['image_url'] = event.get('image_url') 
        event['name'] = event.get('event_name')
        event['event_start_date'] = event.get('event_start_date')
        event['event_end_date'] = event.get('event_end_date')
        event['description'] = event.get('event_description')
        event['approval_status'] = event.get('approval_status')  # Add the approval_status field
        event['email'] = event.get('email')  # Add the email field
        event['capacity'] = event.get('capacity')  # Add the capacity field
        event['submittedTime'] = event.get('events_submitted_time')
        if event['email'] == session['email'] or session['role'] == "admin":
            event['ubtn'] = True
        else:
            event['ubtn'] = False


    sorted_unapproved_events = sorted(unapproved_events, key=lambda x: x.get('submittedTime', 0))
    
    return render_template('approveevent.html', events=sorted_unapproved_events)


@approval_bp.route('/test_unapproved_events', methods=['GET'])
def test_unapproved_events_route():
    # create a fake event
    items = [{
        'event_id': '123',
        'event_name': 'Test Event 1',
        'event_start_date': '2020-01-01',
        'event_end_date': '2020-01-02',
        'event_description': 'This is a test event',
        'approval_status': 'Pending',
        'email': 'vZ8p9@example.com',
        'capacity': 10,
        'submitted_time': datetime.now().strftime("%d/%m/%Y")
    },
    {
        'event_id': '456',
        'event_name': 'Test Event 2',
        'event_start_date': '2020-01-01',
        'event_end_date': '2020-01-02',
        'event_description': 'This is a test event',
        'approval_status': 'Pending',
        'email': 'vZ8p9@example.com',
        'capacity': 10,
        'submitted_time': datetime.now().strftime("%d/%m/%Y")}]
    return jsonify(items)

# Route to approve an event
@approval_bp.route('/approve_event_route/<event_id>', methods=['POST'])
def approve_event_route(event_id):
    # The 'event_id' parameter is available here as part of the route
    response = approve_event(event_id)
    return redirect(url_for('approval.get_unapproved_events_route'))
   
# Route to reject an event
@approval_bp.route('/reject_event_route/<event_id>', methods=['POST'])
def reject_event_route(event_id):

    response = reject_event(event_id)
    return redirect(url_for('approval.get_unapproved_events_route'))