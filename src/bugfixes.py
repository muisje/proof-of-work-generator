from config import *
from jira import JIRA
import datetime
import gitlab
import re

gl = gitlab.Gitlab('https://gitlab.com', private_token= gl_private_token)
gl_project = gl.projects.get(gl_project_id)
gl_mrs = gl_project.mergerequests.list(all = True)

jira = JIRA(jira_server, auth=(jira_username, jira_password))


markdown_table_header = '| Commit(s) | Changed Files |'
markdown_table_header_seperator = '|---|---|'


file = open('bugfixes.md','w') 

file.write('# Achieved Bugfixes')
file.write('\n')
file.write('\n')

for issue in jira.search_issues(
    'issuetype = Bug AND (assignee = currentUser() OR "Assignee\'s" = currentUser()) AND Sprint = 6 AND status = Done ORDER BY updated'
):
    issue_link = jira_server + "/browse/" + issue.key
    markdown_issue_link = "[" + issue.key + "](" + issue_link + ")"
    file.write("## " + markdown_issue_link + " / " + issue.fields.summary)
    file.write('\n')
    file.write('\n')
    file.write("### Description")
    file.write('\n')
    file.write('\n')
    if issue.fields.description is not None:
        file.write(re.sub(r'{.+?}', '', issue.fields.description))
    file.write('\n')
    file.write('\n')
    file.write("### Commits")
    file.write('\n')
    file.write('\n')
    if issue.fields.customfield_10204 is not None:
        for mr in gl_mrs:
            if mr.attributes['web_url']  == issue.fields.customfield_10204:
                markdown_table_lines = list()
                for item in mr.commits():
                    markdown_table_cell_commit = ''
                    markdown_table_cell_changed_files = ''
                    markdown_table_cell_commit += item.attributes['author_name'] + ' - [' + item.attributes['title'] + '](' + item.attributes['web_url'] + ')' + '<br>'
                    for diff in item.diff():
                        markdown_table_cell_changed_files += diff['new_path'] + '<br>'
                    markdown_table_line = '| ' + markdown_table_cell_commit + ' | ' + markdown_table_cell_changed_files + ' | '
                    markdown_table_lines.append(markdown_table_line)
                markdown_table = markdown_table_header + '\n' + markdown_table_header_seperator + '\n'
                for markdown_table_line in markdown_table_lines:
                    markdown_table += markdown_table_line + '\n'
                file.write(markdown_table)
    file.write('\n')
    file.write('\n')
file.close()