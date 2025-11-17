'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useCart } from '@/contexts/CartContext';
import PaymentMethod from '@/components/PaymentMethod';
import OrderSummary from '@/components/OrderSummary';
import { api } from '@/services/api';
import type { OrderType, PaymentMethod as PaymentMethodType, OrderExtras } from '@/types';
import { Loader2, CheckCircle } from 'lucide-react';

/**
 * Página de checkout - Demonstra TODOS os padrões integrados
 */
export default function CheckoutPage() {
  const router = useRouter();
  const { items, getCartTotal, clearCart } = useCart();
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Dados do cliente
  const [customerData, setCustomerData] = useState({
    name: '',
    email: '',
    phone: '',
    address: '',
  });

  // Tipo de pedido (Factory Method)
  const [orderType, setOrderType] = useState<OrderType>('regular');

  // Método de pagamento (Strategy)
  const [paymentMethod, setPaymentMethod] = useState<PaymentMethodType>('credit_card');

  // Extras (Decorator)
  const [extras, setExtras] = useState<OrderExtras>({
    gift_wrap: false,
    gift_message: '',
    insurance: false,
    insurance_type: 'standard',
  });

  const subtotal = getCartTotal();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (items.length === 0) {
      setError('Carrinho vazio');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      // Prepara dados do pedido
      const orderData = {
        customer: customerData,
        order_type: orderType,
        payment_method: paymentMethod,
        items: items.map((item) => ({
          product_id: item.product.id,
          quantity: item.quantity,
        })),
        extras: extras.gift_wrap || extras.insurance ? extras : undefined,
      };

      // Cria pedido usando API (usa TODOS os padrões no backend)
      const order = await api.createOrder(orderData);

      setSuccess(true);
      clearCart();

      // Redireciona para página do pedido após 2 segundos
      setTimeout(() => {
        router.push(`/orders/${order.id}`);
      }, 2000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao criar pedido');
      console.error('Erro ao criar pedido:', err);
    } finally {
      setLoading(false);
    }
  };

  if (items.length === 0 && !success) {
    router.push('/cart');
    return null;
  }

  if (success) {
    return (
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-md mx-auto bg-white rounded-lg shadow-md p-8 text-center">
          <CheckCircle className="h-16 w-16 text-green-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-800 mb-2">
            Pedido Criado com Sucesso!
          </h2>
          <p className="text-gray-600 mb-4">
            Você será redirecionado para os detalhes do pedido...
          </p>
          <Loader2 className="h-6 w-6 animate-spin text-primary-600 mx-auto" />
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold text-gray-800 mb-8">
        Finalizar Compra
      </h1>

      <form onSubmit={handleSubmit}>
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Formulário */}
          <div className="lg:col-span-2 space-y-6">
            {/* Dados do Cliente */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">
                Dados de Entrega
              </h2>
              <div className="grid md:grid-cols-2 gap-4">
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Nome Completo *
                  </label>
                  <input
                    type="text"
                    required
                    value={customerData.name}
                    onChange={(e) =>
                      setCustomerData({ ...customerData, name: e.target.value })
                    }
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Email *
                  </label>
                  <input
                    type="email"
                    required
                    value={customerData.email}
                    onChange={(e) =>
                      setCustomerData({ ...customerData, email: e.target.value })
                    }
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Telefone *
                  </label>
                  <input
                    type="tel"
                    required
                    value={customerData.phone}
                    onChange={(e) =>
                      setCustomerData({ ...customerData, phone: e.target.value })
                    }
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Endereço Completo *
                  </label>
                  <textarea
                    required
                    value={customerData.address}
                    onChange={(e) =>
                      setCustomerData({ ...customerData, address: e.target.value })
                    }
                    rows={3}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>
              </div>
            </div>

            {/* Tipo de Entrega (Factory Method) */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">
                Tipo de Entrega
              </h2>
              <div className="space-y-3">
                {[
                  { id: 'regular', name: 'Regular', desc: '7-10 dias úteis - Grátis' },
                  { id: 'express', name: 'Expressa', desc: '2-3 dias úteis - +15%' },
                  { id: 'international', name: 'Internacional', desc: '15-30 dias - +30%' },
                ].map((type) => (
                  <label
                    key={type.id}
                    className={`flex items-center p-4 border-2 rounded-lg cursor-pointer transition-all ${
                      orderType === type.id
                        ? 'border-primary-600 bg-primary-50'
                        : 'border-gray-200 hover:border-primary-300'
                    }`}
                  >
                    <input
                      type="radio"
                      name="orderType"
                      value={type.id}
                      checked={orderType === type.id}
                      onChange={(e) => setOrderType(e.target.value as OrderType)}
                      className="mr-3"
                    />
                    <div>
                      <p className="font-semibold">{type.name}</p>
                      <p className="text-sm text-gray-600">{type.desc}</p>
                    </div>
                  </label>
                ))}
              </div>
            </div>

            {/* Método de Pagamento (Strategy) */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <PaymentMethod selected={paymentMethod} onChange={setPaymentMethod} />
            </div>

            {/* Extras (Decorator) */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">
                Extras Opcionais
              </h2>
              <div className="space-y-4">
                {/* Embalagem Presente */}
                <label className="flex items-start gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={extras.gift_wrap}
                    onChange={(e) =>
                      setExtras({ ...extras, gift_wrap: e.target.checked })
                    }
                    className="mt-1"
                  />
                  <div className="flex-1">
                    <p className="font-semibold">Embalagem Presente (+R$ 10,00)</p>
                    {extras.gift_wrap && (
                      <input
                        type="text"
                        placeholder="Mensagem do cartão (opcional)"
                        value={extras.gift_message}
                        onChange={(e) =>
                          setExtras({ ...extras, gift_message: e.target.value })
                        }
                        className="mt-2 w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-primary-500"
                      />
                    )}
                  </div>
                </label>

                {/* Seguro */}
                <label className="flex items-start gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={extras.insurance}
                    onChange={(e) =>
                      setExtras({ ...extras, insurance: e.target.checked })
                    }
                    className="mt-1"
                  />
                  <div className="flex-1">
                    <p className="font-semibold">Seguro de Transporte</p>
                    {extras.insurance && (
                      <div className="mt-2 space-y-2">
                        <label className="flex items-center gap-2">
                          <input
                            type="radio"
                            name="insuranceType"
                            value="standard"
                            checked={extras.insurance_type === 'standard'}
                            onChange={(e) =>
                              setExtras({ ...extras, insurance_type: 'standard' })
                            }
                          />
                          <span className="text-sm">Padrão (+5%)</span>
                        </label>
                        <label className="flex items-center gap-2">
                          <input
                            type="radio"
                            name="insuranceType"
                            value="premium"
                            checked={extras.insurance_type === 'premium'}
                            onChange={(e) =>
                              setExtras({ ...extras, insurance_type: 'premium' })
                            }
                          />
                          <span className="text-sm">Premium (+8%)</span>
                        </label>
                      </div>
                    )}
                  </div>
                </label>
              </div>
            </div>
          </div>

          {/* Resumo */}
          <div className="lg:col-span-1">
            <OrderSummary
              subtotal={subtotal}
              orderType={orderType}
              extras={extras}
            />

            {/* Botão Finalizar */}
            <button
              type="submit"
              disabled={loading}
              className="w-full mt-6 bg-primary-600 text-white py-4 rounded-lg font-bold text-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader2 className="h-5 w-5 animate-spin" />
                  Processando...
                </>
              ) : (
                'Finalizar Pedido'
              )}
            </button>

            {error && (
              <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-4">
                <p className="text-red-800 text-sm">{error}</p>
              </div>
            )}
          </div>
        </div>
      </form>
    </div>
  );
}
