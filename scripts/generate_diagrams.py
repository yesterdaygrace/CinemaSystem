import os
import subprocess
import shutil

def create_topology_svg():
    width = 2400
    height = 1520

    svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Background Gradients -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#070b14" />
      <stop offset="50%" stop-color="#0d1527" />
      <stop offset="100%" stop-color="#0a101f" />
    </linearGradient>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#151f33" />
      <stop offset="100%" stop-color="#0e1726" />
    </linearGradient>
    <linearGradient id="tierHeaderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e293b" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>
    <linearGradient id="subCardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#162238" />
      <stop offset="100%" stop-color="#0f192b" />
    </linearGradient>
    <linearGradient id="amberCardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2a1d08" />
      <stop offset="100%" stop-color="#171106" />
    </linearGradient>

    <!-- Filters -->
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="10" stdDeviation="8" flood-color="#000000" flood-opacity="0.6"/>
    </filter>

    <!-- Markers -->
    <marker id="arrowCyan" viewBox="0 0 12 12" refX="9" refY="6" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 1 1 L 11 6 L 1 11 z" fill="#38bdf8" />
    </marker>
    <marker id="arrowGreen" viewBox="0 0 12 12" refX="9" refY="6" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 1 1 L 11 6 L 1 11 z" fill="#10b981" />
    </marker>
    <marker id="arrowAmber" viewBox="0 0 12 12" refX="9" refY="6" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 1 1 L 11 6 L 1 11 z" fill="#f59e0b" />
    </marker>

    <!-- Background Pattern -->
    <pattern id="dotGrid" width="36" height="36" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.2" fill="#334155" opacity="0.35"/>
    </pattern>
  </defs>

  <!-- Background Base -->
  <rect width="{width}" height="{height}" fill="url(#bgGrad)" />
  <rect width="{width}" height="{height}" fill="url(#dotGrid)" />

  <!-- ==================== HEADER BANNER ==================== -->
  <rect x="70" y="40" width="2260" height="110" rx="18" fill="url(#cardGrad)" stroke="#38bdf8" stroke-width="1.8" filter="url(#shadow)"/>
  
  <!-- Icon & Header Text -->
  <g transform="translate(95, 60)">
    <rect width="70" height="70" rx="14" fill="#0284c7" fill-opacity="0.25" stroke="#38bdf8" stroke-width="1.5"/>
    <!-- Cloud & Topology Vector Icon -->
    <path d="M 23 44 A 9 9 0 0 1 32 35 A 14 14 0 0 1 54 36 A 10 10 0 0 1 57 48 L 23 48 Z" fill="#38bdf8" />
    <circle cx="28" cy="55" r="3.5" fill="#38bdf8" />
    <circle cx="47" cy="55" r="3.5" fill="#38bdf8" />
    <line x1="28" y1="48" x2="28" y2="52" stroke="#38bdf8" stroke-width="2" />
    <line x1="47" y1="48" x2="47" y2="52" stroke="#38bdf8" stroke-width="2" />
  </g>
  
  <text x="185" y="83" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="28" font-weight="800" letter-spacing="0.5">ARSITEKTUR &amp; TOPOLOGI SISTEM TIKET BIOSKOP (BIG PICTURE)</text>
  <text x="185" y="115" fill="#94a3b8" font-family="'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="500">Gambaran Arsitektur Awan Skala Nasional • Alur Kerja dari Akses Pengguna, Pintu Keamanan, Layanan Bisnis hingga Basis Data &amp; Mitra Pembayaran</text>

  <!-- Header Badges -->
  <g transform="translate(1600, 68)">
    <rect x="0" y="0" width="195" height="42" rx="21" fill="#0284c7" fill-opacity="0.2" stroke="#38bdf8" stroke-width="1.2"/>
    <text x="97" y="26" fill="#38bdf8" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" text-anchor="middle">High Availability 99.95%</text>

    <rect x="210" y="0" width="175" height="42" rx="21" fill="#b45309" fill-opacity="0.2" stroke="#f59e0b" stroke-width="1.2"/>
    <text x="297" y="26" fill="#f59e0b" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" text-anchor="middle">Respon &lt; 1 Milidetik</text>

    <rect x="400" y="0" width="185" height="42" rx="21" fill="#065f46" fill-opacity="0.2" stroke="#10b981" stroke-width="1.2"/>
    <text x="492" y="26" fill="#34d399" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" text-anchor="middle">Zero Double-Booking</text>
  </g>


  <!-- ==================== 4 MAIN ARCHITECTURAL TIERS ==================== -->

  <!-- TIER 1: CLIENT CHANNELS (Saluran Pengguna) -->
  <g transform="translate(70, 180)">
    <rect width="470" height="1030" rx="18" fill="url(#cardGrad)" stroke="#38bdf8" stroke-width="1.5" filter="url(#shadow)"/>
    
    <!-- Title Bar -->
    <rect width="470" height="56" rx="18" fill="url(#tierHeaderGrad)" />
    <rect y="30" width="470" height="26" fill="url(#tierHeaderGrad)" />
    <circle cx="32" cy="28" r="9" fill="#38bdf8" />
    <text x="52" y="34" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="17" font-weight="800">1. SALURAN PENGGUNA (CHANNELS)</text>
    <text x="445" y="34" fill="#38bdf8" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" text-anchor="end">Front-End</text>

    <text x="25" y="85" fill="#94a3b8" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">Berbagai pintu masuk bagi penonton dan staf:</text>

    <!-- Card 1.1: Mobile App -->
    <g transform="translate(25, 105)">
      <rect width="420" height="195" rx="14" fill="url(#subCardGrad)" stroke="#334155" stroke-width="1.2" />
      <g transform="translate(20, 20)">
        <rect width="40" height="40" rx="10" fill="#0284c7" fill-opacity="0.25" stroke="#38bdf8" stroke-width="1.2"/>
        <!-- Phone Vector Icon -->
        <rect x="13" y="8" width="14" height="24" rx="3" fill="none" stroke="#38bdf8" stroke-width="2" />
        <circle cx="20" cy="27" r="1.5" fill="#38bdf8" />
      </g>
      <text x="75" y="38" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="17" font-weight="800">Aplikasi Mobile (iOS &amp; Android)</text>
      <text x="75" y="58" fill="#38bdf8" font-family="'Segoe UI', Roboto, sans-serif" font-size="12.5" font-weight="600">Flutter / Native Client</text>
      
      <line x1="20" y1="72" x2="400" y2="72" stroke="#1e293b" />
      <text x="20" y="100" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Pemesanan tiket praktis di smartphone</text>
      <text x="20" y="125" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Tampilan denah kursi interaktif real-time</text>
      <text x="20" y="150" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Simpan E-Ticket QR siap scan di bioskop</text>
      <rect x="20" y="165" width="380" height="20" rx="4" fill="#0c1e38" />
      <text x="210" y="179" fill="#7dd3fc" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" text-anchor="middle">Digunakan oleh Mayoritas Penonton</text>
    </g>

    <!-- Card 1.2: Web Customer Portal -->
    <g transform="translate(25, 320)">
      <rect width="420" height="195" rx="14" fill="url(#subCardGrad)" stroke="#334155" stroke-width="1.2" />
      <g transform="translate(20, 20)">
        <rect width="40" height="40" rx="10" fill="#4f46e5" fill-opacity="0.25" stroke="#818cf8" stroke-width="1.2"/>
        <!-- Monitor Vector Icon -->
        <rect x="8" y="9" width="24" height="16" rx="2" fill="none" stroke="#818cf8" stroke-width="2" />
        <line x1="16" y1="25" x2="24" y2="25" stroke="#818cf8" stroke-width="2" />
        <line x1="20" y1="25" x2="20" y2="29" stroke="#818cf8" stroke-width="2" />
        <line x1="14" y1="29" x2="26" y2="29" stroke="#818cf8" stroke-width="2" />
      </g>
      <text x="75" y="38" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="17" font-weight="800">Website Bioskop (Web Portal)</text>
      <text x="75" y="58" fill="#818cf8" font-family="'Segoe UI', Roboto, sans-serif" font-size="12.5" font-weight="600">Responsive Web (Next.js)</text>
      
      <line x1="20" y1="72" x2="400" y2="72" stroke="#1e293b" />
      <text x="20" y="100" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Akses cepat tanpa perlu install aplikasi</text>
      <text x="20" y="125" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Pencarian jadwal film lengkap multi-kota</text>
      <text x="20" y="150" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Checkout mudah via peramban laptop / HP</text>
      <rect x="20" y="165" width="380" height="20" rx="4" fill="#141438" />
      <text x="210" y="179" fill="#a5b4fc" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" text-anchor="middle">Mudah Diakses Melalui Google Search</text>
    </g>

    <!-- Card 1.3: Box Office Kiosk -->
    <g transform="translate(25, 535)">
      <rect width="420" height="195" rx="14" fill="url(#subCardGrad)" stroke="#334155" stroke-width="1.2" />
      <g transform="translate(20, 20)">
        <rect width="40" height="40" rx="10" fill="#db2777" fill-opacity="0.25" stroke="#f472b6" stroke-width="1.2"/>
        <!-- Ticket POS Vector Icon -->
        <rect x="9" y="12" width="22" height="16" rx="2" fill="none" stroke="#f472b6" stroke-width="2" />
        <line x1="9" y1="20" x2="31" y2="20" stroke="#f472b6" stroke-width="1.5" stroke-dasharray="2 2" />
        <circle cx="9" cy="20" r="2" fill="#162238" />
        <circle cx="31" cy="20" r="2" fill="#162238" />
      </g>
      <text x="75" y="38" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="17" font-weight="800">Loket Fisik (Box Office POS)</text>
      <text x="75" y="58" fill="#f472b6" font-family="'Segoe UI', Roboto, sans-serif" font-size="12.5" font-weight="600">On-Site Cinema Counters</text>
      
      <line x1="20" y1="72" x2="400" y2="72" stroke="#1e293b" />
      <text x="20" y="100" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Kasir on-the-spot di lobi cabang bioskop</text>
      <text x="20" y="125" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Cetak tiket fisik &amp; layani bayar tunai / EDC</text>
      <text x="20" y="150" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Terhubung ke data inventaris kursi terpusat</text>
      <rect x="20" y="165" width="380" height="20" rx="4" fill="#310f22" />
      <text x="210" y="179" fill="#fbcfe8" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" text-anchor="middle">Sinkron Seketika dengan Penjualan Online</text>
    </g>

    <!-- Card 1.4: Admin Dashboard -->
    <g transform="translate(25, 750)">
      <rect width="420" height="195" rx="14" fill="url(#subCardGrad)" stroke="#334155" stroke-width="1.2" />
      <g transform="translate(20, 20)">
        <rect width="40" height="40" rx="10" fill="#d97706" fill-opacity="0.25" stroke="#f59e0b" stroke-width="1.2"/>
        <!-- Sliders / Gear Vector Icon -->
        <line x1="10" y1="14" x2="30" y2="14" stroke="#f59e0b" stroke-width="2" />
        <circle cx="16" cy="14" r="3" fill="#f59e0b" />
        <line x1="10" y1="26" x2="30" y2="26" stroke="#f59e0b" stroke-width="2" />
        <circle cx="24" cy="26" r="3" fill="#f59e0b" />
      </g>
      <text x="75" y="38" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="17" font-weight="800">Portal Admin Manajemen</text>
      <text x="75" y="58" fill="#f59e0b" font-family="'Segoe UI', Roboto, sans-serif" font-size="12.5" font-weight="600">HQ &amp; Branch Operations</text>
      
      <line x1="20" y1="72" x2="400" y2="72" stroke="#1e293b" />
      <text x="20" y="100" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Input jadwal tayang film di tiap studio</text>
      <text x="20" y="125" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Monitor penjualan tiket &amp; okupansi bioskop</text>
      <text x="20" y="150" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Tombol pembatalan darurat &amp; auto-refund</text>
      <rect x="20" y="165" width="380" height="20" rx="4" fill="#2d1c08" />
      <text x="210" y="179" fill="#fde68a" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" text-anchor="middle">Kontrol Operasional Bioskop Terpusat</text>
    </g>

    <!-- Bottom summary badge -->
    <rect x="25" y="960" width="420" height="50" rx="10" fill="#091322" stroke="#1e293b" />
    <text x="235" y="990" fill="#38bdf8" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" text-anchor="middle">Enkripsi Aman Jalur HTTPS / TLS 1.3</text>
  </g>

  <!-- Flow Arrow Tier 1 -> Tier 2 -->
  <line x1="540" y1="695" x2="590" y2="695" stroke="#38bdf8" stroke-width="4" marker-end="url(#arrowCyan)" />


  <!-- TIER 2: GATEWAY & SECURITY (Keamanan & Pintu Gerbang) -->
  <g transform="translate(600, 180)">
    <rect width="450" height="1030" rx="18" fill="url(#cardGrad)" stroke="#f59e0b" stroke-width="1.5" filter="url(#shadow)"/>
    
    <!-- Title Bar -->
    <rect width="450" height="56" rx="18" fill="url(#tierHeaderGrad)" />
    <rect y="30" width="450" height="26" fill="url(#tierHeaderGrad)" />
    <circle cx="32" cy="28" r="9" fill="#f59e0b" />
    <text x="52" y="34" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="17" font-weight="800">2. KEAMANAN &amp; GERBANG (GATEWAY)</text>
    <text x="425" y="34" fill="#f59e0b" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" text-anchor="end">Security</text>

    <text x="25" y="85" fill="#94a3b8" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">Menyaring dan melindungi sistem dari ancaman:</text>

    <!-- Card 2.1: Cloudflare & DDoS Shield -->
    <g transform="translate(25, 120)">
      <rect width="400" height="240" rx="14" fill="url(#subCardGrad)" stroke="#f59e0b" stroke-width="1.2" />
      <g transform="translate(20, 20)">
        <rect width="40" height="40" rx="10" fill="#d97706" fill-opacity="0.25" stroke="#f59e0b" stroke-width="1.2"/>
        <!-- Shield Vector Icon -->
        <path d="M 20 8 L 32 13 L 32 24 C 32 30 20 34 20 34 C 20 34 8 30 8 24 L 8 13 Z" fill="none" stroke="#f59e0b" stroke-width="2" />
        <polyline points="15,20 18,23 25,16" fill="none" stroke="#f59e0b" stroke-width="2" />
      </g>
      <text x="75" y="38" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="17" font-weight="800">Cloudflare Edge &amp; WAF</text>
      <text x="75" y="58" fill="#f59e0b" font-family="'Segoe UI', Roboto, sans-serif" font-size="12.5" font-weight="600">Perlindungan Serangan Siber</text>
      
      <line x1="20" y1="75" x2="380" y2="75" stroke="#1e293b" />
      <text x="20" y="105" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• <tspan fill="#fde68a" font-weight="700">Anti-DDoS:</tspan> Menangkal banjir trafik jahat</text>
      <text x="20" y="133" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• <tspan fill="#fde68a" font-weight="700">WAF &amp; Bot Guard:</tspan> Memblokir calo tiket otomatis</text>
      <text x="20" y="161" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• <tspan fill="#fde68a" font-weight="700">Global CDN:</tspan> Poster film termuat kilat</text>
      <text x="20" y="189" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• <tspan fill="#fde68a" font-weight="700">Rate Limiter:</tspan> Mencegah spam klik berulang</text>

      <rect x="20" y="205" width="360" height="22" rx="4" fill="#2d1c08" />
      <text x="200" y="220" fill="#fde68a" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="700" text-anchor="middle">Menangkal Serangan Sebelum Masuk Server</text>
    </g>

    <!-- Card 2.2: API Gateway & Load Balancer -->
    <g transform="translate(25, 400)">
      <rect width="400" height="250" rx="14" fill="url(#subCardGrad)" stroke="#38bdf8" stroke-width="1.2" />
      <g transform="translate(20, 20)">
        <rect width="40" height="40" rx="10" fill="#0284c7" fill-opacity="0.25" stroke="#38bdf8" stroke-width="1.2"/>
        <!-- Router Vector Icon -->
        <circle cx="20" cy="14" r="4" fill="none" stroke="#38bdf8" stroke-width="2" />
        <circle cx="12" cy="27" r="4" fill="none" stroke="#38bdf8" stroke-width="2" />
        <circle cx="28" cy="27" r="4" fill="none" stroke="#38bdf8" stroke-width="2" />
        <line x1="18" y1="17" x2="14" y2="24" stroke="#38bdf8" stroke-width="1.5" />
        <line x1="22" y1="17" x2="26" y2="24" stroke="#38bdf8" stroke-width="1.5" />
      </g>
      <text x="75" y="38" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="17" font-weight="800">Smart Gateway &amp; Balancer</text>
      <text x="75" y="58" fill="#38bdf8" font-family="'Segoe UI', Roboto, sans-serif" font-size="12.5" font-weight="600">Pengatur Lalu Lintas Trafik</text>
      
      <line x1="20" y1="75" x2="380" y2="75" stroke="#1e293b" />
      <text x="20" y="105" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• <tspan fill="#7dd3fc" font-weight="700">Load Balancer:</tspan> Beban dibagi merata ke server</text>
      <text x="20" y="133" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• <tspan fill="#7dd3fc" font-weight="700">Single Door:</tspan> Seluruh kanal masuk lewat 1 pintu</text>
      <text x="20" y="161" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• <tspan fill="#7dd3fc" font-weight="700">Auto Failover:</tspan> Server rusak langsung dialihkan</text>
      <text x="20" y="189" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• <tspan fill="#7dd3fc" font-weight="700">Verifikasi JWT:</tspan> Otentikasi login pengguna sah</text>

      <rect x="20" y="210" width="360" height="24" rx="4" fill="#08223d" />
      <text x="200" y="226" fill="#7dd3fc" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="700" text-anchor="middle">Trafik Mengalir Efisien &amp; Tanpa Macet</text>
    </g>

    <!-- Card 2.3: Virtual Waiting Room (Feature) -->
    <g transform="translate(25, 690)">
      <rect width="400" height="220" rx="14" fill="url(#subCardGrad)" stroke="#10b981" stroke-width="1.2" />
      <g transform="translate(20, 20)">
        <rect width="40" height="40" rx="10" fill="#059669" fill-opacity="0.25" stroke="#10b981" stroke-width="1.2"/>
        <!-- Hourglass / Clock Icon -->
        <circle cx="20" cy="20" r="11" fill="none" stroke="#10b981" stroke-width="2" />
        <polyline points="20,13 20,20 25,23" fill="none" stroke="#10b981" stroke-width="2" />
      </g>
      <text x="75" y="38" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="17" font-weight="800">Virtual Waiting Room</text>
      <text x="75" y="58" fill="#34d399" font-family="'Segoe UI', Roboto, sans-serif" font-size="12.5" font-weight="600">Peredam Lonjakan Blockbuster</text>
      
      <line x1="20" y1="75" x2="380" y2="75" stroke="#1e293b" />
      <text x="20" y="105" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Mengantrekan penonton secara tertib saat</text>
      <text x="20" y="128" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">  tiket film viral / box office dibuka serentak</text>
      <text x="20" y="153" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Menjamin server inti tidak pernah tumbang</text>

      <rect x="20" y="175" width="360" height="24" rx="4" fill="#063824" />
      <text x="200" y="191" fill="#6ee7b7" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="700" text-anchor="middle">Sistem Tetap Kokoh di Trafik Puncak</text>
    </g>

    <!-- Bottom summary badge -->
    <rect x="25" y="960" width="400" height="50" rx="10" fill="#1c1917" stroke="#b45309" />
    <text x="225" y="990" fill="#fde68a" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" text-anchor="middle">Zero Down-Time Protection Architecture</text>
  </g>

  <!-- Flow Arrow Tier 2 -> Tier 3 -->
  <line x1="1050" y1="695" x2="1100" y2="695" stroke="#f59e0b" stroke-width="4" marker-end="url(#arrowAmber)" />


  <!-- TIER 3: CORE CINEMA PLATFORM (Mesin Bisnis Utama) -->
  <g transform="translate(1110, 180)">
    <rect width="580" height="1030" rx="18" fill="url(#cardGrad)" stroke="#10b981" stroke-width="1.8" filter="url(#shadow)"/>
    
    <!-- Title Bar -->
    <rect width="580" height="56" rx="18" fill="url(#tierHeaderGrad)" />
    <rect y="30" width="580" height="26" fill="url(#tierHeaderGrad)" />
    <circle cx="32" cy="28" r="9" fill="#10b981" />
    <text x="52" y="34" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="17" font-weight="800">3. MESIN BISNIS UTAMA (CORE PLATFORM)</text>
    <text x="555" y="34" fill="#10b981" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" text-anchor="end">Business Logic</text>

    <text x="25" y="85" fill="#94a3b8" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">Layanan cerdas yang menjalankan seluruh alur bisnis bioskop:</text>

    <!-- Card 3.1: Movie & Schedule Management -->
    <g transform="translate(25, 105)">
      <rect width="530" height="195" rx="14" fill="url(#subCardGrad)" stroke="#334155" stroke-width="1.2" />
      <g transform="translate(20, 20)">
        <rect width="40" height="40" rx="10" fill="#0284c7" fill-opacity="0.25" stroke="#38bdf8" stroke-width="1.2"/>
        <!-- Film Reel Vector Icon -->
        <circle cx="20" cy="20" r="12" fill="none" stroke="#38bdf8" stroke-width="2" />
        <circle cx="20" cy="20" r="4" fill="#38bdf8" />
        <circle cx="20" cy="11" r="2" fill="#38bdf8" />
        <circle cx="20" cy="29" r="2" fill="#38bdf8" />
        <circle cx="11" cy="20" r="2" fill="#38bdf8" />
        <circle cx="29" cy="20" r="2" fill="#38bdf8" />
      </g>
      <text x="75" y="38" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="17" font-weight="800">Layanan Film &amp; Jadwal (Schedule Engine)</text>
      <text x="75" y="58" fill="#38bdf8" font-family="'Segoe UI', Roboto, sans-serif" font-size="12.5" font-weight="600">Multi-Branch Cinema Catalog</text>
      
      <line x1="20" y1="72" x2="510" y2="72" stroke="#1e293b" />
      <text x="20" y="100" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Sinkronisasi katalog film bioskop di seluruh kota di Indonesia</text>
      <text x="20" y="125" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Jadwal otomatis menyesuaikan zona waktu lokal (WIB, WITA, WIT)</text>
      <text x="20" y="150" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Pencegahan otomatis bentrok jadwal film di studio yang sama</text>
      <rect x="20" y="165" width="490" height="20" rx="4" fill="#08233d" />
      <text x="265" y="179" fill="#7dd3fc" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" text-anchor="middle">Jadwal Selalu Rapi &amp; Tidak Pernah Tumpang Tindih</text>
    </g>

    <!-- Card 3.2: Seat Locking Engine (FEATURED) -->
    <g transform="translate(25, 320)">
      <rect width="530" height="205" rx="14" fill="url(#amberCardGrad)" stroke="#f59e0b" stroke-width="2" filter="url(#shadow)"/>
      <g transform="translate(20, 20)">
        <rect width="40" height="40" rx="10" fill="#d97706" fill-opacity="0.3" stroke="#f59e0b" stroke-width="1.5"/>
        <!-- Padlock Vector Icon -->
        <rect x="11" y="16" width="18" height="14" rx="2" fill="none" stroke="#f59e0b" stroke-width="2" />
        <path d="M 14 16 L 14 11 A 6 6 0 0 1 26 11 L 26 16" fill="none" stroke="#f59e0b" stroke-width="2" />
        <circle cx="20" cy="23" r="1.5" fill="#f59e0b" />
      </g>
      <text x="75" y="38" fill="#fde68a" font-family="'Segoe UI', Roboto, sans-serif" font-size="17" font-weight="800">Mesin Pengunci Kursi 10 Menit (Seat Lock)</text>
      <text x="75" y="58" fill="#f59e0b" font-family="'Segoe UI', Roboto, sans-serif" font-size="12.5" font-weight="700">Zero Double-Booking Guarantee</text>
      
      <line x1="20" y1="72" x2="510" y2="72" stroke="#78350f" stroke-width="1.2" />
      <text x="20" y="100" fill="#fef3c7" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5" font-weight="600">• Seketika mengunci kursi terpilih dalam hitungan milidetik</text>
      <text x="20" y="125" fill="#fef3c7" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5" font-weight="600">• Menjamin 2 pembeli tidak bisa mengambil kursi sama di waktu bersamaan</text>
      <text x="20" y="150" fill="#fef3c7" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5" font-weight="600">• Memberikan rasa aman dan waktu eksklusif 10 menit bagi pembeli</text>
      <rect x="20" y="170" width="490" height="24" rx="4" fill="#1c1917" stroke="#78350f" />
      <text x="265" y="186" fill="#fbbf24" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="800" text-anchor="middle">Inti Proteksi: Rebutan Kursi Mustahil Terjadi 100%</text>
    </g>

    <!-- Card 3.3: Order & Payment Processing -->
    <g transform="translate(25, 545)">
      <rect width="530" height="195" rx="14" fill="url(#subCardGrad)" stroke="#334155" stroke-width="1.2" />
      <g transform="translate(20, 20)">
        <rect width="40" height="40" rx="10" fill="#059669" fill-opacity="0.25" stroke="#10b981" stroke-width="1.2"/>
        <!-- Credit Card Vector Icon -->
        <rect x="8" y="11" width="24" height="18" rx="2" fill="none" stroke="#10b981" stroke-width="2" />
        <line x1="8" y1="17" x2="32" y2="17" stroke="#10b981" stroke-width="2" />
        <rect x="12" y="22" width="5" height="3" fill="#10b981" />
      </g>
      <text x="75" y="38" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="17" font-weight="800">Layanan Pesanan &amp; E-Tiket (Orders &amp; Tickets)</text>
      <text x="75" y="58" fill="#34d399" font-family="'Segoe UI', Roboto, sans-serif" font-size="12.5" font-weight="600">Checkout &amp; QR Code Issuance</text>
      
      <line x1="20" y1="72" x2="510" y2="72" stroke="#1e293b" />
      <text x="20" y="100" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Menghitung total transaksi dan menerbitkan tagihan checkout instan</text>
      <text x="20" y="125" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Mengonfirmasi notifikasi pelunasan dari payment gateway</text>
      <text x="20" y="150" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Menerbitkan tiket digital resmi dengan QR code unik anti-pemalsuan</text>
      <rect x="20" y="165" width="490" height="20" rx="4" fill="#063822" />
      <text x="265" y="179" fill="#a7f3d0" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" text-anchor="middle">Tiket Sah Langsung Tersimpan di HP Pengguna</text>
    </g>

    <!-- Card 3.4: Automated Workers (Restock & Refund) -->
    <g transform="translate(25, 760)">
      <rect width="530" height="195" rx="14" fill="url(#subCardGrad)" stroke="#38bdf8" stroke-width="1.2" />
      <g transform="translate(20, 20)">
        <rect width="40" height="40" rx="10" fill="#0284c7" fill-opacity="0.25" stroke="#38bdf8" stroke-width="1.2"/>
        <!-- Robot / Cogs Vector Icon -->
        <circle cx="20" cy="20" r="10" fill="none" stroke="#38bdf8" stroke-width="2" />
        <circle cx="20" cy="20" r="3" fill="#38bdf8" />
        <line x1="20" y1="6" x2="20" y2="10" stroke="#38bdf8" stroke-width="2" />
        <line x1="20" y1="30" x2="20" y2="34" stroke="#38bdf8" stroke-width="2" />
        <line x1="6" y1="20" x2="10" y2="20" stroke="#38bdf8" stroke-width="2" />
        <line x1="30" y1="20" x2="34" y2="20" stroke="#38bdf8" stroke-width="2" />
      </g>
      <text x="75" y="38" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="17" font-weight="800">Robot Otomatis (Restock &amp; Refund Workers)</text>
      <text x="75" y="58" fill="#38bdf8" font-family="'Segoe UI', Roboto, sans-serif" font-size="12.5" font-weight="600">Background Automation Engine</text>
      
      <line x1="20" y1="72" x2="510" y2="72" stroke="#1e293b" />
      <text x="20" y="100" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• <tspan fill="#f59e0b" font-weight="700">Restok Otomatis:</tspan> Melepaskan kursi yang tidak dibayar dalam 10 menit</text>
      <text x="20" y="125" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• <tspan fill="#34d399" font-weight="700">Refund 100%:</tspan> Mentransfer balik dana penonton saat jadwal bioskop batal</text>
      <text x="20" y="150" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Bekerja 24/7 di latar belakang tanpa membutuhkan intervensi manual staf</text>
      <rect x="20" y="165" width="490" height="20" rx="4" fill="#08233d" />
      <text x="265" y="179" fill="#7dd3fc" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" text-anchor="middle">Otomatisasi Menghilangkan Human-Error</text>
    </g>

    <!-- Bottom summary badge -->
    <rect x="25" y="965" width="530" height="50" rx="10" fill="#063124" stroke="#059669" />
    <text x="290" y="995" fill="#a7f3d0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" text-anchor="middle">Mesin Golang Berkecepatan Tinggi &amp; Efisien</text>
  </g>

  <!-- Flow Arrow Tier 3 -> Tier 4 -->
  <line x1="1690" y1="695" x2="1740" y2="695" stroke="#10b981" stroke-width="4" marker-end="url(#arrowGreen)" />


  <!-- TIER 4: DATA STORAGE & PARTNER INTEGRATION (Pusat Data & Mitra) -->
  <g transform="translate(1750, 180)">
    <rect width="580" height="1030" rx="18" fill="url(#cardGrad)" stroke="#c084fc" stroke-width="1.5" filter="url(#shadow)"/>
    
    <!-- Title Bar -->
    <rect width="580" height="56" rx="18" fill="url(#tierHeaderGrad)" />
    <rect y="30" width="580" height="26" fill="url(#tierHeaderGrad)" />
    <circle cx="32" cy="28" r="9" fill="#c084fc" />
    <text x="52" y="34" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="17" font-weight="800">4. PUSAT DATA &amp; INTEGRASI (DATA &amp; PARTNERS)</text>
    <text x="555" y="34" fill="#c084fc" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" text-anchor="end">Storage &amp; Sync</text>

    <text x="25" y="85" fill="#94a3b8" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">Penyimpanan permanen berintegritas tinggi dan ekosistem mitra luar:</text>

    <!-- Card 4.1: Redis High-Speed Cache -->
    <g transform="translate(25, 105)">
      <rect width="530" height="195" rx="14" fill="url(#subCardGrad)" stroke="#f59e0b" stroke-width="1.2" />
      <g transform="translate(20, 20)">
        <rect width="40" height="40" rx="10" fill="#d97706" fill-opacity="0.25" stroke="#f59e0b" stroke-width="1.2"/>
        <!-- Lightning Vector Icon -->
        <polygon points="21,7 11,21 19,21 17,33 29,17 21,17" fill="#f59e0b" />
      </g>
      <text x="75" y="38" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="17" font-weight="800">Penyimpanan Memori Cepat (Redis Cluster)</text>
      <text x="75" y="58" fill="#f59e0b" font-family="'Segoe UI', Roboto, sans-serif" font-size="12.5" font-weight="600">Sub-Millisecond In-Memory Store</text>
      
      <line x1="20" y1="72" x2="510" y2="72" stroke="#1e293b" />
      <text x="20" y="100" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Menyimpan status kunci kursi sementara dengan timer 10 menit</text>
      <text x="20" y="125" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Menghadirkan respon super kilat (&lt; 1 milidetik) saat penonton klik kursi</text>
      <text x="20" y="150" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Melindungi database utama dari banjir permintaan saat film laris</text>
      <rect x="20" y="165" width="490" height="20" rx="4" fill="#2d1c08" />
      <text x="265" y="179" fill="#fde68a" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" text-anchor="middle">Denah Terbuka Cepat Tanpa Loading Berat</text>
    </g>

    <!-- Card 4.2: PostgreSQL Database -->
    <g transform="translate(25, 320)">
      <rect width="530" height="205" rx="14" fill="url(#subCardGrad)" stroke="#38bdf8" stroke-width="1.5" />
      <g transform="translate(20, 20)">
        <rect width="40" height="40" rx="10" fill="#0284c7" fill-opacity="0.25" stroke="#38bdf8" stroke-width="1.2"/>
        <!-- Database Cylinder Icon -->
        <ellipse cx="20" cy="12" rx="12" ry="4" fill="none" stroke="#38bdf8" stroke-width="2" />
        <path d="M 8 12 L 8 20 A 12 4 0 0 0 32 20 L 32 12" fill="none" stroke="#38bdf8" stroke-width="2" />
        <path d="M 8 20 L 8 28 A 12 4 0 0 0 32 28 L 32 20" fill="none" stroke="#38bdf8" stroke-width="2" />
      </g>
      <text x="75" y="38" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="17" font-weight="800">Basis Data Utama (PostgreSQL Multi-AZ)</text>
      <text x="75" y="58" fill="#38bdf8" font-family="'Segoe UI', Roboto, sans-serif" font-size="12.5" font-weight="600">The Authoritative Single Source of Truth</text>
      
      <line x1="20" y1="72" x2="510" y2="72" stroke="#1e293b" />
      <text x="20" y="100" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Rekam data resmi: Akun Pengguna, Jadwal, Pesanan &amp; E-Tiket Sah</text>
      <text x="20" y="125" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Transaksi ACID: Data finansial tidak akan pernah hilang atau rusak</text>
      <text x="20" y="150" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Replikasi Multi-Zona: Cadangan otomatis siaga jika server data center mati</text>
      <rect x="20" y="170" width="490" height="24" rx="4" fill="#08233d" />
      <text x="265" y="186" fill="#7dd3fc" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="800" text-anchor="middle">Sumber Kebenaran Data Transaksi yang Sah &amp; Legal</text>
    </g>

    <!-- Card 4.3: Real-Time Event Broker -->
    <g transform="translate(25, 545)">
      <rect width="530" height="195" rx="14" fill="url(#subCardGrad)" stroke="#c084fc" stroke-width="1.2" />
      <g transform="translate(20, 20)">
        <rect width="40" height="40" rx="10" fill="#9333ea" fill-opacity="0.25" stroke="#c084fc" stroke-width="1.2"/>
        <!-- Signal / Broadcast Icon -->
        <circle cx="20" cy="20" r="3" fill="#c084fc" />
        <path d="M 14 14 A 9 9 0 0 0 14 26" fill="none" stroke="#c084fc" stroke-width="2" />
        <path d="M 26 14 A 9 9 0 0 1 26 26" fill="none" stroke="#c084fc" stroke-width="2" />
        <path d="M 10 10 A 15 15 0 0 0 10 30" fill="none" stroke="#c084fc" stroke-width="2" />
        <path d="M 30 10 A 15 15 0 0 1 30 30" fill="none" stroke="#c084fc" stroke-width="2" />
      </g>
      <text x="75" y="38" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="17" font-weight="800">Penyalur Sinyal Real-Time (Event Broker)</text>
      <text x="75" y="58" fill="#c084fc" font-family="'Segoe UI', Roboto, sans-serif" font-size="12.5" font-weight="600">Message Queue &amp; Real-time Streaming</text>
      
      <line x1="20" y1="72" x2="510" y2="72" stroke="#1e293b" />
      <text x="20" y="100" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Menyiarkan perubahan warna denah kursi ke jutaan HP penonton</text>
      <text x="20" y="125" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Memerintahkan robot sistem mengeksekusi restok &amp; pengembalian dana</text>
      <text x="20" y="150" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Merekam audit trail keamanan yang tidak bisa diubah (immutable)</text>
      <rect x="20" y="165" width="490" height="20" rx="4" fill="#200d33" />
      <text x="265" y="179" fill="#e9d5ff" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" text-anchor="middle">Komunikasi Antar-Layanan Sangat Cepat &amp; Tanggap</text>
    </g>

    <!-- Card 4.4: External Partners (Payment & Messaging) -->
    <g transform="translate(25, 760)">
      <rect width="530" height="195" rx="14" fill="url(#subCardGrad)" stroke="#10b981" stroke-width="1.2" />
      <g transform="translate(20, 20)">
        <rect width="40" height="40" rx="10" fill="#059669" fill-opacity="0.25" stroke="#10b981" stroke-width="1.2"/>
        <!-- Handshake / World Icon -->
        <circle cx="20" cy="20" r="12" fill="none" stroke="#10b981" stroke-width="2" />
        <ellipse cx="20" cy="20" rx="6" ry="12" fill="none" stroke="#10b981" stroke-width="1.5" />
        <line x1="8" y1="20" x2="32" y2="20" stroke="#10b981" stroke-width="1.5" />
      </g>
      <text x="75" y="38" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="17" font-weight="800">Mitra Pembayaran &amp; Komunikasi Eksternal</text>
      <text x="75" y="58" fill="#34d399" font-family="'Segoe UI', Roboto, sans-serif" font-size="12.5" font-weight="600">National Ecosystem Integrations</text>
      
      <line x1="20" y1="72" x2="510" y2="72" stroke="#1e293b" />
      <text x="20" y="100" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• <tspan fill="#34d399" font-weight="700">Payment Gateway:</tspan> QRIS nasional, GoPay, OVO, VA BCA &amp; Mandiri</text>
      <text x="20" y="125" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• <tspan fill="#34d399" font-weight="700">WhatsApp &amp; Email API:</tspan> Kirim QR e-ticket &amp; notifikasi pengembalian dana</text>
      <text x="20" y="150" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Terhubung otomatis dengan sistem rekonsiliasi keuangan akuntansi</text>
      <rect x="20" y="165" width="490" height="20" rx="4" fill="#063822" />
      <text x="265" y="179" fill="#a7f3d0" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" text-anchor="middle">Terkoneksi dengan Ekosistem Pembayaran Seluruh Bank</text>
    </g>

    <!-- Bottom summary badge -->
    <rect x="25" y="965" width="530" height="50" rx="10" fill="#1b122e" stroke="#7e22ce" />
    <text x="290" y="995" fill="#e9d5ff" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" text-anchor="middle">Kepatuhan Standar Industri Finansial &amp; Keamanan Data</text>
  </g>


  <!-- ==================== BOTTOM BANNER: 4 KEUNGGULAN BISNIS (BUSINESS VALUE) ==================== -->
  <g transform="translate(70, 1235)">
    <rect width="2260" height="245" rx="18" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5" filter="url(#shadow)"/>
    
    <!-- Title Bar -->
    <rect width="2260" height="44" rx="18" fill="#1e293b" />
    <rect y="24" width="2260" height="20" fill="#1e293b" />
    <text x="35" y="28" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="800">4 NILAI BISNIS UTAMA BAGI KLIEN, MANAJEMEN BIOSKOP, DAN PENGGUNA</text>

    <!-- 4 Value Cards -->
    <g transform="translate(35, 65)">
      <!-- Value 1: Zero Double Booking -->
      <g transform="translate(0, 0)">
        <rect width="525" height="150" rx="12" fill="#0b1b16" stroke="#10b981" stroke-width="1.5" />
        <rect x="20" y="18" width="36" height="36" rx="8" fill="#059669" />
        <circle cx="38" cy="36" r="8" fill="#a7f3d0" />
        <text x="68" y="34" fill="#a7f3d0" font-family="'Segoe UI', Roboto, sans-serif" font-size="16.5" font-weight="800">Garansi Bebas Rebutan Kursi</text>
        <text x="68" y="52" fill="#34d399" font-family="'Segoe UI', Roboto, sans-serif" font-size="12.5" font-weight="700">Zero Double-Booking Guarantee</text>
        
        <text x="20" y="85" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">Teknologi penguncian seketika (<tspan fill="#a7f3d0" font-weight="700">&lt; 1 milidetik</tspan>) menjamin</text>
        <text x="20" y="108" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13">dua penonton di kota berbeda tidak akan pernah bisa</text>
        <text x="20" y="128" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13">membeli nomor kursi yang sama. 100% Bebas komplain.</text>
      </g>

      <!-- Value 2: Auto Restock -->
      <g transform="translate(555, 0)">
        <rect width="525" height="150" rx="12" fill="#1f180d" stroke="#f59e0b" stroke-width="1.5" />
        <rect x="20" y="18" width="36" height="36" rx="8" fill="#d97706" />
        <circle cx="38" cy="36" r="8" fill="#fef3c7" />
        <text x="68" y="34" fill="#fde68a" font-family="'Segoe UI', Roboto, sans-serif" font-size="16.5" font-weight="800">Restok Inventaris Otomatis</text>
        <text x="68" y="52" fill="#f59e0b" font-family="'Segoe UI', Roboto, sans-serif" font-size="12.5" font-weight="700">Zero Inventory Waste</text>
        
        <text x="20" y="85" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">Kursi yang batal dibayar dalam 10 menit langsung</text>
        <text x="20" y="108" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13">kembali tersedia di aplikasi. Bioskop tidak kehilangan</text>
        <text x="20" y="128" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13">potensi penjualan tiket dan okupansi studio tetap optimal.</text>
      </g>

      <!-- Value 3: 100% Refund -->
      <g transform="translate(1110, 0)">
        <rect width="525" height="150" rx="12" fill="#1f1113" stroke="#ef4444" stroke-width="1.5" />
        <rect x="20" y="18" width="36" height="36" rx="8" fill="#b91c1c" />
        <circle cx="38" cy="36" r="8" fill="#fee2e2" />
        <text x="68" y="34" fill="#fca5a5" font-family="'Segoe UI', Roboto, sans-serif" font-size="16.5" font-weight="800">Garansi Refund 100% Cepat</text>
        <text x="68" y="52" fill="#f87171" font-family="'Segoe UI', Roboto, sans-serif" font-size="12.5" font-weight="700">Customer Protection &amp; Trust</text>
        
        <text x="20" y="85" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">Jika bioskop menghadapi kendala teknis darurat,</text>
        <text x="20" y="108" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13">sistem otomatis mentransfer balik dana pelanggan tanpa</text>
        <text x="20" y="128" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13">potongan biaya admin dan mengirim struk via WhatsApp.</text>
      </g>

      <!-- Value 4: Scalability & Uptime -->
      <g transform="translate(1665, 0)">
        <rect width="525" height="150" rx="12" fill="#091b33" stroke="#38bdf8" stroke-width="1.5" />
        <rect x="20" y="18" width="36" height="36" rx="8" fill="#0284c7" />
        <circle cx="38" cy="36" r="8" fill="#bae6fd" />
        <text x="68" y="34" fill="#bae6fd" font-family="'Segoe UI', Roboto, sans-serif" font-size="16.5" font-weight="800">Kapasitas Skala Nasional</text>
        <text x="68" y="52" fill="#38bdf8" font-family="'Segoe UI', Roboto, sans-serif" font-size="12.5" font-weight="700">High Scalability &amp; 99.95% SLA</text>
        
        <text x="20" y="85" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">Arsitektur komputasi awan siap menampung lonjakan</text>
        <text x="20" y="108" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13">puluhan ribu penonton serentak saat perilisan tiket film</text>
        <text x="20" y="128" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13">box office tanpa penurunan performa sistem.</text>
      </g>
    </g>
  </g>

</svg>'''
    with open('/tmp/system_topology.svg', 'w') as f:
        f.write(svg)



def create_database_erd_svg():
    svg = '''<svg width="1700" height="1200" viewBox="0 0 1700 1200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#090d16" />
      <stop offset="100%" stop-color="#111827" />
    </linearGradient>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="6" stdDeviation="4" flood-color="#000000" flood-opacity="0.5"/>
    </filter>
  </defs>

  <rect width="1700" height="1200" fill="url(#bgGrad)" />

  <!-- Header -->
  <rect x="50" y="30" width="1600" height="90" rx="12" fill="#1f2937" stroke="#3b82f6" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="90" y="70" fill="#f9fafb" font-family="sans-serif" font-size="26" font-weight="bold">ENTITY RELATIONSHIP DIAGRAM (ERD) - NATIONAL CINEMA DATABASE</text>
  <text x="90" y="98" fill="#9ca3af" font-family="sans-serif" font-size="15">PostgreSQL 15 Dialect • 14 Relational Tables • 3NF Normalized • PostgreSQL btree_gist Exclusion Constraint • High-Performance Indices</text>

  <!-- TABLE BOXES -->

  <!-- 1. PENGGUNA (users) -->
  <g transform="translate(60, 150)">
    <rect width="250" height="210" rx="8" fill="#111827" stroke="#3b82f6" stroke-width="1.5" filter="url(#shadow)"/>
    <rect width="250" height="36" rx="8" fill="#1e3a8a" />
    <text x="125" y="24" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">pengguna (users)</text>
    <text x="15" y="60" fill="#f59e0b" font-family="monospace" font-size="12">PK  id : BIGSERIAL</text>
    <text x="15" y="82" fill="#e5e7eb" font-family="monospace" font-size="12">    nama : VARCHAR(255)</text>
    <text x="15" y="104" fill="#60a5fa" font-family="monospace" font-size="12">UQ  email : VARCHAR(255)</text>
    <text x="15" y="126" fill="#e5e7eb" font-family="monospace" font-size="12">    hash_kata_sandi : VARCHAR</text>
    <text x="15" y="148" fill="#e5e7eb" font-family="monospace" font-size="12">    peran : VARCHAR(50)</text>
    <text x="15" y="170" fill="#9ca3af" font-family="monospace" font-size="11">    dibuat_pada : TIMESTAMPTZ</text>
    <text x="15" y="190" fill="#9ca3af" font-family="monospace" font-size="11">    diperbarui_pada : TIMESTAMPTZ</text>
  </g>

  <!-- 2. BIOSKOP (cinemas) -->
  <g transform="translate(370, 150)">
    <rect width="240" height="210" rx="8" fill="#111827" stroke="#10b981" stroke-width="1.5" filter="url(#shadow)"/>
    <rect width="240" height="36" rx="8" fill="#065f46" />
    <text x="120" y="24" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">bioskop (cinemas)</text>
    <text x="15" y="60" fill="#f59e0b" font-family="monospace" font-size="12">PK  id : BIGSERIAL</text>
    <text x="15" y="82" fill="#e5e7eb" font-family="monospace" font-size="12">    nama : VARCHAR(255)</text>
    <text x="15" y="104" fill="#e5e7eb" font-family="monospace" font-size="12">    kota : VARCHAR(100)</text>
    <text x="15" y="126" fill="#10b981" font-family="monospace" font-size="12">    zona_waktu : VARCHAR(50)</text>
    <text x="15" y="148" fill="#e5e7eb" font-family="monospace" font-size="12">    alamat : TEXT</text>
    <text x="15" y="170" fill="#e5e7eb" font-family="monospace" font-size="12">    status : VARCHAR(50)</text>
    <text x="15" y="192" fill="#9ca3af" font-family="monospace" font-size="11">    dibuat_pada : TIMESTAMPTZ</text>
  </g>

  <!-- 3. STUDIO (studios) -->
  <g transform="translate(670, 150)">
    <rect width="240" height="210" rx="8" fill="#111827" stroke="#10b981" stroke-width="1.5" filter="url(#shadow)"/>
    <rect width="240" height="36" rx="8" fill="#065f46" />
    <text x="120" y="24" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">studio (studios)</text>
    <text x="15" y="60" fill="#f59e0b" font-family="monospace" font-size="12">PK  id : BIGSERIAL</text>
    <text x="15" y="82" fill="#38bdf8" font-family="monospace" font-size="12">FK  bioskop_id : BIGINT</text>
    <text x="15" y="104" fill="#e5e7eb" font-family="monospace" font-size="12">    nama : VARCHAR(100)</text>
    <text x="15" y="126" fill="#e5e7eb" font-family="monospace" font-size="12">    kapasitas : INT</text>
    <text x="15" y="148" fill="#e5e7eb" font-family="monospace" font-size="12">    tipe : VARCHAR(50)</text>
    <text x="15" y="170" fill="#e5e7eb" font-family="monospace" font-size="12">    status : VARCHAR(50)</text>
    <text x="15" y="192" fill="#9ca3af" font-family="monospace" font-size="11">    dibuat_pada : TIMESTAMPTZ</text>
  </g>

  <!-- 4. KURSI (seats) -->
  <g transform="translate(970, 150)">
    <rect width="250" height="200" rx="8" fill="#111827" stroke="#10b981" stroke-width="1.5" filter="url(#shadow)"/>
    <rect width="250" height="36" rx="8" fill="#065f46" />
    <text x="125" y="24" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">kursi (seats)</text>
    <text x="15" y="60" fill="#f59e0b" font-family="monospace" font-size="12">PK  id : BIGSERIAL</text>
    <text x="15" y="82" fill="#38bdf8" font-family="monospace" font-size="12">FK  studio_id : BIGINT</text>
    <text x="15" y="104" fill="#e5e7eb" font-family="monospace" font-size="12">    label_baris : VARCHAR(10)</text>
    <text x="15" y="126" fill="#e5e7eb" font-family="monospace" font-size="12">    nomor_kursi : INT</text>
    <text x="15" y="148" fill="#e5e7eb" font-family="monospace" font-size="12">    tipe_kursi : VARCHAR(50)</text>
    <text x="15" y="170" fill="#60a5fa" font-family="monospace" font-size="11">UQ  (studio, baris, nomor)</text>
  </g>

  <!-- 5. FILM (movies) -->
  <g transform="translate(1280, 150)">
    <rect width="260" height="210" rx="8" fill="#111827" stroke="#8b5cf6" stroke-width="1.5" filter="url(#shadow)"/>
    <rect width="260" height="36" rx="8" fill="#5b21b6" />
    <text x="130" y="24" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">film (movies)</text>
    <text x="15" y="60" fill="#f59e0b" font-family="monospace" font-size="12">PK  id : BIGSERIAL</text>
    <text x="15" y="82" fill="#e5e7eb" font-family="monospace" font-size="12">    judul : VARCHAR(255)</text>
    <text x="15" y="104" fill="#e5e7eb" font-family="monospace" font-size="12">    deskripsi : TEXT</text>
    <text x="15" y="126" fill="#e5e7eb" font-family="monospace" font-size="12">    durasi_menit : INT</text>
    <text x="15" y="148" fill="#e5e7eb" font-family="monospace" font-size="12">    rating_usia : VARCHAR(20)</text>
    <text x="15" y="170" fill="#e5e7eb" font-family="monospace" font-size="12">    status : VARCHAR(50)</text>
    <text x="15" y="192" fill="#9ca3af" font-family="monospace" font-size="11">    dibuat_pada : TIMESTAMPTZ</text>
  </g>

  <!-- 14. EVENT PEMBAYARAN (payment_events) -->
  <g transform="translate(60, 420)">
    <rect width="260" height="240" rx="8" fill="#111827" stroke="#10b981" stroke-width="1.8" filter="url(#shadow)"/>
    <rect width="260" height="36" rx="8" fill="#065f46" />
    <text x="130" y="24" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">event_pembayaran (webhook)</text>
    <text x="15" y="60" fill="#f59e0b" font-family="monospace" font-size="12">PK  id : BIGSERIAL</text>
    <text x="15" y="82" fill="#60a5fa" font-family="monospace" font-size="12">UQ  id_event_provider : VARCHAR</text>
    <text x="15" y="104" fill="#38bdf8" font-family="monospace" font-size="12">FK  pembayaran_id : BIGINT</text>
    <text x="15" y="126" fill="#e5e7eb" font-family="monospace" font-size="12">    tipe_event : VARCHAR(100)</text>
    <text x="15" y="148" fill="#cbd5e1" font-family="monospace" font-size="11">    payload : JSONB</text>
    <text x="15" y="170" fill="#9ca3af" font-family="monospace" font-size="11">    diterima_pada : TIMESTAMPTZ</text>
    <text x="15" y="192" fill="#9ca3af" font-family="monospace" font-size="11">    diproses_pada : TIMESTAMPTZ</text>
    <text x="15" y="214" fill="#10b981" font-family="monospace" font-size="11">IDX (id_event_provider)</text>
  </g>

  <!-- 8. PESANAN (orders) -->
  <g transform="translate(370, 420)">
    <rect width="250" height="240" rx="8" fill="#111827" stroke="#3b82f6" stroke-width="1.8" filter="url(#shadow)"/>
    <rect width="250" height="36" rx="8" fill="#1e3a8a" />
    <text x="125" y="24" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">pesanan (orders)</text>
    <text x="15" y="60" fill="#f59e0b" font-family="monospace" font-size="12">PK  id : BIGSERIAL</text>
    <text x="15" y="82" fill="#60a5fa" font-family="monospace" font-size="12">UQ  nomor_pesanan : VARCHAR</text>
    <text x="15" y="104" fill="#38bdf8" font-family="monospace" font-size="12">FK  pengguna_id : BIGINT</text>
    <text x="15" y="126" fill="#e5e7eb" font-family="monospace" font-size="12">    total_harga : DECIMAL(12,2)</text>
    <text x="15" y="148" fill="#e5e7eb" font-family="monospace" font-size="12">    status : VARCHAR(50)</text>
    <text x="15" y="170" fill="#ef4444" font-family="monospace" font-size="11">    kedaluwarsa_pada : TIMESTZ</text>
    <text x="15" y="192" fill="#9ca3af" font-family="monospace" font-size="11">    dibuat_pada : TIMESTAMPTZ</text>
    <text x="15" y="214" fill="#9ca3af" font-family="monospace" font-size="11">    diperbarui_pada : TIMESTZ</text>
  </g>

  <!-- 6. JADWAL (schedules) -->
  <g transform="translate(670, 420)">
    <rect width="260" height="240" rx="8" fill="#111827" stroke="#f59e0b" stroke-width="2" filter="url(#shadow)"/>
    <rect width="260" height="36" rx="8" fill="#b45309" />
    <text x="130" y="24" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">jadwal (schedules)</text>
    <text x="15" y="60" fill="#f59e0b" font-family="monospace" font-size="12">PK  id : BIGSERIAL</text>
    <text x="15" y="82" fill="#38bdf8" font-family="monospace" font-size="12">FK  film_id : BIGINT</text>
    <text x="15" y="104" fill="#38bdf8" font-family="monospace" font-size="12">FK  studio_id : BIGINT</text>
    <text x="15" y="126" fill="#ef4444" font-family="monospace" font-size="12">IDX waktu_mulai : TIMESTAMPTZ</text>
    <text x="15" y="148" fill="#ef4444" font-family="monospace" font-size="12">IDX waktu_selesai : TIMESTAMPTZ</text>
    <text x="15" y="170" fill="#e5e7eb" font-family="monospace" font-size="12">    status : VARCHAR(50)</text>
    <text x="15" y="192" fill="#a7f3d0" font-family="monospace" font-size="11">CHK waktu_selesai &gt; mulai</text>
    <text x="15" y="214" fill="#fca5a5" font-family="monospace" font-size="11">EXC no_overlapping_schedule</text>
  </g>

  <!-- 7. KURSI JADWAL (show_seats) -->
  <g transform="translate(1050, 420)">
    <rect width="270" height="240" rx="8" fill="#111827" stroke="#ec4899" stroke-width="1.8" filter="url(#shadow)"/>
    <rect width="270" height="36" rx="8" fill="#be185d" />
    <text x="135" y="24" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">kursi_jadwal (show_seats)</text>
    <text x="15" y="60" fill="#f59e0b" font-family="monospace" font-size="12">PK  id : BIGSERIAL</text>
    <text x="15" y="82" fill="#38bdf8" font-family="monospace" font-size="12">FK  jadwal_id : BIGINT</text>
    <text x="15" y="104" fill="#38bdf8" font-family="monospace" font-size="12">FK  kursi_id : BIGINT</text>
    <text x="15" y="126" fill="#e5e7eb" font-family="monospace" font-size="12">    harga : DECIMAL(12,2)</text>
    <text x="15" y="148" fill="#ec4899" font-family="monospace" font-size="12">IDX status : VARCHAR(50)</text>
    <text x="15" y="170" fill="#38bdf8" font-family="monospace" font-size="12">FK  ditahan_oleh : BIGINT</text>
    <text x="15" y="192" fill="#e5e7eb" font-family="monospace" font-size="11">    ditahan_sampai : TIMESTZ</text>
    <text x="15" y="214" fill="#60a5fa" font-family="monospace" font-size="11">UQ  (jadwal_id, kursi_id)</text>
  </g>

  <!-- 9. ITEM PESANAN (order_items) -->
  <g transform="translate(720, 720)">
    <rect width="250" height="190" rx="8" fill="#111827" stroke="#6366f1" stroke-width="1.5" filter="url(#shadow)"/>
    <rect width="250" height="36" rx="8" fill="#4338ca" />
    <text x="125" y="24" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">item_pesanan (order_items)</text>
    <text x="15" y="60" fill="#f59e0b" font-family="monospace" font-size="12">PK  id : BIGSERIAL</text>
    <text x="15" y="82" fill="#38bdf8" font-family="monospace" font-size="12">FK  pesanan_id : BIGINT</text>
    <text x="15" y="104" fill="#38bdf8" font-family="monospace" font-size="12">FK  kursi_jadwal_id : BIGINT</text>
    <text x="15" y="126" fill="#e5e7eb" font-family="monospace" font-size="12">    harga : DECIMAL(12,2)</text>
    <text x="15" y="148" fill="#60a5fa" font-family="monospace" font-size="11">UQ  (pesanan, kursi_jadwal)</text>
    <text x="15" y="170" fill="#9ca3af" font-family="monospace" font-size="11">IDX (pesanan_id)</text>
  </g>

  <!-- 10. PEMBAYARAN (payments) -->
  <g transform="translate(370, 720)">
    <rect width="260" height="210" rx="8" fill="#111827" stroke="#10b981" stroke-width="1.5" filter="url(#shadow)"/>
    <rect width="260" height="36" rx="8" fill="#065f46" />
    <text x="130" y="24" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">pembayaran (payments)</text>
    <text x="15" y="60" fill="#f59e0b" font-family="monospace" font-size="12">PK  id : BIGSERIAL</text>
    <text x="15" y="82" fill="#38bdf8" font-family="monospace" font-size="12">FK  pesanan_id : BIGINT</text>
    <text x="15" y="104" fill="#60a5fa" font-family="monospace" font-size="12">UQ  referensi_pembayaran</text>
    <text x="15" y="126" fill="#e5e7eb" font-family="monospace" font-size="12">    metode_pembayaran</text>
    <text x="15" y="148" fill="#e5e7eb" font-family="monospace" font-size="12">    total_bayar : DECIMAL</text>
    <text x="15" y="170" fill="#e5e7eb" font-family="monospace" font-size="12">    status : VARCHAR(50)</text>
    <text x="15" y="192" fill="#9ca3af" font-family="monospace" font-size="11">    dibayar_pada : TIMESTAMPTZ</text>
  </g>

  <!-- 11. TIKET (tickets) -->
  <g transform="translate(1050, 720)">
    <rect width="260" height="190" rx="8" fill="#111827" stroke="#38bdf8" stroke-width="1.5" filter="url(#shadow)"/>
    <rect width="260" height="36" rx="8" fill="#0369a1" />
    <text x="130" y="24" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">tiket (tickets)</text>
    <text x="15" y="60" fill="#f59e0b" font-family="monospace" font-size="12">PK  id : BIGSERIAL</text>
    <text x="15" y="82" fill="#60a5fa" font-family="monospace" font-size="12">UQ  kode_tiket : VARCHAR(100)</text>
    <text x="15" y="104" fill="#38bdf8" font-family="monospace" font-size="12">FK  item_pesanan_id : BIGINT</text>
    <text x="15" y="126" fill="#e5e7eb" font-family="monospace" font-size="12">    status : VARCHAR(50)</text>
    <text x="15" y="148" fill="#9ca3af" font-family="monospace" font-size="11">    diterbitkan_pada : TIMESTZ</text>
    <text x="15" y="170" fill="#9ca3af" font-family="monospace" font-size="11">    dibatalkan_pada : TIMESTZ</text>
  </g>

  <!-- 12. PENGEMBALIAN DANA (refunds) -->
  <g transform="translate(60, 720)">
    <rect width="260" height="210" rx="8" fill="#111827" stroke="#ef4444" stroke-width="1.5" filter="url(#shadow)"/>
    <rect width="260" height="36" rx="8" fill="#991b1b" />
    <text x="130" y="24" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">pengembalian_dana (refunds)</text>
    <text x="15" y="60" fill="#f59e0b" font-family="monospace" font-size="12">PK  id : BIGSERIAL</text>
    <text x="15" y="82" fill="#38bdf8" font-family="monospace" font-size="12">FK  pembayaran_id : BIGINT</text>
    <text x="15" y="104" fill="#60a5fa" font-family="monospace" font-size="12">UQ  referensi_pengembalian</text>
    <text x="15" y="126" fill="#e5e7eb" font-family="monospace" font-size="12">    alasan : TEXT</text>
    <text x="15" y="148" fill="#e5e7eb" font-family="monospace" font-size="12">    total_kembali : DECIMAL</text>
    <text x="15" y="170" fill="#e5e7eb" font-family="monospace" font-size="12">    status : VARCHAR(50)</text>
    <text x="15" y="192" fill="#9ca3af" font-family="monospace" font-size="11">    diproses_pada : TIMESTAMPTZ</text>
  </g>

  <!-- 13. LOG AUDIT (audit_logs) -->
  <g transform="translate(1360, 720)">
    <rect width="270" height="210" rx="8" fill="#111827" stroke="#6b7280" stroke-width="1.5" filter="url(#shadow)"/>
    <rect width="270" height="36" rx="8" fill="#374151" />
    <text x="135" y="24" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">log_audit (audit_logs)</text>
    <text x="15" y="60" fill="#f59e0b" font-family="monospace" font-size="12">PK  id : BIGSERIAL</text>
    <text x="15" y="82" fill="#38bdf8" font-family="monospace" font-size="12">FK  pengguna_id : BIGINT</text>
    <text x="15" y="104" fill="#e5e7eb" font-family="monospace" font-size="12">    aksi : VARCHAR(100)</text>
    <text x="15" y="126" fill="#e5e7eb" font-family="monospace" font-size="12">    tipe_entitas : VARCHAR(100)</text>
    <text x="15" y="148" fill="#e5e7eb" font-family="monospace" font-size="12">    entitas_id : BIGINT</text>
    <text x="15" y="170" fill="#cbd5e1" font-family="monospace" font-size="11">    nilai_lama : JSONB</text>
    <text x="15" y="190" fill="#cbd5e1" font-family="monospace" font-size="11">    nilai_baru : JSONB</text>
  </g>

  <!-- RELATIONSHIP ARROWS / CONNECTORS -->
  <path d="M 610 240 L 670 240" stroke="#10b981" stroke-width="2" stroke-dasharray="4" />
  <path d="M 910 240 L 970 240" stroke="#10b981" stroke-width="2" stroke-dasharray="4" />
  <path d="M 790 360 L 790 420" stroke="#f59e0b" stroke-width="2" />
  <path d="M 1280 255 L 930 480" stroke="#8b5cf6" stroke-width="2" />
  <path d="M 930 535 L 1050 535" stroke="#ec4899" stroke-width="2" />
  <path d="M 1095 350 L 1095 420" stroke="#10b981" stroke-width="2" stroke-dasharray="4" />
  <path d="M 310 260 L 370 470" stroke="#3b82f6" stroke-width="2" />
  <path d="M 580 660 L 720 750" stroke="#3b82f6" stroke-width="2" />
  <path d="M 1100 660 L 970 750" stroke="#ec4899" stroke-width="2" />
  <path d="M 495 660 L 495 720" stroke="#10b981" stroke-width="2" />
  <path d="M 370 820 L 320 820" stroke="#ef4444" stroke-width="2" />
  <path d="M 190 660 L 370 770" stroke="#10b981" stroke-width="2" stroke-dasharray="4" />
  <path d="M 970 815 L 1050 815" stroke="#38bdf8" stroke-width="2" />

  <!-- Footnote -->
  <rect x="50" y="990" width="1600" height="150" rx="12" fill="#1e293b" stroke="#475569" stroke-width="1"/>
  <text x="80" y="1025" fill="#f8fafc" font-family="sans-serif" font-size="16" font-weight="bold">Key Integrity Guarantees &amp; Technical Solutions (14 Tables Normalized 3NF):</text>
  <text x="80" y="1052" fill="#cbd5e1" font-family="sans-serif" font-size="13">1. Anti Double-Booking: UNIQUE (jadwal_id, kursi_id) constraint on kursi_jadwal table + state machine (AVAILABLE → HELD → SOLD).</text>
  <text x="80" y="1075" fill="#cbd5e1" font-family="sans-serif" font-size="13">2. Dual-Layer Overlap Prevention: Application validation + PostgreSQL EXCLUDE USING gist (studio_id WITH =, tstzrange(mulai, selesai, '[)') WITH &amp;&amp;).</text>
  <text x="80" y="1098" fill="#cbd5e1" font-family="sans-serif" font-size="13">3. Idempotency &amp; Webhook Guard: event_pembayaran table with UNIQUE(id_event_provider) prevents duplicate payment webhook processing.</text>
  <text x="80" y="1121" fill="#cbd5e1" font-family="sans-serif" font-size="13">4. Restock vs Refund: Expiration returns seats to AVAILABLE; Cinema cancellation marks schedule CANCELLED &amp; show_seat INACTIVE, issuing 100% refund.</text>
</svg>'''
    with open('/tmp/database_erd.svg', 'w') as f:
        f.write(svg)



def create_flowchart_svg():
    width = 2400
    height = 1520
    
    svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Background Gradients -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#070b14" />
      <stop offset="50%" stop-color="#0d1527" />
      <stop offset="100%" stop-color="#0a101f" />
    </linearGradient>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#151f33" />
      <stop offset="100%" stop-color="#0e1726" />
    </linearGradient>
    <linearGradient id="primaryCardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#172544" />
      <stop offset="100%" stop-color="#0f1b33" />
    </linearGradient>
    <linearGradient id="amberCardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2a1e0a" />
      <stop offset="100%" stop-color="#181105" />
    </linearGradient>
    <linearGradient id="greenCardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0c291d" />
      <stop offset="100%" stop-color="#071911" />
    </linearGradient>
    <linearGradient id="redCardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2a1117" />
      <stop offset="100%" stop-color="#18080c" />
    </linearGradient>

    <!-- Filters -->
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="10" stdDeviation="8" flood-color="#000000" flood-opacity="0.6"/>
    </filter>

    <!-- Markers -->
    <marker id="arrowCyan" viewBox="0 0 12 12" refX="9" refY="6" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 1 1 L 11 6 L 1 11 z" fill="#38bdf8" />
    </marker>
    <marker id="arrowGreen" viewBox="0 0 12 12" refX="9" refY="6" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 1 1 L 11 6 L 1 11 z" fill="#10b981" />
    </marker>
    <marker id="arrowAmber" viewBox="0 0 12 12" refX="9" refY="6" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 1 1 L 11 6 L 1 11 z" fill="#f59e0b" />
    </marker>
    <marker id="arrowRed" viewBox="0 0 12 12" refX="9" refY="6" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 1 1 L 11 6 L 1 11 z" fill="#f87171" />
    </marker>

    <!-- Background Pattern -->
    <pattern id="dotGrid" width="36" height="36" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.2" fill="#334155" opacity="0.35"/>
    </pattern>
  </defs>

  <!-- Background Base -->
  <rect width="{width}" height="{height}" fill="url(#bgGrad)" />
  <rect width="{width}" height="{height}" fill="url(#dotGrid)" />

  <!-- ==================== HEADER BANNER ==================== -->
  <rect x="70" y="40" width="2260" height="110" rx="18" fill="url(#cardGrad)" stroke="#38bdf8" stroke-width="1.8" filter="url(#shadow)"/>
  
  <!-- Icon & Header Text -->
  <g transform="translate(95, 60)">
    <rect width="70" height="70" rx="14" fill="#0284c7" fill-opacity="0.25" stroke="#38bdf8" stroke-width="1.5"/>
    <!-- Film Reel & Ticket Vector Icon -->
    <rect x="14" y="20" width="42" height="30" rx="4" fill="none" stroke="#38bdf8" stroke-width="2.2" />
    <line x1="28" y1="20" x2="28" y2="50" stroke="#38bdf8" stroke-width="1.8" stroke-dasharray="3 3" />
    <circle cx="21" cy="35" r="3.5" fill="#38bdf8" />
    <circle cx="35" cy="35" r="3.5" fill="#38bdf8" />
    <circle cx="21" cy="14" r="2.5" fill="#38bdf8" />
    <circle cx="35" cy="14" r="2.5" fill="#38bdf8" />
    <circle cx="49" cy="14" r="2.5" fill="#38bdf8" />
  </g>
  
  <text x="185" y="83" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="28" font-weight="800" letter-spacing="0.5">ALUR TRANSAKSI &amp; LOGIKA BISNIS PEMESANAN TIKET BIOSKOP</text>
  <text x="185" y="115" fill="#94a3b8" font-family="'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="500">Panduan Big Picture untuk Klien &amp; Pengguna • Proses Booking, Penguncian Kursi 10 Menit, Restok Otomatis &amp; Garansi Refund 100%</text>

  <!-- Header Badges -->
  <g transform="translate(1600, 68)">
    <rect x="0" y="0" width="190" height="42" rx="21" fill="#0284c7" fill-opacity="0.2" stroke="#38bdf8" stroke-width="1.2"/>
    <text x="95" y="26" fill="#38bdf8" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" text-anchor="middle">Anti Double-Booking</text>

    <rect x="205" y="0" width="175" height="42" rx="21" fill="#b45309" fill-opacity="0.2" stroke="#f59e0b" stroke-width="1.2"/>
    <text x="292" y="26" fill="#f59e0b" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" text-anchor="middle">Kunci Kursi 10 Menit</text>

    <rect x="395" y="0" width="190" height="42" rx="21" fill="#065f46" fill-opacity="0.2" stroke="#10b981" stroke-width="1.2"/>
    <text x="490" y="26" fill="#34d399" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" text-anchor="middle">Garansi 100% Refund</text>
  </g>


  <!-- ==================== BAGIAN 1: ALUR UTAMA (HAPPY PATH) ==================== -->
  <rect x="70" y="175" width="2260" height="525" rx="20" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5" filter="url(#shadow)"/>
  
  <!-- Section Title Bar -->
  <rect x="70" y="175" width="2260" height="54" rx="20" fill="#1e293b" />
  <rect x="70" y="210" width="2260" height="19" fill="#1e293b" />
  <circle cx="105" cy="202" r="10" fill="#38bdf8" />
  <text x="128" y="208" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="17" font-weight="800">ALUR UTAMA (HAPPY PATH): 5 LANGKAH DARI MEMILIH FILM HINGGA MENERIMA TIKET RESMI</text>
  <text x="2150" y="208" fill="#38bdf8" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="700">Langkah 1 s/d 5</text>

  <!-- 5 Horizontal Step Cards -->
  <!-- Card 1: Pilih Film & Jadwal -->
  <g transform="translate(100, 255)">
    <rect width="390" height="235" rx="16" fill="url(#primaryCardGrad)" stroke="#38bdf8" stroke-width="1.5" />
    <g transform="translate(20, 20)">
      <rect width="46" height="46" rx="12" fill="#0284c7" />
      <text x="23" y="32" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="900" text-anchor="middle">1</text>
    </g>
    <text x="80" y="44" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="19" font-weight="800">Pilih Film &amp; Jadwal</text>
    <text x="80" y="65" fill="#38bdf8" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="600">Movie &amp; Screening Selection</text>

    <line x1="20" y1="82" x2="370" y2="82" stroke="#334155" stroke-width="1" />

    <text x="25" y="112" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="500">• Buka Aplikasi atau Website Bioskop</text>
    <text x="25" y="137" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="500">• Pilih Kota &amp; Cabang Bioskop Terdekat</text>
    <text x="25" y="162" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="500">• Tentukan Tanggal &amp; Jam Penayangan</text>

    <rect x="20" y="185" width="350" height="34" rx="8" fill="#0f172a" stroke="#1e293b" />
    <text x="195" y="207" fill="#38bdf8" font-family="'Segoe UI', Roboto, sans-serif" font-size="12.5" font-weight="700" text-anchor="middle">Jadwal &amp; Jam Tayang Terupdate Real-Time</text>
  </g>

  <!-- Arrow 1 -> 2 -->
  <line x1="500" y1="372" x2="538" y2="372" stroke="#38bdf8" stroke-width="3" marker-end="url(#arrowCyan)" />

  <!-- Card 2: Pilih Kursi di Denah -->
  <g transform="translate(545, 255)">
    <rect width="390" height="235" rx="16" fill="url(#primaryCardGrad)" stroke="#38bdf8" stroke-width="1.5" />
    <g transform="translate(20, 20)">
      <rect width="46" height="46" rx="12" fill="#0284c7" />
      <text x="23" y="32" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="900" text-anchor="middle">2</text>
    </g>
    <text x="80" y="44" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="19" font-weight="800">Pilih Kursi (Seatmap)</text>
    <text x="80" y="65" fill="#38bdf8" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="600">Interactive Seat Selection</text>

    <line x1="20" y1="82" x2="370" y2="82" stroke="#334155" stroke-width="1" />

    <text x="25" y="112" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="500">• Denah studio interaktif terbuka di layar</text>
    <text x="25" y="137" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="500">• <tspan fill="#34d399" font-weight="700">Warna HIJAU</tspan> : Kursi kosong &amp; bebas dipilih</text>
    <text x="25" y="162" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="500">• <tspan fill="#94a3b8" font-weight="700">Warna ABU-ABU</tspan> : Sudah terisi / terjual</text>

    <rect x="20" y="185" width="350" height="34" rx="8" fill="#0f172a" stroke="#1e293b" />
    <text x="195" y="207" fill="#38bdf8" font-family="'Segoe UI', Roboto, sans-serif" font-size="12.5" font-weight="700" text-anchor="middle">Langsung Klik Kursi Favorit Anda</text>
  </g>

  <!-- Arrow 2 -> 3 -->
  <line x1="945" y1="372" x2="983" y2="372" stroke="#38bdf8" stroke-width="3" marker-end="url(#arrowCyan)" />

  <!-- Card 3: Kunci Kursi 10 Menit (FEATURED) -->
  <g transform="translate(990, 255)">
    <rect width="400" height="235" rx="16" fill="url(#amberCardGrad)" stroke="#f59e0b" stroke-width="2.5" filter="url(#shadow)"/>
    <g transform="translate(20, 20)">
      <rect width="46" height="46" rx="12" fill="#d97706" />
      <text x="23" y="32" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="900" text-anchor="middle">3</text>
    </g>
    <text x="80" y="44" fill="#fde68a" font-family="'Segoe UI', Roboto, sans-serif" font-size="19" font-weight="800">Kunci Kursi (10 Menit)</text>
    <text x="80" y="65" fill="#f59e0b" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700">Temporary Seat Hold (Anti-Rebutan)</text>

    <line x1="20" y1="82" x2="380" y2="82" stroke="#78350f" stroke-width="1.2" />

    <text x="25" y="112" fill="#fef3c7" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="600">• Kursi berubah jadi <tspan fill="#f59e0b" font-weight="800">KUNING (HELD)</tspan></text>
    <text x="25" y="137" fill="#fef3c7" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="600">• Orang lain <tspan fill="#ef4444" font-weight="800">TIDAK BISA</tspan> memilih kursi ini</text>
    <text x="25" y="162" fill="#fef3c7" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="600">• Timer hitung mundur 10 menit aktif</text>

    <rect x="20" y="185" width="360" height="34" rx="8" fill="#1c1917" stroke="#78350f" />
    <text x="200" y="207" fill="#fbbf24" font-family="'Segoe UI', Roboto, sans-serif" font-size="12.5" font-weight="800" text-anchor="middle">Garansi Anti Double-Booking: Aman 100%</text>
  </g>

  <!-- Arrow 3 -> 4 -->
  <line x1="1400" y1="372" x2="1438" y2="372" stroke="#f59e0b" stroke-width="3" marker-end="url(#arrowAmber)" />

  <!-- Card 4: Pembayaran Online -->
  <g transform="translate(1445, 255)">
    <rect width="390" height="235" rx="16" fill="url(#primaryCardGrad)" stroke="#38bdf8" stroke-width="1.5" />
    <g transform="translate(20, 20)">
      <rect width="46" height="46" rx="12" fill="#0284c7" />
      <text x="23" y="32" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="900" text-anchor="middle">4</text>
    </g>
    <text x="80" y="44" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="19" font-weight="800">Pembayaran Online</text>
    <text x="80" y="65" fill="#38bdf8" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="600">Fast &amp; Secure Checkout</text>

    <line x1="20" y1="82" x2="370" y2="82" stroke="#334155" stroke-width="1" />

    <text x="25" y="112" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="500">• Bayar via QRIS (BCA, Mandiri, BRI, dll)</text>
    <text x="25" y="137" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="500">• E-Wallet (GoPay, OVO, Dana, ShopeePay)</text>
    <text x="25" y="162" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="500">• Virtual Account &amp; Kartu Kredit</text>

    <rect x="20" y="185" width="350" height="34" rx="8" fill="#0f172a" stroke="#1e293b" />
    <text x="195" y="207" fill="#38bdf8" font-family="'Segoe UI', Roboto, sans-serif" font-size="12.5" font-weight="700" text-anchor="middle">Konfirmasi Pembayaran Otomatis</text>
  </g>

  <!-- Arrow 4 -> 5 with Decision Badge -->
  <line x1="1845" y1="372" x2="1883" y2="372" stroke="#10b981" stroke-width="3" marker-end="url(#arrowGreen)" />
  <rect x="1836" y="328" width="56" height="24" rx="6" fill="#065f46" stroke="#10b981" stroke-width="1"/>
  <text x="1864" y="344" fill="#a7f3d0" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" font-weight="800" text-anchor="middle">LUNAS</text>

  <!-- Card 5: Tiket Resmi Terbit (SUCCESS) -->
  <g transform="translate(1890, 255)">
    <rect width="400" height="235" rx="16" fill="url(#greenCardGrad)" stroke="#10b981" stroke-width="2.5" filter="url(#shadow)"/>
    <g transform="translate(20, 20)">
      <rect width="46" height="46" rx="12" fill="#059669" />
      <text x="23" y="32" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="900" text-anchor="middle">5</text>
    </g>
    <text x="80" y="44" fill="#a7f3d0" font-family="'Segoe UI', Roboto, sans-serif" font-size="19" font-weight="800">Tiket Terbit (LUNAS)</text>
    <text x="80" y="65" fill="#34d399" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700">Official E-Ticket &amp; QR Code</text>

    <line x1="20" y1="82" x2="380" y2="82" stroke="#065f46" stroke-width="1.2" />

    <text x="25" y="112" fill="#d1fae5" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="600">• Status kursi resmi menjadi <tspan fill="#34d399" font-weight="800">SOLD</tspan></text>
    <text x="25" y="137" fill="#d1fae5" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="600">• Terbit E-Ticket dengan Barcode / QR Code</text>
    <text x="25" y="162" fill="#d1fae5" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="600">• Dikirim langsung ke WhatsApp &amp; Email</text>

    <rect x="20" y="185" width="360" height="34" rx="8" fill="#064e3b" stroke="#059669" />
    <text x="200" y="207" fill="#6ee7b7" font-family="'Segoe UI', Roboto, sans-serif" font-size="12.5" font-weight="800" text-anchor="middle">Scan QR di Pintu Masuk Bioskop</text>
  </g>

  <!-- Big Picture Explanation Banner below Step Cards -->
  <g transform="translate(100, 515)">
    <rect width="2190" height="155" rx="14" fill="#0b1324" stroke="#334155" stroke-width="1.2" />
    
    <g transform="translate(25, 20)">
      <rect width="40" height="40" rx="10" fill="#38bdf8" fill-opacity="0.15" stroke="#38bdf8" stroke-width="1.2"/>
      <circle cx="20" cy="20" r="10" fill="none" stroke="#38bdf8" stroke-width="2" />
      <text x="20" y="25" fill="#38bdf8" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="800" text-anchor="middle">i</text>
    </g>
    <text x="78" y="46" fill="#f8fafc" font-family="'Segoe UI', Roboto, sans-serif" font-size="16.5" font-weight="800">KEPASTIAN &amp; KENYAMANAN BISNIS BAGI PENGGUNA &amp; MANAJEMEN BIOSKOP:</text>
    
    <g transform="translate(30, 78)">
      <circle cx="8" cy="8" r="5" fill="#38bdf8" />
      <text x="24" y="13" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="14.5" font-weight="500"><tspan fill="#ffffff" font-weight="700">Waktu Eksklusif 10 Menit:</tspan> Pelanggan memiliki waktu tenang 10 menit untuk menyelesaikan pembayaran tanpa khawatir kursi diserobot orang lain.</text>
      
      <circle cx="8" cy="40" r="5" fill="#10b981" />
      <text x="24" y="45" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="14.5" font-weight="500"><tspan fill="#ffffff" font-weight="700">Kepastian Transaksi 100%:</tspan> Saat pembayaran berhasil terverifikasi, kursi seketika sah menjadi hak milik pembeli dan kode QR tiket dapat langsung dipakai.</text>
    </g>

    <!-- Visual Status Flow Badge on Right -->
    <g transform="translate(1690, 30)">
      <rect width="470" height="98" rx="10" fill="#111c33" stroke="#1e293b" />
      <text x="235" y="28" fill="#94a3b8" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" text-anchor="middle">TRANSISI STATUS KURSI (HAPPY PATH)</text>
      <g transform="translate(35, 45)">
        <rect x="0" y="0" width="105" height="34" rx="6" fill="#065f46" stroke="#10b981" stroke-width="1.2"/>
        <text x="52" y="22" fill="#34d399" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="800" text-anchor="middle">AVAILABLE</text>

        <text x="122" y="23" fill="#38bdf8" font-family="'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="900">→</text>

        <rect x="140" y="0" width="115" height="34" rx="6" fill="#78350f" stroke="#f59e0b" stroke-width="1.2"/>
        <text x="197" y="22" fill="#fde68a" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="800" text-anchor="middle">HELD (10 Mnt)</text>

        <text x="272" y="23" fill="#38bdf8" font-family="'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="900">→</text>

        <rect x="290" y="0" width="105" height="34" rx="6" fill="#1e293b" stroke="#10b981" stroke-width="1.8"/>
        <text x="342" y="22" fill="#a7f3d0" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="800" text-anchor="middle">SOLD (Sah)</text>
      </g>
    </g>
  </g>


  <!-- ==================== BAGIAN 2: DUA SKENARIO PENGAMAN (EXCEPTION & GUARANTEES) ==================== -->
  
  <!-- KIRI: SKENARIO 1 - AUTO-RESTOCK (JIKA BATAL / TELAT BAYAR) -->
  <g transform="translate(70, 725)">
    <rect width="1110" height="490" rx="20" fill="url(#cardGrad)" stroke="#f59e0b" stroke-width="1.8" filter="url(#shadow)"/>
    
    <!-- Title Bar -->
    <rect width="1110" height="52" rx="20" fill="#78350f" fill-opacity="0.6" />
    <rect y="30" width="1110" height="22" fill="#78350f" fill-opacity="0.6" />
    <circle cx="35" cy="26" r="10" fill="#f59e0b" />
    <text x="56" y="32" fill="#fef3c7" font-family="'Segoe UI', Roboto, sans-serif" font-size="17" font-weight="800">SKENARIO 1: AUTO-RESTOCK (BATAS WAKTU 10 MENIT HABIS / PESANAN BATAL)</text>

    <!-- Branch Indicator Badge -->
    <rect x="860" y="14" width="220" height="26" rx="6" fill="#b45309" />
    <text x="970" y="31" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" text-anchor="middle">Jalur Jika Pembayaran Gagal</text>

    <!-- Situation Box -->
    <rect x="35" y="75" width="1040" height="60" rx="10" fill="#1c1917" stroke="#b45309" stroke-width="1" />
    <text x="55" y="100" fill="#fde68a" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="700">Kondisi Pemicu:</text>
    <text x="175" y="100" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="14">Pelanggan tidak menyelesaikan pembayaran dalam 10 menit, sinyal terputus, atau menutup aplikasi sebelum bayar.</text>
    <text x="55" y="122" fill="#94a3b8" font-family="'Segoe UI', Roboto, sans-serif" font-size="13">Status pesanan otomatis dinyatakan kedaluwarsa (EXPIRED) tanpa memotong biaya apapun dari pelanggan.</text>

    <!-- 3 Simple Flow Steps -->
    <g transform="translate(35, 155)">
      <!-- Step A -->
      <rect x="0" y="0" width="320" height="190" rx="12" fill="#131b2e" stroke="#334155" />
      <circle cx="30" cy="30" r="14" fill="#f59e0b" fill-opacity="0.2" stroke="#f59e0b" />
      <text x="30" y="36" fill="#f59e0b" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="800" text-anchor="middle">A</text>
      <text x="55" y="35" fill="#f8fafc" font-family="'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="700">Waktu 10 Menit Habis</text>
      
      <line x1="15" y1="58" x2="305" y2="58" stroke="#1e293b" />
      <text x="15" y="85" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Sistem mendeteksi pesanan</text>
      <text x="15" y="107" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">  telah melewati batas waktu.</text>
      <text x="15" y="132" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Pembayaran belum diterima</text>
      <text x="15" y="154" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">  dari penyedia pembayaran.</text>

      <rect x="15" y="162" width="290" height="22" rx="4" fill="#1c1917" />
      <text x="160" y="177" fill="#f59e0b" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="700" text-anchor="middle">Order Status: EXPIRED</text>

      <!-- Arrow A -> B -->
      <line x1="330" y1="95" x2="350" y2="95" stroke="#f59e0b" stroke-width="2.5" marker-end="url(#arrowAmber)" />

      <!-- Step B -->
      <g transform="translate(360, 0)">
        <rect width="320" height="190" rx="12" fill="#131b2e" stroke="#334155" />
        <circle cx="30" cy="30" r="14" fill="#f59e0b" fill-opacity="0.2" stroke="#f59e0b" />
        <text x="30" y="36" fill="#f59e0b" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="800" text-anchor="middle">B</text>
        <text x="55" y="35" fill="#f8fafc" font-family="'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="700">Kunci Kursi Terlepas</text>
        
        <line x1="15" y1="58" x2="305" y2="58" stroke="#1e293b" />
        <text x="15" y="85" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Robot sistem otomatis</text>
        <text x="15" y="107" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">  membuka gembok kunci kursi.</text>
        <text x="15" y="132" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Tanpa perlu intervensi staf</text>
        <text x="15" y="154" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">  atau admin operasional.</text>

        <rect x="15" y="162" width="290" height="22" rx="4" fill="#1c1917" />
        <text x="160" y="177" fill="#38bdf8" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="700" text-anchor="middle">Proses Otomatis &lt; 1 Detik</text>
      </g>

      <!-- Arrow B -> C -->
      <line x1="690" y1="95" x2="710" y2="95" stroke="#10b981" stroke-width="2.5" marker-end="url(#arrowGreen)" />

      <!-- Step C -->
      <g transform="translate(720, 0)">
        <rect width="320" height="190" rx="12" fill="url(#greenCardGrad)" stroke="#10b981" stroke-width="1.8" />
        <circle cx="30" cy="30" r="14" fill="#059669" />
        <text x="30" y="36" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="800" text-anchor="middle">C</text>
        <text x="55" y="35" fill="#a7f3d0" font-family="'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="700">Kursi Kembali Hijau</text>
        
        <line x1="15" y1="58" x2="305" y2="58" stroke="#065f46" />
        <text x="15" y="85" fill="#d1fae5" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Denah bioskop terupdate</text>
        <text x="15" y="107" fill="#d1fae5" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">  seketika menjadi HIJAU.</text>
        <text x="15" y="132" fill="#d1fae5" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Pelanggan lain di seluruh</text>
        <text x="15" y="154" fill="#d1fae5" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">  Indonesia siap membelinya.</text>

        <rect x="15" y="162" width="290" height="22" rx="4" fill="#064e3b" />
        <text x="160" y="177" fill="#6ee7b7" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="800" text-anchor="middle">Status: AVAILABLE Kembali</text>
      </g>
    </g>

    <!-- Bottom Benefit Card -->
    <rect x="35" y="370" width="1040" height="95" rx="12" fill="#141824" stroke="#334155" />
    <text x="60" y="402" fill="#38bdf8" font-family="'Segoe UI', Roboto, sans-serif" font-size="15" font-weight="800">NILAI BISNIS UNTUK MANAJEMEN BIOSKOP:</text>
    <text x="60" y="426" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5"><tspan fill="#f59e0b" font-weight="700">Zero Inventory Waste (Nol Kursi Mubazir):</tspan> Tidak ada kursi bioskop yang tertahan sia-sia jika calon penonton batal beli.</text>
    <text x="60" y="448" fill="#94a3b8" font-family="'Segoe UI', Roboto, sans-serif" font-size="13">Kursi langsung terdistribusi kembali ke pasar, memaksimalkan okupansi studio dan potensi pendapatan bioskop.</text>
  </g>


  <!-- KANAN: SKENARIO 2 - PEMBATALAN OLEH BIOSKOP (GARANSI 100% REFUND) -->
  <g transform="translate(1220, 725)">
    <rect width="1110" height="490" rx="20" fill="url(#cardGrad)" stroke="#ef4444" stroke-width="1.8" filter="url(#shadow)"/>
    
    <!-- Title Bar -->
    <rect width="1110" height="52" rx="20" fill="#7f1d1d" fill-opacity="0.6" />
    <rect y="30" width="1110" height="22" fill="#7f1d1d" fill-opacity="0.6" />
    <circle cx="35" cy="26" r="10" fill="#ef4444" />
    <text x="56" y="32" fill="#fee2e2" font-family="'Segoe UI', Roboto, sans-serif" font-size="17" font-weight="800">SKENARIO 2: KENDALA OPERASIONAL BIOSKOP (GARANSI PENGEMBALIAN DANA 100%)</text>

    <!-- Branch Indicator Badge -->
    <rect x="860" y="14" width="220" height="26" rx="6" fill="#991b1b" />
    <text x="970" y="31" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" text-anchor="middle">Jalur Jika Bioskop Batalkan</text>

    <!-- Situation Box -->
    <rect x="35" y="75" width="1040" height="60" rx="10" fill="#1f1113" stroke="#991b1b" stroke-width="1" />
    <text x="55" y="100" fill="#fca5a5" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="700">Kondisi Pemicu:</text>
    <text x="175" y="100" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="14">Kendala teknis tak terduga (proyektor studio rusak mendadak, mati listrik total, izin film dicabut, bencana alam).</text>
    <text x="55" y="122" fill="#94a3b8" font-family="'Segoe UI', Roboto, sans-serif" font-size="13">Manajer Bioskop menekan tombol "Batalkan Jadwal" pada Portal Admin untuk melindungi kenyamanan penonton.</text>

    <!-- 3 Simple Flow Steps -->
    <g transform="translate(35, 155)">
      <!-- Step A -->
      <rect x="0" y="0" width="320" height="190" rx="12" fill="#131b2e" stroke="#334155" />
      <circle cx="30" cy="30" r="14" fill="#ef4444" fill-opacity="0.2" stroke="#ef4444" />
      <text x="30" y="36" fill="#f87171" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="800" text-anchor="middle">A</text>
      <text x="55" y="35" fill="#f8fafc" font-family="'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="700">Jadwal Dibatalkan</text>
      
      <line x1="15" y1="58" x2="305" y2="58" stroke="#1e293b" />
      <text x="15" y="85" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Manajer bioskop mengubah</text>
      <text x="15" y="107" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">  status jadwal: CANCELLED.</text>
      <text x="15" y="132" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Semua tiket jadwal tersebut</text>
      <text x="15" y="154" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">  otomatis dinonaktifkan.</text>

      <rect x="15" y="162" width="290" height="22" rx="4" fill="#1f1113" />
      <text x="160" y="177" fill="#f87171" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="700" text-anchor="middle">Jadwal Ditutup Otomatis</text>

      <!-- Arrow A -> B -->
      <line x1="330" y1="95" x2="350" y2="95" stroke="#ef4444" stroke-width="2.5" marker-end="url(#arrowRed)" />

      <!-- Step B -->
      <g transform="translate(360, 0)">
        <rect width="320" height="190" rx="12" fill="#131b2e" stroke="#334155" />
        <circle cx="30" cy="30" r="14" fill="#ef4444" fill-opacity="0.2" stroke="#ef4444" />
        <text x="30" y="36" fill="#f87171" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="800" text-anchor="middle">B</text>
        <text x="55" y="35" fill="#f8fafc" font-family="'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="700">Refund 100% Otomatis</text>
        
        <line x1="15" y1="58" x2="305" y2="58" stroke="#1e293b" />
        <text x="15" y="85" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Robot sistem memicu proses</text>
        <text x="15" y="107" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">  pengembalian dana serentak.</text>
        <text x="15" y="132" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Uang kembali 100% penuh</text>
        <text x="15" y="154" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">  tanpa potongan biaya admin.</text>

        <rect x="15" y="162" width="290" height="22" rx="4" fill="#1f1113" />
        <text x="160" y="177" fill="#38bdf8" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="700" text-anchor="middle">Transfer Balik ke Sumber Dana</text>
      </g>

      <!-- Arrow B -> C -->
      <line x1="690" y1="95" x2="710" y2="95" stroke="#10b981" stroke-width="2.5" marker-end="url(#arrowGreen)" />

      <!-- Step C -->
      <g transform="translate(720, 0)">
        <rect width="320" height="190" rx="12" fill="url(#greenCardGrad)" stroke="#10b981" stroke-width="1.8" />
        <circle cx="30" cy="30" r="14" fill="#059669" />
        <text x="30" y="36" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="800" text-anchor="middle">C</text>
        <text x="55" y="35" fill="#a7f3d0" font-family="'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="700">Notifikasi WA &amp; Bukti</text>
        
        <line x1="15" y1="58" x2="305" y2="58" stroke="#065f46" />
        <text x="15" y="85" fill="#d1fae5" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Pesan permohonan maaf &amp;</text>
        <text x="15" y="107" fill="#d1fae5" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">  struk refund terkirim instan.</text>
        <text x="15" y="132" fill="#d1fae5" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">• Dikirim langsung ke nomor</text>
        <text x="15" y="154" fill="#d1fae5" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">  WhatsApp &amp; Email pelanggan.</text>

        <rect x="15" y="162" width="290" height="22" rx="4" fill="#064e3b" />
        <text x="160" y="177" fill="#6ee7b7" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="800" text-anchor="middle">Status: 100% REFUNDED</text>
      </g>
    </g>

    <!-- Bottom Benefit Card -->
    <rect x="35" y="370" width="1040" height="95" rx="12" fill="#141824" stroke="#334155" />
    <text x="60" y="402" fill="#10b981" font-family="'Segoe UI', Roboto, sans-serif" font-size="15" font-weight="800">PERLINDUNGAN KONSUMEN &amp; REPUTASI BIOSKOP:</text>
    <text x="60" y="426" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5"><tspan fill="#34d399" font-weight="700">Kepuasan &amp; Kepercayaan Pelanggan Terjamin:</tspan> Pelanggan tidak perlu antre atau mengajukan klaim manual yang merepotkan.</text>
    <text x="60" y="448" fill="#94a3b8" font-family="'Segoe UI', Roboto, sans-serif" font-size="13">Seluruh alur refund tercatat transparan di audit log keuangan dan mematuhi standar perlindungan konsumen.</text>
  </g>


  <!-- ==================== BAGIAN 3: RINGKASAN STATUS DENAH & KEUNGGULAN (BOTTOM ROW) ==================== -->
  <g transform="translate(70, 1235)">
    <rect width="2260" height="245" rx="18" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5" filter="url(#shadow)"/>
    
    <!-- Title Bar -->
    <rect width="2260" height="44" rx="18" fill="#1e293b" />
    <rect y="24" width="2260" height="20" fill="#1e293b" />
    <text x="35" y="28" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="800">LEGENDA ARTI WARNA KURSI &amp; TIGA JAMINAN UTAMA BAGI PENGGUNA &amp; KLIEN</text>

    <!-- 4 Seat Status Cards -->
    <g transform="translate(35, 65)">
      <!-- Status 1: Available -->
      <g transform="translate(0, 0)">
        <rect width="265" height="150" rx="12" fill="#0b1b16" stroke="#10b981" stroke-width="1.5" />
        <rect x="18" y="16" width="34" height="34" rx="8" fill="#059669" />
        <circle cx="35" cy="33" r="8" fill="#a7f3d0" />
        <text x="62" y="32" fill="#a7f3d0" font-family="'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="800">HIJAU</text>
        <text x="62" y="48" fill="#34d399" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700">Tersedia (Available)</text>
        
        <text x="18" y="80" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13">Kursi kosong dalam studio.</text>
        <text x="18" y="100" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13">Bebas dipilih langsung oleh</text>
        <text x="18" y="120" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13">siapapun di layar aplikasi.</text>
      </g>

      <!-- Status 2: Held -->
      <g transform="translate(285, 0)">
        <rect width="265" height="150" rx="12" fill="#1f180d" stroke="#f59e0b" stroke-width="1.5" />
        <rect x="18" y="16" width="34" height="34" rx="8" fill="#d97706" />
        <circle cx="35" cy="33" r="8" fill="#fef3c7" />
        <text x="62" y="32" fill="#fde68a" font-family="'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="800">KUNING</text>
        <text x="62" y="48" fill="#f59e0b" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700">Terkunci (Held 10 Menit)</text>
        
        <text x="18" y="80" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13">Sedang proses checkout.</text>
        <text x="18" y="100" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13">Aman dari rebutan orang lain</text>
        <text x="18" y="120" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13">selama jendela 10 menit.</text>
      </g>

      <!-- Status 3: Sold -->
      <g transform="translate(570, 0)">
        <rect width="265" height="150" rx="12" fill="#131b2e" stroke="#64748b" stroke-width="1.5" />
        <rect x="18" y="16" width="34" height="34" rx="8" fill="#334155" />
        <circle cx="35" cy="33" r="8" fill="#94a3b8" />
        <text x="62" y="32" fill="#f1f5f9" font-family="'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="800">ABU-ABU</text>
        <text x="62" y="48" fill="#94a3b8" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700">Terjual (Sold)</text>
        
        <text x="18" y="80" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13">Pembayaran telah lunas.</text>
        <text x="18" y="100" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13">Tiket resmi telah terbit</text>
        <text x="18" y="120" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13">dan kursi siap diduduki.</text>
      </g>

      <!-- Status 4: Refund -->
      <g transform="translate(855, 0)">
        <rect width="265" height="150" rx="12" fill="#1f1113" stroke="#ef4444" stroke-width="1.5" />
        <rect x="18" y="16" width="34" height="34" rx="8" fill="#b91c1c" />
        <circle cx="35" cy="33" r="8" fill="#fee2e2" />
        <text x="62" y="32" fill="#fca5a5" font-family="'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="800">MERAH</text>
        <text x="62" y="48" fill="#f87171" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700">Refund / Batal Tayang</text>
        
        <text x="18" y="80" fill="#e2e8f0" font-family="'Segoe UI', Roboto, sans-serif" font-size="13">Jadwal bioskop dibatalkan.</text>
        <text x="18" y="100" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13">Dana pelanggan 100% telah</text>
        <text x="18" y="120" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13">dikembalikan ke rekening.</text>
      </g>
    </g>

    <!-- Right Side: 3 Big Guarantees for Client -->
    <g transform="translate(1190, 65)">
      <rect width="1035" height="150" rx="12" fill="#0b1324" stroke="#334155" />
      <text x="25" y="30" fill="#f8fafc" font-family="'Segoe UI', Roboto, sans-serif" font-size="15" font-weight="800">3 PRINSIP LOGIKA BISNIS UTAMA YANG DIRANCANG UNTUK KEPUASAN PENGGUNA &amp; KLIEN:</text>

      <g transform="translate(25, 42)">
        <circle cx="8" cy="14" r="6" fill="#38bdf8" />
        <text x="24" y="18" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5" font-weight="700">1. Tanpa Drama Kursi Ganda (Zero Double-Booking): <tspan fill="#cbd5e1" font-weight="400">Penguncian seketika di tingkat server memastikan</tspan></text>
        <text x="24" y="36" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">dua pengguna tidak akan pernah bisa memesan nomor kursi yang sama di detik yang bersamaan.</text>

        <circle cx="8" cy="56" r="6" fill="#f59e0b" />
        <text x="24" y="60" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5" font-weight="700">2. Sirkulasi Kursi Cerdas (Smart Restock): <tspan fill="#cbd5e1" font-weight="400">Jika pembeli urung membayar, sistem otomatis mengembalikan tiket ke</tspan></text>
        <text x="24" y="78" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">denah aplikasi secara instan sehingga pihak bioskop tidak kehilangan potensi pendapatan.</text>

        <circle cx="8" cy="98" r="6" fill="#10b981" />
        <text x="24" y="102" fill="#ffffff" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5" font-weight="700">3. Layanan Terpercaya Tanpa Ribet (Zero Friction Refund): <tspan fill="#cbd5e1" font-weight="400">Jika bioskop mengalami force majeure, dana penonton</tspan></text>
        <text x="24" y="120" fill="#cbd5e1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5">dikembalikan utuh 100% secara otomatis ke rekening atau e-wallet tanpa proses klaim manual.</text>
      </g>
    </g>
  </g>

</svg>'''
    with open('/tmp/flowchart.svg', 'w') as f:
        f.write(svg)



if __name__ == '__main__':
    create_topology_svg()
    create_database_erd_svg()
    create_flowchart_svg()
    print("All 3 SVGs created successfully")

    import os
    import shutil
    os.makedirs("docs", exist_ok=True)
    os.makedirs("docs/tes_mkp", exist_ok=True)

    # Convert SVGs to JPG using ImageMagick
    subprocess.run(["magick", "-density", "150", "/tmp/system_topology.svg", "docs/system-topology.jpg"], check=True)
    subprocess.run(["magick", "-density", "150", "/tmp/database_erd.svg", "docs/database-erd.jpg"], check=True)
    subprocess.run(["magick", "-density", "150", "/tmp/flowchart.svg", "docs/flowchart-pemesanan.jpg"], check=True)
    print("All 3 JPGs converted and saved to docs/ successfully")

    # Sync to docs/tes_mkp/
    shutil.copyfile("docs/system-topology.jpg", "docs/tes_mkp/system-topology.jpg")
    shutil.copyfile("docs/database-erd.jpg", "docs/tes_mkp/database-erd.jpg")
    shutil.copyfile("docs/flowchart-pemesanan.jpg", "docs/tes_mkp/flowchart-pemesanan.jpg")
    print("All 3 JPGs copied to docs/tes_mkp/ successfully")
