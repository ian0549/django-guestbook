from django.http import HttpResponseRedirect, HttpResponse
#from django.views.generic import TemplateView
from django.shortcuts import render
from google.appengine.api import users
import urllib

from Guestbook.models import *

def main_page(request):
    guestbook_name = request.GET.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)

    # Ancestor Queries, as shown here, are strongly consistent with the High
    # Replication Datastore. Queries that span entity groups are eventually
    # consistent. If we omitted the ancestor from this query there would be
    # a slight chance that Greeting that had just been written would not
    # show up in a query.
    greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name))
    greetings = greetings_query.fetch(10)

    if users.get_current_user():
        url = users.create_logout_url(request.get_full_path())
        url_linktext = 'Logout'
    else:
        url = users.create_login_url(request.get_full_path())
        url_linktext = 'Login'

    template_values = {
        'greetings': greetings,
        'guestbook_name': guestbook_name,
        'url': url,
        'url_linktext': url_linktext
    }

    #return direct_to_template(request, 'guestbook/main_page.html')
    #return TemplateView.as_view(template_name='guestbook/main_page.html')
    #return HttpResponse('<h1>Page was found</h1>')
    return render(request, 'guestbook/main_page.html', template_values)

def sign_post(request):
    if request.method == 'POST':
        guestbook_name = request.POST.get('guestbook_name')
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = request.POST.get('content')
        greeting.put()

        return HttpResponseRedirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))
    
    return HttpResponseRedirect('/')