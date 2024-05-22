from django.contrib.admin.widgets import AdminDateWidget
from django.utils.html import format_html
from datetime import datetime, timedelta

class AdminDateWidgetWithTomorrowButton(AdminDateWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = super().render(name, value, attrs, renderer)
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        js_code = f"document.getElementsByName('{name}')[0].value = '{tomorrow}';"
        button = format_html(f'<p style="margin-left: 7px; margin-top: 7px;"> | <p><button type="button" style="appearance: button; backface-visibility: hidden; background-color: #405cf5; border-radius: 6px; border-width: 0; box-shadow: rgba(50, 50, 93, .1) 0 0 0 1px inset,rgba(50, 50, 93, .1) 0 2px 5px 0,rgba(0, 0, 0, .07) 0 1px 1px 0; box-sizing: border-box; color: #fff; cursor: pointer; font-family: -apple-system,system-ui,\'Segoe UI\',Roboto,\'Helvetica Neue\',Ubuntu,sans-serif; font-size: 100%; height: 44px; line-height: 1.15; margin: 12px 0 0; outline: none; overflow: hidden; padding: 0 25px; position: relative; text-align: center; text-transform: none; transform: translateZ(0); transition: all .2s,box-shadow .08s ease-in; user-select: none; -webkit-user-select: none; touch-action: manipulation; width: auto; margin-top: -7px;" onclick="{js_code}">Tomorrow</button>')
        return format_html("{} {}", output, button)
    
