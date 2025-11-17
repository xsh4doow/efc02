'use client';

import { ShoppingCart, Check } from 'lucide-react';
import type { Product } from '@/types';
import { useCart } from '@/contexts/CartContext';

interface ProductCardProps {
  product: Product;
}

/**
 * Card de exibição de produto
 */
export default function ProductCard({ product }: ProductCardProps) {
  const { addToCart, isInCart } = useCart();
  const inCart = isInCart(product.id);

  const handleAddToCart = () => {
    addToCart(product, 1);
  };

  const getProductTypeBadge = () => {
    const badges: Record<string, { text: string; color: string }> = {
      physical: { text: 'Físico', color: 'bg-blue-100 text-blue-800' },
      digital: { text: 'Digital', color: 'bg-green-100 text-green-800' },
      subscription: { text: 'Assinatura', color: 'bg-purple-100 text-purple-800' },
    };

    const badge = badges[product.product_type] || badges.physical;
    return (
      <span
        className={`inline-block px-2 py-1 text-xs font-semibold rounded ${badge.color}`}
      >
        {badge.text}
      </span>
    );
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow">
      {/* Imagem do Produto */}
      <div className="h-48 bg-gray-200 flex items-center justify-center">
        {product.image_url ? (
          <img
            src={product.image_url}
            alt={product.name}
            className="w-full h-full object-cover"
          />
        ) : (
          <span className="text-gray-400 text-sm">Sem imagem</span>
        )}
      </div>

      {/* Conteúdo */}
      <div className="p-4">
        {/* Badge do Tipo */}
        <div className="mb-2">{getProductTypeBadge()}</div>

        {/* Nome */}
        <h3 className="text-lg font-semibold text-gray-800 mb-2">
          {product.name}
        </h3>

        {/* Descrição */}
        <p className="text-gray-600 text-sm mb-4 line-clamp-2">
          {product.description}
        </p>

        {/* Preço e Estoque */}
        <div className="flex items-center justify-between mb-4">
          <span className="text-2xl font-bold text-primary-600">
            R$ {product.price.toFixed(2)}
          </span>
          <span className="text-sm text-gray-500">
            Estoque: {product.stock_quantity}
          </span>
        </div>

        {/* Botão Adicionar ao Carrinho */}
        <button
          onClick={handleAddToCart}
          disabled={product.stock_quantity === 0 || inCart}
          className={`w-full flex items-center justify-center space-x-2 px-4 py-2 rounded-lg font-semibold transition-colors ${
            product.stock_quantity === 0
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : inCart
              ? 'bg-green-500 text-white cursor-default'
              : 'bg-primary-600 text-white hover:bg-primary-700'
          }`}
        >
          {inCart ? (
            <>
              <Check className="h-5 w-5" />
              <span>No Carrinho</span>
            </>
          ) : (
            <>
              <ShoppingCart className="h-5 w-5" />
              <span>
                {product.stock_quantity === 0
                  ? 'Sem Estoque'
                  : 'Adicionar ao Carrinho'}
              </span>
            </>
          )}
        </button>
      </div>
    </div>
  );
}
