# Aicé
 
> Abbreviations for Innovative and Catchy Enthusiasms

## 사용방법

Aicé 팩 디렉토리에 다음 JSON 형식에 맞춰 상용구를 지정합니다.

Aicé 팩 디렉토리는 플랫폼에 따라 다음과 같습니다.

* Windows: `%APPDATA%\Aice\packs`
* Unix: `~/.aice/packs`

```json
{
  ";gd": "안녕하세요",
  "hw": "Hello, world!"
}
```

프로그램을 실행하면 사용구가 지정됩니다.

Windows의 경우 `shell:startup` 디렉토리에 `Aice.exe`에 대한 바로가기를 두어
컴퓨터 실행과 함께 자동으로 실행되도록 설정할 수 있습니다.

## 빌드

### Windows

```
pyinstaller -w -i .\res\icon\icon1024.ico -n Aice __main__.py
```