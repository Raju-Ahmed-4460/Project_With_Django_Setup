from django.db.models.signals import pre_save,post_save,m2m_changed,post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from tasks.models import Task,TaskDetail,Project



@receiver(m2m_changed, sender=Task.assigned_to.through)
def notify_Employee_task_creation(sender, instance, action, **kwargs):
    
    if action == "post_add":   

        assign_email = [emp.email for emp in instance.assigned_to.all()]

        send_mail(
            "New Task assign",
            f"You have been assigned to this Task: {instance.title}",
            "rajur20m@gmail.com",
            assign_email,
        )

