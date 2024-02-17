git clone https://github.com/ultralytics/yolov5.git
cd yolov5/
pip install -r requirements.txt
python3 train.py --img 896 --batch 8 --epochs 1 --data '/home/zea/Desktop/sem4/PHC/dataset.yaml' --weights '/home/zea/Desktop/sem4/PHC/yolov5x.pt' --cache
python3 detect.py --source '/home/zea/Desktop/sem4/PHC/cars_dataset/test/images' --weights '/content/yolov5/runs/train/exp/weights/last.pt' --img 896 --save-txt --save-crop --project "/home/zea/Desktop/sem4/PHC/proj" --name 'experiment_1'





python3 detect.py --source '/home/zea/Desktop/sem4/PHC/cars_dataset/test/images' --weights '/content/yolov5/runs/train/exp/weights/last.pt' --img 896 --save-txt --save-crop --save_dir '/home/zea/Desktop/sem4/PHC/res/'
python detect.py --source '/home/zea/Desktop/sem4/PHC/cars_dataset/test/images' --weights '/content/yolov5/runs/train/exp/weights/last.pt' --img 896 --save-txt --save-crop
