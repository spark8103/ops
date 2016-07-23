# -*- coding: utf-8 -*-
from django.db import models

PROJECT_NAME = (
    ('acc', u"eif-acc-web"),
    ('aci', u"eif-accing-web"),
    ('cas', u"eif-cashier-web"),
    ('cms', u"eif-cms"),
    ('contract', u"eif-contract-web"),
    ('cweb', u"eif-customer-website"),
    ('fds', u"eif-fds-web"),
    ('fdsb', u"eif-fds-bridge-web"),
    ('fdsjob', u"eif-fds-job"),
    ('fis', u"eif-fis-web"),
    ('fisjob', u"eif-fis-job"),
    ('ftc', u"eif-ftc-web"),
    ('ftcjob', u"eif-ftc-job"),
    ('gotong', u"eif-gotong-web"),
    ('mkt', u"eif-market-web"),
    ('mktweb', u"eif-market-website"),
    ('mbr', u"eif-member-web"),
    ('mob', u"eif-mobile-website"),
    ('mtp', u"eif-mtp-web"),
    ('ofc', u"eif-ofc-web"),
    ('omc', u"eif-omc-web"),
    ('pc', u"eif-paycore-web"),
    ('pcf', u"eif-paycore-frontedge-web"),
    ('pcjob', u"eif-paycore-job"),
    ('risk', u"eif-risk-web"),
    ('setting', u"eif-setting-web"),
    ('transcore', u"eif-transcore-web"),
    ('vat', u"eif-verify-accounting-web"),
)


class Deploy(models.Model):
    name = models.CharField(u"项目名称", max_length=32, choices=PROJECT_NAME)
    deploy_time = models.DateTimeField(u"发布时间")
    version = models.CharField(u"git version", max_length=50)
    description = models.TextField(u"desc", blank=True, null=True)
    db = models.TextField(blank=True, default="否")
    disconf = models.TextField(blank=True, default="否")
    lts = models.TextField(blank=True, default="否")
    mq = models.TextField(blank=True, default="否")

    create_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"上线发布"
        verbose_name_plural = verbose_name
