import csv
import os


file = '/home/vignes/Downloads/PCM LIST 310818_modified - PCM Membership 2018 (4).csv'
file = '/home/peugeotclubmalaysia/PCM LIST 310818_modified - PCM Membership 2018 (4).csv'

from pcmappv2.models import Member,Car,Payment,User,Group
Group.objects.get_or_create(name='Member')
Group.objects.get_or_create(name='PCM Admin')
Group.objects.get_or_create(name='Service Center')

with open(file) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        p = Member(member_name=row['member_name'], member_email=row['member_email'],member_since=row['member_since'], member_phone=row['member_phone'],member_on_chat=row['member_on_chat'].capitalize(),member_source=row['member_source'],member_expiry_date=row['member_expiry_date'])
        p.save()
        print(p.id)
        q = Car(member_id=Member.objects.get(pk=p.id),car_reg_no=row['car_reg_no'],car_model=row['car_model'],car_primary_sec=1,car_status=True)
        q.save()
        r = Payment(payment_car_reg_no=Member.objects.get(pk=p.id),payment_date=row['payment_date'],payment_amount=row['payment_amount'],payment_type=row['payment_type'])
        r.save()

from django.contrib.auth.models import User,Group
from pcmapp.models import Member
members = Member.objects.all()
for mem in members:
    r =  User.objects.filter(email=mem.member_email)
    print(mem.id)
    if (r.count() < 1):
        user = User.objects.create_user(mem.member_email,mem.member_email,'asdfgh123')
        user.save()
        g = Group.objects.get(name='Member')
        g.user_set.add(user)
        g.save()
        mem.owner = user
        mem.save()

"""
code for mysqlbackup on python pythonanywhere
mysqldump -u peugeotclubmalay -h peugeotclubmalaysia.mysql.pythonanywhere-services.com 'peugeotclubmalay$pcmapp'  > db-backup_22Feb2020.sql

SELECT m.member_name, m.member_address_state, m.member_expiry_date,c.car_reg_no FROM pcmappv2_member m, pcmappv2_car c where c.member_id_id=m.id and m.member_status=1 and m.member_address_state in ('PG','KH')

"""

"""
get collection by year and month
Payment.objects.values('payment_date__year','payment_date__month').annotate(sum = Sum('payment_amount')).order_by('payment_date__year')

"""

'''
To dump the data. Run in Pythonanywhere console 

import csv 
from pcmappv2.models import *

fields = [f.name for f in Member._meta.fields]

with open('dumpdata.csv', mode='w') as file:
    filewrite = csv.writer(file , delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    filewrite.writerow(fields)
    for row in Member.objects.values(*fields):
        filewrite.writerow([row[field] for field in fields])



'''
#member_name,member_email,member_phone,member_since,member_birthdate,member_address_state,member_address_postcode,member_on_chat,member_source,member_expiry_date
#car_reg_no,car_model,car_engine_chasis,car_primary_sec,car_status
#payment_date,payment_amount,payment_type
