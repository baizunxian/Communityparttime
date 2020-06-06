from django.db import models

# Create your models here.


class Base(models.Model):
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        abstract = True
        verbose_name = "公共字段表"
        db_table = 'Base'


class PartTimeUser(Base):
    class Meta:
        db_table = 'PartTimeUser'

    Pid = models.AutoField(verbose_name='id', primary_key=True, unique=True)
    PUsername = models.CharField(verbose_name='用户名称', max_length=255)
    PPassword = models.CharField(verbose_name='用户密码', max_length=255)
    PSex = models.CharField(verbose_name='用户性别', max_length=255)
    PPhoneNumber = models.CharField(verbose_name='手机号码', max_length=255)
    PIDCard = models.CharField(verbose_name='身份证号', max_length=255)
    PLocation = models.CharField(verbose_name='住址', max_length=255)


class AdminUser(Base):
    class Meta:
        db_table = 'AdminUser'

    Aid = models.AutoField(verbose_name='id', primary_key=True, unique=True)
    Aname = models.CharField(verbose_name='管理员账号', max_length=255)
    Apassword = models.CharField(verbose_name='管理员密码', max_length=255)


class Jobs(Base):
    class Meta:
        db_table = 'Jobs'

    Jid = models.AutoField(verbose_name='id', primary_key=True, unique=True)
    Jobname = models.CharField(verbose_name='岗位', max_length=255)
    Jobloc = models.CharField(verbose_name='详细工作地址', max_length=255)
    JobSalary = models.CharField(verbose_name='薪资', max_length=255)
    JobContact = models.CharField(verbose_name='联系人', max_length=255)
    Jobphonenumber = models.CharField(verbose_name='联系人电话', max_length=255)
    JobHired = models.CharField(verbose_name='订单是否有效', max_length=255, default='0')
    JobDeatails = models.TextField(verbose_name='工作内容', max_length=500)
    Jobtime = models.DateTimeField(verbose_name='发布时间', max_length=255, auto_now=True)
    Province_and_city = models.CharField(verbose_name='省市区', max_length=255, null=True)
    Puser = models.ForeignKey('PartTimeUser', models.CASCADE)

    @classmethod
    def get_jobs(cls, Province_and_city=None, Jobname = None, JobHired='0'):
        q = dict()
        if Province_and_city:
            q['Province_and_city__contains'] = Province_and_city
        if Jobname:
            q['Jobname__contains'] = Jobname
        q['JobHired'] = JobHired
        return cls.objects.filter(**q)


class JobRelation(Base):
    class Meta:
        db_table = 'JobRelation'

    JobPublisher = models.IntegerField(verbose_name='发布人')
    JobApply = models.IntegerField(verbose_name='接单人')


class Collection(Base):
    class Meta:
        db_table = 'Collection'

    Fid = models.AutoField(verbose_name='id', primary_key=True, unique=True)
    FJobFav = models.ForeignKey('PartTimeUser', models.CASCADE)
    Jid = models.ForeignKey('Jobs', models.CASCADE)
