# http://python.org/pypi/recaptcha-client
# Author:  Ben Maurer <support at recaptcha net>
# Home Page: http://recaptcha.net/
# License: MIT/X11

import urllib2, urllib

API_SSL_SERVER="api-secure.recaptcha.net"
API_SERVER="api.recaptcha.net"
VERIFY_SERVER="api-verify.recaptcha.net"

class RecaptchaResponse(object):
    def __init__(self, is_valid, error_code=None):
        self.is_valid = is_valid
        self.error_code = error_code

def displayhtml (public_key, use_ssl=False, error=None,
                 options={}):
    """
    Get the HTML to display for a reCAPTCHA challenge.

    public_key -- The public api key
    use_ssl -- Should the request be sent over ssl?
    error -- An error message to display (from RecaptchaResponse.error_code)
    options -- A dict, e.g. {'theme': 'white', 'tabindex': 2}
    """
    error_param = ''
    if error:
	error_param = '&error=%s' % error
    if use_ssl:
        protocol = 'https'
        server = API_SSL_SERVER
    else:
        protocol = 'http'
        server = API_SERVER
    options_lines = []
    for key in options:
        options_lines.append('%s: %s' % (key, repr(options[key])))
    options_script = ''
    if options_lines:
        options_script = """
<script type="text/javascript">
var RecaptchaOptions = {
  %s
}
</script>
""".strip() % ',\n  '.join(options_lines)
    return """
%(options_script)s
<script type="text/javascript" src="%(protocol)s://%(server)s/challenge?k=%(public_key)s%(error_param)s"></script>

<noscript>
  <iframe src="%(protocol)s://%(server)s/noscript?k=%(public_key)s%(error_param)s" height="300" width="500" frameborder="0"></iframe><br />
  <textarea name="recaptcha_challenge_field" rows="3" cols="40"></textarea>
  <input type='hidden' name='recaptcha_response_field' value='manual_challenge' />
</noscript>
""".strip() % locals()


def submit (recaptcha_challenge_field,
            recaptcha_response_field,
            private_key,
            remoteip):
    """
    Submits a reCAPTCHA request for verification. Returns RecaptchaResponse
    for the request

    recaptcha_challenge_field -- The value of recaptcha_challenge_field from the form
    recaptcha_response_field -- The value of recaptcha_response_field from the form
    private_key -- your reCAPTCHA private key
    remoteip -- the user's ip address
    """

    if not (recaptcha_response_field and recaptcha_challenge_field and
            len (recaptcha_response_field) and len (recaptcha_challenge_field)):
        return RecaptchaResponse (is_valid = False, error_code = 'incorrect-captcha-sol')
    
    
    
    params = urllib.urlencode ({
	    'privatekey': private_key,
            'remoteip' : remoteip,
	    'challenge': recaptcha_challenge_field,
	    'response' : recaptcha_response_field,
	    })

    request = urllib2.Request (
        url = "http://%s/verify" % VERIFY_SERVER,
        data = params,
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "User-agent": "reCAPTCHA Python"
            }
        )
    
    httpresp = urllib2.urlopen (request)

    return_values = httpresp.read ().splitlines ();
    httpresp.close();

    return_code = return_values [0]

    if (return_code == "true"):
        return RecaptchaResponse (is_valid=True)
    else:
        return RecaptchaResponse (is_valid=False, error_code = return_values [1])


