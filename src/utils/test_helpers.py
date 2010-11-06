def build_http_auth_header(username, password):
    base_64_string = '%s:%s' % (username, password)
    auth_header = 'Basic ' + base_64_string.encode('base64')
    return auth_header

