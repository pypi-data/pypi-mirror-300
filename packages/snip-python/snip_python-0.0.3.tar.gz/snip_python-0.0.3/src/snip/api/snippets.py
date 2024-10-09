"""Module for interacting with snippet-related API endpoints.

Allows to generate previews, test snippets and upload snippets to a deployment.
"""

from PIL import Image

from ..token import Token
from .request import request_image


def get_snip_preview(dict: dict, token: Token, **kwargs) -> Image.Image:
    """Generate a preview image for the given snippet as dict /json.

    This method only checks the validity of the dict on the server side
    and returns the preview image as a PIL Image object if it is valid.

    Parameters
    ----------
    dict : dict
        The snippet as a dictionary.
    deployment : str, optional
        The deployment to generate the preview for.
        If None, the default deployment is used.
    **kwargs: Any
        Additional keyword arguments to pass to the requests.post function.

    Returns
    -------
    Image.Image
        The preview image as a PIL Image object.
    """
    return request_image(
        method="POST",
        url=f"{token.deployment_url}/render/snip",
        token=token,
        json=dict,
        **kwargs,
    )
