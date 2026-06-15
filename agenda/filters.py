"""Filtros customizados para o módulo agenda."""

from __future__ import annotations

from typing import Any

from django.db.models import Case, IntegerField, Value, When
from rest_framework.filters import OrderingFilter


class AgendaOrderingFilter(OrderingFilter):
    """OrderingFilter que coloca agendas com modalidade ONLINE sempre."""

    def filter_queryset(self, request: Any, queryset: Any, view: Any) -> Any:
        """Ordena o queryset priorizando agendas com modalidade ONLINE."""
        ordering = self.get_ordering(request, queryset, view)
        queryset = queryset.annotate(
            _online_first=Case(
                When(modalidade__iexact="ONLINE", then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            )
        )
        if ordering:
            return queryset.order_by("_online_first", *ordering)
        return queryset.order_by("_online_first")
