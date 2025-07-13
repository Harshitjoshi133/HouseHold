from celery import shared_task
from flask import current_app, render_template
from sqlalchemy import func
import csv
import io
import os
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from flask_mail import Mail, Message

from models import db, User, Professional, ServiceRequest, Customer, Service, Review
from logger import setup_logger, log_error_with_context, log_performance_metric

# Initialize logger
logger = setup_logger('tasks')

# Email configuration
Sender = "dakshkhosla100@gmail.com"

@shared_task(bind=True)
def send_daily_reminders(self):
    """Send daily reminders to professionals with pending service requests"""
    logger.info("Starting daily reminder task...")
    
    start_time = datetime.now()
    
    try:
        # Get pending requests
        pending_requests = db.session.query(
            Professional.id,
            User.email,
            User.full_name,
            func.count(ServiceRequest.id).label('pending_count')
        ).join(User).join(
            ServiceRequest, 
            (ServiceRequest.professional_id == Professional.id) & 
            (ServiceRequest.status.in_(['assigned', 'in_progress']))
        ).group_by(Professional.id).all()

        logger.info(f"Found {len(pending_requests)} professionals with pending requests.")

        reminders_sent = 0
        for prof_id, email, name, count in pending_requests:
            if count > 0:
                try:
                    logger.info(f"Sending reminder to {email} with {count} pending requests.")
                    send_email(
                        to=email,
                        subject="You have pending service requests",
                        template="emails/daily_reminder.html",
                        name=name,
                        pending_count=count
                    )
                    reminders_sent += 1
                except Exception as e:
                    logger.error(f"Failed to send reminder to {email}: {e}")
                    log_error_with_context(e, {
                        "task": "send_daily_reminders",
                        "professional_id": prof_id,
                        "email": email
                    })

        execution_time = (datetime.now() - start_time).total_seconds()
        log_performance_metric("daily_reminders_execution_time", execution_time * 1000, "ms")
        
        logger.info(f"Daily reminder task completed. Sent {reminders_sent} reminders in {execution_time:.2f}s")
        return f"Sent {reminders_sent} reminders"

    except Exception as e:
        execution_time = (datetime.now() - start_time).total_seconds()
        logger.error(f"Daily reminder task failed after {execution_time:.2f}s: {e}")
        log_error_with_context(e, {
            "task": "send_daily_reminders",
            "execution_time": execution_time
        })
        
        # Retry the task with exponential backoff
        raise self.retry(countdown=60, max_retries=3, exc=e)

@shared_task(bind=True)
def send_monthly_report(self, customer_ids=None):
    """Generate and send monthly activity reports for customers"""
    logger.info("Starting monthly report generation...")
    
    start_time = datetime.now()
    
    try:
        # Get customers to process
        if customer_ids:
            customers = Customer.query.filter(Customer.id.in_(customer_ids)).all()
            logger.info(f"Processing {len(customers)} specific customers")
        else:
            customers = Customer.query.all()
            logger.info(f"Processing all {len(customers)} customers")
        
        today = datetime.utcnow()
        first_day = datetime(today.year, today.month, 1)
        last_month = first_day - timedelta(days=1)
        start_date, end_date = datetime(last_month.year, last_month.month, 1), first_day - timedelta(days=1)

        reports_sent = 0
        reports_failed = 0

        for customer in customers:
            try:
                user = User.query.get(customer.user_id)
                if not user or not user.email:
                    logger.warning(f"Skipping customer {customer.id} - no valid email")
                    continue
                
                # Get service requests for the month
                service_requests = ServiceRequest.query.filter(
                    ServiceRequest.customer_id == customer.id,
                    ServiceRequest.date_of_request.between(start_date, end_date)
                ).all()

                if not service_requests:
                    logger.debug(f"No activity for customer {user.email} in {last_month.strftime('%B %Y')}")
                    continue
                
                # Calculate status counts
                status_counts = {}
                for sr in service_requests:
                    status_counts[sr.status] = status_counts.get(sr.status, 0) + 1

                # Calculate average rating
                avg_rating = db.session.query(func.avg(Review.rating)).join(ServiceRequest).filter(
                    ServiceRequest.customer_id == customer.id,
                    Review.created_at.between(start_date, end_date)
                ).scalar() or 0

                logger.info(f"Sending report to {user.email} for {len(service_requests)} requests.")
                
                send_email(
                    to=user.email,
                    subject=f"Monthly Activity Report - {last_month.strftime('%B %Y')}",
                    template="reports/monthly_activity.html",
                    user_name=user.full_name,
                    month=last_month.strftime('%B %Y'),
                    service_requests=service_requests,
                    status_counts=status_counts,
                    total_requests=len(service_requests),
                    avg_rating=avg_rating
                )
                reports_sent += 1
                
            except Exception as e:
                reports_failed += 1
                logger.error(f"Failed to send report to customer {customer.id}: {e}")
                log_error_with_context(e, {
                    "task": "send_monthly_report",
                    "customer_id": customer.id,
                    "user_email": user.email if 'user' in locals() else None
                })

        execution_time = (datetime.now() - start_time).total_seconds()
        log_performance_metric("monthly_report_execution_time", execution_time * 1000, "ms")
        
        logger.info(f"Monthly report task completed. Sent {reports_sent} reports, {reports_failed} failed in {execution_time:.2f}s")
        return f"Sent {reports_sent} monthly reports, {reports_failed} failed"

    except Exception as e:
        execution_time = (datetime.now() - start_time).total_seconds()
        logger.error(f"Monthly report task failed after {execution_time:.2f}s: {e}")
        log_error_with_context(e, {
            "task": "send_monthly_report",
            "execution_time": execution_time,
            "customer_ids": customer_ids
        })
        
        # Retry the task with exponential backoff
        raise self.retry(countdown=300, max_retries=3, exc=e)

