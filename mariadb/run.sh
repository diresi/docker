set -e

mysqld_safe &
mysqladmin --silent --wait=30 ping || exit 1
mysql -e 'GRANT ALL PRIVILEGES ON *.* TO "root"@"localhost" WITH GRANT OPTION;'
mysql -e 'CREATE USER "flinkwork"@"%" IDENTIFIED BY "flinkwork";'
mysql -e 'GRANT ALL PRIVILEGES ON *.* TO "flinkwork"@"%";'
mysql -e 'CREATE USER "phabricator"@"%" IDENTIFIED BY "phabricator";'
mysql -e 'GRANT ALL PRIVILEGES ON `phabricator\_%`.* TO "phabricator"@"%";'
wait
