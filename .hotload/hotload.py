from microWebSrv import MicroWebSrv
import json
import os

@MicroWebSrv.route('/')
def homepage(httpClient, httpResponse):
    print('homepage visited!')
    content = json.dumps(
        dict(code=0, message='hello from micropython server!'))
    httpResponse.WriteResponseOk(headers=None,
                                 contentType="text/html",
                                 contentCharset="UTF-8",
                                 content=content)


@MicroWebSrv.route('/change-file', 'POST')
def handleChange(httpClient, httpResponse):
    formData = httpClient.ReadRequestPostedFormData()
    event_type = formData['event_type']
    filename = formData['filename']
    # content = formData['content']

    if event_type == 'file_modified':
        with open(filename, 'w') as f:
            f.write(formData['content'])

    if event_type == 'file_deleted':
        try:
            os.remove(filename)
        except:
            pass
    
    if event_type == 'directory_deleted':
        files = os.listdir(filename)
        if files:
            for f in files:
                try:
                    os.remove(filename+'/'+f)
                except:
                    pass

        os.rmdir(filename)
        
    if event_type == 'file_created':
        with open(filename,'w') as f:
            f.write('')
    
    if event_type == 'directory_created':
        try:
            os.mkdir(filename)
        except:
            pass

    if event_type == 'directory_moved':
        dest_path = formData['dest_path']
        try:
            os.rename(filename,dest_path)
        except:
            pass
            
    if event_type == 'file_moved':
        dest_path = formData['dest_path']
        try:
            os.rename(filename,dest_path)
        except:
            pass

    content = json.dumps(dict(code=0, message='%s hotload done.' % filename))
    httpResponse.WriteResponseOk(headers=None,
                                 contentType="text/html",
                                 contentCharset="UTF-8",
                                 content=content)

def hotloader():
    _hotloader = MicroWebSrv()
    return _hotloader
    
