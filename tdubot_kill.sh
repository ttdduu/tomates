pid=$(pgrep -f '/home/tdu/code/tomates/tdubot.py' | sed '/^$/d')
kill $pid
