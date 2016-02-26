from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.utils import timezone
from .models import *

def login(request):
    return render(request, 'pdt/login.html')

def activity(request):
    developer = Developer.create()
    developer.save()
    did = developer.id
    context = {'did': did}
    return render(request, 'pdt/activity.html', context)


def timer(request, did, it_id):
    developer_Session = DeveloperSession.create()
    timer = developer_Session.startTimer(did, it_id)
    context = {'timer': timer}
    return render(request, 'pdt/timer.html', context)


def timer_control(request, judge, tid):
    developer_Session = DeveloperSession.create()
    if int(judge) == 1:#pause timer
        t = developer_Session.pauseTimer(tid)
    elif int(judge) == 2:#stop timer
        t = developer_Session.stopTimer(tid)
    elif int(judge) == 3:#resume timer
        t = developer_Session.resumeTimer(tid)

    result = t.calculate(t.total_time)
    hours = result.get('hours')
    minutes = result.get('minutes')
    seconds = result.get('seconds')

    timer = Timer.objects.get(id=tid)
    context = {'timer': timer,
               'hours': hours,
	       'minutes': minutes,
	       'seconds': seconds}
    return render(request, 'pdt/timer.html', context)

def timer_review(request, did, it_id):
    timers = Timer.objects.filter(iteration_id=it_id, developer_id=did)
    context = {'timers': timers}

    return render(request, 'pdt/timer_review.html', context)


def defect_report(request, did, pid, phid, check, it_id):
    developer_Session = DeveloperSession.create()
    phase = Phase.objects.get(id=phid)
    if int(check) == 1:
        dict = {'it_id': it_id, 'type': request.POST['type'],
                'which_iteration': 'Iteration' + str(phase.coun),
                'description': request.POST['description'],
                'implementation': request.POST['implementation']}
        developer_Session.reportDefect(did, dict)
    context = {'it_id': it_id,
               'pid': pid,
               'phid': phid,
               'did': did}
    return render(request, 'pdt/defect_report.html', context)

def defect_review(request, did, it_id):
    defects = Defect.objects.filter(iteration_id=it_id, developer_id=did)
    context = {'defects': defects}
    return render(request, 'pdt/defect_review.html', context)

def dev_iteration(request, did, pid, phid, check):
    active_iterations = Iteration.objects.filter(phase_id=phid, status=False)
    name = Phase.objects.get(id=phid).name
    context = {'active_iterations': active_iterations,
               'name': name,
               'pid': pid,
               'phid': phid,
               'check': check,
               'did': did}
    path = ""
    if int(check) > 0:
        path = 'pdt/mag_iteration.html'
    else:
        path = 'pdt/dev_iteration.html'
    return render(request, path, context)

def dev_project(request, did, check):
    active_projects = Project.objects.filter(status=False)
    context = {'active_projects': active_projects,
               'check': check,
               'did': did}
    return render(request, 'pdt/dev_project.html', context)

def dev_phase(request, did, pid, check):
    p = Project.objects.get(id=pid)
    active_phases = Phase.objects.filter(project_id=pid, status=False)
    context = {'active_phases': active_phases,
               'check': check,
	       'p': p,
               'pid': pid,
               'did': did}
    return render(request, 'pdt/dev_phase.html', context)


def project(request, pid):
    manager_session = ManagerSession.create()
    if int(pid) == 100000:
        name = request.POST['project_name']
        if name != "":
            proj = manager_session.addProject(name)
    else:
        sloc = request.POST.get('SLOC', False)
        proj = manager_session.closeProject(sloc, pid)
    active_projects = Project.objects.filter(status=False)
    completed_projects = Project.objects.filter(status=True)
    context = {'active_projects': active_projects,
               'completed_projects': completed_projects}
    return render(request, 'pdt/project.html', context)

def phase(request, pid, phid):
    p = Project.objects.get(id=pid)
    manager_session = ManagerSession.create()
    if int(phid) != 10000000:
        sloc = request.POST.get('SLOC', False)
        phase = manager_session.closePhase(sloc, phid)
    active_phases = Phase.objects.filter(project_id=pid, status=False)
    completed_phases = Phase.objects.filter(project_id=pid, status=True)
    context = {'active_phases': active_phases,
               'completed_phases': completed_phases,
               'pid': pid,
	       'p': p}
    return render(request, 'pdt/phase.html', context)

