import os
import subprocess

def create_topology_svg():
    svg = '''<svg width="1600" height="1100" viewBox="0 0 1600 1100" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a" />
      <stop offset="100%" stop-color="#1e1b4b" />
    </linearGradient>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e293b" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="8" stdDeviation="6" flood-color="#000000" flood-opacity="0.4"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="1600" height="1100" fill="url(#bgGrad)" />

  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#334155" stroke-width="0.5" stroke-opacity="0.3"/>
  </pattern>
  <rect width="1600" height="1100" fill="url(#grid)" />

  <!-- Header Banner -->
  <rect x="60" y="40" width="1480" height="100" rx="16" fill="url(#cardGrad)" stroke="#38bdf8" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="100" y="85" fill="#f8fafc" font-family="'Segoe UI', Roboto, sans-serif" font-size="28" font-weight="bold">TOPOLOGI ARSITEKTUR CLOUD SISTEM TIKET BIOSKOP NASIONAL</text>
  <text x="100" y="115" fill="#94a3b8" font-family="'Segoe UI', Roboto, sans-serif" font-size="16">Skala Nasional • Multi-Cabang • Concurrency Seat Locking (Redis Redlock) • Event-Driven Restock &amp; Refund (Kafka)</text>
  <rect x="1350" y="65" width="160" height="40" rx="20" fill="#10b981" />
  <text x="1430" y="90" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">HIGH AVAILABILITY</text>

  <!-- LAYER 1: CLIENT ACCESS LAYER -->
  <g transform="translate(60, 170)">
    <rect width="260" height="880" rx="16" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5" filter="url(#shadow)"/>
    <rect x="0" y="0" width="260" height="50" rx="16" fill="#1e293b" />
    <text x="130" y="32" fill="#38bdf8" font-family="sans-serif" font-size="15" font-weight="bold" text-anchor="middle">1. CLIENT ACCESS LAYER</text>

    <!-- Mobile App -->
    <rect x="20" y="70" width="220" height="130" rx="12" fill="#0f172a" stroke="#475569" stroke-width="1"/>
    <text x="50" y="116" fill="#38bdf8" font-family="sans-serif" font-size="18" text-anchor="middle">📱</text>
    <text x="80" y="105" fill="#f8fafc" font-family="sans-serif" font-size="15" font-weight="bold">Mobile App</text>
    <text x="80" y="125" fill="#94a3b8" font-family="sans-serif" font-size="12">iOS &amp; Android (Flutter)</text>
    <text x="30" y="160" fill="#cbd5e1" font-family="sans-serif" font-size="11">Real-time seat view, QR e-ticket</text>
    <text x="30" y="180" fill="#cbd5e1" font-family="sans-serif" font-size="11">Push notifications &amp; payment</text>

    <!-- Web Portal -->
    <rect x="20" y="220" width="220" height="130" rx="12" fill="#0f172a" stroke="#475569" stroke-width="1"/>
    <text x="50" y="266" fill="#818cf8" font-family="sans-serif" font-size="18" text-anchor="middle">💻</text>
    <text x="80" y="255" fill="#f8fafc" font-family="sans-serif" font-size="15" font-weight="bold">Web Customer</text>
    <text x="80" y="275" fill="#94a3b8" font-family="sans-serif" font-size="12">Next.js / Responsive Web</text>
    <text x="30" y="310" fill="#cbd5e1" font-family="sans-serif" font-size="11">Browsing film, bioskop, jadwal</text>
    <text x="30" y="330" fill="#cbd5e1" font-family="sans-serif" font-size="11">Checkout tiket &amp; riwayat order</text>

    <!-- Admin Portal -->
    <rect x="20" y="370" width="220" height="130" rx="12" fill="#0f172a" stroke="#475569" stroke-width="1"/>
    <text x="50" y="416" fill="#f59e0b" font-family="sans-serif" font-size="18" text-anchor="middle">🛠️</text>
    <text x="80" y="405" fill="#f8fafc" font-family="sans-serif" font-size="15" font-weight="bold">Admin Portal</text>
    <text x="80" y="425" fill="#94a3b8" font-family="sans-serif" font-size="12">Dashboard Manajemen</text>
    <text x="30" y="460" fill="#cbd5e1" font-family="sans-serif" font-size="11">CRUD Jadwal &amp; Studio</text>
    <text x="30" y="480" fill="#cbd5e1" font-family="sans-serif" font-size="11">Audit log &amp; refund trigger</text>

    <!-- On-Site Kiosk -->
    <rect x="20" y="520" width="220" height="130" rx="12" fill="#0f172a" stroke="#475569" stroke-width="1"/>
    <text x="50" y="566" fill="#ec4899" font-family="sans-serif" font-size="18" text-anchor="middle">🎟️</text>
    <text x="80" y="555" fill="#f8fafc" font-family="sans-serif" font-size="15" font-weight="bold">Kios Kasir Bioskop</text>
    <text x="80" y="575" fill="#94a3b8" font-family="sans-serif" font-size="12">Offline / Loket Cabang</text>
    <text x="30" y="610" fill="#cbd5e1" font-family="sans-serif" font-size="11">Cetak tiket fisik di bioskop</text>
    <text x="30" y="630" fill="#cbd5e1" font-family="sans-serif" font-size="11">Sinkronisasi kursi terpadu</text>

    <!-- Protocol Badges -->
    <rect x="20" y="670" width="220" height="180" rx="12" fill="#030712" stroke="#334155" stroke-width="1"/>
    <text x="35" y="700" fill="#f8fafc" font-family="sans-serif" font-size="13" font-weight="bold">Protokol Komunikasi:</text>
    <text x="35" y="730" fill="#38bdf8" font-family="sans-serif" font-size="12">• HTTPS / TLS 1.3</text>
    <text x="35" y="755" fill="#38bdf8" font-family="sans-serif" font-size="12">• REST API (JSON payload)</text>
    <text x="35" y="780" fill="#38bdf8" font-family="sans-serif" font-size="12">• WebSocket (Live Seatmap)</text>
    <text x="35" y="805" fill="#38bdf8" font-family="sans-serif" font-size="12">• JWT Bearer Token Auth</text>
  </g>

  <!-- LAYER 2: EDGE & SECURITY LAYER -->
  <g transform="translate(350, 170)">
    <rect width="250" height="880" rx="16" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5" filter="url(#shadow)"/>
    <rect x="0" y="0" width="250" height="50" rx="16" fill="#1e293b" />
    <text x="125" y="32" fill="#38bdf8" font-family="sans-serif" font-size="15" font-weight="bold" text-anchor="middle">2. EDGE &amp; GATEWAY</text>

    <!-- Cloudflare Edge -->
    <rect x="20" y="70" width="210" height="150" rx="12" fill="#0f172a" stroke="#f59e0b" stroke-width="1.2"/>
    <text x="35" y="100" fill="#f59e0b" font-family="sans-serif" font-size="16" font-weight="bold">Cloudflare Edge</text>
    <text x="35" y="125" fill="#cbd5e1" font-family="sans-serif" font-size="12">• Anycast DNS Global</text>
    <text x="35" y="145" fill="#cbd5e1" font-family="sans-serif" font-size="12">• DDoS Mitigation L3/L4/L7</text>
    <text x="35" y="165" fill="#cbd5e1" font-family="sans-serif" font-size="12">• WAF (Bot &amp; Scraping Shield)</text>
    <text x="35" y="185" fill="#cbd5e1" font-family="sans-serif" font-size="12">• Static Asset CDN (Posters)</text>
    <text x="35" y="205" fill="#10b981" font-family="sans-serif" font-size="11" font-weight="bold">Rate Limiting: 100 req/min</text>

    <!-- Load Balancer -->
    <rect x="20" y="250" width="210" height="130" rx="12" fill="#0f172a" stroke="#38bdf8" stroke-width="1"/>
    <text x="35" y="280" fill="#38bdf8" font-family="sans-serif" font-size="16" font-weight="bold">NGINX / ALB</text>
    <text x="35" y="305" fill="#cbd5e1" font-family="sans-serif" font-size="12">• SSL Termination</text>
    <text x="35" y="325" fill="#cbd5e1" font-family="sans-serif" font-size="12">• Round Robin &amp; Least Conn</text>
    <text x="35" y="345" fill="#cbd5e1" font-family="sans-serif" font-size="12">• Health Check Automatic</text>
    <text x="35" y="365" fill="#cbd5e1" font-family="sans-serif" font-size="12">• HTTP/2 &amp; Keep-Alive</text>

    <!-- API Gateway Routing -->
    <rect x="20" y="410" width="210" height="230" rx="12" fill="#0f172a" stroke="#818cf8" stroke-width="1"/>
    <text x="35" y="440" fill="#818cf8" font-family="sans-serif" font-size="16" font-weight="bold">API Gateway (Kong)</text>
    <text x="35" y="465" fill="#cbd5e1" font-family="sans-serif" font-size="12">• JWT Claims Inspection</text>
    <text x="35" y="485" fill="#cbd5e1" font-family="sans-serif" font-size="12">• RBAC: ADMIN vs CUSTOMER</text>
    <text x="35" y="505" fill="#cbd5e1" font-family="sans-serif" font-size="12">• Request Correlation ID</text>
    <text x="35" y="525" fill="#cbd5e1" font-family="sans-serif" font-size="12">• Centralized Access Logs</text>
    <text x="35" y="555" fill="#f8fafc" font-family="sans-serif" font-size="12" font-weight="bold">Path Routing:</text>
    <text x="35" y="575" fill="#94a3b8" font-family="sans-serif" font-size="11">/api/v1/auth/*</text>
    <text x="35" y="595" fill="#94a3b8" font-family="sans-serif" font-size="11">/api/v1/schedules/*</text>
    <text x="35" y="615" fill="#94a3b8" font-family="sans-serif" font-size="11">/api/v1/orders/*</text>

    <!-- Traffic info -->
    <rect x="20" y="660" width="210" height="190" rx="12" fill="#030712" stroke="#334155" stroke-width="1"/>
    <text x="35" y="690" fill="#f8fafc" font-family="sans-serif" font-size="13" font-weight="bold">Lonjakan Pengunjung:</text>
    <text x="35" y="720" fill="#e2e8f0" font-family="sans-serif" font-size="11">• Virtual Waiting Room saat</text>
    <text x="35" y="738" fill="#e2e8f0" font-family="sans-serif" font-size="11">  tiket blockbuster rilis</text>
    <text x="35" y="765" fill="#e2e8f0" font-family="sans-serif" font-size="11">• Circuit Breaker (Hystrix)</text>
    <text x="35" y="785" fill="#e2e8f0" font-family="sans-serif" font-size="11">• Auto Scaling Group</text>
    <text x="35" y="815" fill="#10b981" font-family="sans-serif" font-size="11" font-weight="bold">Target Uptime: 99.95%</text>
  </g>

  <!-- LAYER 3: CORE BACKEND SERVICES (GOLANG) -->
  <g transform="translate(630, 170)">
    <rect width="360" height="880" rx="16" fill="url(#cardGrad)" stroke="#38bdf8" stroke-width="2" filter="url(#shadow)"/>
    <rect x="0" y="0" width="360" height="50" rx="16" fill="#0284c7" />
    <text x="180" y="32" fill="#ffffff" font-family="sans-serif" font-size="15" font-weight="bold" text-anchor="middle">3. GOLANG BACKEND SERVICES</text>

    <!-- Auth Service -->
    <rect x="20" y="70" width="320" height="110" rx="12" fill="#0f172a" stroke="#475569" stroke-width="1"/>
    <text x="35" y="98" fill="#38bdf8" font-family="sans-serif" font-size="15" font-weight="bold">Autentikasi &amp; Otorisasi Service</text>
    <text x="35" y="120" fill="#cbd5e1" font-family="sans-serif" font-size="12">• Bcrypt Password Hashing (Cost 10)</text>
    <text x="35" y="140" fill="#cbd5e1" font-family="sans-serif" font-size="12">• JWT Sign &amp; Verify (HS256, 24-hr Expiry)</text>
    <text x="35" y="160" fill="#cbd5e1" font-family="sans-serif" font-size="12">• RBAC: ADMIN vs CUSTOMER Enforcement</text>

    <!-- Schedule Service -->
    <rect x="20" y="195" width="320" height="145" rx="12" fill="#0f172a" stroke="#475569" stroke-width="1"/>
    <text x="35" y="223" fill="#38bdf8" font-family="sans-serif" font-size="15" font-weight="bold">Manajemen Jadwal Tayang Service</text>
    <text x="35" y="245" fill="#cbd5e1" font-family="sans-serif" font-size="12">• CRUD Jadwal Tayang Bioskop</text>
    <text x="35" y="265" fill="#ef4444" font-family="sans-serif" font-size="12" font-weight="bold">• Deteksi Konflik Waktu Studio (HTTP 409)</text>
    <text x="35" y="285" fill="#94a3b8" font-family="sans-serif" font-size="11">  (waktu_mulai &lt; selesai_baru &amp;&amp; waktu_selesai &gt; mulai_baru)</text>
    <text x="35" y="305" fill="#cbd5e1" font-family="sans-serif" font-size="12">• Pembatalan Logis (Status CANCELLED)</text>
    <text x="35" y="325" fill="#cbd5e1" font-family="sans-serif" font-size="12">• Emit Event Schedule Cancelled ke Kafka</text>

    <!-- Seat Booking & Concurrency Service -->
    <rect x="20" y="355" width="320" height="165" rx="12" fill="#0f172a" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="35" y="383" fill="#f59e0b" font-family="sans-serif" font-size="15" font-weight="bold">Seat Booking &amp; Concurrency Control</text>
    <text x="35" y="405" fill="#cbd5e1" font-family="sans-serif" font-size="12">• Redis Redlock Atomic Locking Kursi</text>
    <text x="35" y="425" fill="#cbd5e1" font-family="sans-serif" font-size="12">• Status: AVAILABLE → RESERVED → BOOKED</text>
    <text x="35" y="445" fill="#cbd5e1" font-family="sans-serif" font-size="12">• TTL Booking: 10 Menit untuk Selesaikan Bayar</text>
    <text x="35" y="465" fill="#10b981" font-family="sans-serif" font-size="12" font-weight="bold">• Anti Double-Booking Guaranteed 100%</text>
    <text x="35" y="485" fill="#cbd5e1" font-family="sans-serif" font-size="12">• Optimistic Locking Versioning di DB</text>

    <!-- Order & Payment Service -->
    <rect x="20" y="535" width="320" height="135" rx="12" fill="#0f172a" stroke="#475569" stroke-width="1"/>
    <text x="35" y="563" fill="#38bdf8" font-family="sans-serif" font-size="15" font-weight="bold">Pesanan, Pembayaran &amp; Tiket Service</text>
    <text x="35" y="585" fill="#cbd5e1" font-family="sans-serif" font-size="12">• Invoice Creation &amp; Expiry Monitor</text>
    <text x="35" y="605" fill="#cbd5e1" font-family="sans-serif" font-size="12">• Webhook Listener Payment Gateway</text>
    <text x="35" y="625" fill="#cbd5e1" font-family="sans-serif" font-size="12">• Generate Kode Tiket Unik &amp; QR Code</text>
    <text x="35" y="645" fill="#cbd5e1" font-family="sans-serif" font-size="12">• Log Audit Segala Mutasi Data</text>

    <!-- Restock & Refund Worker -->
    <rect x="20" y="685" width="320" height="175" rx="12" fill="#0f172a" stroke="#818cf8" stroke-width="1"/>
    <text x="35" y="713" fill="#818cf8" font-family="sans-serif" font-size="15" font-weight="bold">Worker Restok &amp; Pengembalian Dana</text>
    <text x="35" y="735" fill="#cbd5e1" font-family="sans-serif" font-size="12">• Auto-Restock: Pelepasan kunci kursi jika</text>
    <text x="35" y="753" fill="#cbd5e1" font-family="sans-serif" font-size="12">  pesanan expired / user membatalkan</text>
    <text x="35" y="775" fill="#cbd5e1" font-family="sans-serif" font-size="12">• Auto-Refund: Saat bioskop cancel jadwal,</text>
    <text x="35" y="793" fill="#cbd5e1" font-family="sans-serif" font-size="12">  refund API otomatis dieksekusi 100%</text>
    <text x="35" y="815" fill="#cbd5e1" font-family="sans-serif" font-size="12">• Idempotent Message Consumer</text>
  </g>

  <!-- LAYER 4: DATA & MESSAGING LAYER -->
  <g transform="translate(1020, 170)">
    <rect width="520" height="880" rx="16" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5" filter="url(#shadow)"/>
    <rect x="0" y="0" width="520" height="50" rx="16" fill="#1e293b" />
    <text x="260" y="32" fill="#38bdf8" font-family="sans-serif" font-size="15" font-weight="bold" text-anchor="middle">4. PERSISTENCE, CACHE &amp; EVENT BROKER</text>

    <!-- REDIS CLUSTER -->
    <g transform="translate(20, 70)">
      <rect width="480" height="180" rx="12" fill="#0f172a" stroke="#ef4444" stroke-width="1.5"/>
      <text x="25" y="32" fill="#ef4444" font-family="sans-serif" font-size="16" font-weight="bold">Redis Sentinel / Cluster (In-Memory Engine)</text>
      
      <rect x="25" y="50" width="205" height="110" rx="8" fill="#1e293b" />
      <text x="40" y="75" fill="#f8fafc" font-family="sans-serif" font-size="13" font-weight="bold">Distributed Seat Locks:</text>
      <text x="40" y="98" fill="#cbd5e1" font-family="sans-serif" font-size="11">Key: lock:jadwal:{id}:kursi:{id}</text>
      <text x="40" y="118" fill="#cbd5e1" font-family="sans-serif" font-size="11">Algoritma: SET NX PX (Redlock)</text>
      <text x="40" y="138" fill="#38bdf8" font-family="sans-serif" font-size="11">Masa Kunci: 10 Menit</text>

      <rect x="250" y="50" width="205" height="110" rx="8" fill="#1e293b" />
      <text x="265" y="75" fill="#f8fafc" font-family="sans-serif" font-size="13" font-weight="bold">High-Speed Caches:</text>
      <text x="265" y="98" fill="#cbd5e1" font-family="sans-serif" font-size="11">• Denah Kursi &amp; Bioskop Cache</text>
      <text x="265" y="118" fill="#cbd5e1" font-family="sans-serif" font-size="11">• Status Ketersediaan Kursi</text>
      <text x="265" y="138" fill="#10b981" font-family="sans-serif" font-size="11">Throughput: &gt;100k ops/sec</text>
    </g>

    <!-- APACHE KAFKA / EVENT BROKER -->
    <g transform="translate(20, 270)">
      <rect width="480" height="170" rx="12" fill="#0f172a" stroke="#818cf8" stroke-width="1.2"/>
      <text x="25" y="32" fill="#818cf8" font-family="sans-serif" font-size="16" font-weight="bold">Message Broker: Apache Kafka / RabbitMQ</text>
      
      <rect x="25" y="50" width="135" height="100" rx="8" fill="#1e293b" />
      <text x="35" y="75" fill="#38bdf8" font-family="sans-serif" font-size="12" font-weight="bold">Topic: Order Events</text>
      <text x="35" y="95" fill="#94a3b8" font-family="sans-serif" font-size="10">• order.created</text>
      <text x="35" y="110" fill="#94a3b8" font-family="sans-serif" font-size="10">• order.paid</text>
      <text x="35" y="125" fill="#94a3b8" font-family="sans-serif" font-size="10">• order.expired</text>

      <rect x="175" y="50" width="135" height="100" rx="8" fill="#1e293b" />
      <text x="185" y="75" fill="#f59e0b" font-family="sans-serif" font-size="12" font-weight="bold">Topic: Restock</text>
      <text x="185" y="95" fill="#94a3b8" font-family="sans-serif" font-size="10">• seat.release_lock</text>
      <text x="185" y="110" fill="#94a3b8" font-family="sans-serif" font-size="10">• seat.restock_notify</text>
      <text x="185" y="125" fill="#94a3b8" font-family="sans-serif" font-size="10">• broadcast_ws</text>

      <rect x="325" y="50" width="130" height="100" rx="8" fill="#1e293b" />
      <text x="335" y="75" fill="#ef4444" font-family="sans-serif" font-size="12" font-weight="bold">Topic: Refund</text>
      <text x="335" y="95" fill="#94a3b8" font-family="sans-serif" font-size="10">• schedule.cancel</text>
      <text x="335" y="110" fill="#94a3b8" font-family="sans-serif" font-size="10">• trigger.refund</text>
      <text x="335" y="125" fill="#94a3b8" font-family="sans-serif" font-size="10">• notify.whatsapp</text>
    </g>

    <!-- POSTGRESQL PRIMARY & REPLICAS -->
    <g transform="translate(20, 460)">
      <rect width="480" height="230" rx="12" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>
      <text x="25" y="32" fill="#38bdf8" font-family="sans-serif" font-size="16" font-weight="bold">PostgreSQL 15 Cluster (ACID Database)</text>

      <!-- Primary DB -->
      <rect x="25" y="50" width="205" height="160" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="1"/>
      <text x="40" y="75" fill="#10b981" font-family="sans-serif" font-size="14" font-weight="bold">Primary Master (Write/Read)</text>
      <text x="40" y="100" fill="#cbd5e1" font-family="sans-serif" font-size="11">• Multi-AZ Synchronous Replication</text>
      <text x="40" y="120" fill="#cbd5e1" font-family="sans-serif" font-size="11">• Strong Consistency Transaction</text>
      <text x="40" y="140" fill="#cbd5e1" font-family="sans-serif" font-size="11">• Orders, Payments, Seats state</text>
      <text x="40" y="160" fill="#cbd5e1" font-family="sans-serif" font-size="11">• PgBouncer Connection Pool</text>
      <text x="40" y="180" fill="#cbd5e1" font-family="sans-serif" font-size="11">• Automated Failover (Patroni)</text>

      <!-- Read Replicas -->
      <rect x="250" y="50" width="205" height="160" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
      <text x="265" y="75" fill="#38bdf8" font-family="sans-serif" font-size="14" font-weight="bold">Read Replicas (Scale Read)</text>
      <text x="265" y="100" fill="#cbd5e1" font-family="sans-serif" font-size="11">• Melayani Query Jadwal &amp; Film</text>
      <text x="265" y="120" fill="#cbd5e1" font-family="sans-serif" font-size="11">• Auto-scaling saat traffic puncak</text>
      <text x="265" y="140" fill="#cbd5e1" font-family="sans-serif" font-size="11">• Latency &lt; 5ms di Region Lokal</text>
      <text x="265" y="160" fill="#cbd5e1" font-family="sans-serif" font-size="11">• Read-heavy ratio 90:10</text>
      <text x="265" y="180" fill="#cbd5e1" font-family="sans-serif" font-size="11">• Point-in-time recovery (WAL-G)</text>
    </g>

    <!-- EXTERNAL GATEWAYS -->
    <g transform="translate(20, 710)">
      <rect width="480" height="145" rx="12" fill="#030712" stroke="#475569" stroke-width="1"/>
      <text x="25" y="32" fill="#f8fafc" font-family="sans-serif" font-size="14" font-weight="bold">Integrasi Eksternal (Third-Party Providers)</text>
      
      <rect x="25" y="50" width="135" height="75" rx="8" fill="#1e293b" />
      <text x="35" y="72" fill="#38bdf8" font-family="sans-serif" font-size="12" font-weight="bold">Payment Gateway</text>
      <text x="35" y="90" fill="#94a3b8" font-family="sans-serif" font-size="10">Midtrans / Xendit</text>
      <text x="35" y="105" fill="#10b981" font-family="sans-serif" font-size="9">QRIS, VA, Cards</text>

      <rect x="175" y="50" width="135" height="75" rx="8" fill="#1e293b" />
      <text x="185" y="72" fill="#f59e0b" font-family="sans-serif" font-size="12" font-weight="bold">Notification GW</text>
      <text x="185" y="90" fill="#94a3b8" font-family="sans-serif" font-size="10">Twilio / WA Business</text>
      <text x="185" y="105" fill="#38bdf8" font-family="sans-serif" font-size="9">E-Ticket &amp; OTP</text>

      <rect x="325" y="50" width="130" height="75" rx="8" fill="#1e293b" />
      <text x="335" y="72" fill="#ec4899" font-family="sans-serif" font-size="12" font-weight="bold">Monitoring / APM</text>
      <text x="335" y="90" fill="#94a3b8" font-family="sans-serif" font-size="10">Prometheus, Grafana</text>
      <text x="335" y="105" fill="#cbd5e1" font-family="sans-serif" font-size="9">Distributed Tracing</text>
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
  <text x="90" y="70" fill="#f9fafb" font-family="sans-serif" font-size="26" font-weight="bold">ENTITY RELATIONSHIP DIAGRAM (ERD) - BASIS DATA BIOSKOP NASIONAL</text>
  <text x="90" y="98" fill="#9ca3af" font-family="sans-serif" font-size="15">Dialek: PostgreSQL 15 • 13 Tabel Relasional • Normalisasi 3NF • Optimistic Locking Version • Indeks Performa Tinggi</text>

  <!-- TABLE MACRO HELPER STYLES -->
  <!-- We will render table boxes with header, PK, FK, and columns -->

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
    <rect width="240" height="190" rx="8" fill="#111827" stroke="#10b981" stroke-width="1.5" filter="url(#shadow)"/>
    <rect width="240" height="36" rx="8" fill="#065f46" />
    <text x="120" y="24" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">bioskop (cinemas)</text>
    <text x="15" y="60" fill="#f59e0b" font-family="monospace" font-size="12">PK  id : BIGSERIAL</text>
    <text x="15" y="82" fill="#e5e7eb" font-family="monospace" font-size="12">    nama : VARCHAR(255)</text>
    <text x="15" y="104" fill="#e5e7eb" font-family="monospace" font-size="12">    kota : VARCHAR(100)</text>
    <text x="15" y="126" fill="#e5e7eb" font-family="monospace" font-size="12">    alamat : TEXT</text>
    <text x="15" y="148" fill="#e5e7eb" font-family="monospace" font-size="12">    status : VARCHAR(50)</text>
    <text x="15" y="170" fill="#9ca3af" font-family="monospace" font-size="11">    dibuat_pada : TIMESTAMPTZ</text>
  </g>

  <!-- 3. STUDIO (studios) -->
  <g transform="translate(670, 150)">
    <rect width="240" height="190" rx="8" fill="#111827" stroke="#10b981" stroke-width="1.5" filter="url(#shadow)"/>
    <rect width="240" height="36" rx="8" fill="#065f46" />
    <text x="120" y="24" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">studio (studios)</text>
    <text x="15" y="60" fill="#f59e0b" font-family="monospace" font-size="12">PK  id : BIGSERIAL</text>
    <text x="15" y="82" fill="#38bdf8" font-family="monospace" font-size="12">FK  bioskop_id : BIGINT</text>
    <text x="15" y="104" fill="#e5e7eb" font-family="monospace" font-size="12">    nama : VARCHAR(100)</text>
    <text x="15" y="126" fill="#e5e7eb" font-family="monospace" font-size="12">    kapasitas : INT</text>
    <text x="15" y="148" fill="#e5e7eb" font-family="monospace" font-size="12">    tipe : VARCHAR(50)</text>
    <text x="15" y="170" fill="#9ca3af" font-family="monospace" font-size="11">    dibuat_pada : TIMESTAMPTZ</text>
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

  <!-- 6. JADWAL (schedules) -->
  <g transform="translate(670, 420)">
    <rect width="260" height="230" rx="8" fill="#111827" stroke="#f59e0b" stroke-width="2" filter="url(#shadow)"/>
    <rect width="260" height="36" rx="8" fill="#b45309" />
    <text x="130" y="24" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">jadwal (schedules)</text>
    <text x="15" y="60" fill="#f59e0b" font-family="monospace" font-size="12">PK  id : BIGSERIAL</text>
    <text x="15" y="82" fill="#38bdf8" font-family="monospace" font-size="12">FK  film_id : BIGINT</text>
    <text x="15" y="104" fill="#38bdf8" font-family="monospace" font-size="12">FK  studio_id : BIGINT</text>
    <text x="15" y="126" fill="#ef4444" font-family="monospace" font-size="12">IDX waktu_mulai : TIMESTAMPTZ</text>
    <text x="15" y="148" fill="#ef4444" font-family="monospace" font-size="12">IDX waktu_selesai : TIMESTAMPTZ</text>
    <text x="15" y="170" fill="#e5e7eb" font-family="monospace" font-size="12">    status : VARCHAR(50)</text>
    <text x="15" y="192" fill="#9ca3af" font-family="monospace" font-size="11">    dibuat_pada : TIMESTAMPTZ</text>
    <text x="15" y="212" fill="#a7f3d0" font-family="monospace" font-size="11">CHK waktu_selesai &gt; mulai</text>
  </g>

  <!-- 7. KURSI JADWAL (show_seats) -->
  <g transform="translate(1050, 420)">
    <rect width="270" height="230" rx="8" fill="#111827" stroke="#ec4899" stroke-width="1.8" filter="url(#shadow)"/>
    <rect width="270" height="36" rx="8" fill="#be185d" />
    <text x="135" y="24" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">kursi_jadwal (show_seats)</text>
    <text x="15" y="60" fill="#f59e0b" font-family="monospace" font-size="12">PK  id : BIGSERIAL</text>
    <text x="15" y="82" fill="#38bdf8" font-family="monospace" font-size="12">FK  jadwal_id : BIGINT</text>
    <text x="15" y="104" fill="#38bdf8" font-family="monospace" font-size="12">FK  kursi_id : BIGINT</text>
    <text x="15" y="126" fill="#e5e7eb" font-family="monospace" font-size="12">    harga : DECIMAL(12,2)</text>
    <text x="15" y="148" fill="#ec4899" font-family="monospace" font-size="12">IDX status : VARCHAR(50)</text>
    <text x="15" y="170" fill="#e5e7eb" font-family="monospace" font-size="12">    dipesan_sampai : TIMESTAMPTZ</text>
    <text x="15" y="192" fill="#10b981" font-family="monospace" font-size="12">    versi : INT (Opt. Lock)</text>
    <text x="15" y="212" fill="#60a5fa" font-family="monospace" font-size="11">UQ  (jadwal_id, kursi_id)</text>
  </g>

  <!-- 8. PESANAN (orders) -->
  <g transform="translate(370, 420)">
    <rect width="250" height="230" rx="8" fill="#111827" stroke="#3b82f6" stroke-width="1.8" filter="url(#shadow)"/>
    <rect width="250" height="36" rx="8" fill="#1e3a8a" />
    <text x="125" y="24" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">pesanan (orders)</text>
    <text x="15" y="60" fill="#f59e0b" font-family="monospace" font-size="12">PK  id : BIGSERIAL</text>
    <text x="15" y="82" fill="#60a5fa" font-family="monospace" font-size="12">UQ  kode_pesanan : VARCHAR</text>
    <text x="15" y="104" fill="#38bdf8" font-family="monospace" font-size="12">FK  pengguna_id : BIGINT</text>
    <text x="15" y="126" fill="#38bdf8" font-family="monospace" font-size="12">FK  jadwal_id : BIGINT</text>
    <text x="15" y="148" fill="#e5e7eb" font-family="monospace" font-size="12">    total_biaya : DECIMAL</text>
    <text x="15" y="170" fill="#e5e7eb" font-family="monospace" font-size="12">    status : VARCHAR(50)</text>
    <text x="15" y="192" fill="#ef4444" font-family="monospace" font-size="11">    kadaluarsa_pada : TIMESTAMPTZ</text>
    <text x="15" y="212" fill="#9ca3af" font-family="monospace" font-size="11">    dibuat_pada : TIMESTAMPTZ</text>
  </g>

  <!-- 9. ITEM PESANAN (order_items) -->
  <g transform="translate(720, 720)">
    <rect width="250" height="170" rx="8" fill="#111827" stroke="#6366f1" stroke-width="1.5" filter="url(#shadow)"/>
    <rect width="250" height="36" rx="8" fill="#4338ca" />
    <text x="125" y="24" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">item_pesanan (order_items)</text>
    <text x="15" y="60" fill="#f59e0b" font-family="monospace" font-size="12">PK  id : BIGSERIAL</text>
    <text x="15" y="82" fill="#38bdf8" font-family="monospace" font-size="12">FK  pesanan_id : BIGINT</text>
    <text x="15" y="104" fill="#38bdf8" font-family="monospace" font-size="12">FK  kursi_jadwal_id : BIGINT</text>
    <text x="15" y="126" fill="#e5e7eb" font-family="monospace" font-size="12">    harga : DECIMAL(12,2)</text>
    <text x="15" y="148" fill="#60a5fa" font-family="monospace" font-size="11">UQ  (pesanan, kursi_jadwal)</text>
  </g>

  <!-- 10. PEMBAYARAN (payments) -->
  <g transform="translate(370, 720)">
    <rect width="260" height="210" rx="8" fill="#111827" stroke="#10b981" stroke-width="1.5" filter="url(#shadow)"/>
    <rect width="260" height="36" rx="8" fill="#065f46" />
    <text x="130" y="24" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">pembayaran (payments)</text>
    <text x="15" y="60" fill="#f59e0b" font-family="monospace" font-size="12">PK  id : BIGSERIAL</text>
    <text x="15" y="82" fill="#38bdf8" font-family="monospace" font-size="12">FK  pesanan_id : BIGINT</text>
    <text x="15" y="104" fill="#60a5fa" font-family="monospace" font-size="12">UQ  id_transaksi_gateway</text>
    <text x="15" y="126" fill="#e5e7eb" font-family="monospace" font-size="12">    metode_pembayaran</text>
    <text x="15" y="148" fill="#e5e7eb" font-family="monospace" font-size="12">    nominal : DECIMAL</text>
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
    <text x="15" y="104" fill="#38bdf8" font-family="monospace" font-size="12">FK  pesanan_id : BIGINT</text>
    <text x="15" y="126" fill="#38bdf8" font-family="monospace" font-size="12">FK  kursi_jadwal_id : BIGINT</text>
    <text x="15" y="148" fill="#e5e7eb" font-family="monospace" font-size="12">    status : VARCHAR(50)</text>
    <text x="15" y="170" fill="#9ca3af" font-family="monospace" font-size="11">    dibuat_pada : TIMESTAMPTZ</text>
  </g>

  <!-- 12. PENGEMBALIAN DANA (refunds) -->
  <g transform="translate(60, 720)">
    <rect width="260" height="190" rx="8" fill="#111827" stroke="#ef4444" stroke-width="1.5" filter="url(#shadow)"/>
    <rect width="260" height="36" rx="8" fill="#991b1b" />
    <text x="130" y="24" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">pengembalian_dana (refunds)</text>
    <text x="15" y="60" fill="#f59e0b" font-family="monospace" font-size="12">PK  id : BIGSERIAL</text>
    <text x="15" y="82" fill="#38bdf8" font-family="monospace" font-size="12">FK  pesanan_id : BIGINT</text>
    <text x="15" y="104" fill="#e5e7eb" font-family="monospace" font-size="12">    alasan : TEXT</text>
    <text x="15" y="126" fill="#e5e7eb" font-family="monospace" font-size="12">    nominal : DECIMAL</text>
    <text x="15" y="148" fill="#e5e7eb" font-family="monospace" font-size="12">    status : VARCHAR(50)</text>
    <text x="15" y="170" fill="#9ca3af" font-family="monospace" font-size="11">    diproses_pada : TIMESTAMPTZ</text>
  </g>

  <!-- 13. LOG AUDIT (audit_logs) -->
  <g transform="translate(1360, 720)">
    <rect width="270" height="210" rx="8" fill="#111827" stroke="#6b7280" stroke-width="1.5" filter="url(#shadow)"/>
    <rect width="270" height="36" rx="8" fill="#374151" />
    <text x="135" y="24" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">log_audit (audit_logs)</text>
    <text x="15" y="60" fill="#f59e0b" font-family="monospace" font-size="12">PK  id : BIGSERIAL</text>
    <text x="15" y="82" fill="#e5e7eb" font-family="monospace" font-size="12">    nama_entitas : VARCHAR</text>
    <text x="15" y="104" fill="#e5e7eb" font-family="monospace" font-size="12">    id_entitas : BIGINT</text>
    <text x="15" y="126" fill="#e5e7eb" font-family="monospace" font-size="12">    aksi : VARCHAR(50)</text>
    <text x="15" y="148" fill="#e5e7eb" font-family="monospace" font-size="12">    diubah_oleh : VARCHAR</text>
    <text x="15" y="170" fill="#cbd5e1" font-family="monospace" font-size="11">    data_lama : JSONB</text>
    <text x="15" y="190" fill="#cbd5e1" font-family="monospace" font-size="11">    data_baru : JSONB</text>
  </g>

  <!-- RELATIONSHIP ARROWS / CONNECTORS -->
  <!-- bioskop -> studio -->
  <path d="M 610 240 L 670 240" stroke="#10b981" stroke-width="2" stroke-dasharray="4" />
  <!-- studio -> kursi -->
  <path d="M 910 240 L 970 240" stroke="#10b981" stroke-width="2" stroke-dasharray="4" />
  <!-- studio -> jadwal -->
  <path d="M 790 340 L 790 420" stroke="#f59e0b" stroke-width="2" />
  <!-- film -> jadwal -->
  <path d="M 1280 255 L 930 480" stroke="#8b5cf6" stroke-width="2" />
  <!-- jadwal -> kursi_jadwal -->
  <path d="M 930 535 L 1050 535" stroke="#ec4899" stroke-width="2" />
  <!-- kursi -> kursi_jadwal -->
  <path d="M 1095 350 L 1095 420" stroke="#10b981" stroke-width="2" stroke-dasharray="4" />
  <!-- pengguna -> pesanan -->
  <path d="M 310 260 L 370 470" stroke="#3b82f6" stroke-width="2" />
  <!-- jadwal -> pesanan -->
  <path d="M 670 535 L 620 535" stroke="#f59e0b" stroke-width="2" />
  <!-- pesanan -> item_pesanan -->
  <path d="M 580 650 L 720 750" stroke="#3b82f6" stroke-width="2" />
  <!-- kursi_jadwal -> item_pesanan -->
  <path d="M 1100 650 L 940 720" stroke="#ec4899" stroke-width="2" />
  <!-- pesanan -> pembayaran -->
  <path d="M 495 650 L 495 720" stroke="#10b981" stroke-width="2" />
  <!-- pesanan -> pengembalian_dana -->
  <path d="M 400 650 L 220 720" stroke="#ef4444" stroke-width="2" />
  <!-- pesanan -> tiket -->
  <path d="M 620 620 L 1050 780" stroke="#38bdf8" stroke-width="2" />

  <!-- Footnote -->
  <rect x="50" y="990" width="1600" height="150" rx="12" fill="#1e293b" stroke="#475569" stroke-width="1"/>
  <text x="80" y="1030" fill="#f8fafc" font-family="sans-serif" font-size="16" font-weight="bold">Kunci Integritas &amp; Solusi Masalah Teknis:</text>
  <text x="80" y="1060" fill="#cbd5e1" font-family="sans-serif" font-size="13">1. Anti Double-Booking: Batasan UNIQUE (jadwal_id, kursi_id) pada tabel kursi_jadwal ditambah kolom versi untuk Optimistic Locking.</text>
  <text x="80" y="1085" fill="#cbd5e1" font-family="sans-serif" font-size="13">2. Pencegahan Jadwal Bentrok: Indeks komposit idx_jadwal_studio_waktu (studio_id, waktu_mulai, waktu_selesai) dan validasi overlap di layer Go.</text>
  <text x="80" y="1110" fill="#cbd5e1" font-family="sans-serif" font-size="13">3. Restok &amp; Refund: Kolom dipesan_sampai mengontrol batas kadaluarsa pembayaran; pembatalan jadwal memicu pembuatan entri pengembalian_dana otomatis.</text>
</svg>'''
    with open('/tmp/database_erd.svg', 'w') as f:
        f.write(svg)


