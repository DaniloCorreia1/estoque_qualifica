/**
 * sw.js - Service Worker do Estoque Qualifica
 * Responsável por fazer o app funcionar offline (PWA)
 * O Service Worker fica entre o app e a internet, guardando arquivos em cache
 */

// Nome do cache - mude a versão para forçar atualização
const CACHE_NAME = 'estoque-qualifica-v1.2';

// Arquivos que serão guardados em cache para funcionar offline
const ARQUIVOS_PARA_CACHE = [
  '/',
  '/dashboard/',
  '/static/manifest.json',
  'https://cdn.tailwindcss.com',
  'https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap',
];

// ============================================================
// EVENTO: install - Executado quando o SW é instalado pela 1ª vez
// ============================================================
self.addEventListener('install', function(event) {
  console.log('[SW] Instalando Service Worker...');
  event.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      console.log('[SW] Arquivos em cache');
      // Tenta colocar em cache, mas não falha se algum não carregar
      return cache.addAll(ARQUIVOS_PARA_CACHE).catch(function(err) {
        console.log('[SW] Alguns arquivos não foram cacheados:', err);
      });
    })
  );
  // Ativa imediatamente sem esperar fechar outras abas
  self.skipWaiting();
});

// ============================================================
// EVENTO: activate - Quando o SW entra em uso, limpa caches antigos
// ============================================================
self.addEventListener('activate', function(event) {
  console.log('[SW] Service Worker ativado');
  event.waitUntil(
    caches.keys().then(function(nomesDosCache) {
      return Promise.all(
        nomesDosCache
          .filter(function(nome) {
            // Remove caches antigos (de versões anteriores)
            return nome !== CACHE_NAME;
          })
          .map(function(nome) {
            console.log('[SW] Removendo cache antigo:', nome);
            return caches.delete(nome);
          })
      );
    })
  );
  // Assume controle de todas as abas abertas
  self.clients.claim();
});

// ============================================================
// EVENTO: fetch - Intercepta todas as requisições de rede
// Estratégia: Network First (tenta rede, se falhar usa cache)
// ============================================================
self.addEventListener('fetch', function(event) {
  // Só intercepta GET (não intercepta POST para não quebrar formulários)
  if (event.request.method !== 'GET') return;

  // Não intercepta URLs de autenticação e APIs externas
  const url = new URL(event.request.url);
  if (url.pathname.startsWith('/accounts/login') ||
      url.pathname.startsWith('/admin/') ||
      url.pathname.startsWith('/api/')) {
    return;
  }

  event.respondWith(
    // Tenta buscar da rede primeiro
    fetch(event.request)
      .then(function(resposta) {
        // Se conseguiu da rede, guarda no cache para uso futuro
        if (resposta && resposta.status === 200) {
          const respostaClone = resposta.clone();
          caches.open(CACHE_NAME).then(function(cache) {
            cache.put(event.request, respostaClone);
          });
        }
        return resposta;
      })
      .catch(function() {
        // Se falhou na rede (offline), tenta buscar do cache
        return caches.match(event.request).then(function(respostaCache) {
          if (respostaCache) {
            return respostaCache;
          }
          // Se não tem nem no cache, retorna página offline
          if (event.request.destination === 'document') {
            return new Response(
              `<!DOCTYPE html>
              <html lang="pt-BR">
              <head><meta charset="UTF-8"><title>Sem conexão</title>
              <style>body{background:#111827;color:#f9fafb;font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;text-align:center;flex-direction:column;gap:1rem}h1{font-size:2rem;color:#22c55e}p{color:#9ca3af}</style>
              </head>
              <body>
                <h1>📦 Sem conexão</h1>
                <p>Você está offline. Algumas funções do Estoque Qualifica precisam de internet.</p>
                <p>Verifique sua conexão e tente novamente.</p>
                <button onclick="location.reload()" style="background:#22c55e;color:white;border:none;padding:.75rem 1.5rem;border-radius:.5rem;cursor:pointer;font-size:1rem">Tentar novamente</button>
              </body></html>`,
              { headers: { 'Content-Type': 'text/html' } }
            );
          }
        });
      })
  );
});

// ============================================================
// EVENTO: message - Recebe mensagens do app principal
// ============================================================
self.addEventListener('message', function(event) {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
