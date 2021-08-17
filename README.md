# control-yaskawa-robot-r-kube
## 概要
安川電機製ロボットコントローラYRC1000から、イーサネット経由でデータを取得するマイクロサービスです。   
このマイクロサービスを使うには、別途安川電機製ロボットコントローラYRC1000が必要です。

## 動作環境
control-yaskawa-robot-r-kubeは、aion-coreのプラットフォーム上での動作を前提としています。    
使用する際は、事前に下記の通りAIONの動作環境を用意してください。 
- 安川電機製ロボットコントローラYRC1000   
- ARM CPU搭載のデバイス(NVIDIA Jetson シリーズ等) 
- OS: Linux Ubuntu OS 
- CPU: ARM64 
- Kubernetes 
- AION のリソース

## セットアップ手順
### 1. aion-coreのセットアップ
事前に下記リポジトリからaion-coreのセットアップを行ってください。
```   
git clone https://github.com/latonaio/aion-core
```

### 2. ベースイメージの準備
下記リポジトリからベースイメージlatonaio/l4tを用意してください。 
```  
git clone https://github.com/latonaio/python-base-images
```

### 3. リポジトリのクローン
このリポジトリをgit cloneしてください。  
``` 
git clone https://github.com/latonaio/control-yaskawa-robot-r-kube.git
```

### 4.Dockerイメージのビルド
付属のスクリプトを使用して、control-yaskawa-robot-rのDockerイメージをビルドしてください。
```
bash docker-build.sh
```

### 5. 設定ファイルの配置
command_list.jsonとtrigger_list.jsonを、以下のフォルダに配置します。
```
/var/lib/aion/(ネームスペース名)/Data/control-yaskawa-robot-r_1
```
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

### 6. aion-coreの設定ファイルへの起動設定の記載
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

### 7.　AIONの起動
aion-core-manifestsの起動ファイルでAIONを立ち上げます。

## I/O
### input
なし

### output
- RobotData
  - Command               : コマンド番号(16進数値の文字列変換)
  - Result                : 処理成否(True/False)
  - ExpireTime            : データ保持期間(ms)
  - BaseObjectType        : ベースオブジェクトタイプ(文字列)
  - ComponentType         : コンポーネントタイプ(文字列)
  - MotionDeviceSystemType: 設備システムタイプ(文字列)
  - MotionDeviceIdentifier: 設備ID(文字列)
  - MotionDeviceType      : 設備タイプ(文字列)
  - ComponentName         : コンポーネント名(文字列)
  - Manufacturer          : メーカー(文字列)
  - Model                 : モデル(文字列)
  - DataForm              : データフォーマット(データフォーマットを表す文字列),
  - RobotData             : [ ロボットからのコマンド応答データ（命令毎固有フォーマット） ]
- TargetAddress: 通信相手ロボットのIPアドレス
- timestamp    : タイムスタンプ（ロボットからの処理結果応答日時）

### YRC1000との入出力
YRC1000の高速Ethernetサーバ機能に準じます（YRC1000の取扱説明書を確認してください）。

