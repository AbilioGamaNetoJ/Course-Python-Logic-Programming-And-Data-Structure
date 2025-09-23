# 📖 Guia de Uso - Sistema de Gestão Empresarial

## 🚀 Introdução

Bem-vindo ao Sistema de Gestão Empresarial! Este guia irá orientá-lo através de todas as funcionalidades disponíveis no sistema, desde a configuração inicial até o uso avançado de relatórios e auditoria.

## ⚙️ Configuração Inicial

### 1. Preparação do Ambiente

Antes de usar o sistema, certifique-se de ter Python 3.8+ instalado em seu computador.

### 2. Configuração das Variáveis de Ambiente

1. **Copie o arquivo de exemplo**:
   ```bash
   cp .env.example .env
   ```

2. **Configure as variáveis no arquivo `.env`**:
   ```env
   # Configurações de Logging
   LOG_FILE=sistema_gestao.log
   LOG_CONSOLE=true
   LOG_LEVEL=INFO
   LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s

   # Configurações de Database
   DB_TYPE=memory
   DB_PATH=./data/sistema.db
   DB_BACKUP_ENABLED=true
   DB_BACKUP_INTERVAL=3600

   # Regras de Negócio
   DEFAULT_CREDIT_LIMIT=5000.0
   MIN_STOCK_LEVEL=10
   MAX_DISCOUNT_PERCENT=50.0

   # Configurações de Segurança
   AUDIT_ENABLED=true
   SESSION_TIMEOUT=1800
   MAX_LOGIN_ATTEMPTS=3

   # Configurações do Sistema
   INIT_SAMPLE_DATA=true
   CACHE_ENABLED=true
   CACHE_TTL=300
   ```

### 3. Iniciando o Sistema

Execute o comando no terminal:
```bash
python 01_sistema_gestao.py
```

## 🎯 Navegação Principal

Ao iniciar o sistema, você verá o menu principal com as seguintes opções:

```
=== SISTEMA DE GESTÃO EMPRESARIAL ===
1. 👥 Gestão de Clientes
2. 📦 Gestão de Produtos
3. 🛒 Gestão de Pedidos
4. 📊 Relatórios
5. ⚙️ Configurações
6. 🔍 Sistema de Auditoria
0. ❌ Sair
```

## 👥 Gestão de Clientes

### Acessando o Menu de Clientes
Selecione a opção **1** no menu principal.

### Funcionalidades Disponíveis

#### ➕ Cadastrar Novo Cliente
1. Selecione **1 - Cadastrar Cliente**
2. Preencha as informações solicitadas:
   - **Nome completo**
   - **Email** (deve ser único no sistema)
   - **Telefone**
   - **Tipo de cliente** (Pessoa Física ou Jurídica)
   - **Endereço completo**:
     - Rua
     - Número
     - Complemento (opcional)
     - Bairro
     - Cidade
     - Estado
     - CEP
   - **Limite de crédito** (opcional, usa padrão do sistema)

**Exemplo de cadastro**:
```
Nome: João Silva
Email: joao.silva@email.com
Telefone: (11) 99999-9999
Tipo: 1 (Pessoa Física)
Rua: Rua das Flores
Número: 123
Complemento: Apto 45
Bairro: Centro
Cidade: São Paulo
Estado: SP
CEP: 01234-567
Limite de Crédito: 10000.00
```

#### 🔍 Buscar Cliente
1. Selecione **2 - Buscar Cliente**
2. Escolha o tipo de busca:
   - **Por ID**: Digite o ID único do cliente
   - **Por Nome**: Digite parte do nome (busca parcial)
   - **Por Email**: Digite o email exato

#### 📋 Listar Clientes
1. Selecione **3 - Listar Clientes**
2. Escolha o filtro desejado:
   - **Todos os clientes**
   - **Apenas ativos**
   - **Apenas inativos**
   - **Por tipo** (Pessoa Física/Jurídica)

#### ✏️ Atualizar Cliente
1. Selecione **4 - Atualizar Cliente**
2. Informe o ID do cliente
3. Atualize os campos desejados (deixe em branco para manter o valor atual)

#### ❌ Desativar Cliente
1. Selecione **5 - Desativar Cliente**
2. Informe o ID do cliente
3. Confirme a operação

## 📦 Gestão de Produtos

### Acessando o Menu de Produtos
Selecione a opção **2** no menu principal.

### Funcionalidades Disponíveis

#### ➕ Cadastrar Novo Produto
1. Selecione **1 - Cadastrar Produto**
2. Preencha as informações:
   - **Nome do produto**
   - **Descrição detalhada**
   - **Categoria** (Eletrônicos, Roupas, Casa, Livros, Esportes, Outros)
   - **Preço unitário**
   - **Quantidade em estoque**
   - **Estoque mínimo**

