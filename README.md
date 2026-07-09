# Workshift Manager — Gerador de Escalas de Trabalho

## 📖 Sobre o projeto

O **Workshift Manager** é uma aplicação desktop desenvolvida em Python, com interface gráfica em Tkinter e persistência local em SQLite. Seu objetivo é automatizar a criação e o gerenciamento de escalas de trabalho semanais e mensais, facilitando a organização dos colaboradores e reduzindo processos manuais.

A geração das escalas utiliza regras determinísticas: considera o turno, os dias de folga e o período selecionado, sem empregar aleatoriedade. Dessa forma, os mesmos dados de entrada produzem resultados consistentes e previsíveis.

O projeto possui uma arquitetura com responsabilidades separadas entre interface, regras de negócio, modelos e acesso aos dados. Como os dados permanecem armazenados localmente e não há integração com APIs externas, a aplicação não expõe informações por meio de serviços remotos.

## ✨ Funcionalidades

### Gestão de colaboradores

- Cadastro de colaboradores com nome, cargo, turno, dias de folga e status;
- edição e exclusão de colaboradores;
- definição dos turnos Manhã e Tarde;
- configuração dos dias de folga;
- ativação e desativação de colaboradores.

### Geração e visualização de escalas

- Geração automática de escalas semanais ou mensais;
- seleção do período por data inicial no formato `DD/MM/AAAA`;
- aplicação automática dos dias de folga;
- distribuição determinística, sem aleatoriedade;
- organização das escalas por dia;
- filtro por turno;
- exibição em tabela com TreeView;
- destaque visual dos turnos.

### Importação e exportação

- Exportação das escalas para Excel (`.xlsx`);
- importação de dados da versão anterior (v1);
- normalização automática dos dados legados importados.

## 🖼️ Screenshots

### Cadastro de colaboradores

![Tela de cadastro de colaboradores](https://i.postimg.cc/ZKrMmcWv/Projeto-Pythontabelafolgamercado2.png)

### Geração de escala semanal

![Tela de geração da escala semanal](https://i.postimg.cc/vBNv71c8/Projeto-Pythontabelafolgamercado.png)

## 🚀 Tecnologias

- Python 3.x;
- Tkinter para a interface gráfica;
- SQLite e o módulo nativo `sqlite3` para persistência local;
- Pandas para manipulação de dados;
- OpenPyXL para geração de arquivos Excel.

## ⚙️ Como executar

### Pré-requisitos

- Python 3.x instalado;
- terminal PowerShell;
- código-fonte do projeto disponível localmente.

### Criar o ambiente virtual

No diretório que contém o projeto, execute:

```powershell
cd workshift-manager

python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Instalar as dependências

```powershell
pip install -r requirements.txt
```

### Executar a aplicação

```powershell
python -m app.main
```

### Verificação funcional

Após iniciar a aplicação, o fluxo principal pode ser verificado com o seguinte checklist:

1. Cadastrar colaboradores com diferentes turnos;
2. gerar uma escala semanal;
3. gerar uma escala mensal;
4. aplicar o filtro por turno;
5. exportar uma escala para Excel;
6. importar dados de uma versão anterior.

## 📂 Estrutura do projeto

A aplicação separa a interface gráfica, os modelos, as regras de negócio e a persistência de dados:

```text
workshift-manager/
├── app/
│   ├── main.py
│   ├── ui.py
│   ├── models.py
│   ├── services.py
│   └── database.py
├── data/
│   └── database.db
├── assets/
├── README.md
└── requirements.txt
```

- `app/main.py`: ponto de entrada da aplicação;
- `app/ui.py`: interface gráfica e interação com o usuário;
- `app/models.py`: representação das entidades;
- `app/services.py`: regras de negócio, geração das escalas, exportação e importação;
- `app/database.py`: operações de persistência em SQLite;
- `data/database.db`: banco de dados local;
- `assets/`: recursos utilizados pela aplicação;
- `requirements.txt`: dependências necessárias para execução.

## 🌐 Deploy

O Workshift Manager é uma aplicação desktop e, portanto, não possui deploy web. O projeto deve ser instalado e executado localmente após a criação do ambiente virtual e a instalação das dependências indicadas em `requirements.txt`.

Os dados são mantidos no banco SQLite local, sem necessidade de configurar um servidor de banco de dados ou serviço externo.

## 👤 Autor

**Natan Da Luz**

- LinkedIn: [linkedin.com/in/natandaluz](https://www.linkedin.com/in/natandaluz/)
- Portfólio: [portfolionatan.vercel.app](https://portfolionatan.vercel.app/)
- E-mail: [natandaluz01@gmail.com](mailto:natandaluz01@gmail.com)

## 📄 Licença

Este projeto está sem uma licença definida no momento.
