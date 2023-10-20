import logging

from alerta.plugins import PluginBase
#from alerta.models import Alert

LOG = logging.getLogger('alerta.plugins.enhance')

RUNBOOK_URL = 'https://kb.xtools.tv/display/XWIKI'   # example only

class EnhanceAlert(PluginBase):

    def pre_receive(self, alert):

        LOG.info('Enhancing alert...')

        # Set "isOutOfHours" flag for later use by notification plugins
        dayOfWeek = alert.create_time.strftime('%a')
        hourOfDay = alert.create_time.hour
        if dayOfWeek in ['Sat', 'Sun'] or 8 > hourOfDay > 18:
            alert.attributes['isOutOfHours'] = True
        else:
            alert.attributes['isOutOfHours'] = False


        sub = 'team='
        res = [i for i in alert.tags if sub in i]
        s = res.replace('team=','')
        alert.attribures['Team'] = s
        
        # Add link to Run Book based on event name
        alert.attributes['runBookUrl'] = '{}/{}'.format(
            RUNBOOK_URL, alert.event.replace(' ', '-'))

        return alert

    def post_receive(self, alert):
        return

    def status_change(self, alert, status, text):
        return
