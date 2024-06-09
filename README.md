# PC-8001 SDCC 開発サンプル

SDCC を使って PC-8001 のプログラムを開発するための空のプロジェクトです。

## 必要なツール

SDCC (https://sdcc.sourceforge.net/) の他に以下のツールをインストールします。
このプロジェクトの tools の下に実行ファイルが置かれることを前提にしています。
(パスの通ったところにある場合、Makefile を適宜修正してください。)

- hex2bin (https://sourceforge.net/projects/hex2bin/)

SDCC ではインテル HEX が出力されるので、これをバイナリに変換するのに使います。

- t88tool (http://bugfire2009.ojaru.jp/download.html#t88tool)

上記ツールで出力されたバイナリを cmt 形式のファイルに変換します。

## コンパイル方法

このプロジェクトを github からダウンロードし、
コマンドラインから ./sample/build に移動して make コマンドを実行します。

```
$ cd ./sample/build
$ make
```

出力された cmt ファイルは、エミュレーター等で実行して動作を確認できます。
プログラムは mon か L を実行すれば自動的に実行されます。

```
mon
*L
```

## 注意事項

- グローバル変数の初期値を定義できない

本来は初期化時に ROM 領域(コード領域)から RAM 領域(データ領域)へメモリコピーが実行されることで、グローバル変数に初期値が定義されていれば初期化されますが、PC-8001 の場合はすべて RAM 上で動作するためメモリの無駄になってしまいます。
そのようなコピーの処理は省略して、コード上では const で定義した変数をキャストするなどして直接書き換えることで対応します。
