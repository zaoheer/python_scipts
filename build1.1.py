#!/usr/bin/env python
#_*_ coding: utf-8 _*_
import os,sys,time
#判断参数个数，用法提示
Len_args=len(sys.argv)
if Len_args < 5:
    print "Usage:  ./build  项目名称(Lot|Lop|Los)  Tag(eg. x.x.x.yyyymmdd)   配置文件  环境名称   【Items】"
    sys.exit()

#传参附值
ProjectName=sys.argv[1]
if ProjectName not in ('Lot','Lop','Los'):
    print "Error,No This Project"
    sys.exit()
    
Tag=sys.argv[2]

ConfigFile=sys.argv[3]
if os.path.exists(ConfigFile) is not True:
    print "Error,the config file is not exists, exit !!!"
    sys.exit()
EnvName=sys.argv[4]
Items=''
if Len_args > 5:
    Items=sys.argv[5]

#从SVN下载
Base="svn://172.16.22.205/uuzz-yunwei/Test"
PackageDir="update/"+EnvName+"/"+ProjectName+"/"+Tag
SVNdir="svn/"+ProjectName
if os.system('ping -c 1 -t 3 172.16.22.205 >/dev/null') !=0:
    print "Error,connect SVN server timeout,exit!!"
    sys.exit()
command_svn_export="svn export "+Base+"/"+ProjectName+"/"+Tag+"/"+"pkg/app/ --force " +SVNdir +" --username 'zhangguangwei' --password 'zhanggw@uuzz.comSW@' --no-auth-cache #--non-interactive -q"
#print command_svn_export
if os.path.exists(SVNdir):
    YesorNO=raw_input("The SVN tags in local already  exists ,Do you wanna download it again?  Y|N: ")
    YesorNO=YesorNO.lower()
    if YesorNO == "y":
        os.system("rm -rf "+ SVNdir)
        DownResult=os.system(command_svn_export)
        if  DownResult != 0:
            print "Download from SVN  error, exit !"
            sys.exit()
        print  "Download from SVN  successful!"
    print "Cancel download from SVN server!!!"

else:
    DownResult=os.system(command_svn_export)
    if  DownResult != 0:
        print "Download from SVN  error, exit !"
        sys.exit()
    print  "Download from SVN  successful!"



#更新ices
iceFiles=os.popen("find "+SVNdir+"  -name " + Items + "*.tar.gz |grep ice")
for ice in  iceFiles.readlines():
    icePath=ice.strip("\n")
    iceDir=os.path.dirname(icePath)
    icename=os.path.basename(iceDir)
    print "start update "+ icename +"....."
    
    #解压压缩包
    #autoResult=os.system("cd " + iceDir + " &&  unzip -q *.zip  &&  rm -f *.zip " ) 
    autoResult=os.system("cd " + iceDir + " &&  tar xvp -f *.tar.gz  &&  rm -f *.tar.gz " ) 
    if autoResult != 0 :
        print "decompression error deal with " +icename
        continue
        
    findJar_command="find "+iceDir+" -name "+icename+"*.jar"
    jarPath=os.popen(findJar_command)
    jarPath=''.join(jarPath.readlines()).strip('\n')
    #print jarPath
    #更新icenode配置文件
    updateConfig_command="autoconfig  -u "+ConfigFile+" "+jarPath
    print updateConfig_command
    autoResult=os.system(updateConfig_command)
    if autoResult !=0 :
        print "Update configure file error deal with "+icename
        continue
    
    #压缩回去
    time.sleep(1) 
    #compress_command=" cd " + iceDir +" && cd  "+icename+"* && mv * .. && cd .. && rmdir "+icename+"*  && tar --remove-files  -cpz -f " + icename + ".tar.gz * "   #tar 包去顶目
    compress_command="cd " + iceDir +"  && tar --remove-files  -cpz -f " + icename + ".tar.gz * "  #tar 包保顶目
    compress_Result=os.system(compress_command)
    if compress_Result != 0:
        print "Compress error  deal with "+icename
        continue
    print icename +  " update Successfull !!!\n\n\n\n"
    
#更新War包
war_command="find " +SVNdir +" -name *.war"
autoResult=os.popen(war_command)
for warPath in  autoResult.readlines():
    warPath=warPath.strip('\n')
    updatewar_command="autoconfig -u "+ConfigFile+" "+warPath
    print updatewar_command
    os.system(updatewar_command)
#复制更新过的包到指定目录
if os.path.exists(PackageDir) is True:
    baseDir=os.path.dirname(PackageDir)
    baseName=os.path.basename(PackageDir)
    os.system("cd "+baseDir+"&& rm -rf "+baseName)
print "Copy  files  to "+PackageDir
cp_command="mkdir -p "+ PackageDir+" && find  "+SVNdir + " -name '*.tar.gz' -o -name '*.war' |xargs -I {} cp  {} "+PackageDir+" "

copyResult=os.system(cp_command)
if copyResult !=0 :
    print "ERROR ,copy  files "
else:
    print "Copy files OK"
