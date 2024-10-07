import hashlib
import hmac
from urllib.parse import urlparse
import base64


def generate_signature(partner_id, partner_secret, http_method, epoch, endpoint, body=None, content_type=None):
    LF = '\u000a'

    # MD5 hash the body
    if body is not None:
        body_hash = hashlib.md5(body.encode('utf-8')).hexdigest()
    else:
        body = ""
        body_hash = ""
        content_type = ""

    #HTTP Method + LF + MD5 hash of the request body + LF + Content-Type header content + LF
    string_to_sign = http_method + LF + body_hash + LF + content_type + LF
    #Add the x-fivaldi-partner header to the Authorization header.
    string_to_sign += 'x-fivaldi-partner:' + partner_id + LF
    #Add the x-fivaldi-timestamp header to the Authorization header.
    string_to_sign += 'x-fivaldi-timestamp:' + epoch + LF
    #If the endpoint contains a ?, but has no params, remove it.
    if endpoint[-1] == "?":
        endpoint = endpoint[:-1]

    #If the URL contains a querystring, remove everything after it, then push.
    if "?" in endpoint:
        string_to_sign += endpoint.split("?", 1)[0]

    #Otherwise just push it, as is.
    else:
        string_to_sign += endpoint

    #If the request contains a query string, Add it to the Authorization header.
    if "?" in endpoint:
        string_to_sign += LF
        params = urlparse(endpoint)
        string_to_sign += params.query

    hmac.new(partner_secret.encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha256).digest()
    hashed = hmac.new(partner_secret.encode('utf8'), string_to_sign.encode('utf8'), hashlib.sha256).digest()
    hashed_signature = 'Fivaldi ' + base64.b64encode(hashed).decode()
    return hashed_signature
