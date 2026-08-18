"""Modelos da raspagem.

`ScrapedItem` deliberadamente NAO tem `has_identifiable_person` nem
`consent_on_file`. Esses dois campos so existem em `Asset`, e so a curadoria
humana os preenche. A raspagem nao tem direito de opinar sobre eles.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import PurePosixPath
from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict, Field

#: Extensoes que o CDN do Instagram devolve. Fora dessa lista, cai para .jpg.
_EXTENSOES_CONHECIDAS = {".jpg", ".jpeg", ".png", ".webp", ".heic"}


class ScrapedItem(BaseModel):
    """Uma imagem colhida. Uma foto simples vira 1; um carrossel de 5 vira 5."""

    model_config = ConfigDict(extra="forbid")

    shortcode: str
    owner_handle: str = ""
    post_url: str
    display_url: str = ""
    width: int = 0
    height: int = 0
    taken_at: datetime | None = None
    caption: str = ""
    carousel_index: int = 1
    is_video: bool = False

    @property
    def extension(self) -> str:
        sufixo = PurePosixPath(urlparse(self.display_url).path).suffix.lower()
        return sufixo if sufixo in _EXTENSOES_CONHECIDAS else ".jpg"

    @property
    def filename(self) -> str:
        """`<data>_<shortcode>_<indice>.<ext>` - ordenavel e rastreavel a origem."""
        data = self.taken_at.strftime("%Y-%m-%d") if self.taken_at else "sem-data"
        return f"{data}_{self.shortcode}_{self.carousel_index}{self.extension}"


class HarvestBatch(BaseModel):
    """O resultado de parsear um envelope de colheita."""

    model_config = ConfigDict(extra="forbid")

    target_slug: str
    target_kind: str
    harvested_at: datetime
    items: list[ScrapedItem] = Field(default_factory=list)

    @property
    def images(self) -> list[ScrapedItem]:
        """So o que da para baixar como imagem estatica."""
        return [i for i in self.items if not i.is_video and i.display_url]
