<?php
/*
 * Car Armour SG : envoi du formulaire de contact (/contact/).
 * Heberge sur le cPanel de l'agence, derriere Cloudflare.
 *
 * Envoi en SMTP authentifie sur le serveur mail de l'agence. Les identifiants
 * sont dans un .env HORS du repo : /home/<compte>/.env, un niveau au-dessus de
 * public_html (voir .env.example). Aucune dependance, pas de composer.
 *
 * Fichier ecrit a la main, PAS genere par build.py : il vit dans le dossier de
 * sortie /contact/ a cote de l'index.html genere, que build.py reecrit sans
 * toucher au reste. La preproduction GitHub Pages n'execute pas PHP : le
 * formulaire n'y appelle pas ce script (formEndpoint vide en --noindex).
 *
 * Repond 200 si le mail est parti, 400 si la saisie est invalide, 405 hors
 * POST, 500 si l'envoi echoue (detail dans le journal d'erreurs PHP).
 * main.js n'affiche que succes / echec.
 */

header('Content-Type: application/json; charset=utf-8');
header('X-Robots-Tag: noindex');

function reply($code, $msg) {
    http_response_code($code);
    echo json_encode(['ok' => $code === 200, 'message' => $msg]);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') reply(405, 'Method not allowed');

// Champ piege : un humain ne le voit pas, un robot le remplit. On repond 200
// pour ne rien lui apprendre.
if (!empty($_POST['website'])) reply(200, 'ok');

// ── Configuration ────────────────────────────────────────────────────────────
function load_env() {
    foreach ([dirname(__DIR__, 2) . '/.env', dirname(__DIR__) . '/.env'] as $path) {
        if (!is_readable($path)) continue;
        $env = [];
        foreach (file($path, FILE_IGNORE_NEW_LINES) as $line) {
            $line = trim($line);
            if ($line === '' || $line[0] === '#' || strpos($line, '=') === false) continue;
            [$k, $v] = explode('=', $line, 2);
            $env[trim($k)] = trim(trim($v), "\"'");
        }
        return $env;
    }
    return null;
}

$cfg = load_env();
foreach (['SMTP_HOST', 'SMTP_PORT', 'SMTP_USER', 'SMTP_PASS', 'MAIL_FROM', 'MAIL_TO'] as $k) {
    if (empty($cfg[$k])) { error_log("contact/send.php : $k manquant dans .env"); reply(500, 'Not configured'); }
}

// ── Saisie ───────────────────────────────────────────────────────────────────
function field($name, $max) {
    $v = trim((string)($_POST[$name] ?? ''));
    $v = str_replace(["\r\n", "\r"], "\n", $v);
    return mb_substr($v, 0, $max, 'UTF-8');
}
function oneline($v) {   // aucun saut de ligne dans ce qui touche aux en-tetes
    return trim(preg_replace('/[\r\n\t]+/', ' ', $v));
}

$name    = oneline(field('name', 120));
$phone   = oneline(field('phone', 40));
$email   = oneline(field('email', 160));
$car     = oneline(field('car', 120));
$postal  = oneline(field('postal', 6));
$service = oneline(field('service', 60));
$message = field('message', 4000);

if ($name === '' || $phone === '' || $car === '') reply(400, 'Missing fields');
if ($email !== '' && !filter_var($email, FILTER_VALIDATE_EMAIL)) reply(400, 'Invalid email');
if ($postal !== '' && !preg_match('/^\d{6}$/', $postal)) reply(400, 'Invalid postal code');
if (preg_match('/https?:\/\//i', $name . $car)) reply(400, 'Invalid input');

// Derriere Cloudflare, REMOTE_ADDR est l'adresse de Cloudflare, pas du visiteur
$ip = $_SERVER['HTTP_CF_CONNECTING_IP'] ?? $_SERVER['REMOTE_ADDR'] ?? '?';
$ip = preg_replace('/[^0-9a-fA-F:.]/', '', $ip);

$body = "New message from the cararmour.sg contact form\n\n"
      . "Name:         $name\n"
      . "Phone:        $phone\n"
      . "Email:        " . ($email ?: '-') . "\n"
      . "Car model:    $car\n"
      . "Postal code:  " . ($postal ?: '-') . "\n"
      . "Service:      " . ($service ?: '-') . "\n\n"
      . "Message:\n" . ($message !== '' ? $message : '-') . "\n\n"
      . "--\nSent " . date('Y-m-d H:i') . " from " . $ip . "\n";

// ── SMTP ─────────────────────────────────────────────────────────────────────
function smtp_read($fp) {
    $data = '';
    while (($line = fgets($fp, 515)) !== false) {
        $data .= $line;
        if (!isset($line[3]) || $line[3] === ' ') break;   // derniere ligne d'une reponse
    }
    return $data;
}
function smtp_cmd($fp, $cmd, $expect, $label = null) {
    if ($cmd !== null) fwrite($fp, $cmd . "\r\n");
    $res = smtp_read($fp);
    if (!in_array((int)substr($res, 0, 3), (array)$expect, true)) {
        throw new RuntimeException(($label ?? strtok((string)$cmd, ' ')) . ' -> ' . trim($res));
    }
    return $res;
}
function header_encode($text) {
    return '=?UTF-8?B?' . base64_encode($text) . '?=';
}

function smtp_send($cfg, $subject, $body, $replyTo) {
    $port   = (int)$cfg['SMTP_PORT'];
    $secure = strtolower($cfg['SMTP_SECURE'] ?? ($port === 465 ? 'ssl' : 'tls'));
    $remote = ($secure === 'ssl' ? 'ssl://' : 'tcp://') . $cfg['SMTP_HOST'] . ':' . $port;

    $fp = @stream_socket_client($remote, $errno, $errstr, 15);
    if (!$fp) throw new RuntimeException("connexion $remote : $errstr ($errno)");
    stream_set_timeout($fp, 15);

    try {
        $helo = 'EHLO cararmour.sg';
        smtp_cmd($fp, null, 220, 'accueil');
        smtp_cmd($fp, $helo, 250);
        if ($secure === 'tls') {
            smtp_cmd($fp, 'STARTTLS', 220);
            if (!stream_socket_enable_crypto($fp, true, STREAM_CRYPTO_METHOD_TLS_CLIENT)) {
                throw new RuntimeException('STARTTLS : negociation TLS impossible');
            }
            smtp_cmd($fp, $helo, 250);
        }
        smtp_cmd($fp, 'AUTH LOGIN', 334);
        smtp_cmd($fp, base64_encode($cfg['SMTP_USER']), 334, 'AUTH utilisateur');
        smtp_cmd($fp, base64_encode($cfg['SMTP_PASS']), 235, 'AUTH mot de passe');
        smtp_cmd($fp, 'MAIL FROM:<' . $cfg['MAIL_FROM'] . '>', 250);
        smtp_cmd($fp, 'RCPT TO:<' . $cfg['MAIL_TO'] . '>', [250, 251]);
        smtp_cmd($fp, 'DATA', 354);

        $fromName = $cfg['MAIL_FROM_NAME'] ?? 'Car Armour website';
        $headers = [
            'Date: ' . date('r'),
            'From: ' . header_encode($fromName) . ' <' . $cfg['MAIL_FROM'] . '>',
            'To: <' . $cfg['MAIL_TO'] . '>',
            'Subject: ' . header_encode($subject),
            'Message-ID: <' . bin2hex(random_bytes(12)) . '@cararmour.sg>',
            'MIME-Version: 1.0',
            'Content-Type: text/plain; charset=UTF-8',
            'Content-Transfer-Encoding: base64',
        ];
        if ($replyTo !== '') $headers[] = "Reply-To: <$replyTo>";   // repondre = ecrire au client

        // base64 : aucune ligne ne commence par un point, pas de dot-stuffing
        $data = implode("\r\n", $headers) . "\r\n\r\n"
              . rtrim(chunk_split(base64_encode($body), 76, "\r\n")) . "\r\n.";
        smtp_cmd($fp, $data, 250, 'DATA contenu');
        fwrite($fp, "QUIT\r\n");
    } finally {
        fclose($fp);
    }
}

try {
    smtp_send($cfg, "Website enquiry: $name, $car", $body, $email);
} catch (Throwable $e) {
    error_log('contact/send.php : ' . $e->getMessage());
    reply(500, 'Mail not sent');
}
reply(200, 'ok');
