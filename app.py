from datetime import datetime
import uuid
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from event_service.events import events_bp
from announcement_service.announcements import announcements_bp
from login_service.login import login_bp
from comment_service.comments import comments_bp
from record_service.record import record_bp
from approval_service.approval import approval_bp
from botocore.exceptions import ClientError

from model import *
from utils import *
import key_config as keys
import boto3

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app = configure_app(app)

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=keys.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=keys.AWS_SECRET_ACCESS_KEY,
                          region_name=keys.REGION_NAME)

DYNAMODB_TABLE_NAME = 'Users'
table = dynamodb.Table(DYNAMODB_TABLE_NAME)

# Register the events Blueprint with your app
app.register_blueprint(events_bp, url_prefix='/events')  # Prefix the URL for your events routes
app.register_blueprint(login_bp, url_prefix='/login')  # Prefix the URL for your events routes
app.register_blueprint(comments_bp, url_prefix='/comment')  # Prefix the URL for your events routes
app.register_blueprint(record_bp, url_prefix='/record')  # Prefix the URL for your events routes
app.register_blueprint(announcements_bp, url_prefix='/announcement')  # Prefix the URL for your events routes
app.register_blueprint(approval_bp, url_prefix='/approval')
@app.route("/", methods=["GET"])
def home():
    return redirect(url_for('login'))



@app.route("/Bulletin", methods=["GET", "POST"])
def Bulletin():

    # if request.method == "POST":
    #     comment = request.form.get('comment')
    #     print(comment)

    #     if comment:
    #         timestamp = datetime.now().isoformat()  # Get the current timestamp
    #         # Assuming you have the user's username in the session
    #         username = session.get('username')
    #         DYNAMODB_TABLE_NAME = 'comments'  # Replace with your comments table name

    #         # Add the comment data to your DynamoDB table
    #         table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    #         response = table.put_item(
    #             Item={
    #                 # You may need to implement this function
    #                 'commentID': generate_unique_comment_id(),
    #                 'eventID': generate_event_id(),  # You may need to implement this function
    #                 'comment': comment,
    #                 'timestamp': timestamp,
    #                 'username': username,

    #             }
    #         )

    #         # You can handle the response or redirect to a success page
    #         return "Comment posted successfully!"

    # Handle GET requests or if the comment is empty
    return render_template("Bulletin.html")

# Generate a unique comment ID and event ID based on your requirements


def generate_unique_comment_id():
    return str(uuid.uuid4())


def generate_event_id():
    return str(uuid.uuid4())


@app.route("/createevent")
def createevent():
    return render_template("createevent.html")


@app.route("/createeventadmin")
def createeventadmin():
    return render_template("createeventadmin.html")


@app.route("/approveevent")
def approveevent():
    return render_template("approveevent.html")


@app.route("/announcement")
def announcement():
    return render_template("Announcement.html")


@app.route("/announcementadmin")
def announcementadmin():
    return render_template("Announcementadmin.html")


@app.route("/createannouncement")
def createannouncement():
    return render_template("createannouncement.html")

@app.route("/signup")
def signup():
    return render_template("sign-up.html")

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
