.PHONY : clean dist/SimpleBlogPlugin-0.1-py2.4.egg

dist/SimpleBlogPlugin-0.1-py2.4.egg :
	python setup.py bdist_egg
	sudo cp $@ /var/lib/trac/johann/plugins

clean :
	rm -rf build dist SimpleBlogPlugin.egg-info
