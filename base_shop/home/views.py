from django.views.generic import TemplateView

class HomeView(TemplateView):
  template_name = 'home/home.html'
  
def trigger_error(request):
    raise Exception("これはテスト用のサーバーエラーです")