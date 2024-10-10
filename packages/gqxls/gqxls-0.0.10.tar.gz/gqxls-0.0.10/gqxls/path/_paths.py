import os
from typing import List, Union


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
                elif get_folder==False and endswith=='':
                    for name in path_names:
                        if not name.endswith(''):
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


class file_path:
    def __init__(self,get_folder:bool=False)->None:
        """
        Brief Introduction

        Args:
            get_folder:获取文件夹名称,True or False
        """
        self.get_folder=get_folder
    def get_document_names(self,path:Union[str,List[str]])->List[tuple]:
        """
        Brief Introduction

        Args:
            path:文件路径或集,str or List[str]

        Returns:
            List[tuple]:[(全名,标题,后缀)]
        """
        if path == '' or path == None or path == []:
            raise ValueError(f"path:{path}配置为空")
        else:
            if self.path_exist(path)==True:
                head,tail=os.path.splitext(os.path.abspath(path))
                if tail=='':
                    name=os.listdir(path)
                    new_name=list()
                    for i in name:
                        if self.get_folder==True:
                            name,ends=os.path.splitext(i)
                            new_name.append(tuple([i,name,ends]))
                        else:
                            if os.path.splitext(i)[1]!='':
                                name,ends=os.path.splitext(i)
                                new_name.append(tuple([i,name,ends]))
                    return new_name
                else:
                    name,ends=os.path.splitext(tail)
                    new_name=list()
                    new_name.append(tuple([path,name,ends]))
                    return new_name
            elif self.path_exist(path)==False:
                raise FileNotFoundError(f"path:{path}缺失")
    def path_exist(self,path:Union[str,List[str]])->bool:
        """
        Brief Introduction

        Args:
            path:文件路径或集,str or List[str]

        Returns:
            bool:存在->True 不存在->False
        """
        if path=='' or path==None or path==[]:
            raise ValueError(f"path:{path}配置为空")
        else:
            if isinstance(path,str) and os.path.exists(path):
                return True
            elif isinstance(path,list) and all(isinstance(i,str) for i in path) and all(os.path.exists(i) for i in path):
                return True
            else:
                return False
    def get_document_paths(self,path:Union[str,List[str]])->List[tuple]:
        """
        Brief Introduction

        Args:
            path:文件路径或集,str or List[str]

        Returns:
            List[tuple]:[(绝对路径,前置路径,标题,后缀)]
        """
        if path == '' or path == None or path == []:
            raise ValueError(f"path:{path}配置为空")
        else:
            if self.path_exist(path)==True:
                head,tail=os.path.splitext(os.path.abspath(path))
                if tail=='':
                    name=os.listdir(path)
                    new_name=list()
                    for i in name:
                        if self.get_folder==True:
                            title,ends=os.path.splitext(i)
                            new_name.append(tuple([os.path.join(head,i),head,title,ends]))
                        else:
                            if os.path.splitext(i)[1]!='':
                                title,ends=os.path.splitext(i)
                                new_name.append(tuple([os.path.join(head,i),head,title,ends]))
                    return new_name
                else:
                    title,ends=os.path.splitext(tail)
                    new_name=list()
                    new_name.append(tuple([path,head,title,ends]))
                    return new_name
            elif self.path_exist(path)==False:
                raise FileNotFoundError(f"path:{path}不存在")
    def path_no_exit(self,path:Union[str,List[str]])->list:
        """
        Brief Introduction

        Args:
            path:文件路径或集,str or List[str]

        Returns:
            list:[不存在路径]
        """
        if path == '' or path == None or path == []:
            raise ValueError(f"path:{path}配置为空")
        else:
            if self.path_exist(path)==True:
                return list()
            else:
                no_exit=list()
                if isinstance(path,str):
                    no_exit.append(os.path.abspath(path))
                else:
                    for i in path:
                        if isinstance(i,str)==True and self.path_exist(i)==False:
                            no_exit.append(os.path.abspath(i))
                        elif isinstance(i,str)==False:
                            raise TypeError(f"path:{i}类型错误")
                return no_exit
    def file_maker(self,path:Union[str,List[str]])->None:
        """
        Brief Introduction

        Args:
            path:文件路径或集,str or List[str]

        Returns:
            None:创建不存在路径
        """
        if path == '' or path == None or path == []:
            raise ValueError(f"path:{path}配置为空")
        else:
            if isinstance(path,str)==True and self.path_exist(path)==False:
                os.mkdir(path)
            elif isinstance(path,list)==True and self.path_exist(path)==False and self.path_no_exit(path)!=[]:
                for i in self.path_no_exit(path):
                    os.mkdir(i)

class is_path(file_path):
    def __init__(self):
        super().__init__()
    def is_str_path(self,path:str)->bool:
        """
        Brief Introduction

        Args:
            path:文件路径,str

        Returns:
            bool:存在->True 不存在->False
        """
        if path== '' or path == None or path==[]:
            raise ValueError(f"path:{path}配置为空")
        else:
            if isinstance(path,str)==True and self.path_exist(path)==True:
                return True
            else:
                return False
    def is_list_path(self,path:List[str])->bool:
        """
        Brief Introduction

        Args:
            path:文件路径,List[str]

        Returns:
            bool:全部存在->True 不完全存在->False
        """
        if path == '' or path == None or path == []:
            raise ValueError(f"path:{path}配置为空")
        else:
            if isinstance(path,list)==True and self.path_exist(path)==True:
                return True
            else:
                return False

