# Assumes that Python and pip are installed (pre-installed in macOs and Ubuntu)

# Create a clean venv (install virtualenv if needed)
pip install virtualenv
virtualenv venv --clear

# Install requirements in venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

echo "Build complete. Run server locally with './run.sh'"
