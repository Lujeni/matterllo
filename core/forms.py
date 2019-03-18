# -*- coding: utf-8 -*-
from crispy_forms.bootstrap import FormActions, Field
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, HTML
from django import forms

from core.models import Bridge, Webhook


class BridgeCreateForm(forms.ModelForm):
    events = forms.MultipleChoiceField(
        choices=Bridge.EVENT_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        super(BridgeCreateForm, self).__init__(*args, **kwargs)
        helper = self.helper = FormHelper()

        layout = helper.layout = Layout()
        layout.append(Field('events', css_class='board-event'))
        layout.append(FormActions(HTML('<button class="btn btn-info" type="button" onclick="document.querySelectorAll(\'.board-event\').forEach(x => x.checked = true);">Check all</button>')))
        layout.append(FormActions(HTML('<button class="btn btn-info" type="button" onclick="document.querySelectorAll(\'.board-event\').forEach(x => x.checked = false);">Uncheck all</button>')))
        layout.append(FormActions(Submit('save', 'Save')))

        helper.form_show_labels = False
        helper.form_class = 'form-horizontal'
        helper.field_class = 'col-lg-8'
        helper.help_text_inline = True

    class Meta:
        model = Bridge
        fields = ['events']
        help_texts = {
            'events': 'The generated key from <a href="https://docs.mattermost.com/developer/webhooks-incoming.html#setting-up-existing-integrations">Mattermost webhook</a>.',
        }


class WebhookCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(WebhookCreateForm, self).__init__(*args, **kwargs)
        helper = self.helper = FormHelper()

        layout = helper.layout = Layout()
        layout.append(Field('name', placeholder='webhook for town-square'))
        layout.append(Field('incoming_webhook_url', placeholder='https://mattermost.gitlab.com/hooks/b5g6pyoqsjy88fa6kzn7xi1rzy'))
        layout.append(FormActions(Submit('save', 'Next')))

        helper.form_show_labels = False
        helper.form_class = 'form-horizontal'
        helper.field_class = 'col-lg-8'
        helper.help_text_inline = True

    class Meta:
        model = Webhook
        fields = ['name', 'incoming_webhook_url']
        help_texts = {
            'name': 'The description.',
            'incoming_webhook_url': 'The generated url from <a href="https://docs.mattermost.com/developer/webhooks-incoming.html#setting-up-existing-integrations">Mattermost webhook</a>.',
        }
