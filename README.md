# mvp-3-card-game-backend

# Criar venv

```
$ py -m venv app\venv
```

# Iniciar venv

```
$ .\app\venv\Scripts\activate
```

# encerrrar

```
$ deactivate
```

# Instalar dependências

```
(env)$ pip install -r app\requirements.txt
```

# Para executar a API basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

# Criar imagem no Docker

```
docker build -t card-game-backend .
```

# Iniciar imagem no Docker

```
docker run -p 5000:5000 card-game-backend
```
