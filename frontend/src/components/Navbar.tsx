'use client';

import Link from 'next/link';
import { ShoppingCart, Package } from 'lucide-react';
import { useCart } from '@/contexts/CartContext';

/**
 * Componente de navegação principal
 */
export default function Navbar() {
  const { getCartCount } = useCart();
  const cartCount = getCartCount();

  return (
    <nav className="bg-primary-600 text-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo e Nome */}
          <Link href="/" className="flex items-center space-x-2 hover:opacity-80">
            <Package className="h-8 w-8" />
            <span className="text-xl font-bold">E-Commerce Padrões</span>
          </Link>

          {/* Links de Navegação */}
          <div className="flex items-center space-x-6">
            <Link
              href="/"
              className="hover:text-primary-200 transition-colors"
            >
              Início
            </Link>
            <Link
              href="/products"
              className="hover:text-primary-200 transition-colors"
            >
              Produtos
            </Link>
            <Link
              href="/orders"
              className="hover:text-primary-200 transition-colors"
            >
              Meus Pedidos
            </Link>

            {/* Carrinho com Badge */}
            <Link
              href="/cart"
              className="relative flex items-center hover:text-primary-200 transition-colors"
            >
              <ShoppingCart className="h-6 w-6" />
              {cartCount > 0 && (
                <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center">
                  {cartCount}
                </span>
              )}
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
