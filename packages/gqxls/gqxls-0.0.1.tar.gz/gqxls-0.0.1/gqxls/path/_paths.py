import os


class paths:
    def get_document_names(self,path:str,endswith:str='',path_or_name:bool=True,get_folder:bool=False)->list:
        try:
            path = os.path.abspath(path)
            if not os.path.exists(path):
                raise FileNotFoundError(f"path:{path}不存在")
            else:
                path_names = os.listdir(path)
                if path_or_name==True:
                    for i in range(len(path_names)):
                        path_names[i] = os.path.join(path, path_names[i])
                new_path_names = list()
                dict=[".pdf",'.png','.jpg','.jpeg','.txt','.doc',
                      '.docx','.gif','.mp4','.mp3','.avi','.wav',
                      '.xls','.xlsx','.ppt','.pptx','.zip','.exe'
                      ,'.rar','.mov','.bak','.htm','.html']
                if get_folder== True and endswith=='':
                    new_path_names=path_names
                    return new_path_names
                elif get_folder==False and endswith!='' and endswith.lower() in dict:
                    for name in path_names:
                        if name.endswith(endswith):
                            new_path_names.append(name)
                    return new_path_names
                else:
                    raise ValueError(f"endwith:{endswith}和get_folder:{get_folder}参数错误")
        except:
            raise ValueError(f"path:{path}参数错误")

    def maker_path(self,path:str)->None:
        try:
            if not os.path.exists(path):
                os.mkdir(path)
        except:
            raise ValueError(f"path:{path}参数错误")
