from django.db import models
from django.utils import timezone
from datetime import datetime
from django.db.models import Max


class Project(models.Model):
    name = models.CharField(max_length=100)
    status = models.BooleanField('Project completed', default=False)
    start_date = models.DateTimeField('Start date', auto_now=True)
    finish_date = models.DateTimeField('Finish date', blank=True, null=True)
    sloc = models.PositiveIntegerField('Iteration count', default=0)

    duration = models.PositiveIntegerField(default=0)
    injectrate = models.FloatField(default=0)
    removerate = models.FloatField(default=0)

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, name):
        project = cls(name=name)
        project.save()
        phase = project.addPhases(project.id)
        return project

    @staticmethod
    def addPhases(project_id):
        phase1 = Phase.create("Inception", project_id)
        phase2 = Phase.create("Elaboration", project_id)
        phase3 = Phase.create("Construction", project_id)
        phase4 = Phase.create("Transition", project_id)
        return phase1

    def countDefect(self):
        d = 0
        phases = Phase.objects.filter(project_id=self.id)
        for i in phases:
            d += i.countDefect()
        return d

    def countGoodFix(self):
        d = 0
        phases = Phase.objects.filter(project_id=self.id)
        for i in phases:
            d += i.countGoodFix()
        return d

    def countDev(self):
        d = 0
        phases = Phase.objects.filter(project_id=self.id)

        for p in phases:
            iterations = Iteration.objects.filter(phase_id=p.id)

            for i in iterations:
                d += Developer.objects.filter(iteration_id=i.id).count()

        return d

    def countDuration(self):
        iterations = Iteration.objects.filter(phase_id=self.id)

        d = self.countDev()

        if self.finish_date and d > 0:
            c = (self.finish_date - self.start_date).days * 24
            self.duration = round(c / d, 5)

        self.save()
        return self.duration

    def countInjectRate(self):
        d = self.countDuration()
        c = self.countDefect()
        if c > 0:
            self.injectrate = round(c / d, 5)
        self.save()
        return self.injectrate

    def countRemoveRate(self):
        d = self.countDuration()
        c = self.countGoodFix()
        if c > 0:
            self.removerate = round(c / d, 5)
        self.save()
        return self.removerate


class Phase(models.Model):
    name = models.CharField(max_length=100)
    sloc = models.PositiveIntegerField('Phase SLOC', default=0)
    sloc_ppm = models.PositiveIntegerField('SLOC per person-month by phase',
                                           default=0)
    coun = models.PositiveIntegerField('Iteration count', default=0)
    status = models.BooleanField('Project completed', default=False)
    project = models.ForeignKey(Project)
    start_date = models.DateTimeField('Start date', auto_now=False)
    finish_date = models.DateTimeField('Finish date', blank=True, null=True)
    effort = models.PositiveIntegerField('Phase effort', default=0)
    defect_count = models.PositiveIntegerField('Defect count', default=0)

    goodfix_count = models.PositiveIntegerField(default=0)
    defect_density = models.FloatField(default=1)
    duration = models.PositiveIntegerField(default=0)
    injectrate = models.FloatField(default=0)
    removerate = models.FloatField(default=0)

    def __str__(self):
        return str(self.id) + ": " + self.name

    @classmethod
    def create(cls, name, project_id):
        phase = cls(name=name, project_id=project_id)
        phase.save()
        return phase

    def countEffort(self):
        self.effort = 0
        iterations = Iteration.objects.filter(phase_id=self.id)
        for iter in iterations:
            i = iter.countEffort()
            self.effort += iter.effort
        self.save()
        return self.effort
    """
    def count_sloc_ppm(self):
        self.sloc_ppm = 0
        iterations = Iteration.objects.filter(phase_id=self.id)
        for it in iterations:
            i = it.count_sloc_ppm()
        n = 'Iteration' + str(self.coun)
        #result = iterations.aggregate(Max('id'))
        #iter = Iteration.objects.get(id=result['id__max'])
        #self.sloc_ppm = iter.sloc_ppm
        self.save()
        return self.sloc_ppm
    """

    def countDefect(self):
        self.defect_count = 0
        iterations = Iteration.objects.filter(phase_id=self.id)
        for iter in iterations:
            i = iter.countDefect()
            self.defect_count += iter.defect_count
        self.save()
        return self.defect_count

    def calDate(self):
        f = Iteration.objects.filter(
            phase_id=self.id).aggregate(Max('finish_date'))
        self.finish_date = f['finish_date__max']

        self.save()
        return self.finish_date

    def countGoodFix(self):
        self.goodfix_count = 0
        iterations = Iteration.objects.filter(phase_id=self.id)
        for iter in iterations:
            i = iter.countGoodFix()
            self.goodfix_count += iter.goodfix_count
        self.save()
        return self.goodfix_count

    def defectDensity(self):
        self.defect_density = 0
        defect_count = 0
        iterations = Iteration.objects.filter(phase_id=self.id)
        for iter in iterations:
            iter.defectDensity()
            sloc = iter.sloc / 1000
            defect_count += iter.defect_count
            if sloc > 0:
                self.defect_density = defect_count / sloc

        self.save()
        return self.defect_density

    def countDevno(self):
        iterations = Iteration.objects.filter(phase_id=self.id)
        for i in iterations:
            i.countDevno()
            i.countDuration()
            i.countInjectRate()
            i.countRemoveRate()

    def countDuration(self):
        iterations = Iteration.objects.filter(phase_id=self.id)

        d = 0
        for i in iterations:
            d += Developer.objects.filter(iteration_id=i.id).count()

        if self.finish_date and d > 0:
            c = (self.finish_date - self.start_date).days * 24
            self.duration = round(c / d, 5)

        self.save()
        return self.duration

    def countInjectRate(self):
        d = self.countDuration()
        c = self.countDefect()
        if c > 0 and d > 0:
            self.injectrate = round(c / d, 5)
        self.save()
        return self.injectrate

    def countRemoveRate(self):
        d = self.countDuration()
        c = self.countGoodFix()
        if c > 0 and d > 0:
            self.removerate = round(c / d, 5)
        self.save()
        return self.removerate


