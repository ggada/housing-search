#!/usr/bin/python
import json,os,requests,re,time,sys,smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
# import ipdb; ipdb.set_trace()

# TODO
# cron it

with open( os.path.join(sys.path[0], 'lastrun'),'rw+') as f:
    last_run = f.read().replace('\n','')
    f.seek(0)
    f.write(str(int(time.time())))
    f.truncate

data = requests.get('https://graph.facebook.com/v2.6/385662361445807/feed?since=' + last_run + '&limit=100&' + 'access_token=' + os.environ.get('FB_API') )

data_json = json.loads(data.text)

ignore_list = [
    'sublet',
    'subleas',
    'ladies',
    'girl',
    'female',
    'bothell',
    'tacoma'
]
             
for x in reversed(range(len(data_json['data']))):
    if re.search('|'.join(ignore_list),data_json['data'][x]['message'],re.IGNORECASE):
        data_json['data'].pop(x)

tmpl = Template('''
                <table style="border-collapse: collapse;">
   {% for i in range(0,data_json['data']|length) %}
                <tr><td style="border: 1px solid #999; padding: 0.5rem; text-align: left;"><a href="https://facebook.com/{{ data_json['data'][i]['id'] }}" target="_blank">{{ data_json['data'][i]['updated_time'] }}</a></td>
                <td style="border: 1px solid #999; padding: 0.5rem; text-align: left;"><a href="fb://story?id={{ data_json['data'][i]['id'] }}">FBL</a></td>
                <td style="border: 1px solid #999; padding: 0.5rem; text-align: left;"><a href="https://m.facebook.com/groups/{{ data_json['data'][i]['id'].split('_')[0] }}?view=permalink&id={{ data_json['data'][i]['id'].split('_')[1] }}">mob</a></td>
                <td style="border: 1px solid #999; padding: 0.5rem; text-align: left;">{{ data_json['data'][i]['message'] }}</td></tr>
   {% endfor %}
</table>
''')

me = os.environ.get('FROM_EMAIL')
you = os.environ.get('TO_EMAIL')
password = os.environ.get('FROM_EMAIL_PASS')

msg = MIMEMultipart('alternative')
msg['Subject'] = "Housing " + time.strftime('%Y-%m-%d')
msg['From'] = me
msg['To'] = you
msg.attach(MIMEText(tmpl.render(data_json = data_json), 'html',_charset="UTF-8"))
mail = smtplib.SMTP('smtp.gmail.com', 587)
mail.ehlo()
mail.starttls()
mail.login(me, password)
mail.sendmail(me, you, msg.as_string())
mail.quit()
