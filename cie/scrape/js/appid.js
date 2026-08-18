() => {
  // Le o X-IG-App-ID que a propria pagina usa nas chamadas dela.
  // A constante de fallback e o app id publico do Instagram Web; se o Instagram
  // trocar, o regex acha o novo antes de a constante ser usada.
  const html = document.documentElement.innerHTML;
  const padroes = [
    /"X-IG-App-ID"\s*:\s*"(\d+)"/,
    /appId["']?\s*[:=]\s*["'](\d{10,})["']/,
    /APP_ID["']?\s*[:=]\s*["'](\d{10,})["']/,
  ];
  for (const padrao of padroes) {
    const achado = html.match(padrao);
    if (achado) return achado[1];
  }
  return "936619743392459";
}
