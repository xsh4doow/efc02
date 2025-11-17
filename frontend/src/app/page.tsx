import Link from 'next/link';
import { ArrowRight, Package, ShoppingBag, CreditCard } from 'lucide-react';

/**
 * Página inicial (Home)
 */
export default function Home() {
  return (
    <div className="container mx-auto px-4 py-12">
      {/* Hero Section */}
      <div className="text-center mb-16">
        <h1 className="text-5xl font-bold text-gray-800 mb-4">
          Sistema de Pedidos com Padrões de Projeto
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
          Demonstração prática de 6 padrões de projeto integrados em um
          e-commerce funcional
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            href="/products"
            className="flex items-center gap-2 bg-primary-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-700 transition-colors"
          >
            Ver Produtos
            <ArrowRight className="h-5 w-5" />
          </Link>
          <Link
            href="/orders"
            className="flex items-center gap-2 border-2 border-primary-600 text-primary-600 px-6 py-3 rounded-lg font-semibold hover:bg-primary-50 transition-colors"
          >
            Meus Pedidos
          </Link>
        </div>
      </div>

      {/* Features Section */}
      <div className="grid md:grid-cols-3 gap-8 mb-16">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="bg-primary-100 w-12 h-12 rounded-full flex items-center justify-center mb-4">
            <Package className="h-6 w-6 text-primary-600" />
          </div>
          <h3 className="text-xl font-semibold mb-2">Múltiplos Produtos</h3>
          <p className="text-gray-600">
            Produtos físicos, digitais e assinaturas usando{' '}
            <strong>Factory Method</strong>
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="bg-green-100 w-12 h-12 rounded-full flex items-center justify-center mb-4">
            <ShoppingBag className="h-6 w-6 text-green-600" />
          </div>
          <h3 className="text-xl font-semibold mb-2">Tipos de Entrega</h3>
          <p className="text-gray-600">
            Regular, Expressa ou Internacional com cálculo automático de custos
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="bg-purple-100 w-12 h-12 rounded-full flex items-center justify-center mb-4">
            <CreditCard className="h-6 w-6 text-purple-600" />
          </div>
          <h3 className="text-xl font-semibold mb-2">Pagamento Flexível</h3>
          <p className="text-gray-600">
            Cartão, PIX ou Boleto usando padrão <strong>Strategy</strong>
          </p>
        </div>
      </div>

      {/* Design Patterns Section */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-700 text-white rounded-xl p-8 mb-16">
        <h2 className="text-3xl font-bold mb-6 text-center">
          6 Padrões de Projeto Implementados
        </h2>
        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-white/10 backdrop-blur-sm p-4 rounded-lg">
            <h4 className="font-bold mb-2">🏗️ Singleton</h4>
            <p className="text-sm">
              Gerenciamento único de configuração e banco de dados
            </p>
          </div>
          <div className="bg-white/10 backdrop-blur-sm p-4 rounded-lg">
            <h4 className="font-bold mb-2">📦 Repository</h4>
            <p className="text-sm">
              Abstração de acesso a dados separada da lógica de negócio
            </p>
          </div>
          <div className="bg-white/10 backdrop-blur-sm p-4 rounded-lg">
            <h4 className="font-bold mb-2">🏭 Factory Method</h4>
            <p className="text-sm">
              Criação de diferentes tipos de pedidos e produtos
            </p>
          </div>
          <div className="bg-white/10 backdrop-blur-sm p-4 rounded-lg">
            <h4 className="font-bold mb-2">🎯 Strategy</h4>
            <p className="text-sm">
              Múltiplos métodos de pagamento intercambiáveis
            </p>
          </div>
          <div className="bg-white/10 backdrop-blur-sm p-4 rounded-lg">
            <h4 className="font-bold mb-2">👁️ Observer</h4>
            <p className="text-sm">
              Notificações automáticas por email, SMS e logs
            </p>
          </div>
          <div className="bg-white/10 backdrop-blur-sm p-4 rounded-lg">
            <h4 className="font-bold mb-2">🎁 Decorator</h4>
            <p className="text-sm">
              Adição dinâmica de embalagem presente e seguro
            </p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-800 mb-4">
          Experimente Agora!
        </h2>
        <p className="text-gray-600 mb-6">
          Crie um pedido e veja todos os padrões trabalhando juntos
        </p>
        <Link
          href="/products"
          className="inline-flex items-center gap-2 bg-primary-600 text-white px-8 py-4 rounded-lg font-semibold hover:bg-primary-700 transition-colors text-lg"
        >
          Começar Compra
          <ArrowRight className="h-6 w-6" />
        </Link>
      </div>
    </div>
  );
}
