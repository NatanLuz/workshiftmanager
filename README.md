# Workshift Manager — Gerador de Escalas de Trabalho

Aplicação profissional e enxuta para geração de escalas de trabalho (semanal ou mensal), construída em Python com Tkinter e SQLite. Foco total em organização de turnos e escalas, com cadastro mínimo de colaboradores.

![Tela do Projeto 1](https://i.postimg.cc/ZKrMmcWv/Projeto-Pythontabelafolgamercado2.png)
![Tela do Projeto 2](https://i.postimg.cc/vBNv71c8/Projeto-Pythontabelafolgamercado.png)

## Funcionalidades do Projeto

- Cadastro de colaboradores: Nome, Cargo, Turno (Manhã/Tarde), Dias de folga, Status (Ativo/Inativo)
- Geração de escala Semanal ou Mensal (usando apenas a data inicial em DD/MM/AAAA)
- Edição e exclusão de colaboradores
- Filtro por turno na visualização da escala
- Agrupamento por dia com cores por turno (TreeView)
- Exportação da escala para Excel (Pandas + OpenPyXL)
- Importação de colaboradores a partir de Excel da versão anterior (v1), com normalização de turno ("Noite" → "Tarde")

## Tecnologias

- Python 3.x
- Tkinter (interface gráfica)
- SQLite (`sqlite3`) para persistência
- Pandas + OpenPyXL (exportação para Excel)

## Instalação

```powershell
cd "C:\Users\User\Desktop\workshiftmanager"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Execução

```powershell
python -m app.main
```

## Estrutura do Projeto

```
workshift-manager/
├── app/
│   ├── main.py            # Ponto de entrada (inicializa DB e UI)
│   ├── ui.py              # Interface Tkinter (cadastro, escala, exportação/importação)
│   ├── models.py          # Modelos de dados (Collaborator, ScheduleEntry)
│   ├── services.py        # Regras de negócio (CRUD, geração, exportação, importação)
│   └── database.py        # Conexão e schema SQLite
├── data/
│   └── database.db        # Banco SQLite (criado automaticamente)
├── assets/                # (opcional) imagens, ícones
├── README.md
└── requirements.txt
```

## Uso Rápido

- Cadastre colaboradores com Nome, Cargo, Turno (Manhã/Tarde), selecione Dias de folga e Status.
- Na seção "Escala de Trabalho":
  - Escolha "Semanal" ou "Mensal".
  - Informe "Início (DD/MM/AAAA)".
  - Opcional: filtre por Turno e/ou habilite "Agrupar por dia".
  - Clique em "Gerar" para visualizar.
- Clique em "Exportar Excel" para salvar a escala.
- Botão "Importar Excel (v1)": lê Nome, Cargo, Folga Fixa e normaliza o Turno (somente Manhã/Tarde).

## Notas

- Dias de folga são salvos como índices de semana (0=Segunda ... 6=Domingo).
- Exportação Excel inclui Data, Nome, Cargo, Turno.
- Ao iniciar, dados antigos com turno "Noite" são normalizados para "Tarde".
