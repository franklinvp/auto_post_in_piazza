## How to use

1. Create a Python virtual environment with `python -m venv venv`
2. Install piazza_api with `pip install piazza_api`
3. Populate `posts.json` with the posts. The structure should be as follows:
    1. At the root the JSON is a dict with dates (in ISO-format YYYY-MM-DD) as keys.
    2. For each date, the value is a list of dictionaries with the following keys:
        1. `classID`, found in the course's URL in Piazza. For example,
        in https://piazza.com/class/m8lo7g5t4qv7ah the m8lo7g5t4qv7ah is the
        class ID
        2. `subject`
        3. `content`
        For example
        ```json
        {
            "2025-03-25": [
                {
                "classID": "m5hbugfu4i19h",
                "subject": "Announcement for class 1",
                "content": "This is the announcement."
                },
                {
                "classID": "m8lo7g5t4qv7ah",
                "subject": "Announcement for class 2",
                "content": "This is the other announcement"
                }
            ],
            "2025-03-26": [
                {
                "classID": "m8lo7g5t4qv7ah",
                "subject": "Another announcement for class 2",
                "content": "Blah blah blah"
                }
            ]
        }
        ```
4. Run `crontab -b` and append a line like
    ```
    * *     * * *           cd /home/fvera/piazza-api && /usr/bin/bash /home/fvera/piazza-api/script.sh
    ```
    Replace wherever it says `/home/fvera/piazza-api` with the absolute path
    to where you have the script.
    The `*` above can be replaced with specific times, specific days of the
    week or of the month, in which crontab runs the command.
5. Logging information is saved to `create_post.log`
6. In the file `days_ran.txt` the dates when the script attempted to create
    posts are saved. The script will not try to create posts when ran at dates
    appearing in this file. Remove or add dates to this file accordingly.