class Iteration(models.Model):
    name = models.CharField(max_length=100)
    phase = models.ForeignKey(Phase)
    sloc = models.PositiveIntegerField('Iteration SLOC', default=0)
    sloc_ppm = models.PositiveIntegerField('SLOC per person-month by iteration',
                                           default=0)
    start_date = models.DateTimeField('Start date')
    finish_date = models.DateTimeField('Finish date', blank=True, null=True)
    status = models.BooleanField('Iteration completed', default=False)
    effort = models.PositiveIntegerField('Iteration effort', default=0)
    defect_count = models.PositiveIntegerField('Iteration defect count',
                                               default=0)

    goodfix_count = models.PositiveIntegerField(default=0)
    defect_density = models.FloatField(default=0)
    devno = models.PositiveIntegerField(default=0)
    duration = models.PositiveIntegerField(default=0)
    injectrate = models.FloatField(default=0)
    removerate = models.FloatField(default=0)

    def __str__(self):
        return str(self.id) + ": " + self.name

    @classmethod
    def create(cls, name, phase_id):
        iteration = cls(name=name, phase_id=phase_id)
        iteration.save()
        return iteration
    """
    def count_sloc_ppm(self):
        d_count = Developer.objects.filter(iteration_id=self.id).count()
        m_count = (self.finish_date - self.start_date).days / float(30)
        self.sloc_ppm = self.sloc / d_count / m_count
        self.save()
        return self.sloc_ppm
     """
    def countEffort(self):
        self.effort = 0
        timers = Timer.objects.filter(iteration_id=self.id)
        for timer in timers:
            self.effort += timer.total_time
        self.save()
        return self.effort

    def countDefect(self):
        self.defect_count = 0
        self.defect_count = Defect.objects.filter(iteration_id=self.id).count()
        self.save()
        return self.defect_count

    def countGoodFix(self):
        self.goodfix_count = 0
        self.goodfix_count = Defect.objects.filter(
            iteration_id=self.id, implementation='Good Fix').count()
        self.save()
        return self.goodfix_count

    def defectDensity(self):
        self.defect_density = 0
        defect_count = self.countDefect()
        if self.sloc > 0:
            self.defect_density = round((defect_count / self.sloc) * 1000, 2)
        self.save()
        return self.defect_density

    def countDevno(self):
        self.devno = Developer.objects.filter(iteration_id=self.id).count()
        self.save()
        return self.devno

    def countDuration(self):
        d = self.countDevno()
        if self.finish_date is not None and d > 0:
            c = (self.finish_date - self.start_date).days * 24
            self.duration = round(c / d, 5)

        self.save()
        return self.duration

    def countInjectRate(self):
        d = self.countDuration()
        c = self.countDefect()
        if c > 0 and d > 0:
            self.injectrate = round(c / d, 5)
        self.save()
        return self.injectrate

    def countRemoveRate(self):
        d = self.countDuration()
        c = self.countGoodFix()
        if c > 0 and d > 0:
            self.removerate = round(c / d, 5)
        self.save()
        return self.injectrate


class Developer(models.Model):
    iteration = models.ForeignKey(Iteration, null=True)

    def __str__(self):
        return str(self.id)

    @classmethod
    def create(cls):
        developer = cls()
        developer.save()
        return developer


