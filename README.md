# mvp-3-card-game-backend

# Criar venv

```
$ py -m venv venv
```

# Iniciar venv

```
$ .\venv\Scripts\activate
```

# Encerrar venv

```
$ deactivate
```

# Instalar dependências

```
(env)$ pip install -r requirements.txt
```

# Para executar a API:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

# Criar imagem no Docker

```
docker build -t blackjack-backend .
```

# Iniciar imagem no Docker

```
docker run -p 5000:5000 blackjack-backend
```
