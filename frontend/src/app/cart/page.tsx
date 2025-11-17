'use client';

import { useCart } from '@/contexts/CartContext';
import CartItem from '@/components/CartItem';
import Link from 'next/link';
import { ShoppingCart, ArrowRight } from 'lucide-react';

/**
 * Página do carrinho de compras
 */
export default function CartPage() {
  const { items, getCartTotal, clearCart } = useCart();
  const total = getCartTotal();

  if (items.length === 0) {
    return (
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-2xl mx-auto text-center">
          <ShoppingCart className="h-24 w-24 mx-auto text-gray-300 mb-4" />
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            Seu carrinho está vazio
          </h1>
          <p className="text-gray-600 mb-6">
            Adicione alguns produtos para continuar comprando
          </p>
          <Link
            href="/products"
            className="inline-flex items-center gap-2 bg-primary-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-700 transition-colors"
          >
            Ver Produtos
            <ArrowRight className="h-5 w-5" />
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-4xl font-bold text-gray-800">
            Carrinho de Compras
          </h1>
          <button
            onClick={clearCart}
            className="text-red-600 hover:text-red-700 font-semibold text-sm"
          >
            Limpar Carrinho
          </button>
        </div>

        {/* Items */}
        <div className="space-y-4 mb-8">
          {items.map((item) => (
            <CartItem key={item.product.id} item={item} />
          ))}
        </div>

        {/* Total e Checkout */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between mb-6">
            <span className="text-xl font-semibold text-gray-800">
              Total do Carrinho:
            </span>
            <span className="text-3xl font-bold text-primary-600">
              R$ {total.toFixed(2)}
            </span>
          </div>

          <div className="flex gap-4">
            <Link
              href="/products"
              className="flex-1 text-center py-3 border-2 border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50 transition-colors"
            >
              Continuar Comprando
            </Link>
            <Link
              href="/checkout"
              className="flex-1 flex items-center justify-center gap-2 bg-primary-600 text-white py-3 rounded-lg font-semibold hover:bg-primary-700 transition-colors"
            >
              Finalizar Compra
              <ArrowRight className="h-5 w-5" />
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
