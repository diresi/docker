include ../Makefile.inc

RUN_ARGS := -p 8083:80 \
	--link redis:redisio \
	  -e 'GITLAB_URL=http://10.0.0.1:8082' \
	  -e 'GITLAB_APP_ID=cdf1bebcb966cecbcee2341d6a9ac64a17df27c99901812d005964db5e17b855' \
	  -e 'GITLAB_APP_SECRET=3b342a4a619cddff5fc7683cfbf9f60a5201c9c7599a203770857d0e89d9cf30' \
	--link postgresql:postgresql \
	  -e 'DB_USER=flinkwork' \
      -e 'DB_PASS=flinkwork' \
	  -e 'DB_NAME=gitlab_ci'

DATA_DIR := /home/gitlab_ci/data
