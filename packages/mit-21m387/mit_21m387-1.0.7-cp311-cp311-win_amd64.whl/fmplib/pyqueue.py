import requests
from ipywidgets import widgets
from IPython.display import display
import os
import json


HOST = "http://eranegozy.pythonanywhere.com"
# HOST = "http://localhost:5000"


def connect_to_queue(button_type='help', host=HOST):
    home = os.path.expanduser("~")
    config_file = os.path.join(home, ".pyqueue")

    def save_config(name, kerberos):
        with open(config_file, 'w') as file:
            file.write(name + ',' + kerberos)

    def load_config():
        # read data from config file to find previously saved name and kerberos
        name = None
        kerberos = None
        contents = None
        try:
            with open(config_file, 'r') as file:
                contents = file.read()
                res = contents.split(',')
                name, kerberos = res[0].strip(), res[1].strip()
        except:
            pass
        return name, kerberos

    if button_type == 'help':
        button_msg = 'Request Help'
        param_type = 'Help'
    else:
        button_msg = 'Request Checkoff'
        param_type = 'Checkoff'

    name, kerberos = load_config()

    name_field = widgets.Text(description='Name', placeholder='Ben Bitdiddle', value=name)
    kerberos_field = widgets.Text(description='Kerberos', placeholder='benbit', value=kerberos)
    queue_button = widgets.Button(description=button_msg)
    cancel_button = widgets.Button(description="Cancel", layout=widgets.Layout(width='65px'))
    status_text = widgets.Label(value="")

    widget_list = [name_field, kerberos_field, queue_button, cancel_button, status_text]
    queue_box = widgets.HBox(widget_list)
    display(queue_box)

    def get_field_values():
        try:
            name = name_field.value.strip().replace(',', '_')
            kerberos = kerberos_field.value.strip().replace(',', '_')

            if len(name) > 0 and len(kerberos) > 0:
                return name, kerberos
            else:
                raise ValueError
        except:
            print("Please enter your first and last name, and a kerberos")
            return None

    def make_help_request(a):
        fields = get_field_values()
        if fields:
            params = {"name": fields[0], "kerberos": fields[1], "type": param_type}
            r = requests.post(host+'/queue', data=params)
            save_config(fields[0], fields[1])
            response = json.loads(r.text)
            status_text.value = response['message']

    def cancel_request(a):
        fields = get_field_values()
        if fields:
            params = {"kerberos": fields[1], "remove": 'true'}
            r = requests.post(host+'/queue', data=params)
            save_config(fields[0], fields[1])
            response = json.loads(r.text)
            status_text.value = response['message']

    queue_button.on_click(make_help_request)
    cancel_button.on_click(cancel_request)
