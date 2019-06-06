#!/usr/bin/env bash
root=~/Documents/ChromeOS/ChromeBook/00Manual/Python/python_weekly/game/WechatJumpApp/wechat_jump_game-master/Tools/platform-tools/

for i in {90..134}
do
  read -p "Continue:"
  ${root}/adb shell screencap -p /sdcard/Q.png
  ${root}/adb shell input tap 500 1250
  ${root}/adb shell input tap 500 1320
  ${root}/adb shell input tap 500 1000
  sleep 0.1
  ${root}/adb shell screencap -p /sdcard/A.png
  ${root}/adb pull /sdcard/Q.png ~/Desktop/Q/Q${i}.png
  ${root}/adb pull /sdcard/A.png ~/Desktop/A/A${i}.png
  echo "capture question ${i} screenshot successfully!"
done
echo "finished !!!"

