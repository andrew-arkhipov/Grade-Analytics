# Grade-Analytics
Automated grade analytics for UT OnRamps. <br>
*Note: this is semi-automatic - the code gives you 25 seconds to login to the selenium instance with 2FA.*

### Virtual Environment

It is highly recommended to use a Python virtual environment when running this script. Run the following commands in the root directory of the project.
```
python -m venv <env-folder-name>
```

To activate that virtual environment, use the below command:
```
source <env-folder-name>/bin/activate
```

After activating, to install the dependencies run:
```
pip install -r requirements.txt
```

### File Structure
The target directory is hardcoded in `utils.py`, which currently creates a `Records` folder in the current working directory. 
- `SOURCE_DIR` is for downloaded files
- `TARGET_DIR` is where the downloaded files get moved to
  - *TODO: remove hardcoding*

`utils.py` holds utilities to help with scraping.

`scraper.py` is the actual script. To run it, use the below command:
```
python scraper.py
```
