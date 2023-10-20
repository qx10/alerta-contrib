import logging

from alerta.plugins import PluginBase

LOG = logging.getLogger('alerta.plugins.enhance')

RUNBOOK_URL = 'https://kb.xtools.tv/display/XWIKI'   # example only

class EnhanceAlert(PluginBase):
    def find_tag(self, tags, tag_name):
        tag = tag_name.lower() + '='
        for i in tags:
             if i.lower().startswith(tag):
                 return i.split('=')[1]
        return None

    def pre_receive(self, alert):

        LOG.info('Enhancing alert...')

        # Set "isOutOfHours" flag for later use by notification plugins
        dayOfWeek = alert.create_time.strftime('%a')
        hourOfDay = alert.create_time.hour
        if dayOfWeek in ['Sat', 'Sun'] or 8 > hourOfDay > 18:
            alert.attributes['isOutOfHours'] = True
        else:
            alert.attributes['isOutOfHours'] = False


        #sub = 'team='
        #res = [i for i in alert.tags if sub in i]
        #s = res.replace('team=','')
        team = self.find_tag(alert.tags, 'team')
        if team is not None:
            alert.attributes['Team'] = team
        
        # Add link to Run Book based on event name
        alert.attributes['runBookUrl'] = '{}/{}'.format(
            RUNBOOK_URL, alert.event.replace(' ', '-'))

        return alert

    def post_receive(self, alert):
        return

    def status_change(self, alert, status, text):
        return
