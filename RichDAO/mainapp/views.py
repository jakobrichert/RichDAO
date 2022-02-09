from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render

from .forms import (
    CreateAssetForm
)
from .helpers import add_asset
from .models import  Asset


def assets(request):
    """Display all the created assets."""
    assets = Asset.objects
    context = {"assets": assets}
    return render(request, "mainapp/assets.html", context)


def index(request):
    """Create Algorand asset from the form data."""
    if request.method == "POST":

        if "retrieve_passphrase" in request.POST:
            form = CreateAssetForm(request.POST)
        else:

            form = CreateAssetForm(request.POST)

            if form.is_valid():

                asset_id, error_description = add_asset(form.cleaned_data)
                if error_description == "":

                    asset = form.save(commit=False)
                    asset.asset_id = asset_id
                    asset.save()

                    message = "Asset {} has been successfully created!".format(
                        form.cleaned_data["name"]
                    )
                    messages.add_message(request, messages.SUCCESS, message)
                    return redirect("mainapp/assets.html")

                form.add_error(None, error_description)

    else:
        form = CreateAssetForm()

    context = {"form": form}

    return render(request, "mainapp/index.html", context)




















