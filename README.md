# ProdOps

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
