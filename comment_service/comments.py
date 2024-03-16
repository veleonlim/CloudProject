import json
import uuid
from flask import Blueprint, redirect, render_template, request, jsonify, url_for,session
from datetime import datetime
from event_service.database import *
from comment_service.database import *

from datetime import datetime

comments_bp = Blueprint('comment', __name__)

@comments_bp.route('/retrieveevent', methods=['GET'])

def retrieveevent():
    event_id = request.args.get('event_id')  # Get the event_id from the query parameters

    # Retrieve event details based on the event_id
    item = get_event(event_id)

    # Check if the event exists
    if item:
        # Extract relevant attributes (event_date and event_description)
        event_start_date = item.get('event_start_date')['S']
        event_end_date = item.get('event_end_date')['S']
        event_description = item.get('event_description', {}).get('S', 'Default Description')
        event_name = item.get('event_name', {}).get('S', 'Default Name')
        return render_template('addcomment.html', event_id=event_id, event_name=event_name,event_start_date=event_start_date,event_end_date=event_end_date, event_description=event_description)
    else:
        return "Event not found"  # Handle the event not found case
    
@comments_bp.route('/get_comments/<event_id>', methods=['GET'])
def get_comments(event_id):
    # Assuming that you have a function to retrieve comments by event_id in your database module
    comments = get_comments_by_event_id(event_id)

    # Retrieve event details based on the event_id
    item = get_event(event_id)

    if comments:
        # Extract relevant attributes (event_date and event_description)
  
        event_start_date = item.get('event_start_date')['S']
        event_end_date = item.get('event_end_date')['S']
        event_description = item.get('event_description', {}).get('S', 'Default Description')
        event_name = item.get('event_name', {}).get('S', 'Default Name')
        return render_template('viewcomment.html', comments=comments, event_id=event_id, event_name = event_name, event_start_date=event_start_date,event_end_date=event_end_date, event_description=event_description)
    else:
        return "No comments found"  # Handle the case when there are no comments


@comments_bp.route('/add_comment/<event_id>', methods=['POST'])
def add_comment(event_id):
    # Get the comment content from the form
    comment = request.form.get('add_comment')
    # event_id = request.args.get('event_id')  # Get the event_id from the query parameters

    # Retrieve event details based on the event_id
    # item = get_event(event_id)
    # Check if the user is logged in (you may have your own way of handling sessions)
   
     

    # Generate a comment_id and timestamp
    comment_id = generate_unique_comment_id()
    comment_submitted_time = datetime.now().isoformat()
    email = session['email']

    # Call the function to add the comment to the database
    response = create_comment(comment_id, event_id, email, comment, comment_submitted_time)

    if response:
        return redirect(url_for('comment.retrieveevent', event_id=event_id))

    else:
        return "Error adding comment"
    
    
def generate_unique_comment_id():
    # Generate a unique comment ID (you can adjust this based on your requirements)
    return str(uuid.uuid4())
