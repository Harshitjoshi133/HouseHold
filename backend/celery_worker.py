from celery import Celery
from tasks import send_daily_reminders, send_monthly_report

app = create_app()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=18, minute=0),
        send_daily_reminders.s(),
        name='send daily reminders'
    )
    
    sender.add_periodic_task(
        crontab(day_of_month=1, hour=7, minute=0),
        send_monthly_report.s(),
        name='send monthly reports'
    )
