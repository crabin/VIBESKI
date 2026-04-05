"""Verify database/models.py has no domain-specific models."""
import pytest


def test_domain_models_removed():
    """CrawlerTask, AttackTask, ScanResult must not exist in models."""
    import database.models as m
    assert not hasattr(m, "CrawlerTask"), "CrawlerTask should be removed"
    assert not hasattr(m, "AttackTask"), "AttackTask should be removed"
    assert not hasattr(m, "ScanResult"), "ScanResult should be removed"


def test_base_models_kept():
    """Conversation, PromptChainModel, UserConfig, AuditRecord must exist."""
    from database.models import Conversation, PromptChainModel, UserConfig, AuditRecord
    assert Conversation
    assert PromptChainModel
    assert UserConfig
    assert AuditRecord
