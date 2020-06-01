# proof-of-work-generator

I made this because the proof of work we need to provide is required in a specific format for a school project. Doing it manually sucks.

## Dependencies

* python3
* [jira](https://github.com/pycontribs/jira)
* [python-gitlab](https://github.com/python-gitlab/python-gitlab/tree/22d4b465c3217536cb444dafe5c25e9aaa3aa7be)

## Config

### src/config.py

Your jira server, username and password.

### src/days.py

starting_date = starting date of your worklog
amount_of_days = how many days from starting date to export
