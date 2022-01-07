<h2>Special Effects Makeup Demo Server</h2>


<h3>Enviroment</h3>

``` shell
conda create -n MyServer python=3.9.7
conda activate MyServer

conda install opencv
conda install django
conda install pytorch torchvision torchaudio cpuonly -c pytorch
```

<h3>Download Models</h3>

Download models from <a href="https://drive.google.com/drive/folders/1EbizvJtzX5zqOnCxKxSt1X_ROk19hgSL?usp=sharing">here</a><br>
You need put them into **CG_Final_face_gan/CG_Final_Server/PredictPage/models/**

<h3>Run Server</h3>

Change directory to **CG_Final_face_gan/CG_Final_Server** folder, then run following command

``` shell
python .\manage.py runserver
``` 
Now you can access our app at http://127.0.0.1:8000/temp/
