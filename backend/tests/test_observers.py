"""
Testes para o Padrão Observer

Testa o sistema de notificações de pedidos.
"""

import pytest
from app.observers.order_subject import OrderSubject
from app.observers.email_notifier import EmailNotifier
from app.observers.sms_notifier import SmsNotifier
from app.observers.log_notifier import LogNotifier


class TestObserverPattern:
    """Testes para Observer Pattern."""

    def test_attach_observers(self):
        """Testa anexar observadores ao subject."""
        subject = OrderSubject()
        email_notifier = EmailNotifier()
        sms_notifier = SmsNotifier()

        subject.attach(email_notifier)
        subject.attach(sms_notifier)

        assert subject.get_observers_count() == 2
        assert 'email' in subject.get_observers_names()
        assert 'sms' in subject.get_observers_names()

    def test_detach_observers(self):
        """Testa desanexar observadores do subject."""
        subject = OrderSubject()
        email_notifier = EmailNotifier()
        sms_notifier = SmsNotifier()

        subject.attach(email_notifier)
        subject.attach(sms_notifier)
        subject.detach(email_notifier)

        assert subject.get_observers_count() == 1
        assert 'email' not in subject.get_observers_names()
        assert 'sms' in subject.get_observers_names()

    def test_notify_all_observers(self):
        """Testa que todos observadores são notificados."""
        subject = OrderSubject()
        subject.attach(EmailNotifier())
        subject.attach(SmsNotifier())
        subject.attach(LogNotifier())

        order_data = {
            'order_id': 1,
            'customer_id': 1,
            'customer_name': 'João Silva',
            'customer_email': 'joao@email.com',
            'customer_phone': '11999999999',
            'old_status': 'pending',
            'new_status': 'confirmed',
            'note': 'Pagamento aprovado'
        }

        notified = subject.notify(order_data)

        assert len(notified) == 3
        assert 'email' in notified
        assert 'sms' in notified
        assert 'log' in notified

    def test_observer_interface(self):
        """Testa que todos observadores implementam a interface."""
        observers = [
            EmailNotifier(),
            SmsNotifier(),
            LogNotifier()
        ]

        for observer in observers:
            assert hasattr(observer, 'update')
            assert hasattr(observer, 'get_observer_name')
            assert callable(observer.update)
            assert callable(observer.get_observer_name)

    def test_email_notifier_name(self):
        """Testa nome do notificador de email."""
        notifier = EmailNotifier()
        assert notifier.get_observer_name() == 'email'

    def test_sms_notifier_name(self):
        """Testa nome do notificador de SMS."""
        notifier = SmsNotifier()
        assert notifier.get_observer_name() == 'sms'

    def test_log_notifier_name(self):
        """Testa nome do notificador de log."""
        notifier = LogNotifier()
        assert notifier.get_observer_name() == 'log'

    def test_no_duplicate_observers(self):
        """Testa que não é possível anexar o mesmo observador duas vezes."""
        subject = OrderSubject()
        email_notifier = EmailNotifier()

        subject.attach(email_notifier)
        subject.attach(email_notifier)  # Tenta anexar novamente

        assert subject.get_observers_count() == 1  # Deve ter apenas 1
