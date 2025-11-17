'use client';

import { Minus, Plus, X } from 'lucide-react';
import type { CartItem as CartItemType } from '@/types';
import { useCart } from '@/contexts/CartContext';

interface CartItemProps {
  item: CartItemType;
}

/**
 * Componente de item do carrinho com controles de quantidade
 */
export default function CartItem({ item }: CartItemProps) {
  const { updateQuantity, removeFromCart } = useCart();
  const { product, quantity } = item;

  const handleIncrease = () => {
    if (quantity < product.stock_quantity) {
      updateQuantity(product.id, quantity + 1);
    }
  };

  const handleDecrease = () => {
    if (quantity > 1) {
      updateQuantity(product.id, quantity - 1);
    }
  };

  const handleRemove = () => {
    removeFromCart(product.id);
  };

  const subtotal = product.price * quantity;

  return (
    <div className="flex items-center gap-4 bg-white p-4 rounded-lg shadow">
      {/* Imagem */}
      <div className="w-20 h-20 bg-gray-200 rounded flex-shrink-0 flex items-center justify-center">
        {product.image_url ? (
          <img
            src={product.image_url}
            alt={product.name}
            className="w-full h-full object-cover rounded"
          />
        ) : (
          <span className="text-gray-400 text-xs">Sem imagem</span>
        )}
      </div>

      {/* Informações do Produto */}
      <div className="flex-1">
        <h3 className="font-semibold text-gray-800">{product.name}</h3>
        <p className="text-sm text-gray-600">R$ {product.price.toFixed(2)}</p>
        <p className="text-xs text-gray-500">
          Estoque disponível: {product.stock_quantity}
        </p>
      </div>

      {/* Controles de Quantidade */}
      <div className="flex items-center gap-2">
        <button
          onClick={handleDecrease}
          disabled={quantity <= 1}
          className="p-1 rounded-full hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
          aria-label="Diminuir quantidade"
        >
          <Minus className="h-4 w-4" />
        </button>

        <span className="w-12 text-center font-semibold">{quantity}</span>

        <button
          onClick={handleIncrease}
          disabled={quantity >= product.stock_quantity}
          className="p-1 rounded-full hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
          aria-label="Aumentar quantidade"
        >
          <Plus className="h-4 w-4" />
        </button>
      </div>

      {/* Subtotal */}
      <div className="text-right">
        <p className="font-bold text-lg text-primary-600">
          R$ {subtotal.toFixed(2)}
        </p>
      </div>

      {/* Botão Remover */}
      <button
        onClick={handleRemove}
        className="p-2 text-red-500 hover:bg-red-50 rounded-full transition-colors"
        aria-label="Remover item"
      >
        <X className="h-5 w-5" />
      </button>
    </div>
  );
}
