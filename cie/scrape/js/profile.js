async (params) => {
  // Colhe o feed de um perfil.
  // params: {appId, handle, limit}   limit === 0 significa "tudo".
  // Retorna: {source, handle, userId, pages} ou {error}.
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
    const perfil = await pedir(
      `/api/v1/users/web_profile_info/?username=${encodeURIComponent(params.handle)}`
    );
    const userId = perfil?.data?.user?.id;
    if (!userId) {
      return {
        error:
          `perfil @${params.handle} nao encontrado, ou a sessao nao esta logada. ` +
          `Rode 'cie scrape login' e tente de novo.`,
      };
    }

    const pages = [];
    let colhidos = 0;
    let maxId = null;

    while (params.limit === 0 || colhidos < params.limit) {
      const restante = params.limit === 0 ? 12 : Math.min(12, params.limit - colhidos);
      let url = `/api/v1/feed/user/${userId}/?count=${restante}`;
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

    return { source: "feed_user", handle: params.handle, userId, pages };
  } catch (erro) {
    return { error: String(erro && erro.message ? erro.message : erro) };
  }
}
