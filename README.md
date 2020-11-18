# OnRamps Grade Analytics
Automated tasks for UT OnRamps. <br>
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

After activating, install the dependencies with:
```
pip install -r requirements.txt
```

### Usage 

To use the **report scraper**, run the following command:
```
python download.py <absolute/path/to/target/directory>
```

As an example:
```
python download.py /Users/andrew/Downloads
```
*Note: the path is not required, and downloads will be sent to the default Downloads directory on your local machine if it is not specified.*

<br>


To use the **survey filler**, run the following command:
```
python survey.py
```
*Note: the shell will ask you to input the survey url, intro text, and finished text before running the program.*

<br>

To use the **regrade tool** for question 7, run the following command:
```
python regrade.py
```
<br>

To use the **accomodations tool**, run the following command:
```
python accommodate.py <relative/path/to/accommodations.csv>
```
*Note: the path is required, and the shell will ask you for the unit number.* 

<br>


`utils.py` holds utilities to help with scraping.

### Tasks
- [x] Remove hardcoding from `utils.py`
