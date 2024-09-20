.PHONY: push run setup freeze

run:
	source venv/bin/activate && venv/bin/python3 app.py

setup:
	rm -rf venv/
	python3 -m venv venv
	venv/bin/python3 -m pip install -r requirements.txt

freeze: 
	venv/bin/python3 -m pip freeze > requirements.txt