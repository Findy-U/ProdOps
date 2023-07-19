# ProdOps
## Orientações para o SSH key (necessário para utilizar o repositório)

### 1 - Instale o Git:

Se você ainda não instalou o Git, faça o download e instale-o a partir do site oficial: https://git-scm.com/downloads

### 2 - Verifique as chaves SSH existentes:

Primeiro, você precisa verificar se já existem chaves SSH no seu computador. Abra o Git Bash (ou Terminal no VS Code) e digite:
```
ls -al ~/.ssh
```
Isso listará todos os arquivos no seu diretório .ssh. Procure por um arquivo chamado id_rsa.pub ou id_dsa.pub. Se você não tiver um par de chaves público e privado existente, ou não quiser usar nenhum dos disponíveis para o GitHub, prossiga para a próxima etapa.

### 3 - Gere uma nova chave SSH:

No terminal, cole o texto abaixo, substituindo pelo seu endereço de email do GitHub:
```
ssh-keygen -t ed25519 -C "seu_email@exemplo.com"
```
Isso cria uma nova chave SSH, usando o email fornecido como um rótulo. Quando for solicitado a "Inserir um arquivo para salvar a chave", pressione Enter. Isso aceita o local de arquivo padrão.

No prompt, digite uma frase secreta segura (passphrase).

### 4 - Adicione sua chave SSH ao ssh-agent:

Primeiro, inicie o ssh-agent em segundo plano:
```
eval "$(ssh-agent -s)"
```
Se você estiver usando o Git Bash que vem com o Git para Windows, precisa usar este comando:
```
eval $(ssh-agent -s)
```
Adicione sua chave privada SSH ao ssh-agent digitando:
```
ssh-add ~/.ssh/id_ed25519
```
Para imprimir sua chave, utilize:
```
cat ~/.ssh/id_ed25519.pub
```
### 5 - Adicione a chave SSH à sua conta do GitHub:

Copie a chave pública SSH para a área de transferência. Se o arquivo da sua chave pública SSH tiver um nome diferente do código de exemplo, modifique o nome do arquivo para corresponder à sua configuração atual:
```
clip < ~/.ssh/id_ed25519.pub
```
Vá para as configurações da sua conta do GitHub. Clique em "SSH e GPG keys" e depois clique em "New SSH key" (Nova chave SSH).

Dê um título descritivo (como "Laptop Pessoal" ou "Computador de Trabalho"). No campo "Key" (Chave), cole sua chave. Quando terminar, clique em "Add SSH key" (Adicionar chave SSH).

### 6 - Teste a conexão:

Você pode verificar se sua conexão SSH está funcionando corretamente conectando-se ao GitHub por meio de SSH com este comando:
'''
ssh -T git@github.com
'''
Se você receber uma mensagem de que foi autenticado com sucesso, então a conexão foi estabelecida corretamente.

## Orientações para o Git

### 1 - Instale o Git:

Se você ainda não instalou o Git, faça o download e instale-o a partir do site oficial: https://git-scm.com/downloads

### 2 - Clone o repositório:

Para baixar o repositório no seu computador, use o comando git clone com a URL SSH do repositório:
```
git clone git@github.com:Findy-U/ProdOps.git
```
Este comando cria um novo diretório no seu diretório atual, inicializa um diretório .git dentro dele, baixa todos os dados desse repositório e verifica uma cópia de trabalho da versão mais recente.

### 3 - Navegue para o diretório clonado:

Use o comando cd (change directory) para entrar no diretório que foi clonado:
```
cd ProdOps
```
### 4 - Mude para a branch 'develop':

Use o comando git checkout para mudar para a branch 'develop':
```
git checkout develop
```
Atualize a branch 'develop' com as últimas mudanças do repositório remoto:
```
git pull origin develop
```
### 5 - Faça alterações:

Agora você pode começar a fazer alterações no código. Depois de fazer algumas alterações, você pode adicioná-las à "staging area" usando:
```
git add .
```
Nota: O . adicionará todas as alterações. Se você quiser adicionar arquivos específicos, pode especificar o nome do arquivo em vez de ..

### 6 - Commit das alterações:

Depois de adicionar suas alterações à "staging area", você pode confirmá-las (commit):
```
git commit -m "Uma mensagem descrevendo as alterações"
```
### 7 - Envie as alterações:

Depois que suas alterações são confirmadas (committed), você pode enviá-las (push) para o repositório remoto:
```
git push origin develop
```
Nota: Se a branch não existir no repositório remoto, este comando irá criá-la.

### 8 - Crie um Pull Request:

Depois de ter enviado suas alterações, você pode ir ao GitHub para criar um Pull Request. A interface do GitHub irá guiá-lo através disso. Um Pull Request é uma maneira de sugerir alterações do seu código para o projeto principal (main). Quando você cria um Pull Request, os mantenedores do projeto podem revisar suas alterações, discutir ajustes e eventualmente aceitar suas alterações no projeto ou rejeitá-las.

