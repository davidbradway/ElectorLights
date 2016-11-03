#!/bin/bash
sudo service electorlights.sh status| grep 'FAIL\|failed' > /dev/null 2>&1
if [ $? != 0 ]
then
    echo "Still running"
    sudo service electorlights.sh status
else
    echo "FAILED"
    sudo service electorlights.sh start
fi
