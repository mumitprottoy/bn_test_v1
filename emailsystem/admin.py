from django.contrib import admin
from django import forms
from .models import EmailCred, EmailConfig

class EmailCredCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, help_text="Enter raw password here.")

    class Meta:
        model = EmailCred
        fields = ['email', 'password']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance


@admin.register(EmailCred)
class EmailCredAdmin(admin.ModelAdmin):
    list_display = ('key', 'email')

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['form'] = EmailCredCreationForm
        return super().get_form(request, obj, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['key', 'email']
        return []

    def get_fields(self, request, obj=None):
        if obj is None:
            return ['key', 'email', 'password']
        else:
            return ['key', 'email']


@admin.register(EmailConfig)
class EmailConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'backend', 'host', 'port', 'use_tls')
    readonly_fields = ('name', 'backend', 'host', 'port', 'use_tls')
    fields = ('name', 'backend', 'host', 'port', 'use_tls')