class Defect(models.Model):
    developer = models.ForeignKey(Developer)
    iteration = models.ForeignKey(Iteration)
    type = models.CharField(max_length=100)
    which_iteration = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    implementation = models.CharField(max_length=100, default="Bad fix")

    def __str__(self):
        return self.type

    @classmethod
    def create(cls, iteration_id, developer_id, type, which_iteration,
               description, implementation):
        defect = cls(iteration_id=iteration_id, developer_id=developer_id,
                     type=type, which_iteration=which_iteration,
                     description=description, implementation=implementation)
        defect.save()
        return defect


class Timer(models.Model):
    start_time = models.DateTimeField('start time', auto_now=True)
    resume_time = models.DateTimeField('resume time', auto_now=True)
    end_time = models.DateTimeField('end time', blank=True, null=True)
    total_time = models.PositiveIntegerField('total time(in seconds)',
                                             default=0)
    modified_time = models.PositiveIntegerField('modified time(in seconds)',
                                                default=0)
    developer = models.ForeignKey(Developer)
    iteration = models.ForeignKey(Iteration)

    def __str__(self):
        return str(self.id)

    @classmethod
    def create(cls, iteration_id, developer_id):
        timer = cls(iteration_id=iteration_id, developer_id=developer_id)
        timer.save()
        return timer

    @staticmethod
    def calculate(diff):
        hours = diff // 3600
        minutes = (diff % 3600) // 60
        seconds = (diff % 3600) % 60
        result = {'hours': hours, 'minutes': minutes, 'seconds': seconds}
        return result


class DeveloperSession(models.Model):
    def __str__(self):
        return str(self.id)

    @classmethod
    def create(cls):
        developerSession = cls()
        developerSession.save()
        return developerSession

    @staticmethod
    def startTimer(did, iteration_id):
        developer = Developer.objects.get(id=did)
        developer.iteration_id = iteration_id
        developer.save()
        timer = Timer.create(iteration_id, developer.id)
        return timer

    @staticmethod
    def pauseTimer(tid):
        timer = Timer.objects.get(id=tid)
        timer.total_time += (timezone.now() - timer.resume_time).seconds
        timer.save()
        return timer

    @staticmethod
    def resumeTimer(tid):
        timer = Timer.objects.get(id=tid)
        timer.resume_time = datetime.now()
        timer.save()
        return timer

    @staticmethod
    def stopTimer(tid):
        timer = Timer.objects.get(id=tid)
        timer.end_time = timezone.now()
        timer.total_time += (timer.end_time - timer.start_time).seconds
        timer.modified_time = (timer.end_time - timer.start_time).seconds
        timer.save()
        return timer

    @staticmethod
    def reportDefect(did, dict):
        developer = Developer.objects.get(id=did)
        developer.iteration_id = dict.get('it_id')
        developer.save()
        defect = Defect.create(dict.get('it_id'),
                               developer.id, dict.get('type'),
                               dict.get('which_iteration'),
                               dict.get('description'),
                               dict.get('implementation'))
        return defect


class ManagerSession(models.Model):
    def __str__(self):
        return str(self.id)

    @classmethod
    def create(cls):
        managerSession = cls()
        managerSession.save()
        return managerSession

    @staticmethod
    def countDefectEffort(pid):
        project = Project.objects.get(id=pid)
        phases = Phase.objects.filter(project_id=pid)
        for phase in phases:
            d = phase.countDefect()
            e = phase.countEffort()
            # s = phase.count_sloc_ppm()
            f = phase.countGoodFix()
            g = phase.defectDensity()
            h = phase.countDevno()
            i = phase.calDate()
            k = phase.countDuration()
            l = phase.countInjectRate()
            m = phase.countRemoveRate()
        return project

    @staticmethod  # use static method to avoid extra instance object passed in
    def addProject(name):
        project = Project.create(name)
        return project

    @staticmethod
    def closeProject(sloc, pid):
        p = Project.objects.filter(id=pid)
        p.update(status=True, sloc=sloc)
        p.update(finish_date=timezone.now())
        return p

    @staticmethod
    def closePhase(sloc, phid):
        phase = Phase.objects.get(id=phid)
        phase.sloc = sloc
        phase.status = True
        phase.finish_date = timezone.now()
        phase.save()
        return phase

    @staticmethod
    # get(for only one instance) should be used with save, filter with update
    def addIteration(phase_id):
        phase = Phase.objects.get(id=phase_id)
        name = 'Iteration' + str(phase.coun + 1)
        phase.coun = phase.coun + 1
        phase.save()
        iter = Iteration.create(name, phase_id)
        return iter

    @staticmethod
    def closeIteration(sloc, iter_id):
        iter = Iteration.objects.filter(id=iter_id)
        iter.update(status=True, sloc=sloc)
        iter.update(finish_date=timezone.now())
        return iter