**Exemplo de cadastro**:
```
Nome: Smartphone XYZ
Descrição: Smartphone com 128GB, câmera 48MP
Categoria: 1 (Eletrônicos)
Preço: 899.99
Quantidade em Estoque: 50
Estoque Mínimo: 10
```

#### 🔍 Buscar Produto
- **Por ID**: Busca exata por identificador
- **Por Nome**: Busca parcial no nome
- **Por Categoria**: Lista produtos de uma categoria específica

#### 📋 Listar Produtos
- **Todos os produtos**
- **Produtos ativos**
- **Produtos com estoque baixo**
- **Por faixa de preço**

#### 📈 Atualizar Estoque
1. Selecione **5 - Atualizar Estoque**
2. Informe o ID do produto
3. Escolha a operação:
   - **Adicionar** ao estoque
   - **Remover** do estoque
   - **Definir** quantidade exata

## 🛒 Gestão de Pedidos

### Acessando o Menu de Pedidos
Selecione a opção **3** no menu principal.

### Criando um Novo Pedido

#### Passo 1: Iniciar Pedido
1. Selecione **1 - Criar Pedido**
2. Informe o **ID do cliente**
3. O sistema validará se o cliente existe e está ativo

#### Passo 2: Adicionar Itens
1. Para cada item do pedido:
   - **ID do produto**
   - **Quantidade desejada**
   - **Desconto** (opcional, máximo 50%)

2. O sistema verificará:
   - Se o produto existe
   - Se há estoque suficiente
   - Se o desconto está dentro do limite

#### Passo 3: Finalizar Pedido
1. Revise o resumo do pedido
2. Confirme a criação
3. O sistema:
   - Atualizará o estoque automaticamente
   - Calculará o total com descontos
   - Verificará o limite de crédito do cliente
   - Gerará um ID único para o pedido

### Gerenciando Pedidos Existentes

#### 🔍 Buscar Pedidos
- **Por ID do pedido**
- **Por cliente**
- **Por período**
- **Por status**

#### 📋 Listar Pedidos
- **Todos os pedidos**
- **Pedidos pendentes**
- **Pedidos processados**
- **Pedidos cancelados**

#### 🔄 Atualizar Status
1. Selecione **4 - Atualizar Status**
2. Informe o ID do pedido
3. Escolha o novo status:
   - **Pendente**
   - **Processando**
   - **Enviado**
   - **Entregue**
   - **Cancelado**

## 📊 Sistema de Relatórios

### Acessando Relatórios
Selecione a opção **4** no menu principal.

### Tipos de Relatórios Disponíveis

#### 📈 Relatório de Vendas por Período
1. Selecione **1 - Vendas por Período**
2. Informe:
   - **Data inicial** (formato: DD/MM/AAAA)
   - **Data final** (formato: DD/MM/AAAA)
3. O relatório mostrará:
   - Total de vendas no período
   - Número de pedidos
   - Ticket médio
   - Produtos mais vendidos

#### 📦 Relatório de Estoque Atual
1. Selecione **2 - Estoque Atual**
2. Visualize:
   - Produtos com estoque baixo
   - Valor total do estoque
   - Produtos sem movimento
   - Sugestões de reposição

#### 👥 Relatório de Clientes
1. Selecione **3 - Dados de Clientes**
2. Analise:
   - Clientes mais ativos
   - Distribuição por tipo
   - Limite de crédito utilizado
   - Clientes inativos

#### 🏆 Performance de Produtos
1. Selecione **4 - Performance de Produtos**
2. Veja:
   - Produtos mais vendidos
   - Margem de lucro por produto
   - Produtos com baixa rotatividade
   - Análise de categorias

#### 💰 Relatório Financeiro
1. Selecione **5 - Relatório Financeiro**
2. Obtenha:
   - Receita total
   - Receita por período
   - Análise de descontos
   - Projeções de faturamento

#### 📋 Dashboard Executivo
1. Selecione **6 - Dashboard Executivo**
2. Visão geral com:
   - KPIs principais
   - Gráficos de tendência
   - Alertas importantes
   - Resumo de performance

### 💾 Exportação de Relatórios
Todos os relatórios podem ser exportados em formato CSV:
1. Após gerar qualquer relatório
2. Selecione a opção **Exportar para CSV**
3. O arquivo será salvo na pasta `exports/`

## 🔍 Sistema de Auditoria

### Acessando a Auditoria
Selecione a opção **6** no menu principal.

### Funcionalidades de Auditoria

#### 📋 Visualizar Logs
1. Selecione **1 - Visualizar Logs**
2. Escolha o filtro:
   - **Todos os logs**
   - **Por usuário**
   - **Por tipo de operação**
   - **Por período**
   - **Por entidade** (Cliente, Produto, Pedido)

#### 🔍 Buscar Logs Específicos
1. Selecione **2 - Buscar Logs**
2. Use filtros combinados:
   - **Data/hora específica**
   - **Tipo de operação** (CREATE, UPDATE, DELETE, READ)
   - **ID da entidade**
   - **Usuário responsável**

