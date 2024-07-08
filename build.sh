# build_files.sh
pip3 install -r requirements.txt
python manage.py collectstatic
python manage.py migrate