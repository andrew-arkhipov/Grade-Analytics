# Grade-Analytics
Automated grade analytics for UT OnRamps. <br>
*Note: this is semi-automatic - the code gives you 25 seconds to login to the selenium instance with 2FA.*

### Virtual Environment

It is highly recommended to use a Python virtual environment when running this script. Run the following commands in the root directory of the project.
```
python3 -m venv <env-folder-name>
```

To activate that virtual environment, use the below command:
```
source <env-folder-name>/bin/activate
```

After activating, to install the dependencies run:
```
pip3 install -r requirements.txt
```

### File Structure
`Reports` holds all grade reports. The target directory is hardcoded in `utils.py`.

`selenium_scraper.py` is the actual script. To run it, use the below command:
```
python scraper.py
```

