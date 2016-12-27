开机自动运行需要加入以下命令

sudo 
nano /etc/rc.local
在/etc/rc.local的文件中间加入
sleep 10
sudo rm -rf /home/pi/Desktop/test.jpg
sudo python /home/pi/Desktop/PiCameraRig-master/run.py
最后reboot

todo：
1. ffmpeg streaming， 通过mqtt开通和关闭
2. 自动更新和下载最新程序
3. 上传logging的数据
4. 加入2轴转动的马达
