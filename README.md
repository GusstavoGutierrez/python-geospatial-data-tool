# Análise de Dados Geoespaciais com Interface Visual

**Aluno:** Gustavo Vitor Gutierrez
**Disciplina:** Software Básico - 1° Semestre / 2025
**Professor:** Paulo José Almeida
**Instituição:** Universidade de Mogi das Cruzes

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/gustavo-vitor-gutierrez-b520a2341/) [![Instagram](https://img.shields.io/badge/-Instagram-%23E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/gustavo.gutierreez/) [![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://wa.me/+5511952018042)

## 📝 Descrição do Projeto

Este projeto foi desenvolvido como parte da disciplina de Software Básico e tem como objetivo criar um sistema em Python para processar dados geoespaciais em múltiplos formatos (CSV, JSON, XML), gerar visualizações em mapas interativos e tabelas, e oferecer uma interface gráfica intuitiva para o usuário.

O sistema permite carregar dados de arquivos existentes, bem como criar novos conjuntos de dados geoespaciais através de entrada manual de coordenadas ou geocodificação de endereços. As visualizações são geradas utilizando Plotly para os mapas e uma tabela integrada à interface para visualização dos dados brutos.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Manipulação de Dados:**
    * Pandas: Para estruturação e manipulação de dados tabulares.
    * GeoPandas: Para manipulação avançada de dados geoespaciais.
* **Visualização:**
    * Plotly (Plotly Express): Para a criação de mapas interativos.
* **Interface Gráfica (GUI):**
    * Tkinter (com `tkinter.ttk`): Para a construção da interface do usuário desktop.
* **Geocodificação:**
    * Geopy (com Nominatim): Para converter endereços em coordenadas geográficas.
* **Manipulação de XML:**
    * `xml.etree.ElementTree`: Para parsear e gerar arquivos XML.
    * `xml.dom.minidom`: Para formatação (pretty print) de arquivos XML.

## ✨ Funcionalidades Implementadas

* **Carregamento de Dados:**
    * Suporte para arquivos nos formatos `.csv`, `.json` e `.xml`.
    * Interface para seleção de arquivos locais.
* **Criação de Novos Dados:**
    * Interface dedicada (`NovoLocalDialog`) para adicionar novos locais.
    * Entrada de dados por nome do local, coordenadas (latitude/longitude) ou endereço completo.
    * Geocodificação automática de endereços para obtenção de coordenadas.
    * Adição de múltiplos locais antes de salvar.
* **Salvamento de Dados:**
    * Capacidade de salvar os dados processados ou criados nos formatos `.csv`, `.json` e `.xml`.
    * Os arquivos são salvos na pasta `datas/` (criada automaticamente se não existir).
* **Visualização:**
    * **Mapa Interativo:** Geração de um mapa utilizando Plotly Express que exibe os pontos geoespaciais. O mapa é salvo como `mapa.html` e aberto automaticamente no navegador padrão.
    * **Tabela de Dados:** Exibição dos dados carregados ou criados em uma tabela interativa (com barras de rolagem) em uma janela separada da interface principal.
* **Interface Gráfica:**
    * Janela principal com opções claras para o usuário.
    * Diálogos informativos para feedback ao usuário (sucesso, erro, aviso).

## ⚙️ Pré-requisitos

* Python 3.7 ou superior.
* As demais dependências estão listadas no arquivo `requirements.txt`.

## 🖱️ Como Usar a Aplicação

A interface principal apresenta três opções:

1.  **"📂 Abrir Arquivo Existente":**
    * Clique neste botão para abrir uma caixa de diálogo de seleção de arquivos.
    * Navegue e selecione um arquivo de dados geoespaciais nos formatos `.csv`, `.json` ou `.xml`.
        * **CSV:** Deve conter as colunas `nome`, `latitude`, `longitude`.
        * **JSON:** Deve ser um array de objetos, cada objeto com as chaves `nome`, `latitude`, `longitude`.
        * **XML:** Deve seguir a estrutura com um elemento raiz (ex: `<dados>`) contendo múltiplos elementos `<registro>`, cada um com subelementos `<nome>`, `<latitude>`, `<longitude>`.
    * Após o carregamento bem-sucedido, um mapa interativo (`mapa.html`) será gerado e aberto no seu navegador, e uma janela com a tabela de dados será exibida.

2.  **"➕ Criar Novo Arquivo":**
    * Clique neste botão para abrir o diálogo "Adicionar Locais e Salvar Arquivo".
    * **Nome do Local:** Digite o nome do ponto de interesse.
    * **Método de Entrada:**
        * **Coordenadas:** Selecione esta opção e insira os valores de Latitude e Longitude.
        * **Endereço:** Selecione esta opção e digite o endereço completo para geocodificação.
    * Clique em **"Adicionar Local à Lista"**. O local será processado (geocodificado, se necessário) e adicionado à lista na parte inferior do diálogo. Você pode adicionar múltiplos locais.
    * **Nome do Arquivo:** Digite o nome desejado para o arquivo (sem a extensão).
    * **Formato:** Selecione o formato de salvamento (CSV, JSON ou XML).
    * Clique em **"Salvar Arquivo e Gerar Mapa"**. O arquivo será salvo na pasta `datas/`, um mapa (`mapa.html`) será gerado e aberto no navegador, e uma janela com a tabela de dados dos locais adicionados será exibida.
    * Clique em **"Cancelar"** para fechar o diálogo sem salvar.

3.  **"Sair":**
    * Fecha a aplicação.

## 📂 Estrutura do Projeto

* `main.py`: Ponto de entrada da aplicação, inicia a interface gráfica.
* `app_interface.py`: Define a janela principal da interface gráfica e seus elementos básicos.
* `logica_fluxo.py`: Contém a lógica de interação do usuário com a interface, incluindo a classe `NovoLocalDialog` para entrada de novos dados e as funções que orquestram o processamento de arquivos existentes e novos.
* `gui_utils.py`: Contém funções utilitárias para a interface gráfica, como `exibir_tabela_dados`.
* `processamento.py`: Responsável pelo carregamento de dados de diferentes formatos (CSV, JSON, XML) e pelo salvamento de dados nesses formatos.
* `visualizacao.py`: Gera o mapa interativo utilizando Plotly.
* `requirements.txt`: Lista as dependências do projeto.
* `datas/`: Pasta criada automaticamente para salvar os arquivos gerados pelo usuário.
* `mapa.html`: Arquivo HTML do mapa gerado, aberto automaticamente no navegador.
---
