import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import Navbar from '@/components/Navbar';
import { CartProvider } from '@/contexts/CartContext';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'E-Commerce - Sistema de Pedidos',
  description: 'Sistema de e-commerce demonstrando padrões de projeto',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body className={inter.className}>
        <CartProvider>
          <Navbar />
          <main className="min-h-screen">{children}</main>
          <footer className="bg-gray-800 text-white py-6 mt-12">
            <div className="container mx-auto px-4 text-center">
              <p className="text-sm">
                © 2024 E-Commerce Padrões de Projeto
              </p>
              <p className="text-xs text-gray-400 mt-1">
                Desenvolvido como atividade acadêmica
              </p>
            </div>
          </footer>
        </CartProvider>
      </body>
    </html>
  );
}
