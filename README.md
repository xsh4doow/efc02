# Sistema de Pedidos - E-commerce com Padrões de Projeto

Sistema de e-commerce desenvolvido para demonstrar a aplicação prática de **6 padrões de projeto** de forma natural e funcional.

## 📝 Sobre o Projeto

Este projeto implementa um sistema completo de e-commerce com gerenciamento de pedidos, produtos e clientes. O foco principal é demonstrar como múltiplos padrões de projeto podem ser integrados de forma natural em uma aplicação real, resolvendo problemas reais de software.

### 🎯 Objetivo Acadêmico

Atividade de Estudo e Aplicação de Padrões de Projeto - Parte 2

## 🏗️ Arquitetura e Padrões de Projeto

### Padrões Implementados

#### 1. **Singleton** (Criacional)
- **Localização**: `backend/app/config.py` e `backend/app/database.py`
- **Classe**: `ConfigManager` e `DatabaseManager`
- **Propósito**: Garantir uma única instância de configuração e conexão de banco de dados
- **Benefício**: Previne múltiplas instâncias, garante estado consistente e economiza recursos

#### 2. **Repository** (Arquitetural)
- **Localização**: `backend/app/repositories/`
- **Classes**: `BaseRepository`, `ProductRepository`, `CustomerRepository`, `OrderRepository`
- **Propósito**: Abstrair lógica de acesso a dados da lógica de negócio
- **Benefício**: Facilita testes, permite trocar banco de dados sem alterar lógica de negócio

#### 3. **Factory Method** (Criacional)
- **Localização**: `backend/app/factories/`
- **Classes**: `OrderFactory`, `ProductFactory`
- **Propósito**: Criar diferentes tipos de objetos sem expor lógica de criação
- **Benefício**: Evita código condicional complexo, facilita adicionar novos tipos

**Tipos de Pedidos:**
- `RegularOrder`: Entrega padrão (7-10 dias), sem taxas extras
- `ExpressOrder`: Entrega rápida (2-3 dias), +15% de taxa
- `InternationalOrder`: Envio internacional (15-30 dias), +30% de taxa

**Tipos de Produtos:**
- `PhysicalProduct`: Produtos físicos que precisam de envio
- `DigitalProduct`: Produtos digitais (download)
- `SubscriptionProduct`: Assinaturas mensais

#### 4. **Strategy** (Comportamental)
- **Localização**: `backend/app/strategies/`
- **Classes**: `PaymentStrategy`, `CreditCardPayment`, `PixPayment`, `BoletoPayment`
- **Propósito**: Definir família de algoritmos intercambiáveis
- **Benefício**: Elimina condicionais, cada estratégia é independente e testável

**Métodos de Pagamento:**
- `CreditCard`: Aprovação instantânea
- `PIX`: Gera código/QR code, expira em 30 minutos
- `Boleto`: Gera boleto bancário, vence em 3 dias

#### 5. **Observer** (Comportamental)
- **Localização**: `backend/app/observers/`
- **Classes**: `OrderSubject`, `EmailNotifier`, `SmsNotifier`, `LogNotifier`
- **Propósito**: Notificar múltiplos objetos quando estado muda
- **Benefício**: Baixo acoplamento, fácil adicionar/remover notificadores

**Notificadores:**
- `EmailNotifier`: Envia emails sobre mudanças de status
- `SmsNotifier`: Envia SMS para cliente
- `LogNotifier`: Registra mudanças em logs

#### 6. **Decorator** (Estrutural)
- **Localização**: `backend/app/decorators/`
- **Classes**: `OrderDecorator`, `GiftWrapDecorator`, `InsuranceDecorator`
- **Propósito**: Adicionar responsabilidades dinamicamente
- **Benefício**: Evita explosão de subclasses, permite combinações flexíveis

**Extras Disponíveis:**
- `GiftWrap`: Adiciona embalagem presente (+R$ 10,00)
- `Insurance`: Adiciona seguro (5% ou 8% do valor)

### 🔄 Integração dos Padrões

O `OrderService` demonstra como todos os padrões trabalham juntos:

```python
# 1. Repository: Obtém dados
customer = customer_repo.get_by_email(email)

# 2. Decorator: Calcula extras
order_component = BaseOrder(subtotal)
if has_gift_wrap:
    order_component = GiftWrapDecorator(order_component)

# 3. Factory Method: Cria pedido do tipo correto
order = OrderFactory.create_order(order_type, order_data)

# 4. Strategy: Processa pagamento
payment_result = payment_strategy.process_payment(amount, details)

# 5. Repository: Persiste
created_order = order_repo.create_with_items(order, items)

# 6. Observer: Notifica
notification_service.notify_order_status_change(...)
```

