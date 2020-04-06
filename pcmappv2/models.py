from django.db import models
from datetime import date
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User,Group

# Create your models here.

class Member(models.Model):
    STATE_CHOICES = (
        ('JH','Johor'),
        ('KH','Kedah'),
        ('KN','Kelantan'),
        ('KL','Kuala Lumpur'),
        ('LA','Labuan'),
        ('ME','Melaka'),
        ('NS','Negeri Sembilan'),
        ('PH','Pahang'),
        ('PK','Perak'),
        ('PL','Perlis'),
        ('PG','Pulau Pinang'),
        ('PJ','Putrajaya'),
        ('SA','Sabah'),
        ('SK','Sarawak'),
        ('SL','Selangor'),
        ('TE','Terengganu'),
    )
    SOURCE_CHOICES = (
        ('FB','Facebook'),
        ('TW','Twitter'),
        ('SC','Service Center'),
        ('IN','Instagram'),
        ('RE','Referral'),
        ('WO','Word of Mouth'),
        ('OT','Other'),
        )

    member_name = models.CharField(max_length=200, verbose_name='Full Name')
    member_email = models.EmailField(max_length=200, verbose_name='Email Address', unique=True)
    member_phone = models.CharField(max_length=20,verbose_name='Mobile Number')
    member_since = models.DateField(blank=True, null=True)
    member_birthdate = models.DateField(blank=True, null=True, verbose_name='Your Birthdate')
    member_address_state = models.CharField(max_length=2,choices=STATE_CHOICES,blank=True,null=True, verbose_name='Current Location (State)')
    member_address_postcode = models.CharField(max_length=5,blank=True,null=True, verbose_name = 'Postcode')
    member_on_chat = models.BooleanField(default=True,verbose_name = 'Would you like to be added to our WhatsApp Group?' )
    member_source = models.CharField(max_length=2,choices = SOURCE_CHOICES,blank=True,null=True,verbose_name = 'Where did you hear about us?')
    member_expiry_date = models.DateField(blank=True,null=True)
    member_pdpa_accepted = models.BooleanField(default=False,blank=False,verbose_name='By selecting "Yes" you agree to the PCM PDPA policy.')
    member_status =  models.BooleanField(default=True,verbose_name='Membership Status')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["member_name"]

    def __str__(self):
        return self.member_name

    def save(self, *args, **kwargs):
        for field_name in ['member_name']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.upper())
        r =  User.objects.filter(email=self.member_email)
        if (r.count() < 1):
            user = User.objects.create_user(self.member_email,self.member_email,'asdfgh123')
            firstname = self.member_name[:25] + ( self.member_name[25:] and "...")
            user.first_name = firstname
            user.save()
            g = Group.objects.get(name='Member')
            g.user_set.add(user)
            g.save()
            self.owner = user
        super(Member, self).save(*args, **kwargs)

    @property
    def is_expired(self):
        if self.member_expiry_date:
            if self.member_expiry_date < date.today():
                return True
            return False

    @property
    def is_member_expiring_in_month(self):
        if self.member_expiry_date.month == date.today().month and self.member_expiry_date.year==date.today().year and self.member_status==True:
            return True
        else:
            return False

    @property
    def is_expiring_in_month(self):
        #if Payment.objects.filter(payment_date__lte=self.member_expiry_date):
        if self.member_expiry_date < date.today() and self.member_status==True:
            x =  Payment.objects.filter(payment_car_reg_no=self.pk).latest('payment_date')
            if x.payment_date.year == self.member_expiry_date.year:
                return False
            return True
        else:
            return False
    #self.get_queryset().filter(member_expiry_date__lte = date.today())

    def get_absolute_url(self):
        return reverse('member-detail',args=[str(self.id)] )


