# Copyright (C) 2006 Johann C. Rocholl <johann@browsershots.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
XML-RPC request handler.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

import xmlrpclib, re

# A list of sub-modules to export through XML-RPC.
export_modules = ['system', 'auth', 'request']

def import_deep(name):
    """
    Import a module from some.levels.deep and return the module
    itself, not its uppermost parent.
    """
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def module_method(module_methodname):
    """
    Import a module and method by string names.
    If the module has magic names, these will be considered.
    """
    modulename, methodname = module_methodname.rsplit('.', 1)
    module = import_deep('shotserver03.xmlrpc.%s' % modulename)
    if hasattr(module, 'magic_names'):
        if module.magic_names.has_key(methodname):
            methodname = module.magic_names[methodname]
    assert hasattr(module, methodname)
    method = getattr(module, methodname)
    return module, method

whitespace_match = re.compile(r'\n*([\s\t]*)').match
signature_match = re.compile(r'(\w+)\(([^\)]*)\)\s+=>\s+(\w+)\s*$').match
def split_docstring(doc):
    """
    split_docstring(string) => array
    Split a docstring into signature lines and documentation.
        Remove first level of docstring indentation.
        Also skip doctest dialogue.
    >>> split_docstring(split_docstring.__doc__)[0]
    [['array', 'string']]
    >>> print split_docstring(split_docstring.__doc__)[1]
    Split a docstring into signature lines and documentation.
        Remove first level of docstring indentation.
        Also skip doctest dialogue.
    """
    # Remove indentation.
    whitespace = whitespace_match(doc).group(1)
    if whitespace:
        doc = doc.replace('\n'+whitespace, '\n')
    doc = doc.strip()
    lines = doc.split('\n')
    # Parse signature lines.
    signatures = []
    match = signature_match(lines[0])
    while match:
        dummy, params, result = match.groups()
        signature = [result]
        for param in params.split(','):
            signature.append(param.strip())
        signatures.append(signature)
        lines.pop(0)
        match = signature_match(lines[0])
    # Remove doctest dialogue.
    doc = []
    while lines:
        if lines[0].startswith('>>>'):
            break
        doc.append(lines.pop(0).rstrip())
    doc = '\n'.join(doc).strip()
    return signatures, doc

def handler(req):
    """
    Handler for XML-RPC requests.
    """
    __builtins__['req'] = req
    from mod_python import apache
    data = req.read()
    if not data:
        explain = (
            "Your browser does not speak XML-RPC.",
            "Use an XML-RPC client to access this resource.",
            "The following is an example client in Python.")
        req.content_type = 'text/plain'
        req.write('\n'.join(explain))
        req.write('\n\n')
        req.sendfile('/usr/bin/xmlrpc_help.py')
        return apache.OK
    params, module_methodname = xmlrpclib.loads(data)
    dummy, method = module_method(module_methodname)
    answer = method(*params)
    answer = xmlrpclib.dumps((answer, ), methodresponse = True)
    req.write(answer)
    return apache.OK

if __name__ == '__main__':
    import sys, doctest
    errors, tests = doctest.testmod()
    if errors:
        sys.exit(1)
