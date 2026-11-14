name: Gerar Arquivos de Itens
on: [workflow_dispatch] # Permite executar manualmente pela aba "Actions"
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13' # Versão do Python
      - run: python gerar_itens.py
      - uses: actions/upload-artifact@v4
        with:
          name: itens-gerados
          path: items/
