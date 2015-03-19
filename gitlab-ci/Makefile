include ../Makefile.inc

RUN_ARGS := -p 8083:80 \
	--link redis:redisio \
	  -e 'GITLAB_URL=http://10.0.0.1:8082' \
	  -e 'GITLAB_APP_ID=4cf1130c55619579ea762ff10e2acd0c96a7b6302f921f96d14de5a7994f1f33' \
	  -e 'GITLAB_APP_SECRET=9b97eed46a64e863713fb97a71bb25c93cf8a48ff7d6e032df2727bc06b59c1a' \
	--link postgresql:postgresql \
	  -e 'DB_USER=flinkwork' \
      -e 'DB_PASS=flinkwork' \
	  -e 'DB_NAME=gitlab_ci'

DATA_DIR := /home/gitlab_ci/data
