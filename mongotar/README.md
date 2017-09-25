命令行指令


Git 全局设置

git config --global user.name "Administrator"
git config --global user.email "admin@example.com"

创建新版本库

git clone git@192.168.9.250:root/mongotar.git
cd mongotar
touch README.md
git add README.md
git commit -m "add README"
git push -u origin master

已存在的文件夹或 Git 仓库

cd existing_folder
git init
git remote add origin git@192.168.9.250:root/mongotar.git
git add .
git commit
git push -u origin master