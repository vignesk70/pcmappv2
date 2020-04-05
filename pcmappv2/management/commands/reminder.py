from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date,timedelta
from pcmappv2.views import *
from pcmappv2.models import Member

class Command(BaseCommand):
    help = 'Sends out reminder to members'

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)
        members=Member.objects.filter(member_expiry_date__gte=date.today())
        for member in members:
            self.stdout.write(member.member_name+" "+ str(member.member_expiry_date))
            expiringdate = date.today()+timedelta(days=+7)
            date2 = member.member_expiry_date
            if (date2==expiringdate):
                self.stdout.write("Expiring on "+str(date2))
                email_renewal_notice(member)
            if (date.today()==member.member_expiry_date):
                self.stdout.write("Expiring today")
                email_renewal_notice(member)
            
            
            