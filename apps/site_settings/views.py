from django.shortcuts import render


def handler404(request, *args, **kwargs):
    return render(request, "http_errors/404.html", status=404)

# def handler500(request, *args, **kwargs):
#     return render(request, "errors/error_500.html", status=500)
