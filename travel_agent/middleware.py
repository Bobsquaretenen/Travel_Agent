class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Referrer-Policy (управляет тем, какую информацию передавать при переходах)
        if 'Referrer-Policy' not in response:
            response['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        # Permissions-Policy (отключает ненужные API браузера)
        if 'Permissions-Policy' not in response:
            response['Permissions-Policy'] = 'geolocation=(), camera=(), microphone=()'

        return response