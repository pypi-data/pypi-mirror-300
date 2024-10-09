test:
	python3 -m unittest discover

clean:
	rm -rf dist
	rm -rf django_vanityurls.egg-info

build: clean
	python -m build

publish: build
	twine upload dist/*
