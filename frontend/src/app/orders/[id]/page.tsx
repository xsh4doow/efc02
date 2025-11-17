'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { api } from '@/services/api';
import type { Order } from '@/types';
import { Loader2, ArrowLeft, Package, User, CreditCard, Truck } from 'lucide-react';

/**
 * Página de detalhes de um pedido específico
 */
export default function OrderDetailPage() {
  const params = useParams();
  const router = useRouter();
  const orderId = parseInt(params.id as string);

  const [order, setOrder] = useState<Order | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (orderId) {
      loadOrder();
    }
  }, [orderId]);

  const loadOrder = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getOrder(orderId);
      setOrder(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao carregar pedido');
      console.error('Erro ao carregar pedido:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-12">
        <div className="flex items-center justify-center min-h-[400px]">
          <Loader2 className="h-12 w-12 animate-spin text-primary-600" />
        </div>
      </div>
    );
  }

  if (error || !order) {
    return (
      <div className="container mx-auto px-4 py-12">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
          <p className="text-red-800 font-semibold mb-2">
            {error || 'Pedido não encontrado'}
          </p>
          <Link
            href="/orders"
            className="inline-block mt-4 px-4 py-2 bg-primary-600 text-white rounded hover:bg-primary-700"
          >
            Voltar para Pedidos
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-12">
      {/* Header */}
      <div className="mb-8">
        <Link
          href="/orders"
          className="inline-flex items-center gap-2 text-primary-600 hover:text-primary-700 mb-4"
        >
          <ArrowLeft className="h-4 w-4" />
          Voltar para Pedidos
        </Link>
        <h1 className="text-4xl font-bold text-gray-800">
          Pedido #{order.id}
        </h1>
        <p className="text-gray-600">{formatDate(order.created_at)}</p>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Informações Principais */}
        <div className="lg:col-span-2 space-y-6">
          {/* Status */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center gap-2 mb-4">
              <Package className="h-6 w-6 text-primary-600" />
              <h2 className="text-xl font-semibold">Status do Pedido</h2>
            </div>
            <p className="text-3xl font-bold text-primary-600 capitalize">
              {order.status}
            </p>
          </div>

          {/* Itens */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">Itens do Pedido</h2>
            <div className="space-y-4">
              {order.items.map((item) => (
                <div
                  key={item.id}
                  className="flex items-center gap-4 pb-4 border-b last:border-0"
                >
                  <div className="w-16 h-16 bg-gray-200 rounded flex-shrink-0" />
                  <div className="flex-1">
                    <p className="font-semibold">
                      {item.product?.name || 'Produto não disponível'}
                    </p>
                    <p className="text-sm text-gray-600">
                      Quantidade: {item.quantity} × R$ {(item.price || item.unit_price || 0).toFixed(2)}
                    </p>
                  </div>
                  <p className="font-bold">
                    R$ {(item.quantity * (item.price || item.unit_price || 0)).toFixed(2)}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Cliente */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center gap-2 mb-4">
              <User className="h-6 w-6 text-primary-600" />
              <h2 className="text-xl font-semibold">Informações do Cliente</h2>
            </div>
            <div className="space-y-2">
              <p>
                <strong>Nome:</strong> {order.customer?.name || 'Não disponível'}
              </p>
              <p>
                <strong>Email:</strong> {order.customer?.email || 'Não disponível'}
              </p>
              <p>
                <strong>Telefone:</strong> {order.customer?.phone || 'Não disponível'}
              </p>
              <p>
                <strong>Endereço:</strong> {order.customer?.address || 'Não disponível'}
              </p>
            </div>
          </div>

          {/* Entrega */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center gap-2 mb-4">
              <Truck className="h-6 w-6 text-primary-600" />
              <h2 className="text-xl font-semibold">Entrega</h2>
            </div>
            <p>
              <strong>Tipo:</strong>{' '}
              <span className="capitalize">{order.order_type}</span>
            </p>
            <p>
              <strong>Custo de Envio:</strong> R${' '}
              {(order.shipping_cost || 0).toFixed(2)}
            </p>
          </div>

          {/* Pagamento */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center gap-2 mb-4">
              <CreditCard className="h-6 w-6 text-primary-600" />
              <h2 className="text-xl font-semibold">Pagamento</h2>
            </div>
            <p>
              <strong>Método:</strong>{' '}
              <span className="capitalize">
                {order.payment_method.replace('_', ' ')}
              </span>
            </p>
            {order.payment_details && (
              <div className="mt-2 text-sm text-gray-600">
                <pre className="bg-gray-50 p-2 rounded overflow-auto">
                  {JSON.stringify(order.payment_details, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </div>

        {/* Resumo */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-md p-6 sticky top-4">
            <h2 className="text-xl font-semibold mb-4">Resumo</h2>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">Subtotal</span>
                <span>R$ {order.subtotal.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Envio</span>
                <span>R$ {(order.shipping_cost || 0).toFixed(2)}</span>
              </div>
              {(order.extras_cost || 0) > 0 && (
                <div className="flex justify-between">
                  <span className="text-gray-600">Extras</span>
                  <span>R$ {(order.extras_cost || 0).toFixed(2)}</span>
                </div>
              )}
              <div className="border-t pt-3">
                <div className="flex justify-between text-lg font-bold">
                  <span>Total</span>
                  <span className="text-primary-600">
                    R$ {order.total_amount.toFixed(2)}
                  </span>
                </div>
              </div>
            </div>

            {/* Extras Details */}
            {order.extras_details && Object.keys(order.extras_details).length > 0 && (
              <div className="mt-6 pt-6 border-t">
                <h3 className="font-semibold mb-2">Extras</h3>
                <div className="text-sm text-gray-600">
                  <pre className="bg-gray-50 p-2 rounded overflow-auto">
                    {JSON.stringify(order.extras_details, null, 2)}
                  </pre>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