## 🚀 Como Executar

### Pré-requisitos

**Backend:**
- Python 3.11+
- pip (gerenciador de pacotes Python)

**Frontend:**
- Node.js 18+
- npm ou yarn

### Instalação e Execução do Backend

```bash
# 1. Entre na pasta do backend
cd backend

# 2. Crie ambiente virtual
python -m venv venv

# 3. Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instale dependências
pip install -r requirements.txt

# 5. Execute seed para popular banco com produtos
python -m app.seed

# 6. Inicie o servidor
uvicorn app.main:app --reload

# OU simplesmente:
python -m app.main
```

### Instalação e Execução do Frontend

```bash
# 1. Entre na pasta do frontend
cd frontend

# 2. Instale as dependências
npm install
# ou
yarn install

# 3. Configure variáveis de ambiente (já criado)
# O arquivo .env.local já está configurado com:
# NEXT_PUBLIC_API_URL=http://localhost:8000

# 4. Inicie o servidor de desenvolvimento
npm run dev
# ou
yarn dev
```

### Acessar Aplicação

**Backend:**
- **API**: http://localhost:8000
- **Documentação Interativa (Swagger)**: http://localhost:8000/docs
- **Documentação Alternativa (ReDoc)**: http://localhost:8000/redoc

**Frontend:**
- **Aplicação Web**: http://localhost:3000
- **Páginas Disponíveis**:
  - `/` - Home com apresentação dos padrões
  - `/products` - Catálogo de produtos
  - `/cart` - Carrinho de compras
  - `/checkout` - Finalização de pedido (demonstra TODOS os padrões)
  - `/orders` - Lista de pedidos
  - `/orders/[id]` - Detalhes de um pedido específico

## 📂 Estrutura do Projeto

```
EFC 02/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # Entry point FastAPI
│   │   ├── config.py                  # Singleton: ConfigManager
│   │   ├── database.py                # Singleton: DatabaseManager
│   │   ├── seed.py                    # Script para popular BD
│   │   │
│   │   ├── models/                    # Models SQLAlchemy
│   │   │   ├── product.py
│   │   │   ├── customer.py
│   │   │   └── order.py
│   │   │
│   │   ├── schemas/                   # Schemas Pydantic
│   │   │   ├── product_schema.py
│   │   │   ├── customer_schema.py
│   │   │   └── order_schema.py
│   │   │
│   │   ├── repositories/              # Repository Pattern
│   │   │   ├── base_repository.py
│   │   │   ├── product_repository.py
│   │   │   ├── customer_repository.py
│   │   │   └── order_repository.py
│   │   │
│   │   ├── factories/                 # Factory Method Pattern
│   │   │   ├── order_factory.py
│   │   │   └── product_factory.py
│   │   │
│   │   ├── strategies/                # Strategy Pattern
│   │   │   ├── payment_strategy.py
│   │   │   ├── credit_card_payment.py
│   │   │   ├── pix_payment.py
│   │   │   └── boleto_payment.py
│   │   │
│   │   ├── observers/                 # Observer Pattern
│   │   │   ├── order_observer.py
│   │   │   ├── order_subject.py
│   │   │   ├── email_notifier.py
│   │   │   ├── sms_notifier.py
│   │   │   └── log_notifier.py
│   │   │
│   │   ├── decorators/                # Decorator Pattern
│   │   │   ├── order_decorator.py
│   │   │   ├── gift_wrap_decorator.py
│   │   │   └── insurance_decorator.py
│   │   │
│   │   ├── services/                  # Lógica de negócio
│   │   │   ├── order_service.py       # Integra todos os padrões
│   │   │   └── notification_service.py
│   │   │
│   │   └── routers/                   # Endpoints FastAPI
│   │       ├── products.py
│   │       ├── customers.py
│   │       └── orders.py
│   │
│   ├── tests/                         # Testes pytest
│   │   ├── test_factories.py
│   │   ├── test_strategies.py
│   │   ├── test_observers.py
│   │   └── test_decorators.py
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── app/                       # Next.js App Router
│   │   │   ├── layout.tsx             # Layout principal
│   │   │   ├── page.tsx               # Página inicial
│   │   │   ├── globals.css            # Estilos globais
│   │   │   ├── products/              # Página de produtos
│   │   │   ├── cart/                  # Página do carrinho
│   │   │   ├── checkout/              # Página de checkout
│   │   │   └── orders/                # Páginas de pedidos
│   │   │
│   │   ├── components/                # Componentes React
│   │   │   ├── Navbar.tsx             # Navegação
│   │   │   ├── ProductCard.tsx        # Card de produto
│   │   │   ├── CartItem.tsx           # Item do carrinho
│   │   │   ├── PaymentMethod.tsx      # Seleção de pagamento
│   │   │   └── OrderSummary.tsx       # Resumo do pedido
│   │   │
│   │   ├── contexts/                  # React Contexts
│   │   │   └── CartContext.tsx        # Estado do carrinho
│   │   │
│   │   ├── services/                  # Serviços e API
│   │   │   └── api.ts                 # Cliente Axios
│   │   │
│   │   └── types/                     # TypeScript Types
│   │       └── index.ts               # Definições de tipos
│   │
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.js
│   └── .env.local
│
├── docs/
│   └── RESUMO.md                      # Estudo teórico dos padrões
│
├── .gitignore
└── README.md                          # Este arquivo
```