#### ⚠️ Atividades Suspeitas
1. Selecione **3 - Atividades Suspeitas**
2. O sistema detecta automaticamente:
   - Múltiplas tentativas de acesso
   - Operações fora do horário comercial
   - Alterações em massa
   - Padrões anômalos de uso

#### 📊 Relatório de Atividades
1. Selecione **4 - Relatório de Atividades**
2. Analise:
   - Operações por usuário
   - Horários de maior atividade
   - Tipos de operação mais frequentes
   - Estatísticas de uso do sistema

#### 🧹 Limpeza de Logs
1. Selecione **5 - Limpeza de Logs**
2. Configure:
   - **Período de retenção** (em dias)
   - **Tipos de log a manter**
   - **Backup antes da limpeza**

## ⚙️ Configurações do Sistema

### Acessando Configurações
Selecione a opção **5** no menu principal.

### Opções de Configuração

#### 🔧 Configurações Gerais
- **Limite de crédito padrão**
- **Estoque mínimo padrão**
- **Desconto máximo permitido**
- **Timeout de sessão**

#### 📝 Configurações de Log
- **Nível de log** (DEBUG, INFO, WARNING, ERROR)
- **Arquivo de log**
- **Rotação de logs**
- **Log no console**

#### 💾 Configurações de Backup
- **Intervalo de backup automático**
- **Pasta de backup**
- **Número de backups a manter**
- **Compressão de backups**

#### 🔒 Configurações de Segurança
- **Auditoria habilitada**
- **Tentativas máximas de login**
- **Tempo de bloqueio**
- **Criptografia de dados**

## 🆘 Solução de Problemas

### Problemas Comuns

#### ❌ "Email já cadastrado"
**Causa**: Tentativa de cadastrar cliente com email já existente
**Solução**: Use um email diferente ou atualize o cliente existente

#### ❌ "Estoque insuficiente"
**Causa**: Tentativa de vender mais produtos do que disponível
**Solução**: Verifique o estoque atual ou reduza a quantidade

#### ❌ "Cliente não encontrado"
**Causa**: ID do cliente inválido ou cliente desativado
**Solução**: Verifique o ID ou reative o cliente se necessário

#### ❌ "Limite de crédito excedido"
**Causa**: Valor do pedido ultrapassa o limite do cliente
**Solução**: Aumente o limite do cliente ou reduza o valor do pedido

### 🔧 Manutenção do Sistema

#### Backup Manual
```bash
# Criar backup dos dados
python -c "from repositories import RepositorioArquivo; repo = RepositorioArquivo('./data'); repo.backup()"
```

#### Limpeza de Logs
```bash
# Limpar logs antigos (mais de 30 dias)
python -c "from audit import SistemaAuditoria; audit = SistemaAuditoria(); audit.limpar_logs_antigos(30)"
```

#### Verificação de Integridade
```bash
# Executar testes do sistema
python test_sistema_modular.py
```

## 📞 Suporte

### Logs do Sistema
Em caso de problemas, verifique os arquivos de log:
- `sistema_gestao.log` - Log principal do sistema
- `auditoria.log` - Log de auditoria
- `exports/` - Relatórios exportados
- `backups/` - Backups automáticos

### Informações Técnicas
- **Versão do Python**: 3.8+
- **Arquitetura**: Modular
- **Persistência**: Arquivo/Memória
- **Formato de dados**: JSON
- **Encoding**: UTF-8

### Contato
Para suporte técnico ou dúvidas sobre funcionalidades, consulte:
- **Documentação Técnica**: `ARQUITETURA_MODULAR.md`
- **Código Fonte**: Módulos individuais na pasta do projeto
- **Testes**: `test_sistema_modular.py`

---

## 🎯 Dicas de Uso Eficiente

### ✅ Boas Práticas
1. **Sempre faça backup** antes de operações em massa
2. **Monitore os logs** regularmente para detectar problemas
3. **Use filtros** nos relatórios para obter informações específicas
4. **Mantenha dados atualizados** para relatórios precisos
5. **Configure alertas** para estoque baixo

### ⚡ Atalhos Úteis
- **Ctrl+C**: Interrompe operação atual
- **Enter**: Confirma operação
- **0**: Volta ao menu anterior
- **q**: Sair rápido (em alguns menus)

### 📈 Otimização de Performance
- **Use filtros** ao listar grandes quantidades de dados
- **Exporte relatórios** em horários de menor uso
- **Limpe logs antigos** periodicamente
- **Monitore uso de memória** em operações grandes

---

**🎉 Parabéns!** Agora você está pronto para usar todas as funcionalidades do Sistema de Gestão Empresarial. Explore as diferentes opções e aproveite a flexibilidade e robustez da arquitetura modular implementada!