from algosdk.constants import address_len, mnemonic_len, note_max_length
from algosdk.encoding import is_valid_address
from django import forms
from django.core.exceptions import ValidationError
from django.forms.fields import CharField

from .models import Asset




class CreateAssetForm(forms.models.ModelForm):
    """Django model form for creating Algorand assets."""

    passphrase = CharField(required=False)

    class Meta:
        model = Asset
        fields = (
            "creator",
            "name",
            "unit",
            "total",
            "decimals",
            "frozen",
            "url",
            "metadata",
            "manager",
            "reserve",
            "freeze",
            "clawback",
        )

    def _clean_address(self, field):
        """Base method for validation of fields holding Algorand address."""
        data = self.cleaned_data[field]
        if data != "" and not is_valid_address(data):
            raise ValidationError("Provided value is not a valid Algorand address!")
        return data

    def clean_creator(self):
        return self._clean_address("creator")

    def clean_manager(self):
        return self._clean_address("manager")

    def clean_reserve(self):
        return self._clean_address("reserve")

    def clean_freeze(self):
        return self._clean_address("freeze")

    def clean_clawback(self):
        return self._clean_address("clawback")
