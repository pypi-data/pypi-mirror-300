# keycripty

**keycripty** é um framework para criptografia em Python, desenvolvido por **César Neves**. Este pacote permite a encriptação e decriptação de dados de forma segura, utilizando técnicas de substituição, chaves e camadas de criptografia.
**keycripty** é um framework robusto para a criptografia e decriptografia de dados, utilizando técnicas avançadas de substituição e múltiplas camadas para proporcionar uma segurança superior das informações. Este framework foi projetado para ser intuitivo, permitindo que desenvolvedores integrem facilmente funcionalidades de segurança em suas aplicações.

**Funções Principai**

**Camadas**
O keycripty suporta um sistema de camadas, onde o número de camadas pode ser especificado durante a #criptografia. Isso significa que o texto é criptografado várias vezes, aumentando a complexidade e a segurança da decriptografia.

**Cálculo de Deslocamento**
A função calcular_deslocamento(chave) calcula um deslocamento baseado na soma dos valores ASCII dos caracteres da chave, que é utilizado nas operações de criptografia e decriptografia.

**Geração de Caracteres Aleatórios**
A função gerar_caractere_aleatorio() gera caracteres aleatórios a partir de um conjunto que inclui letras, dígitos e símbolos especiais, adicionando uma camada extra de segurança aos dados criptografados.

**Criptografia**
A função criptografar(texto, chave, numero_de_camadas) realiza a criptografia do texto utilizando a chave fornecida e um número especificado de camadas. A cada camada, o texto é processado e caracteres aleatórios são adicionados para ofuscação.

**Decriptografia**
A função decriptografar(texto, chave) reverte o processo de criptografia, utilizando a mesma chave e o número de camadas para restaurar o texto original

**Criptografia e Decriptografia de Arquivos**
As funções criptografar_arquivo(arquivo_entrada, arquivo_saida, chave, numero_de_camadas) e decriptografar_arquivo(arquivo_entrada, arquivo_saida, chave, numero_de_camadas) permitem a criptografia e decriptografia de conteúdos de arquivos, facilitando a proteção de dados em larga escala

**Criptografia Usada**
O keycripty utiliza técnicas de substituição e ofuscação com a adição de caracteres aleatórios, aumentando a segurança dos dados criptografados. Este método é eficaz para proteger informações sensíveis.

**Exemplos de Uso**

## Exemplo de Código
```python
from keycripty import encript # função para criptografia
from keycripty import decript # função para decriptografia
from keycripty import processkey # função para criptografia e decriptografia de Arquivos

# key= - Cria uma chave para criptografar
# cmd= - Adicione um número de camandas

# Criptografando Dados
__dadoCripto__ = encript('keycripty - framework para criptografia', key='criarChave', cmd=1)
print ('\n DADOS CRIPTOGAFADO:',__dadoCripto__)

# keyDecript= - Cria uma chave para criptografar
# cmd= - Adicione um número de camandas

# decriptografando Dados
__dadosdecriptografados__ = decript('0001MXgwaOeatwatrgv4@w-j@khatycholgzyhq1tLmW@ArUcCtscc@Ze4tHkBrFvKqvirtZcShYkFc==!', keyDecript='criarChave', cmd=1)
print ('\n DADOS DECRIPTOGRAFADOS:',__dadosdecriptografados__)

# action='crypt' - Para criptografar os dados do arquivo

# CRIPTOGRAFANDO ARQUIVO
try:
    processkey('file.txt', key='chave', cmd=2, action='crypt')
except TypeError:
    print ('')
    print ('\n <ERROR> PARAMENTOS INCOMPLETOS.')

# action='decrypt' - Para decriptografar os dados do arquivo

# CRIPTOGRAFANDO ARQUIVO
try:
    processkey('file.txt', key='chave', cmd=2, action='decrypt')
except TypeError:
    print ('')
    print ('\n <ERROR> PARAMENTOS INCOMPLETOS.')
```
**O keycripty** oferece uma solução prática e segura para o tratamento de dados sensíveis. Com funcionalidades robustas e suporte a múltiplas camadas de segurança, é uma excelente escolha para desenvolvedores que buscam proteger informações em suas aplicações.

## Versão

`0.1.0`

## Autor

César Neves  
[cesarioneves104@gmail.com](mailto:cesarioneves104@gmail.com)

## Instalação

Para instalar o `keycripty`, você pode usar o seguinte comando:

```bash
pip install keycripty
