document.addEventListener('DOMContentLoaded', () => {
    const termInput = document.getElementById('terminal-input');
    const termOutput = document.getElementById('terminal-output');

    // Basit bir sanal dosya sistemi durumu (State)
    let currentDir = '/home/student';
    const FILESYSTEM = {
        '/home/student': ['cyber_notes.txt', 'network_scan.py', 'challenges/'],
        '/home/student/challenges': ['flag1.txt', 'hint.md'],
        '/etc': ['passwd', 'hosts']
    };

    // Komut Beyaz Listesi (Simülasyon Yanıtları)
    const COMMANDS = {
        'help': () => `Desteklenen Komutlar:
  help    - Bu yardım menüsünü gösterir
  ls      - Bulunduğunuz dizindeki dosyaları listeler
  pwd     - Mevcut çalışma dizinini yazdırır
  cd      - Dizin değiştirir (Örn: cd challenges)
  whoami  - Geçerli kullanıcıyı gösterir
  cat     - Dosya içeriğini okur (Örn: cat cyber_notes.txt)
  clear   - Terminal ekranını temizler
  nmap    - [Simülasyon] Ağ tarama aracı
  ping    - [Simülasyon] Paket gönderim testi`,

        'whoami': () => 'student',

        'pwd': () => currentDir,

        'ls': (args) => {
            const dir = args.length > 0 ? args[0] : currentDir;
            if (FILESYSTEM[dir] || FILESYSTEM[currentDir]) {
                return (FILESYSTEM[dir] || FILESYSTEM[currentDir]).join('  ');
            }
            return `ls: cannot access '${dir}': No such file or directory`;
        },

        'cd': (args) => {
            if (args.length === 0 || args[0] === '~') {
                currentDir = '/home/student';
                return '';
            }

            let target = args[0];
            if (target === '..') {
                const parts = currentDir.split('/').filter(Boolean);
                parts.pop();
                currentDir = '/' + parts.join('/');
                if (currentDir === '/') currentDir = '/';
                else if (currentDir === '') currentDir = '/';
                return '';
            }

            const potentialPath = currentDir === '/' ? `/${target}` : `${currentDir}/${target}`.replace(/\/+$/, '');

            // Sadece klasörleri kontrol et
            if (FILESYSTEM[potentialPath]) {
                currentDir = potentialPath;
                return '';
            } else if (FILESYSTEM[currentDir] && FILESYSTEM[currentDir].includes(target + '/')) {
                currentDir = potentialPath;
                return '';
            }

            return `-bash: cd: ${target}: No such file or directory`;
        },

        'cat': (args) => {
            if (args.length === 0) return 'Kullanım: cat <dosya_adi>';
            const file = args[0];

            if (currentDir === '/home/student' && file === 'cyber_notes.txt') {
                return '[Notlar]\n- Her zaman nmap -sV kullan\n- Wireshark ile pcap analizi yapmayı unutma!';
            }
            if (currentDir === '/home/student/challenges' && file === 'flag1.txt') {
                return 'CyberLearnPI{b4s1c_l1nux_sk1llz}';
            }
            if (file === '/etc/passwd') {
                return 'root:x:0:0:root:/root:/bin/bash\nstudent:x:1000:1000:,,,:/home/student:/bin/bash\npi:x:1001:1001:,,,:/home/pi:/bin/bash';
            }

            return `cat: ${file}: No such file or directory`;
        },

        'clear': () => {
            termOutput.innerHTML = '';
            return null; // Çıktı döndürme, sadece temizle
        },

        'ping': (args) => {
            const target = args.length > 0 ? args[0] : '8.8.8.8';
            return `PING ${target} (Simülasyon):\n64 bytes from ${target}: icmp_seq=1 ttl=117 time=14.2 ms\n64 bytes from ${target}: icmp_seq=2 ttl=117 time=13.8 ms\n64 bytes from ${target}: icmp_seq=3 ttl=117 time=14.5 ms\n\n--- ${target} ping statistics ---\n3 packets transmitted, 3 received, 0% packet loss`;
        },

        'nmap': (args) => {
            return `Starting Nmap 7.91 ( https://nmap.org ) (Simülasyon Modu)\nNmap scan report for target (192.168.1.100)\nHost is up (0.0050s latency).\nNot shown: 996 closed ports\nPORT     STATE SERVICE\n22/tcp   open  ssh\n80/tcp   open  http\n443/tcp  open  https\n3306/tcp open  mysql\n\nNmap done: 1 IP address (1 host up) scanned in 2.34 seconds`;
        }
    };

    termInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            const val = this.value.trim();
            this.value = '';

            // Ekrana girilen komutu yazdır
            printTerminal(`student@cyberlearn-pi:${currentDir === '/home/student' ? '~' : currentDir}$ ${val}`);

            if (val) {
                processCommand(val);
            }

            // En alta kaydır
            termOutput.scrollTop = termOutput.scrollHeight;
        }
    });

    function printTerminal(text, isError = false) {
        if (text === null) return; // clear komutu için

        const div = document.createElement('div');
        div.className = isError ? 'text-red-400 whitespace-pre-wrap' : 'whitespace-pre-wrap';
        div.textContent = text;
        termOutput.appendChild(div);
    }

    function processCommand(input) {
        const parts = input.split(' ').filter(Boolean);
        const cmd = parts[0];
        const args = parts.slice(1);

        if (COMMANDS[cmd]) {
            const output = COMMANDS[cmd](args);
            if (output !== null && output !== '') {
                printTerminal(output);
            }
        } else {
            printTerminal(`-bash: ${cmd}: command not found`, true);
        }
    }

    // Tıklanınca input'a odaklan
    document.querySelector('.bg-gray-900').addEventListener('click', () => {
        termInput.focus();
    });
});
