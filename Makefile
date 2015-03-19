include Makefile.inc

.PHONY: stop kill

stopall:
	find ${CURDIR} -maxdepth 1 -type d -exec make -C '{}' stop \;

killall:
	find ${CURDIR} -maxdepth 1 -type d -exec make -C '{}' kill \;
