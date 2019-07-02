cd /home/${USER}/src/Odm/odm_ws
dt=`date '+%d_%m_%Y_%H_%M_%S'`
mkdir -p ${dt}/images
cp -r /home/${USER}/src/Odm/offlinemap/stamped* ${dt}/images
echo ${dt}" folder created in odm_ws"
cd /home/${USER}/src/Odm/ODM
sudo ./run.sh ${dt}
echo "next step ./run.sh "${dt}
cd /home/${USER}/src/Odm/odm_ws/${dt}/odm_orthophoto
xdg-open odm_orthophoto.png
