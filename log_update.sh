#!/bin/bash

# リポジトリへのパス。これを適切なものに変更してください。
REPO_PATH="TakutoIyanagi-littletree/st-chatgpt"

# 更新したいファイルのパス
FILE_PATH="$REPO_PATH/qa_log.txt"

# Gitリポジトリに移動
cd $REPO_PATH

# ファイルを更新（ここでは例としてファイルに日付と時刻を追加）
echo "Updated on $(date)" >> $FILE_PATH
echo ファイルに追記する >> file.txt

# 変更をステージング
git add $FILE_PATH

# コミットを作成
git commit -m "Updated the file with the current date and time"

# リモートリポジトリにプッシュ
git push origin master

echo "File updated and pushed to GitHub"

git config --global user.email "little.lab829@mail.com"
git config --global user.name "TakutoIyanagi-littletree"
