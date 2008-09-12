install :
	python setup.py install

initial_data : \
shotserver05/platforms/fixtures/initial_data.json \
shotserver05/browsers/fixtures/initial_data.json \

shotserver05/%/fixtures/initial_data.json :
	mkdir -p shotserver05/$*/fixtures
	shotserver05/manage.py dumpdata --indent=4 $* > $@

docs : \
docs/xml-rpc.txt \

docs/xml-rpc.txt :
	xmlrpcdoc http://127.0.0.1:8000/xmlrpc/ > $@

docs/html : docs
	mkdir -p $@
	ls docs | grep txt | sed s/.txt// \
	| xargs -Iname rst2html.py docs/name.txt docs/html/name.html

precommit : docs headers pep8
	mkdir -p $@
	cat docs/xml-rpc.txt | sort -u > precommit/docs-xml-rpc-sorted.txt
	cat shotserver05/*/admin.py | sort -u > precommit/admin-sorted.txt
	cat shotserver05/*/forms.py | sort -u > precommit/forms-sorted.txt
	cat shotserver05/*/models.py | sort -u > precommit/models-sorted.txt
	cat shotserver05/*/urls.py | sort -u > precommit/urls-sorted.txt
	cat shotserver05/*/views.py | sort -u > precommit/views-sorted.txt
	cat shotserver05/*/xmlrpc.py | sort -u > precommit/xmlrpc-sorted.txt

headers :
	find . -name "*.py" | grep -v build/ \
	| xargs header.py shotserver05/__init__.py

properties :
	find . -name "*.py" \
	| grep -v build/ \
	| xargs svn propset svn:keywords "Rev Date Author"
	find . -type f | grep -v build/ | grep -v \\.svn \
	| grep -v \\.bz2 | grep -v \\.gz | grep -v \\.pyc \
	| grep -v \\.png | grep -v \\.ico | grep -v \\.jpg \
	| grep -v django.mo | grep -v rosetta-shotserver \
	| xargs svn propset svn:eol-style native

pep8 :
	pep8.py --filename=*.py shotserver05

pylint :
	-pylint shotserver05 \
	| grep -v "Relative import 'se" \
	| grep -v 'Invalid name "urlpatterns"' \
	| grep -v "Unused import deseb" \
	| grep -v "Inline] Missing docstring" \
	| grep -v "Admin] Missing docstring" \
	| grep -v "Meta] Missing docstring" \
	| grep -v "Meta] Class has no __init__ method" \
	| grep -v "Meta] Too few public methods" \
	| grep -v /tests.py:

jquery :
	wget -O shotserver05/static/js/jquery.form.js \
http://jqueryjs.googlecode.com/svn/trunk/plugins/form/jquery.form.js
	wget -O shotserver05/static/js/jquery.js \
http://jqueryjs.googlecode.com/files/jquery-1.2.6.min.js
#http://jqueryjs.googlecode.com/files/jquery-1.2.6.js
#http://jqueryjs.googlecode.com/files/jquery-1.2.6.pack.js

# You need to start the test server first, in a separate shell:
# manage.py testserver authtestdata
xmlrpc :
	tools/xmlrpc.py system.listMethods | grep methodHelp
	tools/xmlrpc.py system.methodHelp system.methodHelp | grep Arguments
	tools/xmlrpc.py system.methodSignature system.methodHelp | grep string
	tools/xmlrpc.py platforms.operatingSystemDetails leopard | grep Leo
	tools/xmlrpc.py factories.factoryDetails testfactory | grep 404
	rm -f testclient.html testfactory.html
	wget -q http://127.0.0.1:8000/users/auth/testclient.html
	tools/xmlrpc.py --auth=testclient.html factories.createFactory \
	testclient testfactory leopard MacBook | grep OK
	wget -q http://127.0.0.1:8000/factories/auth/testfactory.html
	tools/xmlrpc.py factories.factoryDetails testfactory | grep leopard
	tools/xmlrpc.py factories.listActiveFactories | grep "\[\]"
#	tools/xmlrpc.py --auth=testfactory.html jobs.poll testfactory
#	tools/xmlrpc.py factories.listActiveFactories | grep testfactory
