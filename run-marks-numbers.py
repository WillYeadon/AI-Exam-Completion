import subprocess

# Make sure to updated X, Y, Z with your API key
scripts = ["question_number_update.py", "marks-extraction.py"]

# Run each script in the list
for script in scripts:
    try:
        subprocess.run(['python', script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script}: {e}")
