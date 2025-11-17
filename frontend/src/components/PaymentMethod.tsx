'use client';

import { CreditCard, QrCode, FileText } from 'lucide-react';
import type { PaymentMethod as PaymentMethodType } from '@/types';

interface PaymentMethodProps {
  selected: PaymentMethodType;
  onChange: (method: PaymentMethodType) => void;
}

/**
 * Componente de seleção de método de pagamento
 * Demonstra o padrão Strategy - diferentes estratégias de pagamento
 */
export default function PaymentMethod({
  selected,
  onChange,
}: PaymentMethodProps) {
  const methods: Array<{
    id: PaymentMethodType;
    name: string;
    description: string;
    icon: React.ReactNode;
  }> = [
    {
      id: 'credit_card',
      name: 'Cartão de Crédito',
      description: 'Aprovação instantânea',
      icon: <CreditCard className="h-6 w-6" />,
    },
    {
      id: 'pix',
      name: 'PIX',
      description: 'Código expira em 30 minutos',
      icon: <QrCode className="h-6 w-6" />,
    },
    {
      id: 'boleto',
      name: 'Boleto Bancário',
      description: 'Vencimento em 3 dias',
      icon: <FileText className="h-6 w-6" />,
    },
  ];

  return (
    <div className="space-y-3">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">
        Método de Pagamento
      </h3>

      {methods.map((method) => (
        <button
          key={method.id}
          onClick={() => onChange(method.id)}
          className={`w-full flex items-center gap-4 p-4 rounded-lg border-2 transition-all ${
            selected === method.id
              ? 'border-primary-600 bg-primary-50'
              : 'border-gray-200 hover:border-primary-300'
          }`}
        >
          {/* Ícone */}
          <div
            className={`${
              selected === method.id ? 'text-primary-600' : 'text-gray-400'
            }`}
          >
            {method.icon}
          </div>

          {/* Informações */}
          <div className="flex-1 text-left">
            <p className="font-semibold text-gray-800">{method.name}</p>
            <p className="text-sm text-gray-600">{method.description}</p>
          </div>

          {/* Indicador de Seleção */}
          {selected === method.id && (
            <div className="w-5 h-5 rounded-full bg-primary-600 flex items-center justify-center">
              <div className="w-2 h-2 rounded-full bg-white" />
            </div>
          )}
        </button>
      ))}
    </div>
  );
}
