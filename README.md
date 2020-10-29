# 概要

安川電機製ロボットコントローラYRC1000からイーサネット経由でデータを取得するマイクロサービスです。

このマイクロサービスをご利用いただくには、別途安川電機製ロボットコントローラYRC1000が必要となります。

## セットアップ手順

### aion-coreをセットアップする

事前に下記リポジトリからaion-coreのセットアップを行ってください。

https://github.com/latonaio/aion-core

### ベースイメージを準備する

下記リポジトリからベースイメージlatonaio/l4tを用意してください。

https://github.com/latonaio/python-base-images

### リポジトリをクローンする

このリポジトリをgit cloneしてください

git clone https://github.com/latonaio/control-yaskawa-robot-r-kube.git

### Dockerイメージをビルドする

付属のスクリプトを使用して、control-yaskawa-robot-rのDockerイメージをビルドしてください。
```
bash docker-build.sh
```

### 設定ファイルを配置する

command_list.jsonとtrigger_list.jsonを、以下のフォルダに配置します。

/var/lib/aion/(ネームスペース名)/Data/control-yaskawa-robot-r_1

command_list.jsonの例
```
{
  "command": [
    {
      "command": "89",
      "detail": "system information",
      "elementNo": "00",
      "processNo": "01",
      "arrayNo": [
        "11",
        "101"
      ],
      "interval": 86400000,
      "expire_time": 172800
    }
  ]
}

```

trigger_list.jsonの例
```
{
  "command": [
    {
      "trigger": {
        "command": "78",
        "arrayNo": 3001,
        "elementName": "IO",
        "conditions": ">255",
        "always": 0
      },
      "connectionKey": "alpha",
      "metadata": [
        {
          "camera": "on"
        }
      ]
    }
  ]
}
```

### aion-coreの設定ファイルに起動設定を書く

project.ymlに起動設定を追記してください。

例）
```
  control-yaskawa-robot-r:
    command: python3 -m robot_data
    startup: yes
    always: yes
    scale: 1
    env:
      ROBOT_IP_01: "192.168.100.2"
```

### AIONを起動する

aion-core-manifestsの起動ファイルでAIONを立ち上げます。
