screenshots = file('screenshots_screenshot.sql').readlines()
screenshots.pop(0)
screenshots.pop(-1)

requests = file('requests_request.sql').readlines()
print requests.pop(0).rstrip('\n').replace('uploaded', 'screenshot_id')
end = requests.pop(-1).rstrip('\n')


def find_screenshot(request_id):
    for screenshot in screenshots:
        values = screenshot.rstrip('\n').split('\t')
        if values[2] == request_id:
            return values[0]
    return r'\N'


for request in requests:
    values = request.rstrip('\n').split('\t')
    uploaded = values[-1]
    values = values[:-1] + [find_screenshot(values[0])]
    print '\t'.join(values)

print end
