# EANgeneration

MMDAgentWozGUIが出力したログを，EAF (ELAN Annotation Format) に変換するプログラム．
この中で利用するスクリプトも置いている．

## 手順（より詳しくはmanual.pdf参照）
```
1. ファイルの準備  
2. 基準時刻取得  
3. CSVファイル生成  
4. ELANに読み込み  
```
上記の手順3でここにあるスクリプト群を使用する．

generateCsv.batは，その中で OutCsvELAN.py を呼んでいる．  
OutCsvELAN.pyは，ログファイルを入力として動作する（manual.pdf参照）．

## 必要な外部プログラム
ELAN https://archive.mpi.nl/tla/elan  
Pythonの処理系

## ファイル構成（一部）
sample/  
　動作検証用のログファイル（.txt）  
　手順3で生成されるCSVファイル（.csv）  
　手順4でELANから出力可能なEAFファイル（.eaf） 

manual.pdf  
　Hazumi1902収録時に使用したマニュアルを一部改訂して作成
