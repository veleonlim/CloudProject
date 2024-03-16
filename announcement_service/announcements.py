import json
from flask import Blueprint, redirect, render_template, request, jsonify, session, url_for
from announcement_service.database import *
from datetime import datetime
from record_service import record
s3 = boto3.client('s3')


announcements_bp = Blueprint('announcement', __name__)

# Route to create a new event
@announcements_bp.route('/create_announcement', methods=['POST'])
def create_announcement_route():
    
    email = session['email'] 
    
    data = request.form
    announcement_name = data.get('announcement_name') 
    
    announcement_start_date = data.get('announcement_start_date')  # Corrected the field name
    announcement_end_date = data.get('announcement_end_date')  # Corrected the field name
    announcement_description = data.get('announcement_description')  # Corrected the field name
    # Handle image upload
    announcement_image = request.files.get('announcement_img')
    image_url = None
    if announcement_image and announcement_image.filename:
        try:
            if announcement_image and hasattr(announcement_image, 'read'):
                # Pass the image_data directly to the create_event function
                response = create_announcement(
                    announcement_name, announcement_start_date,announcement_end_date, announcement_description, email, announcement_image
                )
                image_url = response.get('image_url')  # You can retrieve the image URL from the response if your create_event function returns it.
                print("Sucessessfully created")
            else:
                print("Invalid or unreadable file object for announcement_img")
        except Exception as e:
            print("Error uploading image to S3:", str(e))
            # Handle the error, log it, or return an error response
    print("image_url:", image_url)
    

    # Assuming create_event() takes the correct parameters
    if session.get('role') == 'admin':
        return redirect(url_for('announcement.Announcementadmin'))
    elif session.get('role') == 'user':
        return redirect(url_for('announcement.Announcementuser'))


@announcements_bp.route('/Announcementadmin', methods=['GET'])
def Announcementadmin():
    # Retrieve all announcements from DynamoDB
    announcements = get_all_announcement()
    for announcement in announcements:
        announcement['image_url'] = announcement.get('image_url')
        print(  announcement['image_url'])
        announcement['name'] = announcement.get('announcement_name')
        announcement['announcement_start_date'] = announcement.get('announcement_start_date')
        announcement['announcement_end_date'] = announcement.get('announcement_end_date')
        announcement['description'] = announcement.get('announcement_description')
        announcement['email'] = announcement.get('email')
        announcement['submittedTime'] = announcement.get('announcement_submitted_time')
        if session['role'] == "admin":
            announcement['ubtn'] = True
        else:
            announcement['ubtn'] = False

    # Sort the processed announcements based on the timestamp
    sorted_announcements = sorted(announcements, key=lambda x: x.get('submittedTime', 0))

    return render_template('Announcementadmin.html', announcements=sorted_announcements)



@announcements_bp.route('/Announcementuser', methods=['GET'])
def Announcementuser():
    # Retrieve all events from DynamoDB
   # Retrieve all announcements from DynamoDB
    announcements = get_all_announcement()
    for announcement in announcements:
        announcement['image_url'] = announcement.get('image_url')
        print(  announcement['image_url'])
        announcement['name'] = announcement.get('announcement_name')
        announcement['announcement_start_date'] = announcement.get('announcement_start_date')
        announcement['announcement_end_date'] = announcement.get('announcement_end_date')
        announcement['description'] = announcement.get('announcement_description')
        announcement['email'] = announcement.get('email')
        announcement['submittedTime'] = announcement.get('announcement_submitted_time')
        if session['role'] == "admin":
            announcement['ubtn'] = True
        else:
            announcement['ubtn'] = False

    # Sort the processed announcements based on the timestamp
    sorted_announcements = sorted(announcements, key=lambda x: x.get('submittedTime', 0))

    return render_template('Announcement.html', announcements=sorted_announcements)



@announcements_bp.route('/retrievannouncement', methods=['GET'])
def retrieveannouncement():
    announcement_id = request.args.get('announcement_id')  # Get the event_id from the query parameters

    # Retrieve event details based on the event_id
    item = get_announcement(announcement_id)

    # Check if the event exists
    if item:
        # Extract all relevant attributes for the event and remove the 'S' key
        announcement_name = item.get('announcement_name')['S']
        announcement_start_date = item.get('announcement_start_date')['S']
        announcement_end_date = item.get('announcement_end_date')['S']
        announcement_description = item.get('announcement_description')['S']
        email = item.get('email')['S']
        submitted_time = item.get('announcement_submitted_time')['S']
        image_url = item.get('image_url')['S']

        return render_template('retrieveannouncement.html', announcement_id=announcement_id, announcement_name=announcement_name, announcement_end_date=announcement_end_date, announcement_start_date=announcement_start_date, announcement_description=announcement_description, email=email,submitted_time=submitted_time, image_url=image_url)
    else:
        return "Announcement not found"  # Handle the event not found case


    
# Route to update an event's details
@announcements_bp.route('/update_announcement/<announcement_id>', methods=['POST']) 
def update_announcement_route(announcement_id):
    announcement_name = request.form.get('announcement_name')
    announcement_start_date = request.form.get('announcement_start_date')
    announcement_end_date = request.form.get('announcement_end_date')
    announcement_description = request.form.get('announcement_description')

    # Call the function to update the event details in the database
    response = update_announcement(announcement_id, announcement_name, announcement_start_date, announcement_end_date,announcement_description)

    if response:
        return redirect(url_for('announcement.retrieveannouncement', announcement_id=announcement_id))
    else:
        return "Error updating event"
# Route to delete an event by event_id
@announcements_bp.route('/delete_announcement/<announcement_id>', methods=['GET'])
def delete_announcement_route(announcement_id):
    response = delete_announcement(announcement_id)
    if session.get('role') == 'admin':
        return redirect(url_for('announcement.Announcementadmin'))
    elif session.get('role') == 'user':
        return redirect(url_for('announcement.Announcementuser'))
