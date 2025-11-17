"""Estratégia de Pagamento via PIX"""

from typing import Dict, Any
from datetime import datetime, timedelta
import hashlib
import uuid
from app.strategies.payment_strategy import PaymentStrategy


class PixPayment(PaymentStrategy):
    """
    Estratégia de pagamento PIX (sistema de pagamento instantâneo brasileiro).

    Gera um código/QR code PIX para pagamento.
    O pagamento é confirmado instantaneamente assim que o cliente paga.
    """

    PIX_EXPIRATION_MINUTES = 30

    def process_payment(self, amount: float, payment_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa pagamento PIX gerando código de pagamento.

        Args:
            amount: Valor a ser pago
            payment_details: Pode conter opcionalmente 'payer_name', 'payer_cpf'

        Returns:
            Dict[str, Any]: Resultado do pagamento com código PIX e QR code
        """
        # Valida valor
        if not self.validate_amount(amount):
            return {
                'success': False,
                'message': 'Valor de pagamento inválido',
                'pix_code': None
            }

        # Gera código PIX e dados do QR code
        pix_code = self._generate_pix_code(amount)
        qr_code_data = self._generate_qr_code_data(pix_code, amount)

        # Calcula tempo de expiração
        expires_at = datetime.now() + timedelta(minutes=self.PIX_EXPIRATION_MINUTES)

        return {
            'success': True,
            'message': 'Código PIX gerado com sucesso',
            'pix_code': pix_code,
            'qr_code_data': qr_code_data,
            'payment_method': 'pix',
            'amount': amount,
            'generated_at': datetime.now().isoformat(),
            'expires_at': expires_at.isoformat(),
            'status': 'pending_payment',
            'instructions': 'Escaneie o QR code ou copie o código PIX para completar o pagamento'
        }

    def get_payment_method_name(self) -> str:
        """Obtém nome do método de pagamento."""
        return "PIX"

    def _generate_pix_code(self, amount: float) -> str:
        """
        Gera um código PIX.

        Args:
            amount: Valor do pagamento

        Returns:
            str: Código PIX
        """
        # Em produção, isso seria gerado pelo provedor de pagamento
        unique_id = str(uuid.uuid4())
        data = f"PIX{amount}{unique_id}"
        return hashlib.sha256(data.encode()).hexdigest()[:32].upper()

    def _generate_qr_code_data(self, pix_code: str, amount: float) -> str:
        """
        Gera dados do QR code para pagamento PIX.

        Args:
            pix_code: Código PIX
            amount: Valor do pagamento

        Returns:
            str: Dados do QR code
        """
        # Dados simplificados do QR code
        # Em produção, isso seguiria o padrão PIX QR code (EMV)
        return f"00020126580014br.gov.bcb.pix0136{pix_code}5204000053039865802BR5913ECOMMERCE6009SAO_PAULO{int(amount * 100):010d}6304"

    def confirm_payment(self, pix_code: str) -> Dict[str, Any]:
        """
        Confirma pagamento PIX (seria chamado por webhook em produção).

        Args:
            pix_code: Código PIX para confirmar

        Returns:
            Dict[str, Any]: Resultado da confirmação
        """
        # Em produção, isso verificaria com o provedor de pagamento
        transaction_id = hashlib.md5(pix_code.encode()).hexdigest()[:16].upper()

        return {
            'success': True,
            'message': 'Pagamento PIX confirmado',
            'transaction_id': transaction_id,
            'confirmed_at': datetime.now().isoformat(),
            'status': 'confirmed'
        }
