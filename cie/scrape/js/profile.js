async (params) => {
  // Colhe o feed de um perfil.
  // params: {appId, handle, limit}   limit === 0 significa "tudo".
  // Retorna: {source, handle, pages} ou {error}.
  //
  // Usa /api/v1/feed/user/<username>/username/, que aceita o handle direto.
  // A rota anterior passava por /api/v1/users/web_profile_info/ so para
  // descobrir o user id numerico. Em 18/08/2026 esse endpoint passou a devolver
  // HTTP 400 com "Asset asset://laser.provider/ig_business_category_subvertical
  // has been deleted" - quebra do lado do Instagram, que atingia todo perfil
  // testado, comercial ou nao. A rota por username dispensa aquela chamada
  // inteira, entao alem de consertar ficou uma requisicao mais curta.
  const headers = {
    "X-IG-App-ID": params.appId,
    "X-Requested-With": "XMLHttpRequest",
  };
  const pedir = async (url) => {
    const resposta = await fetch(url, { headers, credentials: "include" });
    if (!resposta.ok) {
      throw new Error(`HTTP ${resposta.status} em ${url}`);
    }
    return resposta.json();
  };

  try {
    const base = `/api/v1/feed/user/${encodeURIComponent(params.handle)}/username/`;
    const pages = [];
    let colhidos = 0;
    let maxId = null;

    while (params.limit === 0 || colhidos < params.limit) {
      const restante = params.limit === 0 ? 12 : Math.min(12, params.limit - colhidos);
      let url = `${base}?count=${restante}`;
      if (maxId) url += `&max_id=${encodeURIComponent(maxId)}`;

      const pagina = await pedir(url);
      const itens = pagina.items || [];
      if (itens.length === 0) break;

      pages.push(pagina);
      colhidos += itens.length;

      if (!pagina.more_available || !pagina.next_max_id) break;
      maxId = pagina.next_max_id;

      // Pausa entre paginas: raspagem sem respiro rende bloqueio temporario.
      await new Promise((r) => setTimeout(r, 1200));
    }

    if (pages.length === 0) {
      return {
        error:
          `perfil @${params.handle} nao devolveu nenhum post. Perfil inexistente, ` +
          `privado, sem publicacoes, ou a sessao caiu. Rode 'cie scrape status'.`,
      };
    }

    return { source: "feed_user", handle: params.handle, pages };
  } catch (erro) {
    return { error: String(erro && erro.message ? erro.message : erro) };
  }
}