"""
Function to build
1. create user when saving and link to member id
2. update expiry date based on payment date
3. display expiring records (within one month?)

"""
class Car(models.Model):
    PRIMARY_SEC_CHOICES = (
        (1,'Primary'),
        (2,'Secondary'),
        )
    CAR_MODEL = (
        ('2008','2008'),
        ('206','206'),
        ('206 CC','206 CC'),
        ('207 Sedan','207 Sedan'),
        ('207 CC','207 CC'),
        ('208','208'),
        ('208 GTi','208 GTi'),
        ('3008','3008'),
        ('305','305'),
        ('306','306'),
        ('307','307'),
        ('307 SW','307 SW'),
        ('308','308'),
        ('308 CC','308 CC'),
        ('308 GT','308 GT'),
        ('405','405'),
        ('406','406'),
        ('407','407'),
        ('407 SW','407 SW'),
        ('408','408'),
        ('5008','5008'),
        ('504','504'),
        ('505','505'),
        ('508','508'),
        ('508 GT','508 GT'),
        ('508 SW','508 SW'),
        ('607','607'),
        ('807','807'),
        ('Partner','Partner'),
        ('RCZ','RCZ'),
        ('Traveller','Traveller'),
    )
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    car_reg_no = models.CharField(max_length=20, verbose_name='Registration Number')
    car_model = models.CharField(max_length=20, choices=CAR_MODEL,verbose_name='Model')
    #car_engine_chasis = models.CharField(max_length=20, verbose_name='Engine Chassis',blank=True,null=True)
    car_primary_sec = models.SmallIntegerField(blank=True,null=True,choices=PRIMARY_SEC_CHOICES, verbose_name='Primary/Secondary Car')
    car_status = models.BooleanField(default=True,verbose_name='Status')
    def __str__(self):
        return self.car_reg_no
    #def get_absolute_url(self):
    #    return reverse('pcmapp:index')
    def save(self, *args, **kwargs):
        for field_name in ['car_reg_no',]:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.upper())
        for field_name in ['car_reg_no']:
            val =  getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.replace(" ",""))


        super(Car, self).save(*args, **kwargs)
"""
define secondary car insert
"""
class Payment(models.Model):
    PAYMENT_CHOICES= (
        ('1','New'),
        ('2','Renewal'),
        ('3','Supplementary'),
        )
    payment_car_reg_no = models.ForeignKey(Member,on_delete=models.CASCADE)
    payment_date = models.DateField(blank=True,verbose_name='Payment Date')
    payment_amount = models.IntegerField(verbose_name='Payment Amount')
    payment_type = models.CharField(max_length=1,choices = PAYMENT_CHOICES,verbose_name='Payment For')
    payment_receipt_image = models.FileField(upload_to='uploadreceipt',null=False,blank=False,verbose_name='Proof of Payment')
    payment_updated_date = models.DateField(verbose_name="Admin updated date",auto_now=False, auto_now_add=False,blank=True,null=True)
    payment_updated_by = models.ForeignKey(User, verbose_name="Admin User", on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.payment_car_reg_no.member_name

#payment needs to consider the renewal date.
    def save(self, *args, **kwargs):
        if (self._state.adding is True):
            pass
        else:
            mem = Member.objects.get(pk=self.payment_car_reg_no.id)
            #new registration
            if (mem.member_since == None and self.payment_type=='1'):
                mem.member_since=self.payment_date
                mem.member_expiry_date = self.payment_date.replace(self.payment_date.year+2)
                mem.save()
            #update existing member - added logic to avoid saved records to update member expiry.
            if(mem.member_expiry_date != None and self.payment_type=='2'):
                mem.member_expiry_date = mem.member_expiry_date.replace(mem.member_expiry_date.year+2)
                mem.save()
                #self.payment_car_reg_no.member_expiry_date = self.payment_date.replace(self.payment_date.year+2)
        super().save(*args, **kwargs)

class Activity(models.Model):
    activity_title = models.CharField(max_length=50,verbose_name='Event title')
    activity_date = models.DateField(verbose_name='Event date')
    activity_venue = models.CharField(max_length=100,verbose_name='Event location')
    activity_description = models.CharField(max_length=500,verbose_name='Event description')
    activity_link_fb = models.URLField(verbose_name='FB URL', blank=True,null=True)
    activity_link_ig = models.URLField(verbose_name='IG URL', blank=True,null=True)
    activity_create_date = models.DateTimeField()
    activity_image = models.FileField(upload_to='static/images',verbose_name='Upload image')

    class Meta:
        verbose_name_plural='Activities'
        ordering = ["-activity_date"]

    def __str__(self):
        return self.activity_title


"""
Highlight field message - all fields required update the expiry date when payment is made.
"""
