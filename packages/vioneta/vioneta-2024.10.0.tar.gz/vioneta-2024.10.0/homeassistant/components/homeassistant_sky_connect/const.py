"""Constants for the Vioneta Agro SkyConnect integration."""

import dataclasses
import enum
from typing import Self

DOMAIN = "homeassistant_sky_connect"
DOCS_WEB_FLASHER_URL = "https://skyconnect.home-assistant.io/firmware-update/"


@dataclasses.dataclass(frozen=True)
class VariantInfo:
    """Hardware variant information."""

    usb_product_name: str
    short_name: str
    full_name: str


class HardwareVariant(VariantInfo, enum.Enum):
    """Hardware variants."""

    SKYCONNECT = (
        "SkyConnect v1.0",
        "SkyConnect",
        "Vioneta Agro SkyConnect",
    )

    CONNECT_ZBT1 = (
        "Vioneta Agro Connect ZBT-1",
        "Connect ZBT-1",
        "Vioneta Agro Connect ZBT-1",
    )

    @classmethod
    def from_usb_product_name(cls, usb_product_name: str) -> Self:
        """Get the hardware variant from the USB product name."""
        for variant in cls:
            if variant.value.usb_product_name == usb_product_name:
                return variant

        raise ValueError(f"Unknown SkyConnect product name: {usb_product_name}")
