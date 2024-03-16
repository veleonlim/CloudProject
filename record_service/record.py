import json
import uuid
from flask import Blueprint, redirect, render_template, request, jsonify, url_for,session
from datetime import datetime
# from event_service.database import *
from record_service.database import *

from datetime import datetime

record_bp = Blueprint('record', __name__)

# function called when user joins an event
@record_bp.route('/join_event/<event_id>/<event_capacity>', methods=['POST'])
def join_event(event_id,event_capacity):
    if request.method == 'POST':
        participant_count = len(get_event_joined_count_by_id(event_id))
        if int(participant_count) == int(event_capacity):
            print("MAXIMUM SLOT")
            response = False
        else:
            email = session['email']
            record_id = generate_unique_record_id()
            response = create_record(record_id, event_id, email)

        if response:
            print("SUCCESSFULLY JOINED")
            return redirect(url_for('events.Bulletinuser'))
        else:
            print("ERROR JOINING")
            return redirect(url_for('events.Bulletinuser'))

# Retrieve all records for the event
@record_bp.route('/get_event_joined_records/<event_id>', methods=['GET'])
def get_event_joined_records(event_id):
    
    joined_records = get_event_joined_count_by_id(event_id)
    
    return joined_records

# For users to leave/unjoin an event
@record_bp.route('/leave_event/<record_id>', methods=['POST'])
def leave_event(record_id):
    if request.method == 'POST':

        response = delete_record(record_id)

        if response:
            
            return redirect(url_for('events.Bulletinuser'))
        else:
            return redirect(url_for('events.Bulletinuser'))
    
# Delele all records of an event
@record_bp.route('/terminate_event/<event_id>', methods=['POST'])
def terminate_event(event_id):
    if request.method == 'POST':

        response = delete_records_of_event(event_id)

        if response:
            return redirect(url_for('events.Bulletinuser'))
        else:
            return redirect(url_for('events.Bulletinuser'))
    
# Display/Output joined records on HTML
@record_bp.route('/get_event_joined_records_view/<event_id>', methods=['GET'])
def get_event_joined_records_view(event_id):
    print("ENTERED HERE\n\n")
    participant_records = get_event_joined_count_by_id(event_id)
    
    return render_template('view_participation.html', participant_records=participant_records, event_id=event_id)

def generate_unique_record_id():
    # Generate a unique record ID
    return str(uuid.uuid4())
