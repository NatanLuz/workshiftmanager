# Workshift Manager — Gerador de Escalas de Trabalho

Aplicação desktop para geração e gestão de escalas de trabalho, desenvolvida em Python com interface gráfica em Tkinter e persistência em SQLite. Focada em organização operacional, simplicidade de uso e exportação estruturada de dados.

---

## 🎯 Proposta de Valor

Fornecer uma solução prática e eficiente para geração de escalas semanais e mensais, reduzindo esforço manual e garantindo consistência na distribuição de turnos.

**Benefícios principais:**

- Automatização da geração de escalas com base em regras determinísticas
- Organização clara de colaboradores e turnos
- Exportação estruturada para Excel
- Interface direta e de baixo atrito (desktop)

---

## ⚙️ Funcionalidades

### Gestão de Colaboradores

- Cadastro com nome, cargo, turno (Manhã/Tarde), dias de folga e status (Ativo/Inativo)
- Edição e exclusão de registros

### Geração de Escalas

- Geração semanal ou mensal
- Baseada em data inicial (DD/MM/AAAA)
- Aplicação automática de dias de folga
- Filtro por turno
- Agrupamento por dia
- Distribuição baseada em regras determinísticas (sem aleatoriedade)

### Visualização

- Exibição em tabela (TreeView)
- Destaque visual por turno
- Organização opcional por dia

### Exportação e Importação

- Exportação para Excel (`.xlsx`)
- Importação de dados de versão anterior (v1)
- Normalização automática de dados legados

---

## 🏗️ Arquitetura / Estrutura

Separação clara de responsabilidades:

- **UI (Tkinter)** → interface gráfica e interação do usuário
- **Services** → regras de negócio (escala, exportação, importação)
- **Models** → representação de entidades
- **Database** → persistência SQLite

**Lógica de geração de escala:**

A geração segue regras determinísticas, garantindo previsibilidade e consistência:

- Considera:
  - Dias de folga configurados
  - Turno do colaborador
  - Período selecionado (semanal ou mensal)
- Não utiliza aleatoriedade
- Garante repetibilidade para os mesmos inputs

## 📁 Estrutura do Projeto:

```bash
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

---

## 🔐 Segurança

- Armazenamento local via SQLite (sem exposição externa)
- Ausência de integração com APIs externas
- Baixa superfície de ataque (aplicação desktop)
- Validação básica de dados de entrada

---

## 🧰 Stack Tecnológica

- Python 3.x
- Tkinter (interface gráfica)
- SQLite (`sqlite3`)
- Pandas
- OpenPyXL

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.x instalado

### Passos

```powershell
cd workshift-manager

python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

## ▶️ Execução

```powershell
python -m app.main
```

## 🧪 Testes Rápidos

**Checklist funcional:**

1. Cadastrar colaboradores com diferentes turnos
2. Gerar escala semanal
3. Gerar escala mensal
4. Aplicar filtro por turno
5. Exportar escala para Excel
6. Importar dados de versão anterior

## 📸 Screenshots

- Tela de cadastro de colaboradores

![Tela do Projeto 1](https://i.postimg.cc/ZKrMmcWv/Projeto-Pythontabelafolgamercado2.png)

- Geração de escala semanal

![Tela do Projeto 2](https://i.postimg.cc/vBNv71c8/Projeto-Pythontabelafolgamercado.png)

---

## 👤 Autor

Natan Da Luz  
Desenvolvedor de Software  
Contato: natandaluz01@gmail.com
