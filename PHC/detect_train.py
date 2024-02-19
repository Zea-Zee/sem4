from roboflow import Roboflow

api_file = open('signs_roboflow_api.txt', 'r')
api_str = str(api_file.readline().strip())
rf = Roboflow(api_key=api_str)
project = rf.workspace("nsu-sxhmy").project("first_seminar")
dataset = project.version(1).download("yolov8")
