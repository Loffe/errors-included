arch=`uname -m`
if [ $arch == "arm" ]; then
    run-standalone.sh python2.5 $1 2>&1 | grep -v sem_post;
else
    run-standalone.sh python2.5 $1
fi
