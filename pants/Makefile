
DATE=`date -I`

run:
	python manage.py runserver

test:
	python manage.py test -v 2

mm:
	python manage.py makemigrations

migrate:
	python manage.py migrate

shell:
	python manage.py shell_plus

deploycheck:
	python manage.py check --deploy

fixtures:
	python manage.py dumpdata ingredients --indent 3 --no-color --natural-foreign --natural-primary -o fixtures/pants-ingredient-fixture.json

backup:
	python manage.py dumpdata --indent 3 --no-color --natural-foreign --natural-primary -o backups/pants-backup-fixture-${DATE}.json

fixme:
	grep -R 'FIXME' | grep -v ^backup | grep -v ^Makefile | grep -v ^Binary

