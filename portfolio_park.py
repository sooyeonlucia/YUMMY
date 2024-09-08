#portfolio_park


import os
import sys
import json

sys.path.append("/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages")
sys.path.append("/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages")
from shotgun_api3 import shotgun

link = "https://4thacademy.shotgrid.autodesk.com/"
script_name = "test_park"
script_key = "snljjtxjfyfdxQfpnh7lgyf!f"

# json_file_path = '/Users/lucia/Desktop/sub_server/script/project_data-2.json'

class PathFinder():
    def __init__(self):
        pass
        # self.json_file_path = '/Users/lucia/Desktop/sub_server/script/project_data-2.json'
    
    def _read_json_file(self, json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        return json_data

    def _get_project_id(self):
        json_file = self._read_json_file(json_file_path)
        project_id = json_file.get('project_id')
        return project_id
    
class MainPublish():
    def __init__(self) :
        PF = PathFinder()
        self.project_id = PF._get_project_id()

    def connect_sg(self):
    # 샷그리드 연결
        sg = shotgun.Shotgun(link, script_name, script_key) #Shotgun 다시 불러와야?
        return sg

    def _get_sg_validation_list(self, sg, project_id):
        # 프로젝트의 versions 데이터 가져오기 
        # sg = self.connect_sg()
        # project_id = 222
        ver_datas = []

        if project_id:
            filters = [["project", "is", {"type": "Project", "id": project_id}]]
            fields = ["code", "sg_extension", "sg_colorspace_1", "sg_nk_version"]
            versions = sg.find("Version", filters=filters, fields=fields)

            for version in versions:
                code = version.get("code", "N/A")                           #이름
                # sg_status_list = version.get("sg_status_list", "N/A")       #status   
                extension = version.get("sg_extension", "N/A")        #type
                color = version.get("sg_colorspace_1", "N/A")                 #color space
                nuke_ver = version.get("sg_nk_version", "N/A")

                ver_datas.append({
                    "version_name": code,         
                    "extension" : extension,
                    "colorspace" : color,
                    "nuke_ver" : nuke_ver
                    })

        # print(ver_datas)
        return ver_datas

    def _get_sg_validation_info(self, name, list):
        # name = self.name_without_ext
        # list = self._get_sg_validation_list(sg, project_id)
        for k in list:
            if k['version_name'] == name:
                return k
            else : 
                pass
        print("the version is not in shotgrid ;( ")
        return None

    #==================================================================
#협업한, UI 개발 팀원의 데이터 불러오는 코드 
    def _get_nk_validation_info(self):

        nk_file_validation_dict = {}
        root = nuke.root()
        path = root["name"].value()                     # file path
        extend = path.split(".")[-1]                    # extendation
        colorspace = root["colorManagement"].value()    # colorspace
        nuke_version = nuke.NUKE_VERSION_STRING         # nk version
        
        nk_file_validation_dict["file_path"] = path
        nk_file_validation_dict["extension"] = extend
        nk_file_validation_dict["colorspace"] = colorspace
        nk_file_validation_dict["nuke_ver"] = nuke_version

        return nk_file_validation_dict

    def _get_exr_validation_info(self, file_path):

            file_validation_info_dict = {}
            probe = ffmpeg.probe(file_path)

            # extract video_stream
            video_stream = next((stream for stream in probe['streams']if stream['codec_type'] == 'video'),None)
            codec_name = video_stream['codec_name']
            colorspace = video_stream.get('color_space', "N/A")
            width = int(video_stream['width'])
            height = int(video_stream['height'])
            frame = 1
            # a = video_stream.keys()
            # print(a)

            resolution = f"{width}x{height}"

            # file_validation dictionary
            file_validation_info_dict = {
                "file_path": file_path,
                "codec_name": codec_name,
                "colorspace": colorspace,
                "resolution": resolution,
                "frame": frame
            }
            # print(file_validation_info_dict)
            return file_validation_info_dict
    
    def _get_mov_validation_info(self, file_path):

            file_validation_info_dict = {}
            probe = ffmpeg.probe(file_path)

            # extract video_stream
            video_stream = next((stream for stream in probe['streams']if stream['codec_type'] == 'video'),None)
            codec_name = video_stream['codec_name']
            colorspace = video_stream.get('color_space', "N/A")
            width = int(video_stream['width'])
            height = int(video_stream['height'])
            frame = int(video_stream['nb_frames'])
            # a = video_stream.keys()
            # print(a)

            resolution = f"{width}x{height}"

            # file_validation dictionary
            file_validation_info_dict = {
                "file_path": file_path,
                "codec_name": codec_name,
                "colorspace": colorspace,
                "resolution": resolution,
                "frame": frame
            }
            # print(file_validation_info_dict)
            return file_validation_info_dict

    #==================================================================

#현재 version data에는 다양한 key가 있음. nk, exr, mov data도 validate할 내용이 제각각임
#따라 key값이 같은 내용만 서로 비교하도록 작성
    def validate_nuke(self, sg_dict, val_nk):
        # if sg_dict is None or val_nk is None:             
        #     return None
        print("nuke 검증을 시작합니다.")
        all_right = True                                    #모든 값이 같을 경우 True (default)
        for sg_key in sg_dict.keys():                       #모든 sg_key에 대해서 조사
            if sg_key in val_nk:                          #비교하는 대상 dict에도 같은 key가 있을 때
                if sg_dict[sg_key] == val_nk[sg_key] :    #value가 같을 때
                    print(sg_key + "가 같습니다.")
                else : 
                    print(sg_key + "가 다릅니다.")
                    all_right = False                       #다른 내용이 있으면 틀린 내용이 있음을 밝혀줌
            else : pass             #key값이 다르면 pass 
        print("nuke 파일 검증을 마쳤습니다.")

        if all_right == True :
            print("모두 값이 같습니다.")
        else : 
            print("다른 값이 있습니다. 다시 한번 확인해주세요.")

        return all_right

    def validate_exists(self, val_exr_mov):
        print("value가 있는지 검증합니다.")
        result = True
        for k in val_exr_mov:
            if val_exr_mov.get(k) is not None:
                pass
            else :
                result = False
                break
        print("검증을 마쳤습니다.")
        if result == True : 
            print("값이 모두 존재합니다.")
        else : 
            print("빈 값이 있습니다.")
        return result

    def _make_val_dict_and_val(self, result_nk, result_exr, result_mov):
        # sg = self._get_sg_validation_info()
        # nk = self._get_nk_validation_info()               #현재 UI와 연결되어있지 않아 json 파일로 대체
        # exr = self._get_exr_validation_info()
        # mov = self._get_mov_validation_info()

        # result_nk = self.validate_each(sg, nk)              #result = True, False
        # result_exr = self.validate_each(sg, exr)
        # result_mov = self.validate_each(sg, mov)

        results = {
            'result_nk' : result_nk,                        #True, False, None
            'result_exr' : result_exr,
            'result_mov' : result_mov
        }

        for key in list(results.keys()):
            if results[key] is None:                        #비교 대상이 아니었던 내용은 제외한다            
                results.pop(key)

        some_wrong = False
        for key, value in results.items():
            if value is True : 
                print(key + " is validated.")
            else : 
                print(key + " is wrong.")                   #틀린 내용이 발생했음
                some_wrong = True

        if not some_wrong:                                  #some wrong = False 
            print("all the things are True.")
            print("now start to copy, also upload in shotgrid")     #틀린 내용이 없기 때문에 version up, main server 업로드, shotgrid 업로드 시작

        else :                                              #some wrong = True
            user = input("want to force to upload? Y/N : ")           #강제로라도 업로드 하고 싶은지 묻는 과정
            if user == "Y" : 
                print("okay, now force to act.")
                some_wrong = False
            else : 
                print("then validate again.")
                some_wrong = True

        return some_wrong                       

    def make_upload_data(self):
        sg = self.connect_sg()

        PF = PathFinder()
        json_file_path = "/Users/lucia/Desktop/sub_server/script/project_data-2.json"
        login_json = PF._read_json_file(json_file_path)                     #로그인 시 할당받아와야 하는데 임의로 일단 지정
        project_id = login_json.get('project_id', 'N/A')
        user_name = login_json.get('name', 'N/A')
        user_id = login_json.get('user_id', 'N/A')
        
        name_true = 'PKG_030_mm_v100'
        # name_wrong = 'PKG_030_mm_v101'
        part = name_true.split('_')
        shot = part[0] + '_' + part[1]
        team = part[2]
        version = part[3]

        data = []
        if project_id : 
            filters = [["project", "is", {"type": "Project", "id": project_id}]]
            to_use= sg.find("Version", filters = filters)
        if to_use : 
            code = shot + "_" + team + "_" + version
            # file_type = self._get_nk_validation_info_.get('extension')        #원래는 validation data 를 가져와야함
            file_type = "nk"
            # colorspace = self._get_nk_validation_info.get('colorspace')
            colorspace = "OCIO"
            # version_nuke = self._get_nk_validation_info_.get('nuke_ver')
            version_nuke = "15.1v1"
            # description ; UI에 입력된 설명 가져와야함
            description = "uploaded"

            data = {
                "project" : {"type": "Project", "id" : project_id},
                "code" : code,
                "sg_status_list" : "wip",           #pub, sc                    #version에 올리므로 아직은 wip
                "user": {"type" : "HumanUser", "name" : user_name, "id" : user_id},
                "sg_extension" : file_type,         #nk
                "sg_colorspace_1" : colorspace,
                "description" : description,
                "sg_nk_version" : version_nuke
            }
            return data

    def sg_create_ver(self):
        ver_data = self.make_upload_data()
        new_version = sg.create('Version', ver_data)
        # print ("version 생성이 완료되었습니다.")                #print -> Qmessage
        new_version_id = new_version["id"]
        return new_version_id

    def sg_thumbnail_upload(self):
        # path = self.generate_nk_thumbnail_from_file()             #UI에서 png로 썸네일을 만들고, 저장된 path를 가져온다
        path = '/Users/lucia/downloads/IMG_3764.JPG'
        tmb_id = self.sg_create_ver()
        field_name = "image"
        sg.upload("Version", tmb_id, path, field_name = field_name)  #샷그리드는 썸네일을 올릴 version이 특정화 되어있어야 올라간다
        print("version과 thumbnail이 잘 올라갔습니다.")


#setup data
PF = PathFinder()
file_path = "/Users/lucia/Desktop/sub_server/script/"
json_file_path = file_path + "project_data-2.json"
json_nuke_path = file_path + "json_nuke.json"
json_exr_path = file_path + "json_exr.json"
json_mov_path = file_path + "json_mov.json"

login_json = PF._read_json_file(json_file_path)
json_nuke = PF._read_json_file(json_nuke_path)
json_exr = PF._read_json_file(json_exr_path)
json_mov = PF._read_json_file(json_mov_path)
project_id = PF._get_project_id()


test_name_right = 'PKG_030_mm_v100'
test_name_wrong = 'PKG_030_mm_v101'                 #테스트를 위해 임의로 이름 설정

Publish = MainPublish()
sg = Publish.connect_sg()               #샷그리드 연결
sg_version_dict_list = Publish._get_sg_validation_list(sg, project_id)                      #샷그리드에서 version 데이터 가져옴
sg_version_dict = Publish._get_sg_validation_info(test_name_right, sg_version_dict_list)  #version 중 이름과 매치되는 dict만 불러옴

print(sg_version_dict)
# print(json_nuke)
# print(json_exr)
# print(json_mov)

result_nk = Publish.validate_nuke(sg_version_dict, json_nuke)
result_exr = Publish.validate_exists(json_exr)
result_mov = Publish.validate_exists(json_mov)

# print(result_nk)
# print(result_exr)
# print(result_mov)

val = Publish._make_val_dict_and_val(result_nk, result_exr, result_mov)
print(val)


if val == False : 
    sg_data = Publish.make_upload_data()
    upload = Publish.sg_create_ver()
    thumbnail = Publish.sg_thumbnail_upload()


    # Publish.sg_version_upload(sg, json_nuke)


