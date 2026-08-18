async (params) => {
  // Colhe um post pelo media_id (derivado do shortcode no lado Python).
  // params: {appId, mediaId}
  // Retorna: {source, pages} ou {error}.
  const headers = {
    "X-IG-App-ID": params.appId,
    "X-Requested-With": "XMLHttpRequest",
  };
  try {
    const resposta = await fetch(`/api/v1/media/${params.mediaId}/info/`, {
      headers,
      credentials: "include",
    });
    if (!resposta.ok) {
      return {
        error:
          `HTTP ${resposta.status} ao buscar o post. Post privado, apagado, ` +
          `ou a sessao nao esta logada.`,
      };
    }
    const pagina = await resposta.json();
    return { source: "media_info", pages: [pagina] };
  } catch (erro) {
    return { error: String(erro && erro.message ? erro.message : erro) };
  }
}