## 🧪 Executar Testes

```bash
cd backend
pytest -v
```

Os testes cobrem todos os padrões de projeto implementados.

## 📡 API Endpoints

### Produtos

- `GET /api/products` - Lista produtos
- `GET /api/products/{id}` - Detalhes do produto
- `POST /api/products` - Cria produto (usa Factory Method)
- `PATCH /api/products/{id}` - Atualiza produto
- `DELETE /api/products/{id}` - Deleta produto

### Clientes

- `GET /api/customers` - Lista clientes
- `GET /api/customers/{id}` - Detalhes do cliente
- `POST /api/customers` - Cria cliente
- `PATCH /api/customers/{id}` - Atualiza cliente
- `DELETE /api/customers/{id}` - Deleta cliente

### Pedidos (Demonstra TODOS os padrões)

- `POST /api/orders` - **Cria pedido (USA TODOS OS PADRÕES)**
  - Factory Method: Cria tipo correto de pedido
  - Strategy: Processa pagamento
  - Decorator: Adiciona extras
  - Observer: Notifica criação
  - Repository: Persiste dados

- `GET /api/orders` - Lista pedidos
- `GET /api/orders/{id}` - Detalhes do pedido
- `GET /api/orders/customer/{id}` - Pedidos do cliente
- `PATCH /api/orders/{id}/status` - **Atualiza status (DISPARA OBSERVERS)**

### Exemplo de Criação de Pedido

```json
POST /api/orders
{
  "customer": {
    "name": "João Silva",
    "email": "joao@email.com",
    "phone": "11999999999",
    "address": "Rua X, 123"
  },
  "order_type": "express",
  "payment_method": "pix",
  "items": [
    {"product_id": 1, "quantity": 2},
    {"product_id": 3, "quantity": 1}
  ],
  "extras": {
    "gift_wrap": true,
    "gift_message": "Feliz Aniversário!",
    "insurance": true,
    "insurance_type": "premium"
  }
}
```

## 💡 Destaques de Implementação

### Código Limpo
- ✅ Type hints em todas as funções
- ✅ Docstrings em PT-BR
- ✅ Separação clara de responsabilidades
- ✅ Validação com Pydantic
- ✅ Tratamento de erros

### Arquitetura
- ✅ Camadas bem definidas (Models, Repositories, Services, Routers)
- ✅ Baixo acoplamento entre componentes
- ✅ Alta coesão dentro de cada módulo
- ✅ Princípios SOLID aplicados

### Padrões de Projeto
- ✅ Implementação natural (não forçada)
- ✅ Resolvem problemas reais
- ✅ Código funcional e testável
- ✅ Bem documentado e justificado

## 📚 Documentação Adicional

- **RESUMO.md**: Estudo teórico completo dos padrões, comparações, justificativas e exemplos

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.11+**
- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM para banco de dados
- **SQLite** - Banco de dados local
- **Pydantic** - Validação de dados
- **Pytest** - Framework de testes
- **Uvicorn** - Servidor ASGI

### Frontend
- **Next.js 14** - Framework React
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Framework CSS utilitário
- **Axios** - Cliente HTTP
- **Lucide React** - Ícones

## 📄 Licença

MIT

## 👥 Autores

- **Pedro Beresford Rocha**
- **Gabriella Cardoso Dos Santos**

---

