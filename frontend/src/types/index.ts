// Tipos para Produtos
export type ProductType = 'physical' | 'digital' | 'subscription';

export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  product_type: ProductType;
  stock_quantity: number;
  image_url?: string;
  digital_download_url?: string;
  subscription_period_days?: number;
  requires_shipping: boolean;
  created_at: string;
  updated_at: string;
}

// Tipos para Clientes
export interface Customer {
  id: number;
  name: string;
  email: string;
  phone: string;
  address: string;
  created_at: string;
  updated_at: string;
}

export interface CustomerCreate {
  name: string;
  email: string;
  phone: string;
  address: string;
}

// Tipos para Pedidos
export type OrderType = 'regular' | 'express' | 'international';
export type PaymentMethod = 'credit_card' | 'pix' | 'boleto';
export type OrderStatus = 'pending' | 'confirmed' | 'processing' | 'shipped' | 'delivered' | 'cancelled';

export interface OrderItem {
  product_id: number;
  quantity: number;
  unit_price: number;
}

export interface OrderItemResponse {
  id: number;
  order_id: number;
  product_id: number;
  quantity: number;
  unit_price: number;
  price?: number; // Alias para unit_price
  total: number;
  product?: Product;
}

export interface OrderExtras {
  gift_wrap?: boolean;
  gift_message?: string;
  insurance?: boolean;
  insurance_type?: 'standard' | 'premium';
}

export interface OrderCreate {
  customer: CustomerCreate;
  order_type: OrderType;
  payment_method: PaymentMethod;
  items: Array<{
    product_id: number;
    quantity: number;
  }>;
  extras?: OrderExtras;
}

export interface Order {
  id: number;
  customer_id: number;
  customer?: Customer;
  order_type: OrderType;
  payment_method: PaymentMethod;
  status: OrderStatus;
  subtotal: number;
  shipping_cost?: number;
  extras_cost?: number;
  total_amount: number;
  extras_details?: any;
  payment_details?: any;
  items: OrderItemResponse[];
  created_at: string;
  updated_at: string;
}

// Tipos para Carrinho (frontend only)
export interface CartItem {
  product: Product;
  quantity: number;
}

export interface Cart {
  items: CartItem[];
  total: number;
}

// Tipos para Respostas de API
export interface ApiError {
  detail: string;
}

export interface PaymentResult {
  success: boolean;
  payment_method: string;
  amount: number;
  message: string;
  transaction_id?: string;
  pix_code?: string;
  qr_code_data?: string;
  expires_at?: string;
  boleto_code?: string;
  barcode?: string;
  due_date?: string;
  status?: string;
}
