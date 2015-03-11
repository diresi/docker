include ../Makefile.inc

NAME := flask
RUN_ARGS := -p 5000:5000 --link redis:redis --link rabbitmq:rabbitmq -v $(CURDIR)/flask:/home/flask
