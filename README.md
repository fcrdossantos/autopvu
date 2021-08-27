# Auto PvU

Automatizador para Plant vs Undead

# Features

- Verificar informações da fazenda (PVU, LE, Itens, Plantas...)
- Adicionar novas plantas
- Adicionar vasos
- Aguar suas plantas
- Remover corvos
- Colher plantas
- Remover plantas temporárias já colhidas (inúteis)
- Fazer a missão diária
- Comprar itens
- Permite múltiplas sessões
- Técnicas de segurança (Humanização)
- Bypass no verificador de HWID
- Suporte para Debug via Jupyter Notebook (testar funções, alterar rotinas)
- Rotacionar grupos (Batchs) de utilização
- Detecção de manutenção

# Tutorial

## Requisitos

Você precisa ter Windows, testamos apenas no Windows 10, mas creio que a partir do 7 deva funcionar.

Você precisa do Python instalado, para baixar clique [aqui](https://www.python.org/downloads/).

Agora você irá rodar o seguinte comando no terminal (CMD/Powershell):

```bash
cd pasta\do\auto pvu
pip install -r requirements.txt
```

Ex: Caso o Auto PVU esteja em C:\arquivos\jogos\autopvu:

```bash
cd C:\arquivos\jogos\autopvu
pip install -r requirements.txt
```

Isso irá instalar todas as dependências do projeto.

## Preparativos do Navegador

Antes de configurar o bot você vai precisar abrir o seu navegador, instalar o MetaMask, configurá-lo normalmente e acessar o jogo pelo menos uma vez, para o navegador salvar suas contas e configurações.

Caso use mais de uma conta, é necessário fazer isso em todos os navegadores.

Além de prático, esse passo te dá uma maior segurança, visto que nunca terá
que ficar inserindo sua frase de recuperação do MetaMask via automatizador.

## Configuração do certificado

Você precisa ativar o certificado ca.crt no seu computador para acessar livremente o navegador que usamos no automatizador.

Para isso, vá ao Chrome e acesse suas configurações (chrome://settings/)

Procure por certificado (ou certificate se estiver em inglês).

Ele ficará na parte de segurança.

Para um link rápido acesse: chrome://settings/security?search=certific

( o link acima funcionará para ingles e português)

Selecione a opção "Gerenciar Certificados" ou "Manage Certificates"

Abrirá uma janela, vá até a aba "Autoridades de Certificação Raiz Confiáveis" ou "Trusted Root Certification Authorities"

Escolha a opção de Importar um novo Certificado e importe o ca.crt.

Pronto! Agora o certificado está pronto para uso :)

## 2Captcha

Necessário para burlar os captchas do jogo.

Crie uma conta no site oficial do [2Captcha](http://2captcha.com/).

Lá você terá opção de adicionar fundos para usar a API deles.

A cada 1000 requisições (capthcas resolvidos) é cobrado 2.99 dólares.

Se você utilizar **todas** as funções do automatizador, ele fará entre 30 e 100 requisições diárias, dependendo da sorte na missão diária.

Com isso, no melhor do casos você usará 930 requisições e no pior dos casos 3100 requisições mensais.

Caso não ative a missão diária, esse valor cai para cerca de 15 operações diárias, o que dará 450 requisições mensais.

Em 2 dias de missão diária você consegue 0.95 PVU (1 PVU - Taxa de 5% cobrada pelo jogo), o que já dá (na cotação atual) 20 dolares.

Sendo assim, eu recomendo ativar todas as funções e depositar o necessário no 2captcha.

Ao efetuar a compra, vá em Dashboard (https://2captcha.com/enterpage) e procure por "API KEY".

Você verá um valor grande e estranho, como: _1234abc56de7f890fgh123ijk456789l_

Essa é sua chave de API, é ela que você usará para se comunicar com o 2Captcha.

Vamos usá-la em breve no tutorial

## Multiplas Contas

### Chromium

AVISO: Por mais que várias questões de seguranças foram feitas, é recomendável usar apenas uma conta por máquina!

Para isso você precisa ter o Chromium instalado.

Vá até o site do Chromium e escolha a sua versão para download nos [snapshots](https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Win_x64/).

Para os testes foi utilizada a versão 915642 e você pode baixá-la clicando [aqui](https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Win_x64/915642/).

Na página de download você irá baixar tanto o arquivo "chrome-win.zip" quanto o "chromedriver_win32.zip".

Em seguida, descompacte ambos na pasta do **Auto PvU**.

### HWID

Caso você use múltiplas contas, é necessário "falsificar" o seu HWID para o jogo!

Para isso, você irá abrir o "regedit" no windows (Editor de Registros)

Em seguida irá navegar até _Computador\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Cryptography_

Lá você vai encontrar uma chave chamada "MachineGuid" e um valor, como por exemplo:

    123abc45-6789-de01-fg23-hij456kl7m8

Copie esse valor (vamos usá-lo em breve), ele será chamado de HWID_1

Agora delete essa chave (MachineGuid) e feche o regedit.

Abra novamente o Chrome, logue no Metamask e volte ao editor de registro.

Você verá que essa chave agora tem um novo valor, copie esse novo valor tbm, esse será o seu HWID_2.

# Configuração do arquivo de ambiente (.env)

Para rodar o automatizador, iremos precisar também configurar algumas propriedades no arquivo _.env_.

Esse arquivo fica na pasta raiz (principal/inicial) do Auto PvU.

Deixei um exemplo chamado "example_env" para você entender como criar o seu.
Basta ir até ele e editar os valores.

Abaixo explicamos o que é cada um desses valores

Seu automatizador não funcionará sem isso!

Minha dica é: Copie o conteúdo do "example_env", e cole em ".env", feito isso, edite os valores necessários seguindo esse tutorial.

## Captcha => API do 2captcha para passar os captchas

**2CAPTCHA_API** = Sua API do 2Captcha (vide tutorial acima)

## MetaMask => Login no Metamask e Acesso ao PVU

**PASSWORD**: Sua senha do MetaMask (é necessário para o automatizador abrir o metamask toda vez que executar o navegador)

## Current Account => Conta atual (para multiplas contas)

**USER**= Qual das contas o bot vai rodar

## Account 1 => Primeira conta

**HWID_1**= O primeiro HWID que pegamos (tutorial acima)

**DATA_DIR_1**= Diretório do seu perfil no chrome. No Chrome digite chrome://version e veja o valor que mostra em "Caminho do Perfil". Ele terá "\Default" no final, tire essa parte.

Exemplo:

    C:\Users\usuario\AppData\Local\Microsoft\Chrome\User Data\Default

Irá virar:

    C:\Users\usuario\AppData\Local\Microsoft\Chrome\User Data\

**DRIVER_DIR_1**= Caminho para o chromedriver

O valor padrão é _chromedriver.exe_, pois usa o que já está aqui neste projeto

#

## Account 2 => Segunda Conta

**HWID_2**= Seu segundo HWID

**DATA_DIR_2**= O diretório do perfil do Chromium, igual pegamos o do Chrome, mas usando o chromium

**DRIVER_DIR_2**= Diretório do driver do chromium

O valor padrão é _chromiumdriver.exe_

**PATH_BROWSER_2**= Diretório do executável do chromium

O valor padrão é _chromium/chrome.exe_

## Group Reset Info => Informações de reset do grupo

**GROUP_RESET_MINUTE** = Minuto que troca de grupos

Atualmente o jogo não te permite jogar 24h por dia, você tem alguns horários específicos (grupos/batchs).

Eles sempre possuem 1 hora de duração e ficam revezando entre si.

O minuto em que eles iniciam não é fixo, a cada manutenção troca, então as vezes você entraria 14:10 e agora passa a entrar 14:35.

Aqui você vai colocar apenas a parte do minuto, no exemplo acima, seria o valor 35.

## Routines => Rotinas do bot

Coloque valores **True** para _Sim_ e **False** para _Não_

**BUY_ITEMS**= Rotina de comprar itens

**HARVEST**= Colher plantas

**PLANT**= Plantas novas plantas

**POT**= Colocar vasos nas plantas

**WATER**= Regar Plantas

**CROW**= Tirar Corvos

**DAILY**= Fazer a missão diária

Atualmente a missão diária é de regar 15 plantas com menos de 200 irrigações.

## Security: (Make things slow) => Deixa o automatizador mais humanizado, mas demora mais a cada passo

Coloque valores **True** para _Sim_ e **False** para _Não_

**RANDOM_SLEEPS**= O automatizador fará umas pausas aleatórias
**HUMANIZE**= O automatizador estará mais humanizado, simulando as páginas que um humano teria que acessar

## HWID: (Multi Account) => Seguranças de HWID para multiplas contas

Coloque valores **True** para _Sim_ e **False** para _Não_

_ALTAMENTE RECOMENDÁVEL DEIXAR AMBOS COMO TRUE SE VOCÊ USAR MULTIPLAS CONTAS,
MAS DEIXAR O **CLEAN_HWID** COMO FALSE SE VOCÊ JOGAR COM APENAS UMA CONTA_

**CLEAN_HWID**= Se deixa o HWID sempre limpo após o login (ficará deletando novas chaves)

Caso você esteja usando _duas contas_, **ative essa opção**

Caso você esteja usando _uma conta_, **desative essa opção**

**SET_HWID** Coloca o HWID certo de cada conta.

Recomendo True para caso você use multiplas contas.

## Items => Configurações dos seus itens

PS: Para os valores mínimos, caso você tenha menos do que isso na sua conta, caso opte por usar a função de comprar sozinho, ele irá tentar comprar (depende do seu LE, né?) até preencher essa quantidade.

**POT_TYPE**= Qual tipo de vaso usar

Aceita os valores **SMALL** para o vaso pequeno e **BIG** para o vaso grande

**MIN_SMALL_POT**= Quantidade mínima de vasos pequenos

**MIN_BIG_POT**= Quantidade mínima de vasos grandes

**MIN_WATER**= Quantidade mínima de água

**MIN_SCARECROW**= Quantidade mínima de espantalhos
**MIN_GREENHOUSE**= Quantidade mínima de estufas

**MIN_SUNFLOWER_SAPLING**= Quantidade mínima de Sunflower Sapling

**MIN_SUNFLOWER_MAMA**= Quantidade mínima de Sunflower Mama

## Debug: (Utilize o debug.ipynb) => Para depuração e testes

**DEBUG**= Se você irá ou não ativar o Debug. (True/False)

# Rodando o automatizador

Novamente, abra o terminal (CMD/Powershell) e digite:

```bash
cd C:\arquivos\jogos\autopvu
python main.py
```

Ele então carregará as informações do arquivo _.env_ e iniciará o automatizador

Para usar uma segunda conta, volte ao _.env_ e modifique o valor de "USER" na sessão "Current Account", feito isso, abra outro terminal e execute novamente o automatizador.

# Debug

Você pode fazer depuração e testes no código do jogo, vendo como estão as funções, criando rotinas próprias, editando as atuais e afins...

Para isso, implementamos um arquivo do Jupyter Notebook que tornará vitalício o acesso ao navegador do automatizador e te permitirá executar e manipular qualquer função nele.

Para isso, habilite (True) a variável abaixo.

Para o uso do automatizador padrão (sem alterações suas), o Debug deve ficar desativado!

As rotinas padrões não serão executadas no Debug!

Recomendo deixar em False se você não for programador e/ou quiser rodar as minhas rotinas padrões

Lembre-se de Reiniciar o Kernel sempre que for querer reabrir/reiniciar o debug (ex: fechou o navegador)

Por fim, você deve SEMPRE abrir/executar em modo de Administrador, para isso, recomendo usar o VS Code e editar o arquivo por lá (abrindo o VS como admin)
