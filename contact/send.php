<?php
/*
 * Car Armour SG : envoi du formulaire de contact (/contact/).
 * Heberge sur le cPanel de l'agence, derriere Cloudflare.
 *
 * Fichier ecrit a la main, PAS genere par build.py : il vit dans le dossier de
 * sortie /contact/ a cote de l'index.html genere, que build.py reecrit sans
 * toucher au reste. La preproduction GitHub Pages n'execute pas PHP : le
 * formulaire n'y appelle pas ce script (formEndpoint vide en --noindex).
 *
 * Repond 200 si le mail est parti, 400 si la saisie est invalide, 405 hors
 * POST, 500 si mail() echoue. main.js n'affiche que succes / echec.
 */

const TO   = 'info@cararmour.sg';
const FROM = 'website@cararmour.sg';   // adresse du domaine, sinon SPF rejette

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

$subject = '=?UTF-8?B?' . base64_encode("Website enquiry: $name, $car") . '?=';
$headers = [
    'From: Car Armour website <' . FROM . '>',
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
];
if ($email !== '') $headers[] = "Reply-To: $email";   // repondre = ecrire au client

$ok = mail(TO, $subject, $body, implode("\r\n", $headers), '-f' . FROM);
$ok ? reply(200, 'ok') : reply(500, 'Mail not sent');