def create_flowchart_svg():
    svg = '''<svg width="1500" height="1000" viewBox="0 0 1500 1000" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#090d16" />
      <stop offset="100%" stop-color="#1e1b4b" />
    </linearGradient>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#000000" flood-opacity="0.5"/>
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#38bdf8" />
    </marker>
    <marker id="arrowGreen" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#10b981" />
    </marker>
    <marker id="arrowRed" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#ef4444" />
    </marker>
  </defs>

  <rect width="1500" height="1000" fill="url(#bgGrad)" />

  <!-- Header -->
  <rect x="50" y="30" width="1400" height="90" rx="14" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="90" y="70" fill="#f8fafc" font-family="'Segoe UI', Roboto, sans-serif" font-size="26" font-weight="bold">FLOWCHART SISTEM PEMESANAN, RESTOK TIKET, &amp; REFUND (UNTUK ORANG AWAM)</text>
  <text x="90" y="98" fill="#94a3b8" font-family="'Segoe UI', Roboto, sans-serif" font-size="15">Langkah Mudah Memahami Alur Pelanggan • Mekanisme Penguncian Kursi • Pelepasan Otomatis • Pembatalan oleh Bioskop</text>

  <!-- SECTION 1: ALUR UTAMA PEMESANAN (CUSTOMER HAPPY PATH) -->
  <g transform="translate(60, 160)">
    <rect width="1380" height="340" rx="14" fill="#0f172a" stroke="#334155" stroke-width="1.5" filter="url(#shadow)"/>
    <rect width="1380" height="40" rx="14" fill="#1e293b" />
    <text x="25" y="26" fill="#38bdf8" font-family="sans-serif" font-size="14" font-weight="bold">JALUR UTAMA: PEMILIHAN FILM, PENGUNCIAN KURSI, &amp; PEMBAYARAN TIKET</text>

    <!-- Step 1 -->
    <rect x="30" y="65" width="220" height="110" rx="10" fill="#1e293b" stroke="#475569" stroke-width="1"/>
    <circle cx="55" cy="90" r="14" fill="#38bdf8" />
    <text x="55" y="95" fill="#0f172a" font-family="sans-serif" font-size="12" font-weight="bold" text-anchor="middle">1</text>
    <text x="80" y="92" fill="#f8fafc" font-family="sans-serif" font-size="14" font-weight="bold">Pilih Film &amp; Jadwal</text>
    <text x="30" y="125" fill="#94a3b8" font-family="sans-serif" font-size="11">Pelanggan memilih cabang bioskop, judul film, tanggal &amp; jam tayang yang diinginkan.</text>

    <!-- Step 2 -->
    <rect x="310" y="65" width="220" height="110" rx="10" fill="#1e293b" stroke="#475569" stroke-width="1"/>
    <circle cx="335" cy="90" r="14" fill="#38bdf8" />
    <text x="335" y="95" fill="#0f172a" font-family="sans-serif" font-size="12" font-weight="bold" text-anchor="middle">2</text>
    <text x="360" y="92" fill="#f8fafc" font-family="sans-serif" font-size="14" font-weight="bold">Pilih Kursi (Seatmap)</text>
    <text x="310" y="125" fill="#94a3b8" font-family="sans-serif" font-size="11">Melihat denah kursi hijau (tersedia), kuning (dikunci), dan abu-abu (terjual).</text>

    <!-- Step 3 (Crucial Locking) -->
    <rect x="590" y="65" width="240" height="110" rx="10" fill="#1e293b" stroke="#f59e0b" stroke-width="1.8"/>
    <circle cx="615" cy="90" r="14" fill="#f59e0b" />
    <text x="615" y="95" fill="#0f172a" font-family="sans-serif" font-size="12" font-weight="bold" text-anchor="middle">3</text>
    <text x="640" y="92" fill="#f59e0b" font-family="sans-serif" font-size="14" font-weight="bold">Kunci Kursi (10 Menit)</text>
    <text x="590" y="125" fill="#cbd5e1" font-family="sans-serif" font-size="11">Sistem langsung "MENGUNCI" nomor kursi Anda. Orang lain tidak bisa memilih kursi ini!</text>

    <!-- Step 4 -->
    <rect x="890" y="65" width="210" height="110" rx="10" fill="#1e293b" stroke="#475569" stroke-width="1"/>
    <circle cx="915" cy="90" r="14" fill="#38bdf8" />
    <text x="915" y="95" fill="#0f172a" font-family="sans-serif" font-size="12" font-weight="bold" text-anchor="middle">4</text>
    <text x="940" y="92" fill="#f8fafc" font-family="sans-serif" font-size="14" font-weight="bold">Bayar Pesanan</text>
    <text x="890" y="125" fill="#94a3b8" font-family="sans-serif" font-size="11">Bayar melalui QRIS, Virtual Account BCA/Mandiri, atau Kartu Kredit.</text>

    <!-- Step 5 -->
    <rect x="1150" y="65" width="200" height="110" rx="10" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
    <circle cx="1175" cy="90" r="14" fill="#10b981" />
    <text x="1175" y="95" fill="#ffffff" font-family="sans-serif" font-size="12" font-weight="bold" text-anchor="middle">5</text>
    <text x="1200" y="92" fill="#10b981" font-family="sans-serif" font-size="14" font-weight="bold">E-Tiket Terbit!</text>
    <text x="1150" y="125" fill="#a7f3d0" font-family="sans-serif" font-size="11">Tiket QR Code dikirim ke WhatsApp &amp; Email. Siap dipindai di pintu studio!</text>

    <!-- Connecting Arrows -->
    <path d="M 250 120 L 305 120" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrow)" />
    <path d="M 530 120 L 585 120" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrow)" />
    <path d="M 830 120 L 885 120" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrow)" />
    <path d="M 1100 120 L 1145 120" stroke="#10b981" stroke-width="2" marker-end="url(#arrowGreen)" />

    <!-- Explanatory Box below -->
    <rect x="30" y="200" width="1320" height="110" rx="8" fill="#1e293b" />
    <text x="50" y="230" fill="#f8fafc" font-family="sans-serif" font-size="13" font-weight="bold">💡 Mengapa Pelanggan Tidak Perlu Khawatir Kursi Diambil Orang Lain?</text>
    <text x="50" y="255" fill="#94a3b8" font-family="sans-serif" font-size="12">Begitu Anda menekan nomor kursi, sistem komputer menggunakan teknologi "Distributed Lock" (Redis). Kursi tersebut langsung memiliki masa countdown 10 menit.</text>
    <text x="50" y="275" fill="#94a3b8" font-family="sans-serif" font-size="12">Jika ada pembeli lain di seluruh Indonesia yang mencoba mengklik kursi yang sama pada detik yang sama, sistem mereka akan langsung menampilkan pesan: "Kursi Sedang Dipesan".</text>
  </g>

  <!-- SECTION 2: ALUR RESTOK OTOMATIS (JIKA BATAL / TELAT BAYAR) -->
  <g transform="translate(60, 530)">
    <rect width="660" height="420" rx="14" fill="#0f172a" stroke="#f59e0b" stroke-width="1.5" filter="url(#shadow)"/>
    <rect width="660" height="40" rx="14" fill="#78350f" />
    <text x="25" y="26" fill="#fde68a" font-family="sans-serif" font-size="14" font-weight="bold">SKENARIO 1: RESTOK TIKET OTOMATIS (BATAL / TELAT BAYAR)</text>

    <rect x="30" y="60" width="600" height="85" rx="8" fill="#1e293b" stroke="#ef4444" stroke-width="1"/>
    <text x="50" y="85" fill="#f87171" font-family="sans-serif" font-size="13" font-weight="bold">1. Waktu Pembayaran 10 Menit Habis</text>
    <text x="50" y="105" fill="#cbd5e1" font-family="sans-serif" font-size="11">Pelanggan tidak menyelesaikan transfer atau menutup aplikasi sebelum membayar.</text>
    <text x="50" y="125" fill="#cbd5e1" font-family="sans-serif" font-size="11">Status pesanan berubah dari PENDING menjadi EXPIRED.</text>

    <path d="M 330 145 L 330 170" stroke="#f59e0b" stroke-width="2" marker-end="url(#arrow)" />

    <rect x="30" y="175" width="600" height="85" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="1"/>
    <text x="50" y="200" fill="#fde68a" font-family="sans-serif" font-size="13" font-weight="bold">2. Sistem Robot Otomatis (Event Worker Kafka) Bekerja</text>
    <text x="50" y="220" fill="#cbd5e1" font-family="sans-serif" font-size="11">Sistem mendeteksi masa kunci habis dan seketika membuka gembok kursi di Redis dan Database.</text>
    <text x="50" y="240" fill="#cbd5e1" font-family="sans-serif" font-size="11">Status kursi kembali dari RESERVED menjadi AVAILABLE.</text>

    <path d="M 330 260 L 330 285" stroke="#10b981" stroke-width="2" marker-end="url(#arrowGreen)" />

    <rect x="30" y="290" width="600" height="100" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="1"/>
    <text x="50" y="315" fill="#4ade80" font-family="sans-serif" font-size="13" font-weight="bold">3. Tiket Kembali Muncul di Aplikasi (Restocked!)</text>
    <text x="50" y="335" fill="#cbd5e1" font-family="sans-serif" font-size="11">Denah kursi langsung ter-update secara real-time ke semua handphone pengguna.</text>
    <text x="50" y="355" fill="#cbd5e1" font-family="sans-serif" font-size="11">Pembeli lain sekarang dapat langsung memilih dan membeli kursi tersebut tanpa kendala.</text>
  </g>

  <!-- SECTION 3: ALUR PEMBATALAN OLEH PIHAK BIOSKOP (REFUND 100%) -->
  <g transform="translate(780, 530)">
    <rect width="660" height="420" rx="14" fill="#0f172a" stroke="#ef4444" stroke-width="1.5" filter="url(#shadow)"/>
    <rect width="660" height="40" rx="14" fill="#7f1d1d" />
    <text x="25" y="26" fill="#fecaca" font-family="sans-serif" font-size="14" font-weight="bold">SKENARIO 2: PEMBATALAN OLEH PIHAK BIOSKOP &amp; REFUND 100%</text>

    <rect x="30" y="60" width="600" height="85" rx="8" fill="#1e293b" stroke="#ef4444" stroke-width="1"/>
    <text x="50" y="85" fill="#f87171" font-family="sans-serif" font-size="13" font-weight="bold">1. Kendala Operasional Bioskop</text>
    <text x="50" y="105" fill="#cbd5e1" font-family="sans-serif" font-size="11">Misal proyektor rusak, studio mati lampu, atau film ditarik izin tayangnya.</text>
    <text x="50" y="125" fill="#cbd5e1" font-family="sans-serif" font-size="11">Manajer Bioskop mengklik "Batalkan Jadwal" di Dashboard Admin.</text>

    <path d="M 330 145 L 330 170" stroke="#ef4444" stroke-width="2" marker-end="url(#arrowRed)" />

    <rect x="30" y="175" width="600" height="85" rx="8" fill="#1e293b" stroke="#ef4444" stroke-width="1"/>
    <text x="50" y="200" fill="#fca5a5" font-family="sans-serif" font-size="13" font-weight="bold">2. Tiket Dibatalkan &amp; Mesin Refund Otomatis Terpicu</text>
    <text x="50" y="220" fill="#cbd5e1" font-family="sans-serif" font-size="11">Status jadwal menjadi CANCELLED; tiket pelanggan dinonaktifkan.</text>
    <text x="50" y="240" fill="#cbd5e1" font-family="sans-serif" font-size="11">Sistem memicu instruksi pengembalian dana 100% ke Payment Gateway.</text>

    <path d="M 330 260 L 330 285" stroke="#10b981" stroke-width="2" marker-end="url(#arrowGreen)" />

    <rect x="30" y="290" width="600" height="100" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="1"/>
    <text x="50" y="315" fill="#4ade80" font-family="sans-serif" font-size="13" font-weight="bold">3. Dana Kembali 100% &amp; Pemberitahuan Langsung</text>
    <text x="50" y="335" fill="#cbd5e1" font-family="sans-serif" font-size="11">Uang otomatis dikembalikan ke rekening/e-wallet pelanggan tanpa potongan.</text>
    <text x="50" y="355" fill="#cbd5e1" font-family="sans-serif" font-size="11">Pelanggan menerima pesan permohonan maaf dan bukti transfer via WhatsApp/Email.</text>
  </g>

</svg>'''
    with open('/tmp/flowchart.svg', 'w') as f:
        f.write(svg)

create_topology_svg()
create_database_erd_svg()
create_flowchart_svg()
print("All 3 SVGs created successfully")
