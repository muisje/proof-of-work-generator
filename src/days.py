from config import *
from jira import JIRA
import datetime

starting_date = datetime.datetime.fromisoformat('2020-05-18T14:00:00.000+0200'.split('+')[0])
amount_of_days = 7

jira = JIRA(jira_server, auth=(jira_username, jira_password))

file = open('log_week_0.md','w') 

file.write('# Log week 0\n\n')

dates = list()
dates.append(starting_date)
for i in range(amount_of_days - 1): 
    dates.append(dates[-1] + datetime.timedelta(days=1))

markdown_table_header = '| Hours | Task | With whom | Results | Link |'
markdown_table_header_seperator = '|---|---|---|---|---|'

for date in dates:
    file.write('## ' + date.strftime('%A'))
    markdown_table_lines = list()
    for issue in jira.search_issues('(assignee = ' + jira_user_export + ' OR "Assignee\'s" = ' + jira_user_export + ' OR Reviewers = ' + jira_user_export + ' OR worklogAuthor = ' + jira_user_export + ') AND worklogDate = ' + str(date.date()) + ' order by updated', 
    fields="id,key,summary,worklog,assignee,customfield_10201,issuetype,customfield_10204"):
        total_time_spent_seconds = 0
        markdown_worklog_comment = ''
        try:
            for worklog in issue.fields.worklog.worklogs:
                if worklog.author.name == jira_user_export:
                    if datetime.datetime.fromisoformat(worklog.started.split('+')[0]).date() == date.date():
                        total_time_spent_seconds += worklog.timeSpentSeconds
                        markdown_worklog_comment += worklog.comment.replace("\n", "<br>").replace("\r","<br>").replace("|"," ") + '<br><br>' #TODO some regex or something to handle links etc.
        except:
            print('worklog error')

        if total_time_spent_seconds == 0:
            continue;

        assignees = dict()


        if issue.fields.assignee is not None:
            assignees[issue.fields.assignee.name] = issue.fields.assignee.displayName 
        for assignee in issue.fields.customfield_10201:
            assignees[assignee.name] = assignee.displayName

        assignees.pop('Unassigned', None)
        markdown_with_whom = ''
        for assignee in assignees:
            if assignee != jira_user_export:
                markdown_with_whom += assignees[assignee] + ', '

        markdown_with_whom = markdown_with_whom[:-2];        

        issue_link =  jira_server + '/browse/' + issue.key

        markdown_issue_link = '[' + issue.key + '](' + issue_link + ')'

        task = '![' + issue.fields.issuetype.name +'](' + issue.fields.issuetype.iconUrl + ' "'+ issue.fields.issuetype.name + '")' + ' / ' + markdown_issue_link + " / "  + issue.fields.summary
        link = 'None'
        if issue.fields.customfield_10204 is not None:
            link = '[link]' + '(' + issue.fields.customfield_10204 + ')'
        markdown_table_line = '| ' + str(datetime.timedelta(seconds=total_time_spent_seconds)) +  ' | ' + task +  ' | ' + markdown_with_whom  +  ' | ' + markdown_worklog_comment +  ' | ' + link  +  ' |'
        markdown_table_lines.append(markdown_table_line)
    markdown_table = markdown_table_header + '\n' + markdown_table_header_seperator + '\n'
    for markdown_table_line in markdown_table_lines:
        markdown_table += markdown_table_line + '\n'
    file.write('\n\n')
    file.write (markdown_table)
    file.write('\n')
