from django import forms
from tasks.models import Task

class TaskForm(forms.Form):
    title=forms.CharField(max_length=100 ,label="task title")
    description=forms.CharField(widget=forms.Textarea,label="task description")
    due_data=forms.DateField(widget=forms.SelectDateWidget, label="Due Date")
    assigned_to=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=[],label="Assign_To")

    def __init__(self,*args,**kwargs):

        employees=kwargs.pop("employees",[])
        super().__init__(*args,*kwargs)
        self.fields['assigned_to'].choices=[(emp.id , emp.name ) for emp in employees]




class StyleFormMixin:
    defualt_class="display:block; width:100%; border:1px solid #ccc; padding:8px; border-radius:6px; margin-top:5px;"


    def apply_style_widge(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget,forms.TextInput):
                field.widget.attrs.update({
                    'class': 'form-control',
                    'style':self.defualt_class,
                    'placeholder': f"Enter {field.label.lower()}",
                })

            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class': 'form-control',
                    'style':self.defualt_class,
                    'placeholder': f"Enter {field.label.lower()}",
                    

                })

            elif isinstance(field.widget,forms.SelectDateWidget):
                field.widget.attrs.update({
                     'style': 'display:inline; margin-top:5px;border:1px solid #ccc;'

                })
            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'style': 'display:inline; margin-top:5px;border:1px solid #ccc'

                })




## Django model form:
class TaskModelForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model=Task
        fields=['title','description','due_data','assigned_to']
        widgets={
        'due_data':forms.SelectDateWidget,
        'assigned_to':forms.CheckboxSelectMultiple
        }

        # exclude=['project','is_complete','created_at','updated_at']

        '''manual widget'''
        # widgets={
            
        #    'title': forms.TextInput(attrs={
        #         'class': 'form-control',
        #         'placeholder': 'Enter task title',
        #         'style': 'display:block; width:100%; border:1px solid #ccc; padding:8px; border-radius:6px; margin-top:5px;'
        #     }),

        #     'description': forms.Textarea(attrs={
        #         'class': 'form-control',
        #         'rows':4,
        #         'style': 'display:block; width:100%; border:1px solid #ccc; padding:8px; border-radius:6px; margin-top:5px;'
        #     }),

        #     'due_data': forms.SelectDateWidget(attrs={
        #         'style': 'display:line; margin-top:5px;border:1px solid #ccc'
        #     }),

        #     'assigned_to': forms.CheckboxSelectMultiple(attrs={
        #          'style': 'display:line; margin-top:5px;border:1px solid #ccc'
        #     }),
        # }
    '''Using mixin widget'''
    def __init__(self,*arg,**kwarg):
        super().__init__(*arg,**kwarg)
        self.apply_style_widge()
    
