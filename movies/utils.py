def get_client_ip(request):
    """Получение IP пользователя"""

    addr = request.META.get("HTTP_X_FORWARDED_FOR")
    if addr:
        return addr.split(",")[0]
    return request.META.get("REMOTE_ADDR")
