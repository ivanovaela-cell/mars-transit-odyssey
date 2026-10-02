# -*- coding: utf-8 -*-
"""
Builder for Mars Transit Odyssey: Phase 1 (Intro, Crew Selection, LEO Docking & Refueling)
"""

import sys
sys.path.append(r'D:\mars-transit-odyssey')
from textures_b64 import EARTH_B64, CLOUDS_B64, SPEC_B64, MARS_B64, SUN_B64, MOON_B64

with open(r'D:\mars-transit-odyssey\libs\three.min.js', 'r', encoding='utf-8') as f:
    three_src = f.read()

with open(r'D:\mars-transit-odyssey\libs\OrbitControls.js', 'r', encoding='utf-8') as f:
    orbit_src = f.read()

HTML_CONTENT = r'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Арес-1: Марсианский транзит | 2038</title>
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
      -webkit-user-select: none;
    }
    body, html {
      width: 100%;
      height: 100%;
      overflow: hidden;
      background-color: #020409;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      color: #e2e8f0;
    }

    /* Screen Management */
    .screen {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      display: none;
      z-index: 10;
      transition: opacity 0.5s ease;
    }
    .screen.active {
      display: flex;
      opacity: 1;
    }

    /* UI Glass Panels */
    .glass-card {
      background: rgba(8, 14, 28, 0.88);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(0, 210, 255, 0.28);
      border-radius: 14px;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6), inset 0 0 20px rgba(0, 210, 255, 0.08);
    }

    /* Top Bar */
    .top-bar {
      position: absolute;
      top: 16px;
      left: 20px;
      right: 20px;
      height: 56px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 24px;
      z-index: 100;
    }
    .game-logo {
      font-size: 18px;
      font-weight: 800;
      letter-spacing: 2px;
      text-transform: uppercase;
      background: linear-gradient(90deg, #00d2ff, #3a7bd5, #ff5e62);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .top-controls {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .icon-btn {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #9cb3d1;
      padding: 6px 14px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }
    .icon-btn:hover {
      background: rgba(0, 210, 255, 0.2);
      color: #00f0ff;
      border-color: #00f0ff;
    }

    /* ========================================================
       1. SCREEN INTRO (CINEMATIC)
       ======================================================== */
    #screen-intro {
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      background: radial-gradient(circle at center, #0a1630 0%, #020409 80%);
      padding: 30px;
    }
    .intro-video-container {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      overflow: hidden;
      z-index: 1;
    }
    #intro-video {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
    .intro-content {
      position: relative;
      z-index: 2;
      max-width: 680px;
      padding: 40px;
    }
    .intro-year {
      font-size: 16px;
      letter-spacing: 6px;
      color: #00f0ff;
      text-transform: uppercase;
      margin-bottom: 12px;
      font-weight: 700;
    }
    .intro-title {
      font-size: 38px;
      font-weight: 900;
      line-height: 1.2;
      letter-spacing: 2px;
      margin-bottom: 20px;
      text-transform: uppercase;
      background: linear-gradient(135deg, #ffffff 0%, #a5c7f7 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .intro-text {
      font-size: 15px;
      line-height: 1.7;
      color: #94a3b8;
      margin-bottom: 30px;
    }
    .btn-glow {
      background: linear-gradient(135deg, #00d2ff 0%, #0066cc 100%);
      color: white;
      border: none;
      padding: 14px 36px;
      border-radius: 30px;
      font-size: 16px;
      font-weight: 700;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      cursor: pointer;
      box-shadow: 0 0 25px rgba(0, 210, 255, 0.4);
      transition: all 0.25s;
    }
    .btn-glow:hover {
      transform: scale(1.05);
      box-shadow: 0 0 35px rgba(0, 210, 255, 0.7);
    }

    /* ========================================================
       2. SCREEN CREW (BRIEFING & SELECTION)
       ======================================================== */
    #screen-crew {
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 90px 20px 30px 20px;
      background: radial-gradient(circle at top, #091a38 0%, #020409 70%);
      overflow-y: auto;
    }
    .crew-panel {
      max-width: 980px;
      width: 100%;
      padding: 28px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }
    .briefing-box {
      background: rgba(0, 210, 255, 0.05);
      border-left: 4px solid #00f0ff;
      padding: 14px 18px;
      border-radius: 6px;
      font-size: 14px;
      color: #cbd5e1;
      line-height: 1.6;
    }
    .crew-tabs {
      display: flex;
      gap: 10px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 10px;
    }
    .tab-btn {
      background: transparent;
      border: none;
      color: #94a3b8;
      font-size: 14px;
      font-weight: 700;
      padding: 8px 18px;
      cursor: pointer;
      border-radius: 6px;
      transition: all 0.2s;
    }
    .tab-btn.active {
      background: rgba(0, 210, 255, 0.2);
      color: #00f0ff;
    }
    .crew-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 16px;
      margin: 10px 0;
    }
    .crew-card {
      background: rgba(15, 25, 48, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 10px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      transition: all 0.2s;
    }
    .crew-card:hover {
      border-color: rgba(0, 210, 255, 0.4);
      transform: translateY(-2px);
    }
    .crew-avatar {
      font-size: 32px;
      margin-bottom: 4px;
    }
    .crew-name {
      font-size: 15px;
      font-weight: 700;
      color: #ffffff;
    }
    .crew-role {
      font-size: 12px;
      font-weight: 600;
      color: #00f0ff;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .crew-perk {
      font-size: 11px;
      color: #94a3b8;
      background: rgba(255, 255, 255, 0.04);
      padding: 6px 8px;
      border-radius: 4px;
      margin-top: 4px;
    }

    /* ========================================================
       3. SCREEN GAMEPLAY (LEO DOCKING & REFUELING)
       ======================================================== */
    #screen-gameplay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
    }
    #gameplay-canvas {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 1;
    }

    /* Docking HUD Overlay */
    .hud-layer {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 10;
      pointer-events: none;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 85px 20px 20px 20px;
    }
    .clickable {
      pointer-events: auto;
    }

    /* Docking Telemetry Panel (Left) */
    .docking-telemetry {
      position: absolute;
      top: 85px;
      left: 20px;
      width: 320px;
      padding: 18px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .hud-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 13px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      padding-bottom: 6px;
    }
    .hud-label {
      color: #7b91b0;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.8px;
    }
    .hud-value {
      font-family: 'Consolas', monospace;
      font-weight: 700;
      color: #00f0ff;
      font-size: 14px;
    }
    .hud-value.danger {
      color: #ff4757;
    }
    .hud-value.success {
      color: #00e699;
    }

    /* Center Docking Target Reticle */
    .reticle-container {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      pointer-events: none;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }
    .docking-crosshair {
      width: 180px;
      height: 180px;
      border: 2px dashed rgba(0, 210, 255, 0.4);
      border-radius: 50%;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s;
    }
    .docking-crosshair::before, .docking-crosshair::after {
      content: '';
      position: absolute;
      background: #00f0ff;
    }
    .docking-crosshair::before {
      width: 28px;
      height: 2px;
    }
    .docking-crosshair::after {
      width: 2px;
      height: 28px;
    }
    .target-marker {
      width: 24px;
      height: 24px;
      border: 2px solid #00e699;
      position: absolute;
      border-radius: 4px;
      transition: transform 0.05s linear;
    }
    .alignment-text {
      margin-top: 10px;
      font-family: 'Consolas', monospace;
      font-size: 12px;
      font-weight: 700;
      color: #00f0ff;
      background: rgba(5, 15, 35, 0.7);
      padding: 4px 10px;
      border-radius: 4px;
      border: 1px solid rgba(0, 210, 255, 0.3);
    }

    /* Flight & Thruster Control Dock (Bottom) */
    .control-dock {
      align-self: center;
      padding: 16px 28px;
      display: flex;
      align-items: center;
      gap: 20px;
      max-width: 850px;
      width: 95%;
      margin-bottom: 10px;
    }
    .rcs-grid {
      display: grid;
      grid-template-columns: repeat(3, 44px);
      gap: 6px;
    }
    .rcs-btn {
      width: 44px;
      height: 44px;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 8px;
      color: #00f0ff;
      font-size: 16px;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.1s;
    }
    .rcs-btn:active {
      background: rgba(0, 210, 255, 0.35);
      transform: scale(0.94);
    }

    /* Refueling Modal / Dialog */
    .modal-overlay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(2, 4, 10, 0.8);
      backdrop-filter: blur(8px);
      z-index: 200;
      display: none;
      justify-content: center;
      align-items: center;
      padding: 20px;
    }
    .modal-overlay.show {
      display: flex;
    }
    .modal-card {
      max-width: 520px;
      width: 100%;
      padding: 30px;
      text-align: center;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }
    .modal-title {
      font-size: 22px;
      font-weight: 800;
      color: #00e699;
      text-transform: uppercase;
      letter-spacing: 1px;
    }
    .fuel-gauge-container {
      width: 100%;
      height: 24px;
      background: rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      overflow: hidden;
      border: 1px solid rgba(255, 255, 255, 0.15);
      position: relative;
    }
    .fuel-gauge-fill {
      height: 100%;
      width: 8%;
      background: linear-gradient(90deg, #ff9900, #00e699);
      transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .fuel-gauge-text {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      font-family: 'Consolas', monospace;
      font-size: 12px;
      font-weight: 700;
      color: #ffffff;
      text-shadow: 0 1px 4px rgba(0, 0, 0, 0.8);
    }

    /* Toast */
    .toast-msg {
      position: absolute;
      top: 90px;
      left: 50%;
      transform: translateX(-50%);
      padding: 12px 24px;
      background: rgba(8, 20, 42, 0.95);
      border-left: 4px solid #00f0ff;
      border-radius: 8px;
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.8);
      font-size: 14px;
      opacity: 0;
      transition: opacity 0.3s ease;
      z-index: 300;
      pointer-events: none;
    }
    .toast-msg.show {
      opacity: 1;
    }
  </style>
</head>
<body>

  <!-- Top Bar -->
  <div class="top-bar glass-card">
    <div class="game-logo">
      <span>🚀 АРЕС-1 // 2038</span>
    </div>
    <div class="top-controls">
      <button class="icon-btn" id="lang-btn" onclick="toggleLanguage()">RU | EN</button>
      <button class="icon-btn" id="audio-btn" onclick="toggleAudio()">🔊</button>
    </div>
  </div>

  <!-- Toast -->
  <div class="toast-msg" id="toast">Сообщение ЦУП</div>

  <!-- =========================================================
       1. SCREEN: INTRO & VIDEO PROLOGUE
       ========================================================= -->
  <div class="screen active" id="screen-intro">
    <div class="intro-video-container">
      <!-- Fallback or User video -->
      <video id="intro-video" loop muted playsinline poster="">
        <source src="videos/launch.mp4" type="video/mp4">
      </video>
    </div>
    
    <div class="intro-content glass-card">
      <div class="intro-year" id="i18n-intro-year">2038 ГОД // КОСМОДРОМ STARBASE</div>
      <div class="intro-title" id="i18n-intro-title">АРЕС-1: МАРСИАНСКИЙ ТРАНЗИТ</div>
      <div class="intro-text" id="i18n-intro-text">
        Годы подготовки завершены. Многоразовый межпланетный лайнер нового поколения выведен на опорную околоземную орбиту. 
        Баки корабля пусты после старта. До открытия марсианского окна — считанные дни. Начните операцию!
      </div>
      <button class="btn-glow" onclick="showCrewScreen()" id="i18n-btn-start">ПРИСТУПИТЬ К МИССИИ ➔</button>
    </div>
  </div>

  <!-- =========================================================
       2. SCREEN: CREW SELECTION & BRIEFING
       ========================================================= -->
  <div class="screen" id="screen-crew">
    <div class="crew-panel glass-card">
      <div style="font-size: 20px; font-weight: 800; color: #00f0ff; letter-spacing: 1px;" id="i18n-crew-heading">
        БОРТОВОЙ ЖУРНАЛ: ЭКИПАЖ «АРЕС-1»
      </div>
      
      <div class="briefing-box" id="i18n-crew-briefing">
        🎙️ <strong>ЦУП (Хьюстон / Королёв):</strong> «"Арес", вы на расчетной орбите 320 км. Первый танкер заправки Tanker-01 уже выполнил фазирование и находится в зоне видимости. Подтвердите допуск экипажа к миссии!»
      </div>

      <div class="crew-tabs">
        <button class="tab-btn active" onclick="switchCrewTab('canon', this)" id="i18n-tab-canon">ШТАТНЫЙ ЭКИПАЖ (КАНОН)</button>
        <button class="tab-btn" onclick="switchCrewTab('custom', this)" id="i18n-tab-custom">КОНСТРУКТОР ЭКИПАЖА</button>
      </div>

      <!-- Canon Crew Grid -->
      <div class="crew-grid" id="canon-crew-grid">
        <div class="crew-card">
          <div class="crew-avatar">👨‍🚀</div>
          <div class="crew-name">Алекс Вэнс</div>
          <div class="crew-role" id="i18n-role-cmdr">Командир миссии</div>
          <div class="crew-perk">⭐ Перк: Хладнокровие (+15% при пожарах)</div>
        </div>
        <div class="crew-card">
          <div class="crew-avatar">👩‍🚀</div>
          <div class="crew-name">Елена Романова</div>
          <div class="crew-role" id="i18n-role-pilot">Главный пилот</div>
          <div class="crew-perk">⭐ Перк: Ас стыковки (+20% точность «Курс»)</div>
        </div>
        <div class="crew-card">
          <div class="crew-avatar">👨‍🔧</div>
          <div class="crew-name">Чэнь Вэй</div>
          <div class="crew-role" id="i18n-role-eng">Бортинженер</div>
          <div class="crew-perk">⭐ Перк: Эксперт Raptor (-25% запчастей)</div>
        </div>
        <div class="crew-card">
          <div class="crew-avatar">👨‍⚕️</div>
          <div class="crew-name">д-р Маркус Рид</div>
          <div class="crew-role" id="i18n-role-doc">Судовой врач</div>
          <div class="crew-perk">⭐ Перк: Био-регенерация (+20% к здоровью)</div>
        </div>
      </div>

      <!-- Custom Crew Builder (Toggleable) -->
      <div id="custom-crew-box" style="display: none; font-size: 13px; color: #94a3b8; padding: 14px; background: rgba(0,0,0,0.3); border-radius: 8px;">
        <div>Распределите очки специализации экипажа (доступно: 12 очков):</div>
        <div style="display: flex; gap: 20px; margin-top: 10px;">
          <div>🚀 Пилотирование: <strong>+4</strong></div>
          <div>🔧 Инженерия: <strong>+4</strong></div>
          <div>🧬 Медицина: <strong>+2</strong></div>
          <div>🧠 Психика: <strong>+2</strong></div>
        </div>
      </div>

      <div style="display: flex; justify-content: flex-end; margin-top: 10px;">
        <button class="btn-glow" onclick="startDockingGameplay()" id="i18n-btn-confirm-crew">
          УТВЕРДИТЬ ЭКИПАЖ И ВЫЙТИ НА СТЫКОВКУ ➔
        </button>
      </div>
    </div>
  </div>

  <!-- =========================================================
       3. SCREEN: GAMEPLAY (LEO DOCKING & REFUELING)
       ========================================================= -->
  <div class="screen" id="screen-gameplay">
    <div id="gameplay-canvas"></div>

    <div class="hud-layer">
      <!-- Left Telemetry Panel -->
      <div class="docking-telemetry glass-card clickable">
        <div class="hud-row">
          <span class="hud-label" id="i18n-hud-mode">РЕЖИМ</span>
          <span class="hud-value" style="color: #00e699;">СБЛИЖЕНИЕ («КУРС»)</span>
        </div>
        <div class="hud-row">
          <span class="hud-label" id="i18n-hud-target">ЦЕЛЬ</span>
          <span class="hud-value">TANKER-01 (МЕТАН)</span>
        </div>
        <div class="hud-row">
          <span class="hud-label" id="i18n-hud-dist">ДИСТАНЦИЯ</span>
          <span class="hud-value" id="hud-dist">48.2 м</span>
        </div>
        <div class="hud-row">
          <span class="hud-label" id="i18n-hud-vel">СКОРОСТЬ СБЛИЖЕНИЯ</span>
          <span class="hud-value" id="hud-vel">0.42 м/с</span>
        </div>
        <div class="hud-row">
          <span class="hud-label" id="i18n-hud-align">ОТКЛОНЕНИЕ ОСЕЙ</span>
          <span class="hud-value" id="hud-align">±1.4°</span>
        </div>
        <div class="hud-row" style="border: none;">
          <span class="hud-label" id="i18n-hud-fuel">БАКИ КОРАБЛЯ</span>
          <span class="hud-value highlight-fuel" id="hud-propellant">8% (96 т)</span>
        </div>
      </div>

      <!-- Center Docking Reticle -->
      <div class="reticle-container">
        <div class="docking-crosshair" id="crosshair">
          <div class="target-marker" id="target-marker"></div>
        </div>
        <div class="alignment-text" id="hud-alignment-status">ВЫРАВНИВАНИЕ: ДОПУСТИМО</div>
      </div>

      <!-- Bottom Control Dock -->
      <div class="control-dock glass-card clickable">
        <div style="font-size: 11px; color: #7b91b0; font-weight: 700; text-transform: uppercase;">
          РУЧНЫЕ ДВИГАТЕЛИ RCS:
        </div>
        
        <div class="rcs-grid">
          <div></div>
          <button class="rcs-btn" onmousedown="applyThrust('up')" title="Смещение вверх">▲</button>
          <div></div>
          <button class="rcs-btn" onmousedown="applyThrust('left')" title="Смещение влево">◀</button>
          <button class="rcs-btn" onmousedown="applyThrust('forward')" title="Тяга вперед (W)" style="color: #00e699;">W</button>
          <button class="rcs-btn" onmousedown="applyThrust('right')" title="Смещение вправо">▶</button>
          <div></div>
          <button class="rcs-btn" onmousedown="applyThrust('down')" title="Смещение вниз">▼</button>
          <button class="rcs-btn" onmousedown="applyThrust('back')" title="Торможение назад (S)" style="color: #ff9900;">S</button>
        </div>

        <div style="flex: 1; font-size: 12px; color: #94a3b8; line-height: 1.5;">
          💡 <strong>Инструкция:</strong> Подведите носовой штырь к стыковочному кольцу танкера со скоростью менее <strong>0.20 м/с</strong> и отклонением осей менее <strong>2.0°</strong> для жесткого захвата!
        </div>
      </div>
    </div>
  </div>

  <!-- Refueling Modal -->
  <div class="modal-overlay" id="refuel-modal">
    <div class="modal-card glass-card">
      <div class="modal-title" id="i18n-modal-title">🎯 СТЫКОВКА УСПЕШНА!</div>
      <div style="font-size: 14px; color: #cbd5e1;">
        Стыковочный узел зафиксирован. Магистрали перекачки криогенного метана и жидкого кислорода подсоединены к бакам «Ареса».
      </div>

      <div class="fuel-gauge-container">
        <div class="fuel-gauge-fill" id="modal-fuel-fill"></div>
        <div class="fuel-gauge-text" id="modal-fuel-text">8% (96 / 1200 тонн)</div>
      </div>

      <div style="display: flex; gap: 12px; justify-content: center;">
        <button class="btn-glow" id="btn-ullage" onclick="triggerUllageBurn()" style="background: linear-gradient(135deg, #ff9900, #cc6600);">
          🔥 Осаждение топлива (Ullage Burn)
        </button>
        <button class="btn-glow" id="btn-pump" onclick="transferPropellant()" disabled style="opacity: 0.5;">
          ⚡ Перекачать 1200 тонн
        </button>
      </div>

      <div id="tmi-ready-box" style="display: none; margin-top: 10px;">
        <button class="btn-glow" onclick="launchTMI()" style="width: 100%; background: linear-gradient(135deg, #00e699, #009966);">
          🚀 ОТСТЫКОВКА И РАЗГОННЫЙ ИМПУЛЬС TMI ➔
        </button>
      </div>
    </div>
  </div>

  <!-- Three.js + OrbitControls (Inlined) -->
  <script>
__THREE_SRC__
  </script>
  <script>
__ORBIT_SRC__
  </script>

  <script>
    /* ==========================================================
       1. ЛОКАЛИЗАЦИЯ (i18n: RU | EN)
       ========================================================== */
    let currentLang = 'ru';

    const DICT = {
      ru: {
        intro_year: "2038 ГОД // КОСМОДРОМ STARBASE",
        intro_title: "АРЕС-1: МАРСИАНСКИЙ ТРАНЗИТ",
        intro_text: "Годы подготовки завершены. Многоразовый межпланетный лайнер нового поколения выведен на опорную околоземную орбиту. Баки корабля пусты после старта. До открытия марсианского окна — считанные дни. Начните операцию!",
        btn_start: "ПРИСТУПИТЬ К МИССИИ ➔",
        crew_heading: "БОРТОВОЙ ЖУРНАЛ: ЭКИПАЖ «АРЕС-1»",
        crew_briefing: "🎙️ <strong>ЦУП (Хьюстон / Королёв):</strong> «\"Арес\", вы на расчетной орбите 320 км. Первый танкер заправки Tanker-01 уже выполнил фазирование и находится в зоне видимости. Подтвердите допуск экипажа к миссии!»",
        tab_canon: "ШТАТНЫЙ ЭКИПАЖ (КАНОН)",
        tab_custom: "КОНСТРУКТОР ЭКИПАЖА",
        btn_confirm_crew: "УТВЕРДИТЬ ЭКИПАЖ И ВЫЙТИ НА СТЫКОВКУ ➔",
        modal_title: "🎯 СТЫКОВКА УСПЕШНА!",
        toast_dock_success: "Жёсткий захват стыковочного узла зафиксирован!",
        toast_ullage: "Импульс осаждения топлива (Ullage Burn) завершен! Топливо на дне баков.",
        toast_refuel_done: "Баки полностью заправлены! 1200 тонн криогена загружено.",
        toast_tmi: "Рапторы включены! Выход на траекторию к Марсу!"
      },
      en: {
        intro_year: "YEAR 2038 // STARBASE SPACEPORT",
        intro_title: "ARES-1: MARTIAN TRANSIT",
        intro_text: "Years of training are complete. The next-generation reusable interplanetary Starship is in low Earth parking orbit. Propellant tanks are dry after launch. The Mars transfer window opens in days. Initiate operation!",
        btn_start: "BEGIN MISSION ➔",
        crew_heading: "MISSION LOG: ARES-1 CREW",
        crew_briefing: "🎙️ <strong>MISSION CONTROL:</strong> 'Ares, you are in nominal 320 km parking orbit. Orbital Tanker-01 has completed rendezvous phasing and is in visual range. Confirm crew flight clearance!'",
        tab_canon: "NOMINAL CREW (CANON)",
        tab_custom: "CUSTOM CREW BUILDER",
        btn_confirm_crew: "CONFIRM CREW & PROCEED TO DOCKING ➔",
        modal_title: "🎯 HARD CAPTURE CONFIRMED!",
        toast_dock_success: "Docking latch engaged! Cryogenic umbilicals connected.",
        toast_ullage: "Ullage burn complete! Propellant settled at tank sumps.",
        toast_refuel_done: "Tanks full! 1,200 tons of liquid methane & LOX transferred.",
        toast_tmi: "Raptors ignited! On trajectory to Mars!"
      }
    };

    function toggleLanguage() {
      currentLang = currentLang === 'ru' ? 'en' : 'ru';
      document.getElementById('lang-btn').innerText = currentLang === 'ru' ? 'RU | EN' : 'EN | RU';
      applyLanguage();
    }

    function applyLanguage() {
      const d = DICT[currentLang];
      document.getElementById('i18n-intro-year').innerText = d.intro_year;
      document.getElementById('i18n-intro-title').innerText = d.intro_title;
      document.getElementById('i18n-intro-text').innerText = d.intro_text;
      document.getElementById('i18n-btn-start').innerText = d.btn_start;
      document.getElementById('i18n-crew-heading').innerText = d.crew_heading;
      document.getElementById('i18n-crew-briefing').innerHTML = d.crew_briefing;
      document.getElementById('i18n-tab-canon').innerText = d.tab_canon;
      document.getElementById('i18n-tab-custom').innerText = d.tab_custom;
      document.getElementById('i18n-btn-confirm-crew').innerText = d.btn_confirm_crew;
      document.getElementById('i18n-modal-title').innerText = d.modal_title;
    }

    /* ==========================================================
       2. ЗВУКОВОЙ ДВИЖОК (WEB AUDIO API)
       ========================================================== */
    let audioCtx = null;
    let audioEnabled = true;

    function initAudio() {
      if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      }
    }

    function playRCSThrustSound() {
      if (!audioEnabled) return;
      initAudio();
      try {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'white' || 'square';
        osc.frequency.setValueAtTime(120, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.04, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.12);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.12);
      } catch (e) {}
    }

    function playDockingClankSound() {
      if (!audioEnabled) return;
      initAudio();
      try {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(90, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.8);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.8);
      } catch (e) {}
    }

    function toggleAudio() {
      audioEnabled = !audioEnabled;
      document.getElementById('audio-btn').innerText = audioEnabled ? '🔊' : '🔇';
    }

    function showToast(msg) {
      const toast = document.getElementById('toast');
      toast.innerText = msg;
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 3500);
    }

    /* ==========================================================
       3. ПЕРЕКЛЮЧЕНИЕ ЭКРАНОВ
       ========================================================== */
    function showScreen(id) {
      document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
      document.getElementById(id).classList.add('active');
    }

    function showCrewScreen() {
      showScreen('screen-crew');
    }

    function switchCrewTab(tab, btn) {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      if (tab === 'canon') {
        document.getElementById('canon-crew-grid').style.display = 'grid';
        document.getElementById('custom-crew-box').style.display = 'none';
      } else {
        document.getElementById('canon-crew-grid').style.display = 'none';
        document.getElementById('custom-crew-box').style.display = 'block';
      }
    }

    function startDockingGameplay() {
      showScreen('screen-gameplay');
      initThreeJSDocking();
    }

    /* ==========================================================
       4. 3D СЦЕНА СТЫКОВКИ НА ОРБИТЕ (THREE.JS)
       ========================================================== */
    let scene, camera, renderer, controls;
    let earthMesh, starshipGroup, tankerGroup;
    let isDocked = false;

    // Параметры физики стыковки
    let shipPos = { x: 0, y: 0, z: -48.0 }; // Старт в 48 метрах от танкера
    let shipVel = { x: 0, y: 0, z: 0.45 }; // Медленное сближение 0.45 м/с
    let shipRot = { pitch: 0.02, yaw: -0.015, roll: 0 };
    let propellantTons = 96; // 8%

    const TEXTURES_DATA = {
      earth: "__EARTH_B64__",
      clouds: "__CLOUDS_B64__",
      specular: "__SPEC_B64__"
    };

    function initThreeJSDocking() {
      if (scene) return; // уже инициализировано

      const container = document.getElementById('gameplay-canvas');
      scene = new THREE.Scene();
      scene.fog = new THREE.FogExp2(0x020409, 0.0008);

      camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 2000);
      camera.position.set(0, 8, -25);

      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
      renderer.setSize(window.innerWidth, window.innerHeight);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.2;
      container.appendChild(renderer.domElement);

      controls = new THREE.OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.05;
      controls.maxDistance = 100;
      controls.minDistance = 6;

      // Освещение (Солнце на орбите)
      const sunLight = new THREE.DirectionalLight(0xfffaee, 2.8);
      sunLight.position.set(200, 100, 150);
      scene.add(sunLight);

      const ambientLight = new THREE.AmbientLight(0x1a263d, 0.6);
      scene.add(ambientLight);

      // Земля внизу на горизонте (Радиус 400 на дистанции 420)
      const texLoader = new THREE.TextureLoader();
      const earthTex = texLoader.load(TEXTURES_DATA.earth);
      const cloudsTex = texLoader.load(TEXTURES_DATA.clouds);
      const specTex = texLoader.load(TEXTURES_DATA.specular);

      const earthGroup = new THREE.Group();
      earthGroup.position.set(0, -430, 0);

      const earthGeo = new THREE.SphereGeometry(400, 64, 64);
      const earthMat = new THREE.MeshPhongMaterial({
        map: earthTex,
        specularMap: specTex,
        specular: new THREE.Color(0x334466),
        shininess: 25
      });
      earthMesh = new THREE.Mesh(earthGeo, earthMat);
      earthGroup.add(earthMesh);

      const cloudsGeo = new THREE.SphereGeometry(403, 64, 64);
      const cloudsMat = new THREE.MeshStandardMaterial({
        map: cloudsTex,
        transparent: true,
        opacity: 0.85
      });
      const cloudsMesh = new THREE.Mesh(cloudsGeo, cloudsMat);
      earthGroup.add(cloudsMesh);
      scene.add(earthGroup);

      // Звездное небо
      const starGeo = new THREE.BufferGeometry();
      const starCount = 3500;
      const starPos = new Float32Array(starCount * 3);
      for (let i = 0; i < starCount * 3; i++) {
        starPos[i] = (Math.random() - 0.5) * 1600;
      }
      starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
      const starMat = new THREE.PointsMaterial({ size: 1.8, color: 0xffffff, transparent: true, opacity: 0.8 });
      scene.add(new THREE.Points(starGeo, starMat));

      // 1. КОРАБЛЬ ИГРОКА (STARSHIP ARES-1)
      starshipGroup = createStarshipModel(0xf5f5f7, true);
      scene.add(starshipGroup);

      // 2. ЦЕЛЕВОЙ ТАНКЕР (ORBITAL TANKER-01)
      tankerGroup = createTankerModel();
      tankerGroup.position.set(0, 0, 0);
      scene.add(tankerGroup);

      // Обработка клавиш клавиатуры (W, S, A, D, Q, E)
      window.addEventListener('keydown', handleKeyDown);
      window.addEventListener('resize', onWindowResize);

      animateDocking();
    }

    function createStarshipModel(hullColor = 0xf5f5f7, isPlayer = true) {
      const group = new THREE.Group();
      const steelMat = new THREE.MeshStandardMaterial({ color: hullColor, metalness: 0.85, roughness: 0.18 });
      const heatShieldMat = new THREE.MeshStandardMaterial({ color: 0x111115, metalness: 0.3, roughness: 0.8 });

      // Корпус
      const hull = new THREE.Mesh(new THREE.CylinderGeometry(1.4, 1.4, 12, 32), steelMat);
      hull.rotation.x = Math.PI / 2;
      group.add(hull);

      // Носовой конус
      const nose = new THREE.Mesh(new THREE.ConeGeometry(1.4, 4.5, 32), steelMat);
      nose.position.z = 8.25;
      nose.rotation.x = Math.PI / 2;
      group.add(nose);

      // Стыковочный штырь на носу
      const probe = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.3, 1.5, 16), new THREE.MeshStandardMaterial({ color: 0x00f0ff }));
      probe.position.z = 10.8;
      probe.rotation.x = Math.PI / 2;
      group.add(probe);

      // Кормовые и носовые закрылки (Flaps)
      const flapMat = new THREE.MeshStandardMaterial({ color: 0x18181c, metalness: 0.7, roughness: 0.3 });
      const leftAft = new THREE.Mesh(new THREE.BoxGeometry(2.5, 0.1, 3.2), flapMat);
      leftAft.position.set(-2.4, 0, -4.5);
      group.add(leftAft);

      const rightAft = new THREE.Mesh(new THREE.BoxGeometry(2.5, 0.1, 3.2), flapMat);
      rightAft.position.set(2.4, 0, -4.5);
      group.add(rightAft);

      return group;
    }

    function createTankerModel() {
      const group = new THREE.Group();
      const tankerMat = new THREE.MeshStandardMaterial({ color: 0xdde2ea, metalness: 0.8, roughness: 0.25 });

      // Корпус танкера
      const body = new THREE.Mesh(new THREE.CylinderGeometry(1.8, 1.8, 14, 32), tankerMat);
      body.rotation.x = Math.PI / 2;
      group.add(body);

      // Стыковочный конус-приемник с неоновым кольцом
      const ringMat = new THREE.MeshBasicMaterial({ color: 0x00e699 });
      const dockRing = new THREE.Mesh(new THREE.TorusGeometry(1.2, 0.08, 16, 32), ringMat);
      dockRing.position.z = -7.1;
      group.add(dockRing);

      // Большие солнечные батареи танкера
      const panelMat = new THREE.MeshStandardMaterial({ color: 0x0044aa, metalness: 0.7, roughness: 0.3 });
      const p1 = new THREE.Mesh(new THREE.BoxGeometry(9.0, 0.1, 2.5), panelMat);
      p1.position.set(-6.5, 0, 0);
      group.add(p1);

      const p2 = new THREE.Mesh(new THREE.BoxGeometry(9.0, 0.1, 2.5), panelMat);
      p2.position.set(6.5, 0, 0);
      group.add(p2);

      return group;
    }

    /* ==========================================================
       5. УПРАВЛЕНИЕ ТЯГОЙ RCS
       ========================================================== */
    function applyThrust(type) {
      if (isDocked) return;
      playRCSThrustSound();

      const force = 0.05;
      if (type === 'forward') shipVel.z += force;
      if (type === 'back')    shipVel.z -= force;
      if (type === 'left')    shipVel.x -= force;
      if (type === 'right')   shipVel.x += force;
      if (type === 'up')      shipVel.y += force;
      if (type === 'down')    shipVel.y -= force;
    }

    function handleKeyDown(e) {
      if (isDocked) return;
      if (e.code === 'KeyW') applyThrust('forward');
      if (e.code === 'KeyS') applyThrust('back');
      if (e.code === 'KeyA') applyThrust('left');
      if (e.code === 'KeyD') applyThrust('right');
      if (e.code === 'KeyQ') applyThrust('up');
      if (e.code === 'KeyE') applyThrust('down');
    }

    function onWindowResize() {
      if (!camera || !renderer) return;
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    }

    /* ==========================================================
       6. ЦИКЛ АНИМАЦИИ И ФИЗИКИ СТЫКОВКИ
       ========================================================== */
    function animateDocking() {
      requestAnimationFrame(animateDocking);

      if (!isDocked) {
        // Движение корабля к танкеру
        shipPos.z += shipVel.z * 0.1;
        shipPos.x += shipVel.x * 0.1;
        shipPos.y += shipVel.y * 0.1;

        // Позиционирование Starship
        starshipGroup.position.set(shipPos.x, shipPos.y, shipPos.z);
        starshipGroup.rotation.set(shipRot.pitch, shipRot.yaw, shipRot.roll);

        // Расчет дистанции между стыковочным штырем и кольцом танкера
        const dist = Math.abs(shipPos.z - (-7.0));
        const approachVel = shipVel.z;
        const alignOffset = Math.sqrt(shipPos.x * shipPos.x + shipPos.y * shipPos.y);

        // Обновление HUD
        document.getElementById('hud-dist').innerText = dist.toFixed(1) + ' м';
        document.getElementById('hud-vel').innerText = approachVel.toFixed(2) + ' м/с';
        document.getElementById('hud-align').innerText = '±' + (alignOffset * 0.8).toFixed(1) + '°';

        // Движение маркера прицела
        const targetMarker = document.getElementById('target-marker');
        targetMarker.style.transform = `translate(${shipPos.x * 12}px, ${-shipPos.y * 12}px)`;

        // Проверка жесткой сцепки (Hard Capture)
        if (dist < 1.4 && dist > -1.0) {
          if (approachVel <= 0.25 && alignOffset < 1.2) {
            completeDocking();
          } else if (approachVel > 0.4) {
            showToast('⚠️ Слишком большая скорость сближения! Отскок!');
            shipVel.z = -0.15; // отскок
          }
        }
      }

      // Медленное вращение Земли внизу
      if (earthMesh) earthMesh.rotation.y += 0.0003;

      // Слежение камеры за кораблем
      if (starshipGroup) {
        controls.target.copy(starshipGroup.position);
      }

      controls.update();
      renderer.render(scene, camera);
    }

    /* ==========================================================
       7. СЦЕНА ДОЗАПРАВКИ (POST-DOCKING REFUELING)
       ========================================================== */
    function completeDocking() {
      isDocked = true;
      shipVel.z = 0; shipVel.x = 0; shipVel.y = 0;
      shipPos.z = -7.0; shipPos.x = 0; shipPos.y = 0;
      starshipGroup.position.set(0, 0, -7.0);

      playDockingClankSound();
      showToast(DICT[currentLang].toast_dock_success);

      document.getElementById('hud-dist').innerText = '0.0 м (ЗАХВАТ)';
      document.getElementById('hud-dist').classList.add('success');
      document.getElementById('crosshair').style.borderColor = '#00e699';

      setTimeout(() => {
        document.getElementById('refuel-modal').classList.add('show');
      }, 1200);
    }

    function triggerUllageBurn() {
      playRCSThrustSound();
      showToast(DICT[currentLang].toast_ullage);
      document.getElementById('btn-ullage').disabled = true;
      document.getElementById('btn-ullage').style.opacity = '0.4';
      document.getElementById('btn-pump').disabled = false;
      document.getElementById('btn-pump').style.opacity = '1';
    }

    function transferPropellant() {
      const btn = document.getElementById('btn-pump');
      btn.disabled = true;

      let p = 8;
      const interval = setInterval(() => {
        p += 4;
        if (p > 100) p = 100;
        document.getElementById('modal-fuel-fill').style.width = p + '%';
        const tons = Math.round((p / 100) * 1200);
        document.getElementById('modal-fuel-text').innerText = `${p}% (${tons} / 1200 тонн)`;
        document.getElementById('hud-propellant').innerText = `${p}% (${tons} т)`;

        if (p >= 100) {
          clearInterval(interval);
          showToast(DICT[currentLang].toast_refuel_done);
          document.getElementById('tmi-ready-box').style.display = 'block';
        }
      }, 80);
    }

    function launchTMI() {
      showToast(DICT[currentLang].toast_tmi);
      document.getElementById('refuel-modal').classList.remove('show');

      // Анимация включения вакуумных Рапторов и отлета к Марсу
      setTimeout(() => {
        alert(currentLang === 'ru' 
          ? '🎉 Поздравляем! Первый этап миссии «Арес-1» (Стыковка и дозаправка 1200 т) успешно завершен!\nКорабль лег на траекторию перелета к Марсу.' 
          : '🎉 Congratulations! Phase 1 of Ares-1 mission (Docking & 1,200t Refueling) successfully completed!\nStarship is on trajectory to Mars.');
      }, 1500);
    }
  </script>
</body>
</html>
'''

# Perform replacements of inlined three.js, orbitControls, and textures
final_html = HTML_CONTENT.replace('__THREE_SRC__', three_src)
final_html = final_html.replace('__ORBIT_SRC__', orbit_src)
final_html = final_html.replace('__EARTH_B64__', EARTH_B64)
final_html = final_html.replace('__CLOUDS_B64__', CLOUDS_B64)
final_html = final_html.replace('__SPEC_B64__', SPEC_B64)

with open(r'D:\mars-transit-odyssey\index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

# Also update the desktop copy so user can easily launch from Desktop
with open(r'C:\Users\User\Desktop\Полет на Марс 3D.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Game v1 (Intro, Crew, Docking, Refueling) built successfully on Drive D: and Desktop!")
