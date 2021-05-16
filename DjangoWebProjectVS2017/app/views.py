"""
Definition of views.
"""

from django.shortcuts import render,get_object_or_404
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.http.response import HttpResponse, Http404
from django.http import HttpResponseRedirect, HttpResponse
from .models import Question2,Choice2,User2
from django.template import loader
from django.core.urlresolvers import reverse
from app.forms import QuestionForm, ChoiceForm,UserForm
from django.shortcuts import redirect
import json


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Autor de la web',
            'message':'Datos de contacto',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
def index(request):
    latest_question_list = Question2.objects.order_by('-pub_date')
    template = loader.get_template('polls/index.html')
    questions=Question2.objects.all()
    subjects =questions.values('subject').distinct()
    context = {
                'title':'Lista de preguntas de la encuesta',
                'latest_question_list': latest_question_list,
                'subjects':subjects,
              }
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
     question2 = get_object_or_404(Question2, pk=question_id)
     return render(request, 'polls/detail.html', {'title':'Respuestas asociadas a la pregunta:','question': question2})

def results(request, question_id):
    question2 = get_object_or_404(Question2, pk=question_id)
    return render(request, 'polls/results.html', {'title':'Resultados de la pregunta:','question': question2})

def vote(request, question_id):
    p = get_object_or_404(Question2, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice2.DoesNotExist):
        # Vuelve a mostrar el form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "ERROR: No se ha seleccionado una opcion",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Siempre devolver un HttpResponseRedirect despues de procesar
        # exitosamente el POST de un form. Esto evita que los datos se
        # puedan postear dos veces si el usuario vuelve atras en su browser.
        return HttpResponseRedirect(reverse('results', args=(p.id,)))

def question_new(request):
        message=''
        if request.method == "POST":
            form = QuestionForm(request.POST)
            if form.is_valid():
                num=form.cleaned_data['numChoices']
                if num>1 and num<5:
                    question = form.save(commit=False)
                    question.pub_date=datetime.now()
                    question.save()
                    #return redirect('detail', pk=question_id)
                    #return render(request, 'polls/index.html', {'title':'Respuestas posibles','question': question})
                else:
                    message='El número de respuestas debe estar entre 2 y 4'
        else:
            form = QuestionForm()
        return render(request, 'polls/question_new.html', {'form': form, 'message':message})

def choice_add(request, question_id):
        question = Question2.objects.get(id = question_id)
        choiceList =Choice2.objects.filter(question = question_id)
        numChoice = choiceList.count()
        numCorrectas=choiceList.filter(isCorrect = True).count()
        message=''
        if request.method =='POST':
            form = ChoiceForm(request.POST)
            if form.is_valid():
                if numChoice < question.numChoices:
                    choiceCheckBox=form.cleaned_data['isCorrect']
                    if numCorrectas <1 or choiceCheckBox is False:
                        choice = form.save(commit = False)
                        choice.question = question
                        #choice.votes = 0
                        choice.save()         
                        #form.save()
                        message= 'Opción añadida correctamente'
                    else:
                        message= 'Solo puede haber una opción correcta'
                else:
                    message= 'Máximo de opciones alcanzadas'
        else: 
            form = ChoiceForm()
        #return render_to_response ('choice_new.html', {'form': form, 'poll_id': poll_id,}, context_instance = RequestContext(request),)
        return render(request, 'polls/choice_new.html', {'title':'Pregunta:'+ question.question_text, 'message':message, 'form': form})

def chart(request, question_id):
    q=Question2.objects.get(id = question_id)
    qs = Choice2.objects.filter(question=q)
    dates = [obj.choice_text for obj in qs]
    counts = [obj.votes for obj in qs]
    context = {
        'dates': json.dumps(dates),
        'counts': json.dumps(counts),
    }

    return render(request, 'polls/grafico.html', context)

def user_new(request):
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                #return redirect('detail', pk=question_id)
                #return render(request, 'polls/index.html', {'title':'Respuestas posibles','question': question})
        else:
            form = UserForm()
        return render(request, 'polls/user_new.html', {'form': form})

def users_detail(request):
    latest_user_list = User2.objects.order_by('email')
    template = loader.get_template('polls/users.html')
    context = {
                'title':'Lista de usuarios',
                'latest_user_list': latest_user_list,
              }
    return render(request, 'polls/users.html', context)

def ShowQuestions(request):
    latest_question_list = Question2.objects.order_by('-pub_date')
    template = loader.get_template('app/ShowQuestions.html')    
    questions = Question2.objects.all()
    temas = questions.values('subject').distinct()
    context = {
                'title':'Ver preguntas y respuestas',
                'message':'Listado de las preguntas y sus respectivas respuestas',
                'latest_question_list': latest_question_list,
                'subjects':temas,
              }
    return render(request, 'app/ShowQuestions.html', context)

def ShowQuestionsBySubject(request):
    selected = request.POST['dropList']
    listaObjetos = Question2.objects.filter(subject=request.POST['dropList'])

    context = {
            'title':'Ver preguntas y respuestas por tema',
            'message':'Listado de las preguntas y sus respectivas respuestas con el tema "' + selected + '"',
            'listaObjetos': listaObjetos,
            }
    return render(request, 'app/ShowQuestionsBySubject.html', context)
