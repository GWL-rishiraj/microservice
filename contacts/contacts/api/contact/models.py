from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

from django.contrib.postgres.fields import (
	ArrayField,
	JSONField,
	)

from django.core.validators import (
	MinLengthValidator,
	RegexValidator,
	)

from .managers import UserManager

FQDN_REGEX = (
    '(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}\.?$)'
)



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

class Service(BaseModel):
	name = models.CharField(verbose_name=_('ServiceName'),
				max_length=200,blank=False,null=False,unique=True
			)
	hosts = ArrayField(models.CharField(max_length=200,blank=False,null=False,
					validators=[
						RegexValidator(regex=FQDN_REGEX),
						]
					),
				validators=[
					MinLengthValidator(1, message='At least one is required'),
					]
			)

class Api(BaseModel):
	name = models.CharField(max_length=200,blank=False,null=False,unique=True)
	url = models.URLField(null=False)
	service = models.ForeignKey('Service',
			on_delete=models.CASCADE,
			related_name='api_service',
			related_query_name='service'
		)

	def __str__(self):
		return self.name

class Consumer(BaseModel):
	username = models.CharField(max_length=200,blank=False,null=False,unique=True)
	key = models.CharField(max_length=200,blank=False,null=False,
			validators=[
				MinLengthValidator(8),
				]
				)
	def __str__(self):
		return self.username

class ConsumerACL(BaseModel):
	consumer = models.ForeignKey(
			'Consumer',
			on_delete=models.CASCADE,
			related_name='acls',
			related_query_name='acl'
		)
	service = models.ForeignKey('Service',
			on_delete=models.CASCADE,
			related_name='consumer_service',
			related_query_name='service'
		)
	api = models.ForeignKey('Api',
			on_delete=models.CASCADE,
			related_name='consumer_api',
			related_query_name='api'
		)
	all_api = models.BooleanField(verbose_name=_('Has All API Permission'),default=False)
	as_permission = models.BooleanField(verbose_name=_('Has ACL Permission'),default=False)

	class Meta:
		unique_together = ('consumer', 'service','api')

	def __str__(self):
		return '{}: {}'.format(self.consumer.name, self.service)

class Permission(BaseModel):
	name = models.CharField(max_length=254, db_index=True,verbose_name=_('Name'))
	api = models.ForeignKey('Api',
			on_delete=models.CASCADE,
			related_name='api_permission',
			related_query_name='api'
		)#PERMISSION_CATEGORY Permission Category
	slug = models.SlugField(unique=True, null=True, blank=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.api + "_" + self.name)
		super(Permission, self).save(*args, **kwargs)

	def __str__(self):
		return str(self.api + "-" + self.name)


class Group(BaseModel):
	name = models.CharField(max_length=254, db_index=True,verbose_name=_('Name'))
	status = models.CharField(max_length=20, verbose_name=_('Group Status'),choices=STATUS_CHOICES, default='active')

	def __str__(self):
		return str(self.name)

class ContactType(BaseModel):
	type_name = models.CharField(max_length=254, db_index=True,verbose_name=_('Type'))

	def __str__(self):
		return str(self.name)

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
	contact_type = models.ForeignKey(ContactType, null=True, blank=True,on_delete=models.SET_NULL,related_name='user_group')
	email = models.EmailField(max_length=255, unique=True, db_index=True)
	#company = models.ForeignKey(Company, null=True, blank=True,on_delete=models.CASCADE,related_name='contact_company')
	group = models.ForeignKey(Group, null=True, blank=True,on_delete=models.SET_NULL,related_name='user_type')
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

class GroupAndPermission(BaseModel):
	group = models.ForeignKey(Group, on_delete=models.CASCADE,
								verbose_name=_('Group'),
								related_name='group_permission')
	permission = models.ForeignKey(Permission, on_delete=models.CASCADE,
									verbose_name=_('Group Permission'),
									related_name='group_permission')
	company = models.PositiveIntegerField()
	has_permission = models.BooleanField(verbose_name=_('Has Permission'),default=False)

	@classmethod
	def truncate(cls):
		with connection.cursor() as cursor:
			cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(cls._meta.db_table))

	class Meta:
		unique_together = ["group", "permission", "company"]