def iteration(request, pid, phid, it_id):
    name = Phase.objects.get(id=phid).name
    manager_session = ManagerSession.create()
    if int(it_id) == 100000:
        iter = manager_session.addIteration(phid)
    elif int(it_id) >=0 & int(it_id) < 100000:
        sloc = request.POST.get('SLOC', False)
        iter = manager_session.closeIteration(sloc, it_id)
    active_iterations = Iteration.objects.filter(phase_id=phid, status=False)
    completed_iterations = Iteration.objects.filter(phase_id=phid, status=True)
    context = {'active_iterations': active_iterations,
               'completed_iterations': completed_iterations,
               'phid': phid,
	       'pid': pid,
	       'name': name}
    return render(request, 'pdt/iteration.html', context)

def report(request, pid):
    manager_session = ManagerSession.create()
    proj = manager_session.countDefectEffort(pid)

    pj_detail = Project.objects.get(id=pid)
    total_defect = pj_detail.countDefect()
    total_goodfix = pj_detail.countGoodFix()
    total_duration = pj_detail.countDuration()
    total_dev = pj_detail.countDev()
    total_duration = pj_detail.countDuration()
    total_injectrate = pj_detail.countInjectRate()
    total_removerate = pj_detail.countRemoveRate()

    inception = Phase.objects.get(project_id=pid, name="Inception")
    elaboration = Phase.objects.get(project_id=pid, name="Elaboration")
    construction = Phase.objects.get(project_id=pid, name="Construction")
    transition = Phase.objects.get(project_id=pid, name="Transition")
    ii = Iteration.objects.filter(phase_id=inception.id)
    ei = Iteration.objects.filter(phase_id=elaboration.id)
    ci = Iteration.objects.filter(phase_id=construction.id)
    ti = Iteration.objects.filter(phase_id=transition.id)

    i_sloc = 0
    i_devno = 0
    for i in ii:
        i_sloc = i.sloc
        i_devno += Developer.objects.filter(iteration_id=i.id).count()

    e_sloc = 0
    e_devno = 0
    for i in ei:
        e_sloc = i.sloc
        e_devno += Developer.objects.filter(iteration_id=i.id).count()

    c_sloc = 0
    c_devno = 0
    for i in ci:
        c_sloc = i.sloc
        c_devno += Developer.objects.filter(iteration_id=i.id).count()

    t_sloc = 0
    t_devno = 0
    for i in ti:
        t_sloc = i.sloc
        t_devno += Developer.objects.filter(iteration_id=i.id).count()

    i_sloc_per = e_sloc_per = c_sloc_per = 0
    if t_sloc > 0:
        i_sloc_per = round(i_sloc / t_sloc * 100, 2)
        e_sloc_per = round(e_sloc / t_sloc * 100, 2)
        c_sloc_per = round(c_sloc / t_sloc * 100, 2)

    defect_density = 0
    if t_sloc > 0:
        defect_density = round(total_defect / (t_sloc / 1000), 2)


    context = {'inception': inception,
               'elaboration': elaboration,
               'construction': construction,
               'transition': transition,
               'proj': proj,
               'ii': ii, #'lii': lii,
               'ei': ei, #'lei': lei,
               'ci': ci, #'lci': lci,
               'ti': ti,
               'i_sloc': i_sloc,
               'i_devno': i_devno,
               'i_sloc_per': i_sloc_per,
               'e_sloc': e_sloc,
               'e_devno': e_devno,
               'e_sloc_per': e_sloc_per,
               'c_sloc': c_sloc,
               'c_devno': c_devno,
               'c_sloc_per': c_sloc_per,
               't_sloc': t_sloc,
               't_devno': t_devno,
               'total_defect': total_defect,
               'total_goodfix': total_goodfix,
               'total_dev': total_dev,
               'total_duration': total_duration,
               'defect_density': defect_density,
               'total_injectrate': total_injectrate,
               'total_removerate': total_removerate,
               }
    return render(request, 'pdt/report.html', context)
