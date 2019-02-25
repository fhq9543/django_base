from rest_framework.views import exception_handler

from utils.response import res, res_code


def robo_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        detail = response.data.get('detail')
        if detail:
            res['rescode'] = res_code['error']
            res['msg'] = detail
            res['data'] = None
        else:
            data = response.data
            res['rescode'] = str(data.get('rescode', ''))
            res['msg'] = str(data.get('msg', ''))
            res['data'] = None
            response.status_code = int(data.get('status_code', 500))
        response.data = res
        return response
