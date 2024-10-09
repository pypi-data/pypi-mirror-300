from typing import List, Union ,Literal
import os, fitz
from concurrent.futures import ThreadPoolExecutor
from ..information import gain
from ..path import paths
from ._convert_main import convert_main
class pdf_convert:
    def __init__(self,theard_pool:bool=False,sigle_document:bool=False,max_workers:int=4) ->None:
        self.theard_pool=theard_pool
        self.single_document=sigle_document
        self.max_workers=max_workers
    def pdf_to_picture(self,pdf_paths:Union[str, List[str]],image_path:str,dpi:int=300):
        if self.single_document:
            if not isinstance(pdf_paths, str):
                raise ValueError(f"pdf_paths:{pdf_paths}参数类型错误，请输入str类型")
            else:
                if os.path.isfile(pdf_paths):
                    paths().maker_path(image_path)
                    xian_pool = ThreadPoolExecutor(max_workers=self.max_workers)
                    if self.theard_pool:
                        for pages_number in range(fitz.open(pdf_paths).page_count):
                            xian_pool.submit(convert_main().signal_pdf_to_image,pdf_paths,
                                             image_path,pages_number,str(pages_number+1),dpi)
                        xian_pool.shutdown()
                    else:
                        for pages_number in range(fitz.open(pdf_paths).page_count):
                            convert_main().signal_pdf_to_image(pdf_paths, image_path, pages_number,
                                             str(pages_number + 1), dpi)
                else:
                    raise FileExistsError(f"pdf_paths:{pdf_paths}文件不存在")
        else:
            if not isinstance(pdf_paths, list) or not all(isinstance(path, str) for path in pdf_paths):
                raise ValueError(f"pdf_paths:{pdf_paths}参数类型错误，请输入list[str]类型")
            else:
                if not all(os.path.isfile(path) for path in pdf_paths):
                    raise FileExistsError(f"pdf_paths:{pdf_paths}文件缺失")
                else:
                    paths().maker_path(image_path)
                    image_name_list=list()
                    for image_name in range(len(pdf_paths)):
                        image_name_list.append(os.path.join(image_path,gain().get_random_file_name(12)))
                    for image_name in image_name_list:
                        paths().maker_path(image_name)
                    xian_pool=ThreadPoolExecutor(max_workers=self.max_workers)
                    if self.theard_pool:
                        for pdf_count in range(len(pdf_paths)):
                            for pages_number in range(fitz.open(pdf_paths[pdf_count]).page_count):
                                xian_pool.submit(convert_main().signal_pdf_to_image,pdf_paths[pdf_count],
                                                 image_name_list[pdf_count],pages_number,str(pages_number+1),dpi)
                        xian_pool.shutdown()
                    else:
                        paths().maker_path(image_path)
                        image_name_list = list()
                        for image_name in range(len(pdf_paths)):
                            image_name_list.append(os.path.join(image_path, gain().get_random_file_name(12)))
                        for image_name in image_name_list:
                            paths().maker_path(image_name)
                        for pdf_count in range(len(pdf_paths)):
                            for pages_number in range(fitz.open(pdf_paths[pdf_count]).page_count):
                                convert_main().signal_pdf_to_image(pdf_paths[pdf_count],image_name_list[pdf_count],
                                                                   pages_number,str(pages_number+1),dpi)

