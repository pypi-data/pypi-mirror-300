# converter

O pacote `coinverter` é utilizado para realizar conversões de moedas de forma simples e rápida, utilizando a API do AwesomeAPI para obter as cotações mais recentes.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install package_name

```bash
pip install coinverter
```

## Usage

```python
from coinverter import cotacao

# Converte 100 dólares americanos (USD) para reais brasileiros (BRL)
valor_convertido = cotacao('USD', 'BRL', 100)
print(f"Valor convertido: {valor_convertido} BRL")

```

## Funções Disponíveis

### `cotacao(de, para, valor=1)`

Converte um valor de uma moeda para outra utilizando a API do AwesomeAPI para obter a taxa de câmbio mais recente.

#### Parâmetros:
- `de` (str): Código da moeda de origem, como 'USD', 'EUR', etc.
- `para` (str): Código da moeda de destino, como 'BRL', 'USD', etc.
- `valor` (float, opcional): O valor que você deseja converter. O padrão é 1.

#### Retorno:
- `float`: Retorna o valor convertido com base na taxa de câmbio atual.


### Moedas
Algumas das principais moedas suportadas pelo `coinverter` incluem:
- **BRL (Real Brasileiro)**
- **USD (Dólar Americano)**
- **EUR (Euro)**
- **GBP (Libra Esterlina)**
- **JPY (Iene Japonês)**

mais informações [documentação da AwesomeAPI](https://docs.awesomeapi.com.br/api-de-moedas)

## Author
Pedro Arruda

## License
[MIT](https://choosealicense.com/licenses/mit/)