# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import Group
from django.conf import settings

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

SERVER_STATUS = (
    (0, u"Normal"),
    (1, u"Down"),
    (2, u"No Connect"),
    (3, u"Error"),
)
SERVICE_TYPES = (
    ('app', u"app"),
    ('job', u"job"),
    ('mysql', u"mysql"),
    ('oracle', u"oracle"),
    ('ta', u"ta"),
    ('codis', u"codis"),
    ('zookeeper', u"zookeeper"),
    ('dubbo', u"dubbo"),
    ('lts', u"lts"),
    ('rocketmq', u"rocketmq"),
    ('elk', u"elk"),
    ('cat', u"cat"),
    ('fastdfs', u"fastdfs"),
    ('nginx', u"nginx"),
)
ZONE_TYPES = (
    ('APP', u"APP"),
    ('DB', u"DB"),
    ('LOG', u"LOG"),
    ('BUSINESS', u"BUSINESS"),
    ('DMZ-WEB', u"DMZ-WEB"),
    ('DMZ-OUT', u"DMZ-OUT"),
)


class IDC(models.Model):
    name = models.CharField(u"IDC编码", max_length=10)
    address = models.CharField(u"地址", max_length=128)

    contact = models.CharField(u"联系人", max_length=32, blank=True, null=True)
    telphone = models.CharField(u"电话", max_length=32, blank=True, null=True)
    qq = models.CharField(u"QQ", max_length=32, blank=True, null=True)
    customer_id = models.CharField(max_length=128, blank=True, null=True)
    description = models.TextField(u"备注", blank=True, null=True)
#    groups = models.ManyToManyField(Group)  # many

    create_time = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"IDC"
        verbose_name_plural = verbose_name


class Host(models.Model):
    idc = models.ForeignKey(IDC)
    name = models.CharField(u"主机名", max_length=30, db_index=True)
    mip = models.GenericIPAddressField(blank=True, null=True, help_text="manager IP", max_length=15)
    bip = models.GenericIPAddressField(blank=True, null=True, help_text="business IP", max_length=15)
    vip = models.GenericIPAddressField(blank=True, null=True, max_length=15)
    status = models.SmallIntegerField(u"状态", choices=SERVER_STATUS, default=0)

    core_num = models.SmallIntegerField(choices=[(i * 2, "%s Cores" % (i * 2)) for i in range(1, 19)], default=2)
    hard_disk = models.IntegerField(blank=True, null=True)
    memory = models.IntegerField(blank=True, null=True)

    system = models.CharField(u"System OS", max_length=32, choices=[(i, i) for i in (u"centOS7.2", u"rh6.5", u"windows")], default="centOS7.2")

    create_time = models.DateField(auto_now=True)
    service_type = models.CharField(max_length=16, choices=SERVICE_TYPES, db_index=True)
    zone_type = models.CharField(max_length=16, choices=ZONE_TYPES, db_index=True)
    description = models.TextField(u"备注", blank=True, null=True)

#    administrator = models.ForeignKey(AUTH_USER_MODEL, verbose_name="Admin")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"Host"
        verbose_name_plural = verbose_name


class MaintainLog(models.Model):
    host = models.ForeignKey(Host)
    maintain_type = models.CharField(max_length=32)
    time = models.DateTimeField()
    operator = models.CharField(max_length=16)
    note = models.TextField()

    def __unicode__(self):
        return '%s maintain-log [%s] %s %s' % (self.host.name, self.time.strftime('%Y-%m-%d %H:%M:%S'),
                                               self.maintain_type)

    class Meta:
        verbose_name = u"维修日志"
        verbose_name_plural = verbose_name


class HostGroup(models.Model):

    name = models.CharField(max_length=32)
    description = models.TextField(blank=True, null=True)
    hosts = models.ManyToManyField(
        Host, verbose_name=u'Hosts', blank=True, related_name='groups')

    class Meta:
        verbose_name = u"Host Group"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class AccessRecord(models.Model):
    date = models.DateField()
    user_count = models.IntegerField()
    view_count = models.IntegerField()

    class Meta:
        verbose_name = u"Access Record"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "%s Access Record" % self.date.strftime('%Y-%m-%d')
