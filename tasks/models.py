from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Employee(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)

    def __str__(self):
        return self.name

    ## employ r moddha automatic akta task_set ata hole reverse query ar janno


class Task(models.Model):

    STATUS_CHOISES=[
        ('PENDING','Pending'),
        ('IN_PROGRESS','In Progress'),
        ('COMPLETED','Completed')
    ]

    ### many to one relationship
    project=models.ForeignKey("Project",
                              on_delete=models.CASCADE,
                              default=1)
    ## ata korar por automatically akta set tori hoi tasktatiles_setS
    ## many to many


    # assigned_to=models.ManyToManyField(Employee,related_name="task")

    assigned_to=models.ManyToManyField(User,related_name="task")


    title=models.CharField( max_length=150)
    description=models.TextField()
    due_data=models.DateField()
    status=models.CharField(max_length=20,choices=STATUS_CHOISES,default="PENDING")
    is_complete=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    #take tasktatils one to many relation a details name akta copy automatically hoya jabe


#one to one 
#many to one
# many to many

###### Relationship always child table a built korte hobe
class TaskDetail(models.Model):

    high='H'
    medium='M'
    low='L'

    PRIORITY_OPTION=(
        (high,'High'),
        (medium,'Medium'),
        (low,'Low')
    )

    ### one to one relationship
    # std_id=models.CharField(max_length=200,primary_key=True)  ata korle auto primary key tar poriborte ata primary key hobe

    asset_image=models.ImageField(upload_to='task_asset',blank=True,null=True)
    task=models.OneToOneField(Task,on_delete=models.CASCADE,related_name="datils")
   
    # assign_to=models.TextField(max_length=100)
    priority=models.CharField(max_length=1,choices=PRIORITY_OPTION, default=low)
    notes=models.TextField(blank=True,null=True)

    def __str__(self):
        return f"Details for Task {self.task.title}"


    # Task.object.get(id=2)

    #equvalent

    #select *
    #from Task
    #where id=2

    # this is call ORM = Object Relational Model

class Project(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    start_data=models.DateField()
    def __str__(self):
        return  self.name




   

