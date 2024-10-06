import logging
from io import BytesIO

import requests

from typing import Optional
from PIL import Image


class KomootImage:

    def __init__(self, url: str, templated: bool, client_hash: Optional[str] = None, attribution: Optional[str] = None,
                 attribution_url: Optional[str] = None, media_type: Optional[str] = None):
        """
        Komoot Image object.

        :param url: link to the image
        :param templated: wether the link contains template variables
        :param client_hash: a hash set by the client on upload, useful for de-duplicating images
        :param attribution: if set, clients must show this attribution with the image
        :param attribution_url: if attribution exists, this field can contain a link to the attribution source
        :param media_type: media type of the resource, e.g. image/*
        """
        self.url: str = url,
        self.templated: bool = templated
        self.client_hash: Optional[str] = client_hash
        self.attribution: Optional[str] = attribution
        self.attribution_url: Optional[str] = attribution_url
        self.media_type: Optional[str] = media_type
        self.image: Optional[Image] = None

    def load_image(self):
        """Load image from the url."""
        response = requests.get(self.url)
        response.raise_for_status()
        self.image = Image.open(BytesIO(response.content))
