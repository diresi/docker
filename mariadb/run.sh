set -e

mysqld_safe &
mysqladmin --silent --wait=30 ping || exit 1
mysql -e 'GRANT ALL PRIVILEGES ON *.* TO "root"@"localhost" WITH GRANT OPTION;'
mysql -e 'GRANT ALL PRIVILEGES ON *.* TO "flinkwork"@"%" IDENTIFIED BY "flinkwork";'
mysql -e 'GRANT ALL PRIVILEGES ON `phabricator\_%`.* TO "phabricator"@"%" IDENTIFIED BY "phabricator";'
wait
