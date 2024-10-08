# endpoints/controllers/base.py
from asgiref.sync import sync_to_async
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import get_resolver, URLPattern, URLResolver


def list_urls(urlconf, namespace=None, prefix=''):
    urls = []
    for entry in urlconf:
        if isinstance(entry, URLPattern):
            urls.append((namespace, prefix + str(entry.pattern)))
        elif isinstance(entry, URLResolver):
            new_namespace = f"{namespace}:{entry.namespace}" if namespace else entry.namespace
            urls.extend(list_urls(entry.url_patterns, new_namespace, prefix + str(entry.pattern)))
    return urls


def endpoints(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect(settings.EP_NOT_AUTH_REDIRECT_URL)
    all_urls = list_urls(get_resolver().url_patterns)
    app_urls = {}
    media_urls = []
    static_urls = []
    for namespace, url in all_urls:
        if 'media' in url:
            media_urls.append(url)
        elif 'static' in url:
            static_urls.append(url)
        else:
            app_name = namespace.split(':')[0] if namespace else 'root'
            if app_name in settings.EP_EXCLUDED_APPS: continue
            if app_name not in app_urls:
                app_urls[app_name] = []
            app_urls[app_name].append(url)
    custom_links = getattr(settings, 'EP_CUSTOM_LINKS', [])
    return render(request, 'endpoints/endpoints.html', {
        'app_urls': app_urls,
        'media_urls': media_urls,
        'static_urls': static_urls,
        'custom_links': custom_links,
    })


aendpoints = sync_to_async(endpoints)
