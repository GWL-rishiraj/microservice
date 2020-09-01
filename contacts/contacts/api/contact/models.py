from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


ROLE_CHOICES = (
	('admin', _("Admin")),
	('company_owner', _("Company Owner")),
	('client', _("Client")),
	('client_contact', _("Client Contact")),
	('project_manage', _("Project Manager"))
	)

STATUS_CHOICES = (
	('active', _("Active")),
	('inactive', _("Inactive")),
	('deleted', _("Deleted"))
	)

class BaseModel(models.Model):
	"""Base model for other models
	Attributes
	----------
	created_at : Date Field
		Automatic fill the current date
	modified_at: Date Field
		Automatic fill the current date
	"""
	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True

# class Company(BaseModel):
# 	name = models.CharField(max_length=254, unique=True, db_index=True,verbose_name=_('Company Name'))
# 	company_address = models.TextField(verbose_name=_('Company Address'),null=True, blank=True)
# 	city = models.CharField(verbose_name=_('Company City'), null=True,blank=True, max_length=255)
# 	zip_code = models.CharField(verbose_name=_('Company Zip Code'),null=True, blank=True, max_length=255)
# 	state = models.CharField(verbose_name=_('Company State'), null=True,blank=True, max_length=255)
# 	country = models.CharField(verbose_name=_('Company Country'),null=True, blank=True, max_length=255)
# 	owner_email = models.EmailField(verbose_name=_('Owner E-mail Address'),null=True, blank=True,max_length=254)
# 	owner_name = models.CharField(max_length=254, verbose_name=_('Owner Name'))

# 	def __str__(self):
# 		return str(self.name)

class Contact(AbstractUser,BaseModel):
	"""This model have all user in app
	Attributes
	----------
	email : Email Field, required
		This is the username of the user
	role : Choice Field
		choices are adminr, company_owner, client etc
	status : Chooice Field
		choice are 1)Active 2)Inactive 3)Deleted
	"""

	email = models.EmailField(max_length=255, unique=True, db_index=True)
	#company = models.ForeignKey(Company, null=True, blank=True,on_delete=models.CASCADE,related_name='contact_company')
	company = models.PositiveIntegerField()
	role = models.CharField(max_length=40, verbose_name=_('User Type'),choices=ROLE_CHOICES)
	status = models.CharField(max_length=40, verbose_name=_('STATUS_CHOICES'),choices=STATUS_CHOICES, default='inactive')

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	objects = UserManager()
	def save(self, *args, **kwargs):
		self.username = self.email
		super(Contact, self).save(*args, **kwargs)

	def __str__(self):
		return str(self.email)