
# 1. 환경 설치

* Python 3.10 이상

## 1) Python 패키지 매니저 `uv` 설치

```
# Windows(Powershell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## 2) `uv` 사용법

### 시작하기

내가 관리하려고 하는 폴더 내에서 실행

```
uv init
```

### 가상환경 생성 및 활성화

가상환경 이름을 따로 설정하지 않으면 `.venv`가 만들어진다. 

깃허브에 올릴 예정이라면 해당 폴더를 반드시 `.gitignore`에 넣어야 한다. 

```
uv venv [가상환경이름]
venv\Script\activate
```

### 라이브러리 설치

uv에서는 기존 pip install 방식과 더불어, uv add를 사용하여 라이브러리를 설치가 가능

```
# Example
uv pip install "mcp[cli]"
uv add "mcp[cli]"
```

이 프로젝트에서는 의존성 관리의 명확성과 재현성 확보를 위해 uv add 방식을 사용. pyproject.toml에 패키지가 자동 기록됨

```
uv add "mcp[cli]"
```

⚠️ 만약 가상환경 이름이 `.venv`가 아니라면 내가 만든 환경에 라이브러리 설치가 되지 않을 수도 있다. 이럴 때에는 라이브러리 설치시 `--active`를 추가하면 해결된다. 

```
uv add "mcp[cli]" --active
```

### requirements.txt 생성 및 설치

`uv.lock`의 경우 설치한 버전이 명확하게 명시되어 있어, 동일한 환경으로 설치가 가능하다. 

```
uv pip install -r pyproject.toml
uv pip install -r uv.lock
```
