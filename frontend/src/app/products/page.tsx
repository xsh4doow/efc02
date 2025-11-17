'use client';

import { useEffect, useState } from 'react';
import ProductCard from '@/components/ProductCard';
import { api } from '@/services/api';
import type { Product } from '@/types';
import { Loader2 } from 'lucide-react';

/**
 * Página de listagem de produtos
 */
export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getProducts();
      setProducts(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao carregar produtos');
      console.error('Erro ao carregar produtos:', err);
    } finally {
      setLoading(false);
    }
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
          <p className="text-red-800 font-semibold mb-2">Erro ao carregar produtos</p>
          <p className="text-red-600 text-sm">{error}</p>
          <button
            onClick={loadProducts}
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
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-800 mb-2">
          Nossos Produtos
        </h1>
        <p className="text-gray-600">
          Produtos criados usando o padrão <strong>Factory Method</strong>
        </p>
      </div>

      {/* Grid de Produtos */}
      {products.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-600">Nenhum produto disponível no momento</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {products.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      )}

      {/* Info Box */}
      <div className="mt-12 bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="font-semibold text-blue-900 mb-2">
          💡 Padrão Factory Method em Ação
        </h3>
        <p className="text-blue-800 text-sm">
          Cada produto é criado usando o <strong>Factory Method</strong>,
          permitindo diferentes tipos (físico, digital, assinatura) sem código
          condicional complexo. O padrão facilita a adição de novos tipos de
          produtos no futuro.
        </p>
      </div>
    </div>
  );
}
