'use client';

import type { OrderType, OrderExtras } from '@/types';

interface OrderSummaryProps {
  subtotal: number;
  orderType: OrderType;
  extras?: OrderExtras;
}

/**
 * Componente de resumo do pedido
 * Mostra cálculos de custos adicionais (Factory Method + Decorator)
 */
export default function OrderSummary({
  subtotal,
  orderType,
  extras,
}: OrderSummaryProps) {
  // Calcula taxa de envio baseada no tipo de pedido (Factory Method)
  const getShippingCost = () => {
    const rates = {
      regular: 0, // Sem taxa extra
      express: subtotal * 0.15, // +15%
      international: subtotal * 0.3, // +30%
    };
    return rates[orderType];
  };

  // Calcula custo dos extras (Decorator Pattern)
  const getExtrasCost = () => {
    let cost = 0;

    // Embalagem presente (+R$ 10)
    if (extras?.gift_wrap) {
      cost += 10;
    }

    // Seguro (5% ou 8%)
    if (extras?.insurance) {
      const rate = extras.insurance_type === 'premium' ? 0.08 : 0.05;
      cost += subtotal * rate;
    }

    return cost;
  };

  const shippingCost = getShippingCost();
  const extrasCost = getExtrasCost();
  const total = subtotal + shippingCost + extrasCost;

  const orderTypeLabels = {
    regular: 'Regular (7-10 dias)',
    express: 'Expresso (2-3 dias)',
    international: 'Internacional (15-30 dias)',
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-bold text-gray-800 mb-4">
        Resumo do Pedido
      </h2>

      <div className="space-y-3">
        {/* Subtotal */}
        <div className="flex justify-between text-gray-600">
          <span>Subtotal</span>
          <span>R$ {subtotal.toFixed(2)}</span>
        </div>

        {/* Tipo de Envio */}
        <div className="flex justify-between text-gray-600">
          <span>{orderTypeLabels[orderType]}</span>
          <span>
            {shippingCost > 0
              ? `+ R$ ${shippingCost.toFixed(2)}`
              : 'Grátis'}
          </span>
        </div>

        {/* Extras */}
        {extras?.gift_wrap && (
          <div className="flex justify-between text-gray-600">
            <span>Embalagem Presente</span>
            <span>+ R$ 10,00</span>
          </div>
        )}

        {extras?.insurance && (
          <div className="flex justify-between text-gray-600">
            <span>
              Seguro {extras.insurance_type === 'premium' ? 'Premium' : 'Padrão'}
            </span>
            <span>
              + R${' '}
              {(subtotal * (extras.insurance_type === 'premium' ? 0.08 : 0.05)).toFixed(2)}
            </span>
          </div>
        )}

        {/* Divider */}
        <div className="border-t border-gray-200 my-2" />

        {/* Total */}
        <div className="flex justify-between text-lg font-bold text-gray-800">
          <span>Total</span>
          <span className="text-primary-600">R$ {total.toFixed(2)}</span>
        </div>
      </div>

      {/* Informações Adicionais */}
      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <p className="text-sm text-blue-800">
          <strong>💡 Padrões de Projeto em Ação:</strong>
        </p>
        <ul className="mt-2 text-xs text-blue-700 space-y-1">
          <li>• <strong>Factory Method:</strong> Tipo de pedido determina custos</li>
          <li>• <strong>Decorator:</strong> Extras adicionados dinamicamente</li>
          <li>• <strong>Strategy:</strong> Método de pagamento selecionável</li>
        </ul>
      </div>
    </div>
  );
}
