async (params) => {
  // Colhe uma hashtag (secoes "top" e "recent").
  // params: {appId, tag}
  // Retorna: {source, pages} ou {error}.
  const headers = {
    "X-IG-App-ID": params.appId,
    "X-Requested-With": "XMLHttpRequest",
  };
  try {
    const resposta = await fetch(
      `/api/v1/tags/web_info/?tag_name=${encodeURIComponent(params.tag)}`,
      { headers, credentials: "include" }
    );
    if (!resposta.ok) {
      return {
        error:
          `HTTP ${resposta.status} ao buscar #${params.tag}. Hashtag inexistente, ` +
          `bloqueada pelo Instagram, ou a sessao nao esta logada.`,
      };
    }
    const pagina = await resposta.json();
    return { source: "tag_web_info", pages: [pagina] };
  } catch (erro) {
    return { error: String(erro && erro.message ? erro.message : erro) };
  }
}
