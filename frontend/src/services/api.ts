import axios, { AxiosInstance } from 'axios';
import type {
  Product,
  Customer,
  Order,
  OrderCreate,
  CustomerCreate,
} from '@/types';

/**
 * Cliente API para comunicação com o backend FastAPI
 */
class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 10000,
    });

    // Interceptor para tratamento de erros
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('API Error:', error.response?.data || error.message);
        return Promise.reject(error);
      }
    );
  }

  // ========== PRODUTOS ==========

  /**
   * Lista todos os produtos
   */
  async getProducts(): Promise<Product[]> {
    const response = await this.client.get<Product[]>('/api/products');
    return response.data;
  }

  /**
   * Obtém detalhes de um produto específico
   */
  async getProduct(id: number): Promise<Product> {
    const response = await this.client.get<Product>(`/api/products/${id}`);
    return response.data;
  }

  /**
   * Cria um novo produto (admin)
   */
  async createProduct(product: Partial<Product>): Promise<Product> {
    const response = await this.client.post<Product>('/api/products', product);
    return response.data;
  }

  /**
   * Atualiza um produto existente (admin)
   */
  async updateProduct(id: number, product: Partial<Product>): Promise<Product> {
    const response = await this.client.patch<Product>(
      `/api/products/${id}`,
      product
    );
    return response.data;
  }

  /**
   * Deleta um produto (admin)
   */
  async deleteProduct(id: number): Promise<void> {
    await this.client.delete(`/api/products/${id}`);
  }

  // ========== CLIENTES ==========

  /**
   * Lista todos os clientes
   */
  async getCustomers(): Promise<Customer[]> {
    const response = await this.client.get<Customer[]>('/api/customers');
    return response.data;
  }

  /**
   * Obtém detalhes de um cliente específico
   */
  async getCustomer(id: number): Promise<Customer> {
    const response = await this.client.get<Customer>(`/api/customers/${id}`);
    return response.data;
  }

  /**
   * Cria um novo cliente
   */
  async createCustomer(customer: CustomerCreate): Promise<Customer> {
    const response = await this.client.post<Customer>(
      '/api/customers',
      customer
    );
    return response.data;
  }

  /**
   * Atualiza um cliente existente
   */
  async updateCustomer(
    id: number,
    customer: Partial<CustomerCreate>
  ): Promise<Customer> {
    const response = await this.client.patch<Customer>(
      `/api/customers/${id}`,
      customer
    );
    return response.data;
  }

  /**
   * Deleta um cliente
   */
  async deleteCustomer(id: number): Promise<void> {
    await this.client.delete(`/api/customers/${id}`);
  }

  // ========== PEDIDOS ==========

  /**
   * Lista todos os pedidos
   */
  async getOrders(): Promise<Order[]> {
    const response = await this.client.get<Order[]>('/api/orders');
    return response.data;
  }

  /**
   * Obtém detalhes de um pedido específico
   */
  async getOrder(id: number): Promise<Order> {
    const response = await this.client.get<Order>(`/api/orders/${id}`);
    return response.data;
  }

  /**
   * Obtém pedidos de um cliente específico
   */
  async getCustomerOrders(customerId: number): Promise<Order[]> {
    const response = await this.client.get<Order[]>(
      `/api/orders/customer/${customerId}`
    );
    return response.data;
  }

  /**
   * Cria um novo pedido (USA TODOS OS PADRÕES DE PROJETO)
   */
  async createOrder(order: OrderCreate): Promise<Order> {
    const response = await this.client.post<Order>('/api/orders', order);
    return response.data;
  }

  /**
   * Atualiza o status de um pedido (DISPARA OBSERVERS)
   */
  async updateOrderStatus(
    id: number,
    status: string,
    note?: string
  ): Promise<Order> {
    const response = await this.client.patch<Order>(
      `/api/orders/${id}/status`,
      { status, note }
    );
    return response.data;
  }
}

// Exporta instância única do serviço
export const api = new ApiService();
export default api;
