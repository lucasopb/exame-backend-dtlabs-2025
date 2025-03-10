# 🚀 FastAPI IoT Backend  

Este projeto é um backend para aplicações IoT, desenvolvido com **FastAPI**, utilizando **PostgreSQL** para armazenamento de dados e **Docker** para gerenciamento de ambiente.

## 📌 Funcionalidades  

- 📍 **Autenticação JWT** (Registro e Login)  
- 📊 **Registro e consulta de dados de sensores** (temperatura, umidade, tensão e corrente elétrica)  
- 🖥️ **Monitoramento de servidores IoT** (status online/offline)  
- 📄 **Documentação automática com Swagger**  
- 🧪 **Testes automatizados com PyTest**  

---

## 🛠️ Tecnologias Utilizadas  

- **FastAPI** - Framework web para APIs rápidas e eficientes  
- **PostgreSQL** - Banco de dados relacional  
- **Docker** - Containerização do ambiente  
- **Docker Compose** - Gerenciamento simplificado de containers  
- **PyTest** - Testes automatizados  

---

## 🚀 Como Rodar o Projeto  

### 🔹 1. Clonar o Repositório  

```sh
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 🔹 2. Criar e Configurar o Arquivo `.env`  

Crie um arquivo `.env` na raiz do projeto e configure as variáveis de ambiente, como exemplo:  

```ini
DATABASE_URL=postgresql://usuario:senha@db:5432/nome_do_banco
SECRET_KEY=chave-secreta-para-jwt
```

---

## 🐳 Rodando com Docker  

Se você deseja rodar o projeto diretamente no **Docker**, siga estes passos:

### 🔹 3. Subir os containers com Docker Compose  

```sh
docker-compose up -d
```

> Isso iniciará o banco de dados **PostgreSQL** e a API FastAPI no Docker.


### 🔹 4. Acessar a API  

Após a subida dos containers, a API estará disponível em:  

- **Swagger UI** → [`http://localhost:8000/docs`](http://localhost:8000/docs)  
- **Redoc** → [`http://localhost:8000/redoc`](http://localhost:8000/redoc)  
