/**
 * sw.js - Service Worker do Estoque Qualifica
 * IMPORTANTE: Este arquivo precisa ser servido em /sw.js (raiz do site)
 * para ter escopo sobre todas as páginas do sistema.
 */

const CACHE_NAME = 'estoque-qualifica-v3.0';

// Arquivos essenciais que ficam em cache para funcionar offline
const ARQUIVOS_CACHE = [
  '/dashboard/',
  '/static/manifest.json',
  '/static/icons/icon-192.png',
  '/static/icons/icon-512.png',
];

// INSTALA e armazena cache básico
self.addEventListener('install', function(event) {
  console.log('[SW] Instalando v3.0...');
  event.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      // Tenta cachear cada arquivo individualmente — não falha se algum não carregar
      return Promise.allSettled(
        ARQUIVOS_CACHE.map(url => cache.add(url).catch(e => console.warn('[SW] Não cacheou:', url)))
      );
    })
  );
  self.skipWaiting();
});

// ATIVA e remove caches antigos
self.addEventListener('activate', function(event) {
  console.log('[SW] Ativado v3.0');
  event.waitUntil(
    caches.keys().then(function(nomes) {
      return Promise.all(
        nomes.filter(n => n !== CACHE_NAME).map(n => {
          console.log('[SW] Removendo cache antigo:', n);
          return caches.delete(n);
        })
      );
    })
  );
  self.clients.claim();
});

// INTERCEPTA requisições — estratégia: Network First, fallback para cache
self.addEventListener('fetch', function(event) {
  // Ignora requisições não-GET (POST de formulários, APIs, etc.)
  if (event.request.method !== 'GET') return;

  // Ignora URLs de autenticação e admin para não quebrar login
  const url = new URL(event.request.url);
  if (
    url.pathname.startsWith('/accounts/') ||
    url.pathname.startsWith('/admin/') ||
    url.pathname.startsWith('/api/')
  ) return;

  event.respondWith(
    fetch(event.request)
      .then(function(resposta) {
        // Salva no cache se veio da rede com sucesso
        if (resposta && resposta.status === 200 && resposta.type !== 'opaque') {
          const clone = resposta.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        }
        return resposta;
      })
      .catch(function() {
        // Offline: tenta o cache
        return caches.match(event.request).then(function(cached) {
          if (cached) return cached;
          // Página de fallback offline para documentos HTML
          if (event.request.destination === 'document') {
            return new Response(
              `<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Sem conexão — Estoque Qualifica</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #000000; color: #fafafa;
      font-family: sans-serif;
      display: flex; align-items: center; justify-content: center;
      min-height: 100vh; text-align: center; padding: 2rem;
      flex-direction: column; gap: 1.5rem;
    }
    .icon { font-size: 2.5rem; font-weight: 800; letter-spacing: -0.04em; border: 1px solid #404040; border-radius: 1rem; padding: 1rem 1.5rem; }
    h1 { font-size: 1.5rem; color: #ffffff; }
    p { color: #a3a3a3; font-size: 0.9rem; line-height: 1.6; max-width: 300px; }
    button {
      background: #fafafa; color: #0a0a0a; border: none;
      padding: 0.75rem 2rem; border-radius: 0.5rem;
      font-size: 1rem; cursor: pointer; margin-top: 0.5rem;
    }
  </style>
</head>
<body>
  <div class="icon">EQ</div>
  <h1>Você está offline</h1>
  <p>Não foi possível conectar ao Estoque Qualifica. Verifique sua internet e tente novamente.</p>
  <button onclick="location.reload()">Tentar novamente</button>
</body>
</html>`,
              { headers: { 'Content-Type': 'text/html; charset=utf-8' } }
            );
          }
        });
      })
  );
});

// Recebe mensagem do app para pular espera
self.addEventListener('message', function(event) {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});