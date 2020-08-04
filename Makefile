.PHONY: lab
lab:
	@@docker-compose build lab
	@@docker-compose up --detach --force-recreate lab