def send_email(to, subject, template, **kwargs):
    """Send an email using Flask-Mail with error handling"""
    try:
        # Get the current app context
        app = current_app._get_current_object()
        mail = Mail(app)
        
        msg = Message(subject, sender=Sender, recipients=[to])
        
        # Render the template
        try:
            html = render_template(template, **kwargs)
            msg.html = html
        except Exception as template_error:
            logger.error(f"Template rendering failed for {template}: {template_error}")
            # Fallback to simple text
            msg.body = f"Subject: {subject}\n\nThis is an automated message from Household Services."
        
        mail.send(msg)
        logger.info(f"Email sent successfully to {to}")
        
    except Exception as e:
        logger.error(f"Failed to send email to {to}: {e}")
        log_error_with_context(e, {
            "function": "send_email",
            "recipient": to,
            "subject": subject,
            "template": template
        })
        raise

@shared_task(bind=True)
def cleanup_old_data(self):
    """Clean up old data and logs"""
    logger.info("Starting data cleanup task...")
    
    try:
        # Clean up old service requests (older than 1 year)
        cutoff_date = datetime.utcnow() - timedelta(days=365)
        old_requests = ServiceRequest.query.filter(
            ServiceRequest.date_of_request < cutoff_date,
            ServiceRequest.status.in_(['completed', 'closed'])
        ).delete()
        
        logger.info(f"Cleaned up {old_requests} old service requests")
        
        # Clean up old reviews (older than 1 year)
        old_reviews = Review.query.filter(
            Review.created_at < cutoff_date
        ).delete()
        
        logger.info(f"Cleaned up {old_reviews} old reviews")
        
        return f"Cleanup completed: {old_requests} requests, {old_reviews} reviews"
        
    except Exception as e:
        logger.error(f"Data cleanup task failed: {e}")
        log_error_with_context(e, {"task": "cleanup_old_data"})
        raise self.retry(countdown=3600, max_retries=3, exc=e)

@shared_task(bind=True)
def update_professional_ratings(self):
    """Update average ratings for professionals"""
    logger.info("Starting professional ratings update...")
    
    try:
        professionals = Professional.query.all()
        updated_count = 0
        
        for professional in professionals:
            try:
                # Calculate new average rating
                avg_rating = db.session.query(func.avg(Review.rating)).join(
                    ServiceRequest
                ).filter(
                    ServiceRequest.professional_id == professional.id
                ).scalar() or 0.0
                
                # Update professional's average rating
                professional.avg_rating = float(avg_rating)
                updated_count += 1
                
            except Exception as e:
                logger.error(f"Failed to update rating for professional {professional.id}: {e}")
        
        db.session.commit()
        logger.info(f"Updated ratings for {updated_count} professionals")
        
        return f"Updated {updated_count} professional ratings"
        
    except Exception as e:
        logger.error(f"Professional ratings update failed: {e}")
        log_error_with_context(e, {"task": "update_professional_ratings"})
        db.session.rollback()
        raise self.retry(countdown=1800, max_retries=3, exc=e)