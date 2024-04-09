from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Advertisement, Response
from .forms import AdvertisementForm, ResponseForm, CategoryFilterForm
# from django.views.generic import ListView
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@login_required
def create_advertisement(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.creator = request.user
            advertisement.save()
            return redirect('advertisement_detail', pk=advertisement.pk)
    else:
        form = AdvertisementForm()
    return render(request, 'board/create_advertisement.html', {'form': form})


@login_required
def edit_advertisement(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk)
    if advertisement.creator != request.user:
        pass
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, instance=advertisement)
        if form.is_valid():
            advertisement = form.save()
            return redirect('advertisement_detail', pk=advertisement.pk)
    else:
        form = AdvertisementForm(instance=advertisement)
    return render(request, 'board/edit_advertisement.html', {'form': form})


@login_required
def advertisement_detail(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.responder = request.user
            response.advertisement = advertisement
            response.save()
            return redirect('advertisement_detail', pk=pk)
    else:
        form = ResponseForm()
    responses = Response.objects.filter(advertisement=advertisement)
    return render(request, 'board/advertisement_detail.html',
                  {'advertisement': advertisement, 'responses': responses, 'response_form': form})


@login_required
def create_response(request, advertisement_id):
    advertisement = get_object_or_404(Advertisement, pk=advertisement_id)

    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.responder = request.user
            response.advertisement = advertisement
            response.save()


            subject = f'Новый отклик на ваше объявление "{advertisement.title}"'
            message = f'Пользователь {request.user.username} оставил новый отклик на ваше объявление "{advertisement.title}":\n\n{response.text}'
            sender_email = 'goriinmaksim@yandex.ru'
            recipient_email = advertisement.creator.email
            send_mail(subject, message, sender_email, [recipient_email])

            return redirect('advertisement_detail', pk=advertisement_id)
    else:
        form = ResponseForm()

    return render(request, 'board/create_response.html', {'form': form, 'advertisement': advertisement})


def advertisement_list(request, category=None):
    if category:
        advertisements = Advertisement.objects.filter(category=category)
    else:
        advertisements = Advertisement.objects.all()
    return render(request, 'board/advertisement_list.html', {'advertisements': advertisements, 'category': category})


def index(request):
    advertisements = Advertisement.objects.all()
    advertisement_data = []
    category_filter_form = CategoryFilterForm()

    if request.method == 'GET':
        category_filter_form = CategoryFilterForm(request.GET)
        if category_filter_form.is_valid():
            category = category_filter_form.cleaned_data.get('category')
            if category:
                advertisements = advertisements.filter(category=category)

    for ad in advertisements:
        responses = Response.objects.filter(advertisement=ad)
        response_authors = [response.responder.username for response in responses]
        ad_data = {
            'advertisement': ad,
            'responses_count': responses.count(),
            'response_authors': response_authors
        }
        advertisement_data.append(ad_data)

    return render(request, 'board/index.html',
                  {'advertisement_data': advertisement_data, 'category_filter_form': category_filter_form})


def about(request):
    return render(request, 'board/about.html')


# class AdvertisementListView(ListView):
#     model = Advertisement
#     template_name = 'board/index.html'
#     context_object_name = 'advertisement_data'
#     paginate_by = 10

@login_required
def private_responses(request):
    user_responses = Response.objects.filter(responder=request.user)
    return render(request, 'board/private_responses.html', {'user_responses': user_responses})


# def send_newsletter_to_users():
#     news_text = "Здесь ваш текст новости"
#     recipient_list = list(User.objects.values_list('email', flat=True))
#     subject = "Тема вашей новостной рассылки"
#     from_email = settings.EMAIL_HOST_USER
#     html_content = render_to_string('board/news.html', {'news_text': news_text})
#     msg = EmailMultiAlternatives(subject, strip_tags(news_text), from_email, recipient_list)
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()
