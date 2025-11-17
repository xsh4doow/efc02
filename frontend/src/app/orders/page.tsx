'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { api } from '@/services/api';
import type { Order } from '@/types';
import { Loader2, Package, Eye } from 'lucide-react';

/**
 * Página de listagem de pedidos
 */
export default function OrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadOrders();
  }, []);

  const loadOrders = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getOrders();
      setOrders(data.sort((a, b) => b.id - a.id)); // Mais recentes primeiro
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao carregar pedidos');
      console.error('Erro ao carregar pedidos:', err);
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status: string) => {
    const badges: Record<string, { text: string; color: string }> = {
      pending: { text: 'Pendente', color: 'bg-yellow-100 text-yellow-800' },
      confirmed: { text: 'Confirmado', color: 'bg-blue-100 text-blue-800' },
      processing: { text: 'Processando', color: 'bg-purple-100 text-purple-800' },
      shipped: { text: 'Enviado', color: 'bg-indigo-100 text-indigo-800' },
      delivered: { text: 'Entregue', color: 'bg-green-100 text-green-800' },
      cancelled: { text: 'Cancelado', color: 'bg-red-100 text-red-800' },
    };

    const badge = badges[status] || badges.pending;
    return (
      <span
        className={`inline-block px-3 py-1 text-xs font-semibold rounded-full ${badge.color}`}
      >
        {badge.text}
      </span>
    );
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

  if (error) {
    return (
      <div className="container mx-auto px-4 py-12">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
          <p className="text-red-800 font-semibold mb-2">
            Erro ao carregar pedidos
          </p>
          <p className="text-red-600 text-sm">{error}</p>
          <button
            onClick={loadOrders}
            className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            Tentar Novamente
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold text-gray-800 mb-8">Meus Pedidos</h1>

      {orders.length === 0 ? (
        <div className="text-center py-12">
          <Package className="h-24 w-24 mx-auto text-gray-300 mb-4" />
          <p className="text-gray-600 mb-6">Você ainda não fez nenhum pedido</p>
          <Link
            href="/products"
            className="inline-block bg-primary-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-700"
          >
            Ver Produtos
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {orders.map((order) => (
            <div
              key={order.id}
              className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
            >
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-lg font-semibold text-gray-800">
                    Pedido #{order.id}
                  </h3>
                  <p className="text-sm text-gray-600">
                    {formatDate(order.created_at)}
                  </p>
                </div>
                {getStatusBadge(order.status)}
              </div>

              <div className="grid md:grid-cols-3 gap-4 mb-4">
                <div>
                  <p className="text-sm text-gray-600">Cliente</p>
                  <p className="font-semibold">
                    {order.customer?.name || 'Cliente não disponível'}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Tipo de Entrega</p>
                  <p className="font-semibold capitalize">{order.order_type}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Pagamento</p>
                  <p className="font-semibold capitalize">
                    {order.payment_method.replace('_', ' ')}
                  </p>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Total</p>
                  <p className="text-2xl font-bold text-primary-600">
                    R$ {order.total_amount.toFixed(2)}
                  </p>
                </div>
                <Link
                  href={`/orders/${order.id}`}
                  className="flex items-center gap-2 bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors"
                >
                  <Eye className="h-4 w-4" />
                  Ver Detalhes
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Info Box */}
      {orders.length > 0 && (
        <div className="mt-12 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="font-semibold text-blue-900 mb-2">
            👁️ Padrão Observer em Ação
          </h3>
          <p className="text-blue-800 text-sm">
            Cada mudança de status aciona automaticamente notificações via{' '}
            <strong>Observer Pattern</strong>: emails são enviados, SMS
            disparados e logs registrados, tudo sem acoplamento entre os
            componentes.
          </p>
        </div>
      )}
    </div>
  );
}
