# Coletor de Dados do CUB - Florianópolis

Este script em Python extrai e armazena os valores do CUB (Custo Unitário Básico) da construção civil a partir do site do **Sinduscon Florianópolis** e insere esses dados em um banco de dados PostgreSQL.

## 📌 Funcionalidades

- Faz requisição HTTP para acessar a página do **Sinduscon Florianópolis** contendo os valores do CUB.
- Extrai e estrutura os dados relevantes (mês de referência e valor do CUB) utilizando **BeautifulSoup**.
- Converte os valores extraídos para um formato adequado para armazenamento.
- Conecta-se a um banco de dados PostgreSQL e insere os dados, garantindo que informações duplicadas não sejam inseridas.
- Usa **dotenv** para carregar credenciais do banco de dados de forma segura.

---

## 🛠 Tecnologias Utilizadas

- **Python 3.12.5**
- **Requests** - Para fazer requisições HTTP e acessar a página do CUB.
- **BeautifulSoup4** - Para extrair dados do HTML.
- **Pandas** - Para manipulação de dados.
- **SQLAlchemy** - Para conectar-se ao banco de dados PostgreSQL.
- **Python-dotenv** - Para gerenciar credenciais de conexão de forma segura.

---

## 🚀 Como Executar o Script

### 1️⃣ Clonar o Repositório
```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
```

### 2️⃣ Instalar Dependências
Se estiver utilizando **Poetry**:
```bash
poetry install
```
Se estiver utilizando **pip**:
```bash
pip install -r requirements.txt
```

### 3️⃣ Configurar as Variáveis de Ambiente
Crie um arquivo **.env** na raiz do projeto e adicione a seguinte variável:
```env
DB_URL=postgresql://usuario:senha@host:porta/banco_de_dados
```

### 4️⃣ Executar o Script
```bash
python nome_do_arquivo.py
```

---

## 📜 Estrutura do Código

### **1. Função `html_page()`**
- Faz a requisição HTTP para acessar a página do Sinduscon.
- Retorna o HTML da página como uma string.

### **2. Função `data_page(html)`**
- Analisa o HTML com **BeautifulSoup**.
- Extrai o mês de referência e o valor do CUB.
- Converte os dados para um formato estruturado em **Pandas DataFrame**.
- Ajusta a data para o formato `01/MM/AAAA`.

### **3. Função `convert_to_float(value)`**
- Converte o valor do CUB para formato numérico, garantindo compatibilidade com o banco de dados.

### **4. Função `insert_data(df, db_url, table_name)`**
- Conecta ao banco de dados utilizando **SQLAlchemy**.
- Verifica se o dado já existe antes de inseri-lo.
- Insere os dados caso ainda não estejam no banco.

### **5. Função `main()`**
- Executa todas as etapas do processo: busca da página, extração dos dados e inserção no banco de dados.

---

## 🏦 Estrutura da Tabela no Banco de Dados

A tabela onde os dados são armazenados (“cub”) deve ter a seguinte estrutura:
```sql
CREATE TABLE cub (
    "Data" TIMESTAMP PRIMARY KEY,
    "CUB" FLOAT NOT NULL
);
```

---

## 🤝 Contribuição
Fique à vontade para abrir issues e pull requests para contribuir com melhorias no projeto!

---

## 📞 Contato
Se tiver dúvidas ou sugestões, entre em contato via:
- **Email:** seuemail@exemplo.com
- **LinkedIn:** [Seu Perfil](https://www.linkedin.com/in/c%C3%A9zarmaldini/)
- **GitHub:** [Seu GitHub](https://github.com/cezarmaldini)