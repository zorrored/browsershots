from factories.utils import requests_for_factory
from jobs.utils import browser_for_job


@factory_auth
def poll(factory):
    """
    Arguments:
    ~~~~~~~~~~
    * factory_name string (lowercase)

    Return value:
    ~~~~~~~~~~~~~
    * job dict (if matching job found)

    The job dict will contain the following keys:

    * hashkey string
    * browser string
    * major int
    * minor int
    * command string
    """
    jobs = jobs_for_factory(factory)[:1]
    if not len(jobs):
        raise xmlrpclib.Fault(204, "No matching requests.")
    job = jobs[0]
    browser = browser_for_job(job, factory)
    attempt = Attempt.objects.create(
        job=job, hashkey=hashkey, factory=factory)
    return {
        'hashkey': attempt.hashkey,
        'browser': job.group.slug,
        'version': browser.version,
        'major': browser.major,
        'minor': browser.minor,
        'command': browser.command,
        }
