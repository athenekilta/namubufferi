# Requires Python and pip to be installed

# Create a clean venv (install virtualenv if needed)
pip install virtualenv
virtualenv venv --clear

# Install requirements in the venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Good to go.
echo "Build complete. Run server locally with './run.sh'"
