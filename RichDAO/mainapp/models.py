from algosdk.constants import address_len, hash_len, max_asset_decimals, metadata_length
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models





class DAO:
    """Model class for a DAO object"""
    
    wallet = models.CharField(blank=False)
    image = models.URLField(blank=True)
    name = models.CharField(blank = False)


class proposal(DAO):
    proposal_name = models.CharField(blank=False)
    proposal_idea = models.CharField(blank=False)
    proposer = models.CharField(blank=False)


class member(DAO):
    wallet = models.CharField(blank=False)
    name = models.CharField(blank=True)

class bounty(DAO):
    name = models.CharField(blank=False)
    description = models.CharField(blank=False)
    reward = models.FloatField(blank=False)
    currency = models.CharField(blank=False)








class Asset(models.Model):
    """Model class for Algorand assets."""

    asset_id = models.IntegerField(blank=False)
    
    creator = models.CharField(max_length=address_len, blank=False)
    name = models.CharField(max_length=hash_len, blank=True)
    unit = models.CharField(max_length=8, blank=True)
    total = models.IntegerField(
        blank=False,
        validators=[MinValueValidator(1)],
    )
    decimals = models.IntegerField(
        blank=False,
        validators=[MinValueValidator(0), MaxValueValidator(max_asset_decimals)],
    )
    frozen = models.BooleanField(blank=False, default=False)
    url = models.URLField(blank=True)
    metadata = models.CharField(max_length=metadata_length, blank=True)
    manager = models.CharField(max_length=address_len, blank=True)
    reserve = models.CharField(max_length=address_len, blank=True)
    freeze = models.CharField(max_length=address_len, blank=True)
    clawback = models.CharField(max_length=address_len, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Asset's human-readable string representation."""
        return self.name






