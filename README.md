# 概要

安川電機製ロボットコントローラYRC1000からイーサネット経由でデータを取得するマイクロサービスです。

このマイクロサービスをご利用いただくには、別途安川電機製ロボットコントローラYRC1000が必要となります。

## このマイクロサービスの振る舞い

### 入力

なし

### 出力

```
"metadata" {
      "RobotData": {
            "Command": コマンド番号(16進数値の文字列変換),
            "Result": 処理成否(True/False),
            "ExpireTime": データ保持期間(ms),
            "BaseObjectType": ベースオブジェクトタイプ(文字列),
            "ComponentType": コンポーネントタイプ(文字列),
            "MotionDeviceSystemType": 設備システムタイプ(文字列),
            "MotionDeviceIdentifier": 設備ID(文字列),
            "MotionDeviceType": 設備タイプ(文字列),
            "ComponentName": コンポーネント名(文字列),
            "Manufacturer": メーカー(文字列),
            "Model": モデル(文字列),
            "DataForm": データフォーマット(データフォーマットを表す文字列),
            "RobotData": [ ロボットからのコマンド応答データ（命令毎固有フォーマット） ]
      },
      "TargetAddress": 通信相手ロボットのIPアドレス,
      "timestamp": タイムスタンプ（ロボットからの処理結果応答日時）
}
```

### YRC1000との入出力について

YRC1000の高速Ethernetサーバ機能に準ずる
（YRC1000の取扱説明書をご確認ください）

## セットアップ手順

### aion-coreをセットアップする

事前に下記リポジトリからaion-coreのセットアップを行ってください。

https://github.com/latonaio/aion-core


### リポジトリをクローンする

このリポジトリをgit cloneしてください

git clone https://github.com/latonaio/control-yaskawa-robot-r-kube.git

### Dockerイメージをビルドする

付属のスクリプトを使用して、control-yaskawa-robot-r-kube のDockerイメージをビルドしてください。
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

default.ymlに起動設定を追記してください。

例）
```
  control-yaskawa-robot-r-kube:
    command: python3 -m robot_data
    startup: yes
    always: yes
    scale: 1
    env:
      ROBOT_IP_01: "192.168.XXX.X"
```

### AIONを起動する

aion-core-manifestsの起動ファイルでAIONを立ち上げます。
