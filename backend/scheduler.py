from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "dakshkhosla100@gmail.com"
app.config["MAIL_PASSWORD"] = "fqzs lcwv vxou xgju"
mail = Mail(app)

Sender="dakshkhosla100@gmail.com"


def send_email_reminder():
    try:
        with app.app_context():
            msg = Message("Service Request Reminder",
                        sender=Sender,
                        recipients=["dakshkhosla1000@gmail.com"])
            provider_name = "Provider"
            msg.body = f"Hello {provider_name},\n\nYou have pending service requests. Please check your dashboard."
            mail.send(msg)
            print("Email Sent!")
    except Exception as e:  
        print("Error in sending email: ", e)

send_email_reminder()


def generate_monthly_report():
    with app.app_context():  # Required for Flask-Mail
        # **Dummy Data**
        requests_list = [
            (101, "2024-03-01", "Completed"),
            (102, "2024-03-05", "Pending"),
            (103, "2024-03-10", "In Progress"),
        ]
        customer_email = "dakshkhosla1000@gmail.com"

        # **Generate HTML Report**
        html_content = "<h1>Monthly Report</h1><table border='1'><tr><th>Service ID</th><th>Date</th><th>Status</th></tr>"
        for request in requests_list:
            service_id, date_of_request, status = request
            html_content += f"<tr><td>{service_id}</td><td>{date_of_request}</td><td>{status}</td></tr>"
        html_content += "</table>"

        # **Send Email Report**
        subject = "Your Monthly Activity Report"
        message = Message(subject, sender=Sender,recipients=[customer_email])
        message.html = html_content
        mail.send(message)
        print("Monthly Report Sent!")

# **Test Run**
generate_monthly_report()
