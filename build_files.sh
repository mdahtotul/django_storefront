echo "Building the project...."
pipenv install
echo "Project building completed."

echo "Making migrations..."
python3.10 manage.py makemigrations --noinput
python3.10 manage.py migrate --noinput
echo "Migration completed."

echo "Collecting static files..."
python3.10 manage.py collectstatic --noinput --clear
echo "All Done."