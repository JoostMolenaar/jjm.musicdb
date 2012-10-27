
include Makefile.inc

live ?= 0

ifeq ($(live),1)
    ENV = /srv/$(NAME)
    SUDO = sudo
else
    ENV = env
    SUDO =
endif

USER = $(shell id -un)
GROUP = $(shell id -gn)

DEPLOY_WEB = $(ENV)/web
DEPLOY_CONF = $(ENV)/conf

SRC = file://$(shell pwd)

PIP_CACHE = .cache

.PHONY: run

test: runtime
	-yes | $(ENV)/bin/pip uninstall $(PIP_NAME)
	$(ENV)/bin/python -m $(MAIN)

run: deploy
	$(ENV)/bin/pip install $(SRC) 
	cd $(ENV) ; bin/python -m $(MAIN)

runtime: $(ENV)

$(ENV):
ifeq ($(live),1)
	$(SUDO) mkdir -p $(ENV)
	$(SUDO) chown $(USER).$(GROUP) $(ENV)
else
	mkdir -p $(ENV)
endif
	virtualenv $(ENV) 
	$(ENV)/bin/easy_install -U distribute
	$(ENV)/bin/pip install --upgrade --requirement $(REQ) --download-cache $(PIP_CACHE) 

deploy: runtime deploy-code deploy-web deploy-conf touch-conf

deploy-code:
	$(ENV)/bin/pip install $(SRC)
	rm -rf /tmp/pip-*-{build,unpack}

deploy-web:
	@rm -rf $(DEPLOY_WEB)
	cp -r web $(DEPLOY_WEB)

deploy-conf:
	@rm -rf $(DEPLOY_CONF)
	cp -r conf $(DEPLOY_CONF)

touch-conf:
	ls $(DEPLOY_CONF)/uwsgi/* > /dev/null 2>&1 && touch $(DEPLOY_CONF)/uwsgi/*

clean:
	$(SUDO) rm -rf $(ENV)

really-clean: clean
	rm -rf $(PIP_CACHE)


