import requests

filename = 'example.md'

def fix_gif(text, from_position = 0):
    end_position = text.find('.gif', from_position)
    if end_position == -1:
        return text
    else:
        end_position += 4
    start_position = text.rfind('https://', from_position, end_position)
    if start_position == -1:
        return text
    new_file = download(text[start_position:end_position])
    text = text[:start_position] + new_file + text[end_position:]
    return fix_gif(text, start_position + len(new_file))

def download(uri, path = 'img'):
    name_start_position = uri.rfind('/')
    name = uri[name_start_position:]
    if name == '/giphy.gif':
        name = uri[uri.rfind('/', 0, name_start_position):].replace('/giphy', '')
    if name == "":
        return uri
    with open(path + name, 'wb') as f:
        f.write(requests.get(uri).content)
    return path + name


with open(filename, 'r+') as file: 
    text = fix_gif(file.read())
    file.seek(0)
    file.truncate()
    file.write(text)
