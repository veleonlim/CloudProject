import json
from flask import Blueprint, redirect, render_template, request, jsonify, session, url_for
from event_service.database import *
from datetime import datetime
from record_service import record
s3 = boto3.client('s3')


events_bp = Blueprint('events', __name__)

# Route to create a new event
@events_bp.route('/create_event', methods=['POST'])
def create_event_route():
    
    email = session['email'] 
   
    data = request.form
    if session.get('role') == 'admin':
        approval_status='approved'
    elif session.get('role') == 'user':
        approval_status=data.get("approval_status")
    event_name = data.get('event_name') 
    capacity = data.get('capacity')  # Corrected the field name to 'event_name'
    event_start_date = data.get('event_start_date')  # Corrected the field name
    event_end_date = data.get('event_end_date')  # Corrected the field name
    event_description = data.get('event_description')  # Corrected the field name
    # Handle image upload
    event_image = request.files.get('event_img')
    image_url = None
    if event_image and event_image.filename:
        try:
            if event_image and hasattr(event_image, 'read'):
                # Pass the image_data directly to the create_event function
                response = create_event(
                    event_name, event_start_date, event_end_date, event_description, approval_status, email, capacity, event_image
                )
                image_url = response.get('image_url')  # You can retrieve the image URL from the response if your create_event function returns it.
            else:
                print("Invalid or unreadable file object for event_img")
        except Exception as e:
            print("Error uploading image to S3:", str(e))
            # Handle the error, log it, or return an error response
    print("image_url:", image_url)
    

    # Assuming create_event() takes the correct parameters
    if session.get('role') == 'admin':
        return redirect(url_for('events.Bulletinadmin'))
    elif session.get('role') == 'user':
        return redirect(url_for('events.Bulletinuser'))


@events_bp.route('/Bulletinadmin', methods=['GET'])
def Bulletinadmin():
    # Retrieve all events from DynamoDB
    events = get_all_events()
    for event in events:
        event['image_url'] = event.get('image_url') 
        event['name'] = event.get('event_name')  # Update to the correct field name
        event['event_start_date'] = event.get('event_start_date')
        event['event_end_date'] = event.get('event_end_date')
        event['description'] = event.get('event_description')
        event['approval_status'] = event.get('approval_status')  # Add the approval_status field
        event['email'] = event.get('email')  # Add the email field
        event['capacity'] = event.get('capacity')  # Add the capacity field
        event['submittedTime'] = event.get('events_submitted_time')  # Update to the correct field name
        if event['email'] == session['email'] or session['role'] == "admin":
            event['ubtn'] = True
        else:
            event['ubtn']= False

        try:
            participants_record = record.get_event_joined_records(event.get('event_id'))
            event['joined_count'] = len(participants_record)
        except Exception as e:
            print("An error occurred:", str(e))

    # Sort the processed events based on the timestamp
    sorted_events = sorted(events, key=lambda x: x.get('submittedTime', 0))

    return render_template('Bulletinadmin.html', events=sorted_events)


@events_bp.route('/Bulletinuser', methods=['GET'])
def Bulletinuser():
    # Retrieve all events from DynamoDB
    events = get_all_events()
    for event in events:
        event['image_url'] = event.get('image_url') 
        event['name'] = event.get('event_name')  # Update to the correct field name
        event['event_start_date'] = event.get('event_start_date')
        event['event_end_date'] = event.get('event_end_date')
        event['description'] = event.get('event_description')
        event['approval_status'] = event.get('approval_status')  # Add the approval_status field
        event['email'] = event.get('email')  # Add the email field
        event['capacity'] = event.get('capacity')  # Add the capacity field
        event['submittedTime'] = event.get('events_submitted_time')  # Update to the correct field name
        if event['email'] == session['email'] or session['role'] == "admin":
            event['ubtn'] = True
        else:
            event['ubtn']= False
        print(event['ubtn'])
        try:
            participants_record = record.get_event_joined_records(event.get('event_id'))
            event['joined_count'] = len(participants_record)

            event['joined_status'] = False  # Initialize to False

            for participant_record in participants_record:
                print(participant_record)
                if participant_record['email'] == session['email']:
                    event['joined_status'] = True  # Set to True if a match is found
                    event['record_id'] = participant_record.get('record_id')  # Set to True if a match is found

        except Exception as e:
            print("An error occurred:", str(e))

    # Sort the processed events based on the timestamp
      
    sorted_events = sorted(events, key=lambda x: x.get('submittedTime', 0))
    
    return render_template('Bulletin.html', events=sorted_events)



@events_bp.route('/retrieveevent', methods=['GET'])
def retrieveevent():
    event_id = request.args.get('event_id')  # Get the event_id from the query parameters

    # Retrieve event details based on the event_id
    item = get_event(event_id)

    # Check if the event exists
    if item:
        # Extract all relevant attributes for the event and remove the 'S' key
        event_name = item.get('event_name')['S']
        event_start_date = item.get('event_start_date')['S']
        event_end_date = item.get('event_end_date')['S']
        event_description = item.get('event_description')['S']
        approval_status = item.get('approval_status')['S']
        email = item.get('email')['S']
        capacity = item.get('capacity')['S']
        submitted_time = item.get('events_submitted_time')['S']
        image_url = item.get('image_url')['S']

        return render_template('retrieveevent.html', event_id=event_id, event_name=event_name, event_end_date=event_end_date, event_start_date=event_start_date, event_description=event_description, approval_status=approval_status, email=email, capacity=capacity, submitted_time=submitted_time, image_url=image_url)
    else:
        return "Event not found"  # Handle the event not found case


    
# Route to update an event's details
@events_bp.route('/update_event/<event_id>', methods=['POST']) 
def update_event_route(event_id):
    # Retrieve form inputs
    if session.get('role') == 'admin':
        approval_status='approved'
    elif session.get('role') == 'user':
        approval_status=request.form.get("approval_status")
    event_name = request.form.get('event_name')
    event_start_date = request.form.get('event_start_date')
    event_end_date = request.form.get('event_end_date')
    event_description = request.form.get('event_description')
    
    capacity = request.form.get('capacity')

    # Call the function to update the event details in the database
    response = update_event(event_id, event_name, event_start_date, event_end_date, event_description,approval_status, capacity)

    if response:
        return redirect(url_for('events.retrieveevent', event_id=event_id))
    else:
        return "Error updating event"
# Route to delete an event by event_id
@events_bp.route('/delete_event/<event_id>', methods=['GET'])
def delete_event_route(event_id):
    response = delete_event(event_id)
    if session.get('role') == 'admin':
        return redirect(url_for('events.Bulletinadmin'))
    elif session.get('role') == 'user':
        return redirect(url_for('events.Bulletinuser'))


