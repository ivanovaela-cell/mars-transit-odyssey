# -*- coding: utf-8 -*-
"""
Builder v2 for Mars Transit Odyssey: Phase 1 + Science Briefing (Real Orbital Physics, Tsiolkovsky, Cryogenics & Ullage)
"""

import sys
sys.path.append(r'D:\mars-transit-odyssey')
from textures_b64 import EARTH_B64, CLOUDS_B64, SPEC_B64, MARS_B64, SUN_B64, MOON_B64
from crew_b64 import VANCE_B64, ROMANOVA_B64, CHEN_B64, REID_B64

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
      cursor: pointer;
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
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .icon-btn:hover {
      background: rgba(0, 210, 255, 0.2);
      color: #00f0ff;
      border-color: #00f0ff;
    }
    .icon-btn.highlight {
      background: rgba(0, 210, 255, 0.15);
      color: #00f0ff;
      border-color: rgba(0, 210, 255, 0.4);
    }

    /* Common Button Glow */
    .btn-glow {
      background: linear-gradient(135deg, #00d2ff 0%, #0066cc 100%);
      color: white;
      border: none;
      padding: 14px 34px;
      border-radius: 30px;
      font-size: 15px;
      font-weight: 700;
      letter-spacing: 1.2px;
      text-transform: uppercase;
      cursor: pointer;
      box-shadow: 0 0 25px rgba(0, 210, 255, 0.4);
      transition: all 0.25s;
    }
    .btn-glow:hover {
      transform: scale(1.04);
      box-shadow: 0 0 35px rgba(0, 210, 255, 0.7);
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

    /* ========================================================
       2. SCREEN CREW (BRIEFING & DOSSIER)
       ======================================================== */
    #screen-crew {
      flex-direction: column;
      justify-content: flex-start;
      align-items: center;
      padding: 85px 20px 30px 20px;
      background: radial-gradient(circle at top, #091a38 0%, #020409 70%);
      overflow-y: auto;
    }
    .crew-panel {
      max-width: 1040px;
      width: 100%;
      padding: 26px;
      display: flex;
      flex-direction: column;
      gap: 18px;
      margin-bottom: 30px;
    }
    .briefing-box {
      background: rgba(0, 210, 255, 0.06);
      border-left: 4px solid #00f0ff;
      padding: 14px 18px;
      border-radius: 6px;
      font-size: 14px;
      color: #cbd5e1;
      line-height: 1.6;
    }
    .crew-tabs, .science-tabs {
      display: flex;
      gap: 10px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 10px;
      flex-wrap: wrap;
    }
    .tab-btn {
      background: transparent;
      border: none;
      color: #94a3b8;
      font-size: 13px;
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

    /* Realistic Crew Dossier Grid */
    .crew-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(228px, 1fr));
      gap: 16px;
      margin: 8px 0;
    }
    .crew-card {
      background: rgba(11, 20, 38, 0.88);
      border: 1px solid rgba(0, 210, 255, 0.22);
      border-radius: 12px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.6);
      transition: all 0.25s ease;
      position: relative;
    }
    .crew-card:hover {
      border-color: rgba(0, 210, 255, 0.7);
      transform: translateY(-4px);
      box-shadow: 0 14px 36px rgba(0, 210, 255, 0.16);
    }
    .crew-card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 10px;
      letter-spacing: 0.6px;
      color: #7b91b0;
      font-weight: 700;
      white-space: nowrap;
      gap: 6px;
    }
    .crew-agency-tag {
      color: #00d2ff;
      background: rgba(0, 210, 255, 0.1);
      padding: 2px 6px;
      border-radius: 4px;
      border: 1px solid rgba(0, 210, 255, 0.25);
      white-space: nowrap;
    }
    .crew-photo-wrap {
      width: 100%;
      aspect-ratio: 1 / 1;
      border-radius: 8px;
      overflow: hidden;
      position: relative;
      background: #050b16;
      border: 1px solid rgba(255, 255, 255, 0.12);
      box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.8);
    }
    .crew-photo {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      transition: transform 0.3s;
    }
    .crew-card:hover .crew-photo {
      transform: scale(1.04);
    }
    .hud-bracket {
      position: absolute;
      width: 10px;
      height: 10px;
      border-color: #00f0ff;
      pointer-events: none;
      opacity: 0.8;
    }
    .bracket-tl { top: 6px; left: 6px; border-top: 2px solid; border-left: 2px solid; }
    .bracket-tr { top: 6px; right: 6px; border-top: 2px solid; border-right: 2px solid; }
    .bracket-bl { bottom: 6px; left: 6px; border-bottom: 2px solid; border-left: 2px solid; }
    .bracket-br { bottom: 6px; right: 6px; border-bottom: 2px solid; border-right: 2px solid; }

    .crew-name {
      font-size: 16px;
      font-weight: 800;
      color: #ffffff;
      letter-spacing: 0.5px;
    }
    .crew-role {
      font-size: 11px;
      font-weight: 700;
      color: #00f0ff;
      text-transform: uppercase;
      letter-spacing: 0.6px;
    }
    .crew-spec-box {
      background: rgba(0, 0, 0, 0.4);
      border-left: 3px solid #ffaa00;
      border-radius: 4px;
      padding: 8px 10px;
      display: flex;
      flex-direction: column;
      gap: 3px;
    }
    .crew-spec-tag {
      font-size: 10px;
      font-weight: 800;
      color: #ffaa00;
      letter-spacing: 0.8px;
      text-transform: uppercase;
    }
    .crew-spec-desc {
      font-size: 11px;
      color: #cbd5e1;
      line-height: 1.4;
    }
    .crew-status {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.8px;
      color: #00e699;
      margin-top: auto;
    }
    .status-dot {
      width: 7px;
      height: 7px;
      background: #00e699;
      border-radius: 50%;
      box-shadow: 0 0 8px #00e699;
      display: inline-block;
      animation: pulse-dot 2s infinite;
    }
    @keyframes pulse-dot {
      0% { opacity: 0.6; transform: scale(0.9); }
      50% { opacity: 1; transform: scale(1.15); }
      100% { opacity: 0.6; transform: scale(0.9); }
    }

    /* ========================================================
       2.5. SCREEN SCIENCE (РЕАЛЬНАЯ АЭРОКОСМИЧЕСКАЯ ФИЗИКА)
       ======================================================== */
    #screen-science {
      flex-direction: column;
      justify-content: flex-start;
      align-items: center;
      padding: 85px 20px 30px 20px;
      background: radial-gradient(circle at top, #0c1b3d 0%, #020409 75%);
      overflow-y: auto;
    }
    .science-panel {
      max-width: 1040px;
      width: 100%;
      padding: 26px;
      display: flex;
      flex-direction: column;
      gap: 18px;
      margin-bottom: 30px;
    }
    .science-header {
      border-bottom: 1px solid rgba(0, 210, 255, 0.2);
      padding-bottom: 14px;
    }
    .science-tag {
      font-size: 11px;
      font-weight: 800;
      color: #00e699;
      letter-spacing: 2px;
      text-transform: uppercase;
      margin-bottom: 6px;
    }
    .science-title {
      font-size: 22px;
      font-weight: 800;
      color: #ffffff;
      letter-spacing: 0.5px;
    }
    .science-content-box {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .science-card-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 14px;
    }
    .sci-fact-card {
      background: rgba(14, 24, 46, 0.7);
      border: 1px solid rgba(0, 210, 255, 0.2);
      border-radius: 10px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      transition: all 0.2s;
    }
    .sci-fact-card:hover {
      border-color: rgba(0, 210, 255, 0.6);
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(0, 210, 255, 0.12);
    }
    .sci-fact-val {
      font-size: 20px;
      font-weight: 900;
      color: #00f0ff;
      font-family: 'Consolas', monospace;
    }
    .sci-fact-label {
      font-size: 11px;
      font-weight: 700;
      color: #cbd5e1;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .sci-fact-desc {
      font-size: 12px;
      color: #94a3b8;
      line-height: 1.5;
    }
    .sci-formula-box {
      background: rgba(0, 0, 0, 0.5);
      border: 1px solid rgba(0, 230, 153, 0.3);
      border-radius: 8px;
      padding: 14px 20px;
      text-align: center;
    }
    .sci-formula {
      font-family: 'Consolas', monospace;
      font-size: 20px;
      font-weight: 800;
      color: #00e699;
      letter-spacing: 2px;
    }
    .sci-formula-desc {
      font-size: 12px;
      color: #94a3b8;
      margin-top: 4px;
    }
    .sci-body-text {
      background: rgba(0, 210, 255, 0.05);
      border-left: 4px solid #00f0ff;
      padding: 14px 18px;
      border-radius: 6px;
      font-size: 13px;
      color: #cbd5e1;
      line-height: 1.6;
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
    <div class="game-logo" onclick="showIntroScreen()">
      <span>🚀 АРЕС-1 // 2038</span>
    </div>
    <div class="top-controls">
      <button class="icon-btn highlight" id="sci-nav-btn" onclick="showScienceScreen()">💡 НАУКА МИССИИ</button>
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
       2. SCREEN: CREW SELECTION & BRIEFING (REALISTIC DOSSIER)
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

      <!-- Canon Crew Grid with Real High-Tech Dossier Photos -->
      <div class="crew-grid" id="canon-crew-grid">
        <!-- 1. Commander Alex Vance -->
        <div class="crew-card">
          <div class="crew-card-header">
            <span class="crew-agency-tag" id="i18n-agency-1">NASA // SPACEX</span>
            <span>ID: AR1-01 // CDR</span>
          </div>
          <div class="crew-photo-wrap">
            <img src="__VANCE_B64__" class="crew-photo" alt="Alex Vance">
            <div class="hud-bracket bracket-tl"></div>
            <div class="hud-bracket bracket-tr"></div>
            <div class="hud-bracket bracket-bl"></div>
            <div class="hud-bracket bracket-br"></div>
          </div>
          <div class="crew-name" id="i18n-crew-cmdr-name">Алекс Вэнс</div>
          <div class="crew-role" id="i18n-crew-cmdr-role">Командир корабля</div>
          <div class="crew-spec-box">
            <span class="crew-spec-tag" id="i18n-spec-lbl-1">🎖️ СПЕЦИАЛИЗАЦИЯ:</span>
            <div class="crew-spec-desc" id="i18n-crew-cmdr-spec">Борьба за живучесть: +15% к ликвидации системных сбоев</div>
          </div>
          <div class="crew-status">
            <span class="status-dot"></span>
            <span id="i18n-status-1">К ПОЛЕТУ ДОПУЩЕН</span>
          </div>
        </div>

        <!-- 2. Pilot Elena Romanova -->
        <div class="crew-card">
          <div class="crew-card-header">
            <span class="crew-agency-tag" id="i18n-agency-2">РОСКОСМОС</span>
            <span>ID: AR1-02 // PLT</span>
          </div>
          <div class="crew-photo-wrap">
            <img src="__ROMANOVA_B64__" class="crew-photo" alt="Elena Romanova">
            <div class="hud-bracket bracket-tl"></div>
            <div class="hud-bracket bracket-tr"></div>
            <div class="hud-bracket bracket-bl"></div>
            <div class="hud-bracket bracket-br"></div>
          </div>
          <div class="crew-name" id="i18n-crew-plt-name">Елена Романова</div>
          <div class="crew-role" id="i18n-crew-plt-role">Главный пилот</div>
          <div class="crew-spec-box">
            <span class="crew-spec-tag" id="i18n-spec-lbl-2">🎖️ СПЕЦИАЛИЗАЦИЯ:</span>
            <div class="crew-spec-desc" id="i18n-crew-plt-spec">Ручное сближение «Курс»: +20% точность соосности</div>
          </div>
          <div class="crew-status">
            <span class="status-dot"></span>
            <span id="i18n-status-2">К ПОЛЕТУ ДОПУЩЕН</span>
          </div>
        </div>

        <!-- 3. Engineer Chen Wei -->
        <div class="crew-card">
          <div class="crew-card-header">
            <span class="crew-agency-tag" id="i18n-agency-3">CNSA // МАРС</span>
            <span>ID: AR1-03 // ENG</span>
          </div>
          <div class="crew-photo-wrap">
            <img src="__CHEN_B64__" class="crew-photo" alt="Chen Wei">
            <div class="hud-bracket bracket-tl"></div>
            <div class="hud-bracket bracket-tr"></div>
            <div class="hud-bracket bracket-bl"></div>
            <div class="hud-bracket bracket-br"></div>
          </div>
          <div class="crew-name" id="i18n-crew-eng-name">Чэнь Вэй</div>
          <div class="crew-role" id="i18n-crew-eng-role">Бортинженер</div>
          <div class="crew-spec-box">
            <span class="crew-spec-tag" id="i18n-spec-lbl-3">🎖️ СПЕЦИАЛИЗАЦИЯ:</span>
            <div class="crew-spec-desc" id="i18n-crew-eng-spec">Двигатели Raptor 3: -25% износ агрегатов и расход ЗИП</div>
          </div>
          <div class="crew-status">
            <span class="status-dot"></span>
            <span id="i18n-status-3">К ПОЛЕТУ ДОПУЩЕН</span>
          </div>
        </div>

        <!-- 4. Dr. Marcus Reid -->
        <div class="crew-card">
          <div class="crew-card-header">
            <span class="crew-agency-tag" id="i18n-agency-4">ESA // МЕДИЦИНА</span>
            <span>ID: AR1-04 // MED</span>
          </div>
          <div class="crew-photo-wrap">
            <img src="__REID_B64__" class="crew-photo" alt="Dr. Marcus Reid">
            <div class="hud-bracket bracket-tl"></div>
            <div class="hud-bracket bracket-tr"></div>
            <div class="hud-bracket bracket-bl"></div>
            <div class="hud-bracket bracket-br"></div>
          </div>
          <div class="crew-name" id="i18n-crew-med-name">д-р Маркус Рид</div>
          <div class="crew-role" id="i18n-crew-med-role">Судовой врач</div>
          <div class="crew-spec-box">
            <span class="crew-spec-tag" id="i18n-spec-lbl-4">🎖️ СПЕЦИАЛИЗАЦИЯ:</span>
            <div class="crew-spec-desc" id="i18n-crew-med-spec">Микрогравитация и травматология: +20% био-буфер</div>
          </div>
          <div class="crew-status">
            <span class="status-dot"></span>
            <span id="i18n-status-4">К ПОЛЕТУ ДОПУЩЕН</span>
          </div>
        </div>
      </div>

      <!-- Custom Crew Builder (Toggleable) -->
      <div id="custom-crew-box" style="display: none; font-size: 13px; color: #cbd5e1; padding: 18px; background: rgba(0,0,0,0.4); border-radius: 8px; border: 1px solid rgba(0,210,255,0.2);">
        <div id="i18n-custom-desc" style="font-weight: 700; color: #00f0ff;">Распределите очки квалификации экипажа (доступно: 12 очков):</div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 14px; margin-top: 14px;">
          <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 6px;">🚀 <span id="i18n-skill-pilot">Пилотирование</span>: <strong style="color: #00f0ff;">+4</strong></div>
          <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 6px;">🔧 <span id="i18n-skill-eng">Инженерия СЖО/ДУ</span>: <strong style="color: #00f0ff;">+4</strong></div>
          <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 6px;">🧬 <span id="i18n-skill-med">Биомедицина</span>: <strong style="color: #00f0ff;">+2</strong></div>
          <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 6px;">🧠 <span id="i18n-skill-psy">Психоустойчивость</span>: <strong style="color: #00f0ff;">+2</strong></div>
        </div>
      </div>

      <div style="display: flex; justify-content: flex-end; margin-top: 10px;">
        <button class="btn-glow" onclick="showScienceScreen()" id="i18n-btn-confirm-crew">
          УТВЕРДИТЬ ЭКИПАЖ И ПЕРЕЙТИ К БРИФИНГУ ➔
        </button>
      </div>
    </div>
  </div>

  <!-- =========================================================
       2.5. SCREEN: SCIENCE BRIEFING (РЕАЛЬНАЯ АЭРОКОСМИЧЕСКАЯ ФИЗИКА)
       ========================================================= -->
  <div class="screen" id="screen-science">
    <div class="science-panel glass-card">
      <div class="science-header">
        <div class="science-tag" id="i18n-sci-tag">БОРТОВОЙ СПРАВОЧНИК // РЕАЛЬНАЯ АЭРОКОСМИЧЕСКАЯ ФИЗИКА</div>
        <div class="science-title" id="i18n-sci-title">1. ВЫВЕДЕНИЕ НА ОРБИТУ: СВЕРХТЯЖЕЛЫЙ СТАРТ И СКОРОСТЬ 7.8 КМ/С</div>
      </div>

      <div class="science-tabs">
        <button class="tab-btn active" onclick="switchScienceTab('tab-launch', this)" id="i18n-sci-tab1">🚀 1. ВЫВЕДЕНИЕ (7.8 КМ/С)</button>
        <button class="tab-btn" onclick="switchScienceTab('tab-tsiolkovsky', this)" id="i18n-sci-tab2">⛽ 2. УРАВНЕНИЕ ЦИОЛКОВСКОГО</button>
        <button class="tab-btn" onclick="switchScienceTab('tab-ullage', this)" id="i18n-sci-tab3">❄️ 3. КРИОГЕН И НЕВЕСОМОСТЬ (0g)</button>
        <button class="tab-btn" onclick="switchScienceTab('tab-reality', this)" id="i18n-sci-tab4">🛠️ 4. РЕАЛЬНОСТЬ XXI ВЕКА</button>
      </div>

      <!-- Tab 1: Launch & Hot-Staging -->
      <div class="science-content-box" id="tab-launch">
        <div class="science-card-grid">
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-f1-val">5 000 т</div>
            <div class="sci-fact-label" id="i18n-sci-f1-lbl">Стартовая масса системы</div>
            <div class="sci-fact-desc" id="i18n-sci-f1-desc">Super Heavy + Starship. Самая гигантская ракета в истории (в 2 раза мощнее лунной Saturn V).</div>
          </div>
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-f2-val">33 Raptor 3</div>
            <div class="sci-fact-label" id="i18n-sci-f2-lbl">Тяга первой ступени</div>
            <div class="sci-fact-desc" id="i18n-sci-f2-desc">7 500 тонн совокупной тяги на метане (CH4) и жидком кислороде (LOX). Давление в камере 350 атм.</div>
          </div>
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-f3-val">Hot-Staging</div>
            <div class="sci-fact-label" id="i18n-sci-f3-lbl">Горячее разделение</div>
            <div class="sci-fact-desc" id="i18n-sci-f3-desc">Двигатели Starship зажигаются прямо перед отделением ступени через перфорированное титановое кольцо.</div>
          </div>
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-f4-val">28 000 км/ч</div>
            <div class="sci-fact-label" id="i18n-sci-f4-lbl">Первая космическая (v1)</div>
            <div class="sci-fact-desc" id="i18n-sci-f4-desc">Скорость 7.8 км/с, позволяющая «падать мимо Земли» по круговой орбите высотой 320 км.</div>
          </div>
        </div>
        <div class="sci-body-text" id="i18n-sci-body-launch">
          💡 <strong>Как мы здесь оказались:</strong> Чтобы подняться на высоту 320 км и преодолеть гравитацию и сопротивление атмосферы, ракета сожгла колоссальные 3 400 тонн топлива бустера и 1 100 тонн самого корабля. Корабль на орбите — но его баки практически пусты!
        </div>
      </div>

      <!-- Tab 2: Tsiolkovsky Equation -->
      <div class="science-content-box" id="tab-tsiolkovsky" style="display: none;">
        <div class="sci-formula-box">
          <div class="sci-formula">Δv = I_sp · g_0 · ln(m_0 / m_k)</div>
          <div class="sci-formula-desc" id="i18n-sci-formula-desc">Формула Циолковского (1903 г.): «Тирания ракетного уравнения»</div>
        </div>
        <div class="science-card-grid">
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-t1-val">92%</div>
            <div class="sci-fact-label" id="i18n-sci-t1-lbl">Сгорело при старте</div>
            <div class="sci-fact-desc" id="i18n-sci-t1-desc">Ракета несёт топливо, чтобы разгонять само топливо. Масса растет экспоненциально!</div>
          </div>
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-t2-val">8% (96 т)</div>
            <div class="sci-fact-label" id="i18n-sci-t2-lbl">Остаток на орбите</div>
            <div class="sci-fact-desc" id="i18n-sci-t2-desc">Этого хватит лишь на свод с орбиты, но ни о каком Марсе речи быть не может.</div>
          </div>
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-t3-val">3 600 м/с</div>
            <div class="sci-fact-label" id="i18n-sci-t3-lbl">Импульс TMI к Марсу</div>
            <div class="sci-fact-desc" id="i18n-sci-t3-desc">Необходимая характеристическая скорость для перехода на трансферную орбиту Гомана к Марсу.</div>
          </div>
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-t4-val">1 200 тонн</div>
            <div class="sci-fact-label" id="i18n-sci-t4-lbl">Целевая дозаправка</div>
            <div class="sci-fact-desc" id="i18n-sci-t4-desc">Полные баки на орбите дают кораблю запас скорости 6.9 км/с — гарантия перелета и посадки!</div>
          </div>
        </div>
        <div class="sci-body-text" id="i18n-sci-body-tsiolk">
          💡 <strong>Вся правда без иллюзий:</strong> Ни одна ракета в мире не способна стартовать с Земли сразу к Марсу с жилым модулем на 100 тонн. Единственный физически возможный путь в Солнечной системе — вывести корабль на орбиту, а затем серией танкеров наполнить его баки. Без орбитальной дозаправки полет на Марс невозможен!
        </div>
      </div>

      <!-- Tab 3: Cryogenics & Ullage -->
      <div class="science-content-box" id="tab-ullage" style="display: none;">
        <div class="science-card-grid">
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-u1-val">-161°C / -183°C</div>
            <div class="sci-fact-label" id="i18n-sci-u1-lbl">Криогенная пара</div>
            <div class="sci-fact-desc" id="i18n-sci-u1-desc">Жидкий метан (CH4) и жидкий кислород (LOX). Требуют вакуумной теплоизоляции баков.</div>
          </div>
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-u2-val">0g Невесомость</div>
            <div class="sci-fact-label" id="i18n-sci-u2-lbl">Поведение жидкости</div>
            <div class="sci-fact-desc" id="i18n-sci-u2-desc">В невесомости жидкость не прижата ко дну, а плавает пузырями и липнет к стенкам бака.</div>
          </div>
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-u3-val">Кавитация ⚠️</div>
            <div class="sci-fact-label" id="i18n-sci-u3-lbl">Смертельная опасность</div>
            <div class="sci-fact-desc" id="i18n-sci-u3-desc">Если турбонасос захватит пузырь газа при 30 000 об/мин — крыльчатку разорвет, а двигатель взорвется.</div>
          </div>
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-u4-val">Ullage Burn 🔥</div>
            <div class="sci-fact-label" id="i18n-sci-u4-lbl">Импульс осаждения</div>
            <div class="sci-fact-desc" id="i18n-sci-u4-desc">Включение сопел RCS дает ускорение 0.02g: криоген оседает на дно баков к насосам перекачки.</div>
          </div>
        </div>
        <div class="sci-body-text" id="i18n-sci-body-ullage">
          💡 <strong>Инженерная процедура:</strong> Прежде чем перекачивать 1200 тонн метана, экипаж обязан выдать импульс осаждения (Ullage Burn). Как только топливо прижмется ко дну, открываются криогенные магистрали высокого давления.
        </div>
      </div>

      <!-- Tab 4: Real XXI Century Engineering -->
      <div class="science-content-box" id="tab-reality" style="display: none;">
        <div class="science-card-grid">
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-r1-val">Starbase</div>
            <div class="sci-fact-label" id="i18n-sci-r1-lbl">Бока-Чика, Техас</div>
            <div class="sci-fact-desc" id="i18n-sci-r1-desc">Реальная фабрика Starfactory и стартовые комплексы, строящие флот многоразовых кораблей.</div>
          </div>
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-r2-val">Mechazilla</div>
            <div class="sci-fact-label" id="i18n-sci-r2-lbl">Поимка в воздухе</div>
            <div class="sci-fact-desc" id="i18n-sci-r2-desc">В октябре 2024 (полет IFT-5) 71-метровый бустер Super Heavy впервые в истории пойман башней Mechazilla!</div>
          </div>
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-r3-val">NASA Artemis</div>
            <div class="sci-fact-label" id="i18n-sci-r3-lbl">Лунная программа США</div>
            <div class="sci-fact-desc" id="i18n-sci-r3-desc">NASA официально выбрало Starship HLS для высадки людей на Луну с обязательной орбитальной дозаправкой.</div>
          </div>
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-r4-val">Tipping Point</div>
            <div class="sci-fact-label" id="i18n-sci-r4-lbl">Орбитальные тесты</div>
            <div class="sci-fact-desc" id="i18n-sci-r4-desc">SpaceX уже успешно провела первый этап испытаний перекачки криогена в космосе по контракту NASA.</div>
          </div>
        </div>
        <div class="sci-body-text" id="i18n-sci-body-reality">
          💡 <strong>Это не фантастика:</strong> Всё, чем вы управляете в этой миссии — от башни обслуживания до криогенной перекачки — строится и тестируется прямо сейчас инженерами SpaceX и NASA. Наша игра — это строгая проекция реальной космонавтики 2038 года!
        </div>
      </div>

      <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
        <button class="icon-btn" onclick="showCrewScreen()" id="i18n-btn-back-crew">◀ НАЗАД К ЭКИПАЖУ</button>
        <button class="btn-glow" onclick="startDockingGameplay()" id="i18n-btn-start-docking">
          ПРИНЯТЬ УПРАВЛЕНИЕ И ВЫЙТИ НА СТЫКОВКУ ➔
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
          <span class="hud-value" style="color: #00e699;" id="i18n-hud-mode-val">СБЛИЖЕНИЕ («КУРС»)</span>
        </div>
        <div class="hud-row">
          <span class="hud-label" id="i18n-hud-target">ЦЕЛЬ</span>
          <span class="hud-value" id="i18n-hud-target-val">TANKER-01 (МЕТАН)</span>
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
        <div id="i18n-hud-rcs-lbl" style="font-size: 11px; color: #7b91b0; font-weight: 700; text-transform: uppercase;">
          РУЧНЫЕ ДВИГАТЕЛИ RCS:
        </div>
        
        <div class="rcs-grid">
          <div></div>
          <button class="rcs-btn" onmousedown="applyThrust('up')" title="Смещение вверх (Q)">▲</button>
          <div></div>
          <button class="rcs-btn" onmousedown="applyThrust('left')" title="Смещение влево (A)">◀</button>
          <button class="rcs-btn" onmousedown="applyThrust('forward')" title="Тяга вперед (W)" style="color: #00e699;">W</button>
          <button class="rcs-btn" onmousedown="applyThrust('right')" title="Смещение вправо (D)">▶</button>
          <div></div>
          <button class="rcs-btn" onmousedown="applyThrust('down')" title="Смещение вниз (E)">▼</button>
          <button class="rcs-btn" onmousedown="applyThrust('back')" title="Торможение назад (S)" style="color: #ff9900;">S</button>
        </div>

        <div id="i18n-hud-instructions" style="flex: 1; font-size: 12px; color: #94a3b8; line-height: 1.5;">
          💡 <strong>Инструкция:</strong> Совместите носовой штырь со стыковочным конусом танкера на скорости менее <strong>0.25 м/с</strong> и отклонении менее <strong>2.0°</strong> для жесткого захвата замков!
        </div>
      </div>
    </div>
  </div>

  <!-- Refueling Modal -->
  <div class="modal-overlay" id="refuel-modal">
    <div class="modal-card glass-card">
      <div class="modal-title" id="i18n-modal-title">🎯 СТЫКОВКА УСПЕШНА!</div>
      <div id="i18n-modal-desc" style="font-size: 14px; color: #cbd5e1;">
        Стыковочный узел зафиксирован. Магистрали перекачки криогенного метана и жидкого кислорода подсоединены к бакам «Ареса».
      </div>

      <div class="fuel-gauge-container">
        <div class="fuel-gauge-fill" id="modal-fuel-fill"></div>
        <div class="fuel-gauge-text" id="modal-fuel-text">8% (96 / 1200 тонн)</div>
      </div>

      <div style="display: flex; gap: 12px; justify-content: center;">
        <button class="btn-glow" id="btn-ullage" onclick="triggerUllageBurn()" style="background: linear-gradient(135deg, #ff9900, #cc6600);">
          <span id="i18n-btn-ullage">🔥 Осаждение топлива (Ullage Burn)</span>
        </button>
        <button class="btn-glow" id="btn-pump" onclick="transferPropellant()" disabled style="opacity: 0.5;">
          <span id="i18n-btn-pump">⚡ Перекачать 1200 тонн</span>
        </button>
      </div>

      <div id="tmi-ready-box" style="display: none; margin-top: 10px;">
        <button class="btn-glow" id="btn-tmi" onclick="launchTMI()" style="width: 100%; background: linear-gradient(135deg, #00e699, #009966);">
          <span id="i18n-btn-tmi">🚀 ОТСТЫКОВКА И РАЗГОННЫЙ ИМПУЛЬС TMI ➔</span>
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
        sci_nav_btn: "💡 НАУКА МИССИИ",
        intro_year: "2038 ГОД // КОСМОДРОМ STARBASE",
        intro_title: "АРЕС-1: МАРСИАНСКИЙ ТРАНЗИТ",
        intro_text: "Годы подготовки завершены. Многоразовый межпланетный лайнер нового поколения выведен на опорную околоземную орбиту. Баки корабля пусты после старта. До открытия марсианского окна — считанные дни. Начните операцию!",
        btn_start: "ПРИСТУПИТЬ К МИССИИ ➔",
        crew_heading: "БОРТОВОЙ ЖУРНАЛ: ЭКИПАЖ «АРЕС-1»",
        crew_briefing: "🎙️ <strong>ЦУП (Хьюстон / Королёв):</strong> «\"Арес\", вы на расчетной орбите 320 км. Первый танкер заправки Tanker-01 уже выполнил фазирование и находится в зоне видимости. Подтвердите допуск экипажа к миссии!»",
        tab_canon: "ШТАТНЫЙ ЭКИПАЖ (КАНОН)",
        tab_custom: "КОНСТРУКТОР ЭКИПАЖА",
        spec_lbl: "🎖️ СПЕЦИАЛИЗАЦИЯ:",
        agency_1: "NASA // SPACEX",
        agency_2: "РОСКОСМОС",
        agency_3: "CNSA // МАРС",
        agency_4: "ESA // МЕДИЦИНА",
        crew_cmdr_name: "Алекс Вэнс",
        crew_cmdr_role: "Командир корабля",
        crew_cmdr_spec: "Борьба за живучесть: +15% к ликвидации системных сбоев",
        crew_plt_name: "Елена Романова",
        crew_plt_role: "Главный пилот",
        crew_plt_spec: "Ручное сближение «Курс»: +20% точность соосности",
        crew_eng_name: "Чэнь Вэй",
        crew_eng_role: "Бортинженер",
        crew_eng_spec: "Двигатели Raptor 3: -25% износ агрегатов и расход ЗИП",
        crew_med_name: "д-р Маркус Рид",
        crew_med_role: "Судовой врач",
        crew_med_spec: "Микрогравитация и травматология: +20% био-буфер",
        crew_status: "К ПОЛЕТУ ДОПУЩЕН",
        custom_desc: "Распределите очки квалификации экипажа (доступно: 12 очков):",
        skill_pilot: "Пилотирование",
        skill_eng: "Инженерия СЖО/ДУ",
        skill_med: "Биомедицина",
        skill_psy: "Психоустойчивость",
        btn_confirm_crew: "УТВЕРДИТЬ ЭКИПАЖ И ПЕРЕЙТИ К БРИФИНГУ ➔",
        
        // Science Briefing (RU)
        sci_tag: "БОРТОВОЙ СПРАВОЧНИК // РЕАЛЬНАЯ АЭРОКОСМИЧЕСКАЯ ФИЗИКА",
        sci_title_tab_launch: "1. ВЫВЕДЕНИЕ НА ОРБИТУ: СВЕРХТЯЖЕЛЫЙ СТАРТ И СКОРОСТЬ 7.8 КМ/С",
        sci_title_tab_tsiolkovsky: "2. ТИРАНИЯ РАКЕТНОГО УРАВНЕНИЯ ЦИОЛКОВСКОГО И ЗАЧЕМ НУЖНА ДОЗАПРАВКА",
        sci_title_tab_ullage: "3. ФИЗИКА КРИОГЕНА В НЕВЕСОМОСТИ (0g), КАВИТАЦИЯ И МАНЕВР ULLAGE BURN",
        sci_title_tab_reality: "4. ИНЖЕНЕРНАЯ РЕАЛЬНОСТЬ XXI ВЕКА: MECHAZILLA, RAPTOR 3 И NASA ARTEMIS",
        sci_tab1: "🚀 1. ВЫВЕДЕНИЕ (7.8 КМ/С)",
        sci_tab2: "⛽ 2. УРАВНЕНИЕ ЦИОЛКОВСКОГО",
        sci_tab3: "❄️ 3. КРИОГЕН И НЕВЕСОМОСТЬ (0g)",
        sci_tab4: "🛠️ 4. РЕАЛЬНОСТЬ XXI ВЕКА",
        sci_f1_val: "5 000 т",
        sci_f1_lbl: "Стартовая масса системы",
        sci_f1_desc: "Super Heavy + Starship. Самая гигантская ракета в истории (в 2 раза мощнее лунной Saturn V).",
        sci_f2_val: "33 Raptor 3",
        sci_f2_lbl: "Тяга первой ступени",
        sci_f2_desc: "7 500 тонн совокупной тяги на метане (CH4) и жидком кислороде (LOX). 33 двигателя Raptor 3.",
        sci_f3_val: "Hot-Staging",
        sci_f3_lbl: "Горячее разделение",
        sci_f3_desc: "Двигатели Starship зажигаются прямо перед отделением ступени через титановое кольцо (Hot-staging).",
        sci_f4_val: "28 000 км/ч",
        sci_f4_lbl: "Первая космическая (v1)",
        sci_f4_desc: "Скорость 28 000 км/ч (7.8 км/с), позволяющая «падать мимо Земли» по круговой орбите 320 км.",
        sci_body_launch: "💡 <strong>Как мы здесь оказались:</strong> Чтобы подняться на высоту 320 км и преодолеть гравитацию и сопротивление атмосферы, ракета сожгла колоссальные 3 400 тонн топлива бустера и 1 100 тонн самого корабля. Корабль на орбите — но его баки практически пусты!",
        sci_formula_desc: "Формула Циолковского (1903 г.): «Тирания ракетного уравнения»",
        sci_t1_val: "92%",
        sci_t1_lbl: "Сгорело при старте",
        sci_t1_desc: "Ракета несёт топливо, чтобы разгонять само топливо. Масса растет экспоненциально!",
        sci_t2_val: "8% (96 т)",
        sci_t2_lbl: "Остаток на орбите",
        sci_t2_desc: "Этого хватит лишь на свод с орбиты, но ни о каком Марсе речи быть не может.",
        sci_t3_val: "3 600 м/с",
        sci_t3_lbl: "Импульс TMI к Марсу",
        sci_t3_desc: "Необходимая характеристическая скорость для перехода на трансферную орбиту Гомана к Марсу.",
        sci_t4_val: "1 200 тонн",
        sci_t4_lbl: "Целевая дозаправка",
        sci_t4_desc: "Полные баки на орбите дают кораблю запас скорости 6.9 км/с — гарантия перелета и посадки!",
        sci_body_tsiolk: "💡 <strong>Вся правда без иллюзий:</strong> Ни одна ракета в мире не способна стартовать с Земли сразу к Марсу с жилым модулем на 100 тонн. Единственный физически возможный путь в Солнечной системе — вывести корабль на орбиту, а затем серией танкеров наполнить его баки. Без орбитальной дозаправки полет на Марс невозможен!",
        sci_u1_val: "-161°C / -183°C",
        sci_u1_lbl: "Криогенная пара",
        sci_u1_desc: "Жидкий метан (-161°C) и жидкий кислород (-183°C). Требуют вакуумной теплоизоляции баков.",
        sci_u2_val: "0g Невесомость",
        sci_u2_lbl: "Поведение жидкости",
        sci_u2_desc: "В невесомости жидкость не прижата ко дну, а плавает пузырями и липнет к стенкам бака.",
        sci_u3_val: "Кавитация ⚠️",
        sci_u3_lbl: "Смертельная опасность",
        sci_u3_desc: "Если турбонасос захватит пузырь газа при 30 000 об/мин — крыльчатку разорвет, а двигатель взорвется.",
        sci_u4_val: "Ullage Burn 🔥",
        sci_u4_lbl: "Импульс осаждения 🔥",
        sci_u4_desc: "Включение сопел RCS вперед дает ускорение 0.02g: криоген оседает на дно баков к насосам перекачки.",
        sci_body_ullage: "💡 <strong>Инженерная процедура:</strong> Прежде чем перекачивать 1200 тонн метана, экипаж обязан выдать импульс осаждения (Ullage Burn). Как только топливо прижмется ко дну, открываются криогенные магистрали высокого давления.",
        sci_r1_val: "Starbase",
        sci_r1_lbl: "Бока-Чика, Техас",
        sci_r1_desc: "Реальная фабрика Starfactory и стартовые комплексы, строящие флот многоразовых кораблей.",
        sci_r2_val: "Mechazilla",
        sci_r2_lbl: "Поимка в воздухе",
        sci_r2_desc: "В октябре 2024 года 71-метровый бустер Super Heavy впервые в истории пойман башней Mechazilla!",
        sci_r3_val: "NASA Artemis",
        sci_r3_lbl: "Лунная программа США",
        sci_r3_desc: "NASA официально выбрало Starship HLS для высадки людей на Луну с обязательной орбитальной дозаправкой.",
        sci_r4_val: "Tipping Point",
        sci_r4_lbl: "Орбитальные тесты",
        sci_r4_desc: "SpaceX уже успешно провела первый этап испытаний перекачки криогена в космосе по контракту NASA.",
        sci_body_reality: "💡 <strong>Это не фантастика:</strong> Всё, чем вы управляете в этой миссии — от башни обслуживания до криогенной перекачки — строится и тестируется прямо сейчас инженерами SpaceX и NASA. Наша игра — это строгая проекция реальной космонавтики 2038 года!",
        btn_back_crew: "◀ НАЗАД К ЭКИПАЖУ",
        btn_start_docking: "ПРИНЯТЬ УПРАВЛЕНИЕ И ВЫЙТИ НА СТЫКОВКУ ➔",

        // HUD & Gameplay (RU)
        hud_mode_lbl: "РЕЖИМ",
        hud_mode_val: "СБЛИЖЕНИЕ («КУРС»)",
        hud_target_lbl: "ЦЕЛЬ",
        hud_target_val: "TANKER-01 (МЕТАН)",
        hud_dist_lbl: "ДИСТАНЦИЯ",
        hud_vel_lbl: "СКОРОСТЬ СБЛИЖЕНИЯ",
        hud_align_lbl: "ОТКЛОНЕНИЕ ОСЕЙ",
        hud_fuel_lbl: "БАКИ КОРАБЛЯ",
        hud_rcs_lbl: "РУЧНЫЕ ДВИГАТЕЛИ RCS:",
        hud_instructions: "💡 <strong>Инструкция:</strong> Совместите носовой штырь со стыковочным конусом танкера на скорости менее <strong>0.25 м/с</strong> и отклонении менее <strong>2.0°</strong> для жесткого захвата замков!",
        hud_align_ok: "ВЫРАВНИВАНИЕ: ДОПУСТИМО",
        hud_align_bad: "ВЫРАВНИВАНИЕ: КРИТИЧЕСКИЙ УГОЛ!",
        hud_dock_latched: "0.0 м (ЗАХВАТ)",
        modal_title: "🎯 СТЫКОВКА УСПЕШНА!",
        modal_desc: "Стыковочный узел зафиксирован. Магистрали перекачки криогенного метана и жидкого кислорода подсоединены к бакам «Ареса».",
        btn_ullage: "🔥 Осаждение топлива (Ullage Burn)",
        btn_pump: "⚡ Перекачать 1200 тонн",
        btn_tmi: "🚀 ОТСТЫКОВКА И РАЗГОННЫЙ ИМПУЛЬС TMI ➔",
        toast_dock_success: "Жёсткий захват стыковочного узла зафиксирован!",
        toast_ullage: "Импульс осаждения топлива (Ullage Burn) завершен! Топливо на дне баков.",
        toast_refuel_done: "Баки полностью заправлены! 1200 тонн криогена загружено.",
        toast_tmi: "Рапторы включены! Выход на траекторию к Марсу!",
        toast_bounce: "⚠️ Слишком большая скорость сближения! Отскок!"
      },
      en: {
        sci_nav_btn: "💡 MISSION SCIENCE",
        intro_year: "YEAR 2038 // STARBASE SPACEPORT",
        intro_title: "ARES-1: MARTIAN TRANSIT",
        intro_text: "Years of training are complete. The next-generation reusable interplanetary Starship is in low Earth parking orbit. Propellant tanks are dry after launch. The Mars transfer window opens in days. Initiate operation!",
        btn_start: "BEGIN MISSION ➔",
        crew_heading: "MISSION LOG: ARES-1 CREW",
        crew_briefing: "🎙️ <strong>MISSION CONTROL:</strong> 'Ares, you are in nominal 320 km parking orbit. Orbital Tanker-01 has completed rendezvous phasing and is in visual range. Confirm crew flight clearance!'",
        tab_canon: "NOMINAL CREW (CANON)",
        tab_custom: "CUSTOM CREW BUILDER",
        spec_lbl: "🎖️ SPECIALIZATION:",
        agency_1: "NASA // SPACEX",
        agency_2: "ROSCOSMOS",
        agency_3: "CNSA // MARS",
        agency_4: "ESA // BIO-MED",
        crew_cmdr_name: "Alex Vance",
        crew_cmdr_role: "Mission Commander",
        crew_cmdr_spec: "Damage Control: +15% crisis resolution rate",
        crew_plt_name: "Elena Romanova",
        crew_plt_role: "Chief Pilot",
        crew_plt_spec: "Kurs Manual Rendezvous: +20% alignment accuracy",
        crew_eng_name: "Chen Wei",
        crew_eng_role: "Flight Engineer",
        crew_eng_spec: "Raptor 3 Propulsion: -25% component wear & spare parts",
        crew_med_name: "Dr. Marcus Reid",
        crew_med_role: "Chief Medical Officer",
        crew_med_spec: "Zero-G Trauma Care: +20% crew bio-resilience",
        crew_status: "FLIGHT CERTIFIED",
        custom_desc: "Allocate crew qualification points (12 points available):",
        skill_pilot: "Piloting",
        skill_eng: "Propulsion & ECLSS",
        skill_med: "Biomedicine",
        skill_psy: "Psychological Resilience",
        btn_confirm_crew: "CONFIRM CREW & PROCEED TO BRIEFING ➔",

        // Science Briefing (EN)
        sci_tag: "MISSION MANUAL // REAL AEROSPACE PHYSICS",
        sci_title_tab_launch: "1. ORBITAL INSERTION: SUPER HEAVY ASCENT & 7.8 KM/S VELOCITY",
        sci_title_tab_tsiolkovsky: "2. THE TYRANNY OF TSIOLKOVSKY EQUATION & WHY REFUELING IS MANDATORY",
        sci_title_tab_ullage: "3. ZERO-G CRYOGENIC DYNAMICS, CAVITATION RISK & ULLAGE BURN MANEUVER",
        sci_title_tab_reality: "4. XXI CENTURY AEROSPACE REALITY: MECHAZILLA, RAPTOR 3 & NASA ARTEMIS",
        sci_tab1: "🚀 1. ORBITAL ASCENT (7.8 KM/S)",
        sci_tab2: "⛽ 2. TSIOLKOVSKY EQUATION",
        sci_tab3: "❄️ 3. ZERO-G & CRYOGENICS",
        sci_tab4: "🛠️ 4. XXI CENTURY REALITY",
        sci_f1_val: "5,000 t",
        sci_f1_lbl: "System Launch Mass",
        sci_f1_desc: "Super Heavy + Starship. The most colossal and powerful rocket in human history (2x Apollo Saturn V).",
        sci_f2_val: "33 Raptor 3",
        sci_f2_lbl: "Booster Thrust",
        sci_f2_desc: "7,500 metric tons of thrust burning methane (CH4) and liquid oxygen (LOX). 33 Raptor 3 engines.",
        sci_f3_val: "Hot-Staging",
        sci_f3_lbl: "Hot-Staging Separation",
        sci_f3_desc: "Starship vacuum engines ignite right before stage separation through a perforated titanium interstage ring.",
        sci_f4_val: "28,000 km/h",
        sci_f4_lbl: "Orbital Velocity (v1)",
        sci_f4_desc: "Speed of 28,000 km/h (7.8 km/s) enabling the ship to permanently 'fall around the Earth' at 320 km.",
        sci_body_launch: "💡 <strong>How we arrived here:</strong> To climb to 320 km and beat atmospheric drag, the stack consumed 3,400 tons of booster propellant and 1,100 tons of ship propellant. Starship is in orbit — but its tanks are virtually dry!",
        sci_formula_desc: "Tsiolkovsky Formula (1903): 'The Tyranny of the Rocket Equation'",
        sci_t1_val: "92%",
        sci_t1_lbl: "Burned at Launch",
        sci_t1_desc: "A rocket must carry propellant merely to accelerate its own propellant. Mass increases exponentially!",
        sci_t2_val: "8% (96 t)",
        sci_t2_lbl: "Orbital Remainder",
        sci_t2_desc: "Enough only for deorbit maneuvers, completely inadequate for a Mars transfer trajectory.",
        sci_t3_val: "3,600 m/s",
        sci_t3_lbl: "TMI Delta-v to Mars",
        sci_t3_desc: "Required characteristic velocity increment to enter the Hohmann transfer trajectory toward Mars.",
        sci_t4_val: "1,200 tons",
        sci_t4_lbl: "Target Refueling",
        sci_t4_desc: "Full propellant tanks in orbit yield 6.9 km/s delta-v — ensuring Earth departure, cruise, and Mars landing!",
        sci_body_tsiolk: "💡 <strong>Hard reality without illusions:</strong> No rocket can launch from Earth directly to Mars with a 100-ton habitat. The only physically viable path in our solar system is launching empty and refueling in LEO via orbital tankers. Without orbital refueling, Mars is impossible!",
        sci_u1_val: "-161°C / -183°C",
        sci_u1_lbl: "Cryogenic Propellant",
        sci_u1_desc: "Liquid methane (-161°C) and liquid oxygen (-183°C). Requiring vacuum-jacketed cryogenic tanks.",
        sci_u2_val: "0g Microgravity",
        sci_u2_lbl: "Zero-G Fluid Dynamics",
        sci_u2_desc: "In microgravity, liquids do not stay at the bottom; surface tension causes them to float in bubbles and coat tank walls.",
        sci_u3_val: "Cavitation ⚠️",
        sci_u3_lbl: "Turbopump Cavitation ⚠️",
        sci_u3_desc: "If a turbopump spinning at 30,000 RPM ingests a gas bubble, catastrophic cavitation will rupture the engine.",
        sci_u4_val: "Ullage Burn 🔥",
        sci_u4_lbl: "Ullage Burn Maneuver 🔥",
        sci_u4_desc: "Firing forward RCS thrusters produces 0.02g acceleration, forcing 1,200t of cryogenic propellant to the sumps.",
        sci_body_ullage: "💡 <strong>Engineering Procedure:</strong> Prior to cryogenic transfer, the crew executes an Ullage Burn. Only once propellant settles at the tank sumps are the high-pressure cryogenic transfer umbilicals opened.",
        sci_r1_val: "Starbase",
        sci_r1_lbl: "Boca Chica, Texas",
        sci_r1_desc: "The real Starfactory facility and launch complexes engineered to build an interplanetary armada.",
        sci_r2_val: "Mechazilla",
        sci_r2_lbl: "Mid-Air Catch",
        sci_r2_desc: "In October 2024 (IFT-5), the 71-meter Super Heavy booster returned from space and was caught mid-air by Mechazilla Chopsticks!",
        sci_r3_val: "NASA Artemis",
        sci_r3_lbl: "NASA Artemis Program",
        sci_r3_desc: "NASA officially selected Starship HLS to land astronauts on the Moon, mandating orbital propellant refueling.",
        sci_r4_val: "Tipping Point",
        sci_r4_lbl: "Orbital Tests",
        sci_r4_desc: "SpaceX successfully demonstrated cryogenic propellant transfer inside Starship under NASA's Tipping Point contract.",
        sci_body_reality: "💡 <strong>This is not science fiction:</strong> Everything you operate in this mission — from Mechazilla to cryogenic transfer — is being engineered and flight-tested today by SpaceX and NASA. Our game is a rigorous simulation of real 2038 spaceflight!",
        btn_back_crew: "◀ BACK TO CREW",
        btn_start_docking: "TAKE CONTROLS & INITIATE DOCKING ➔",

        // HUD & Gameplay (EN)
        hud_mode_lbl: "MODE",
        hud_mode_val: "APPROACH (KURS SYSTEM)",
        hud_target_lbl: "TARGET",
        hud_target_val: "TANKER-01 (CH4/LOX)",
        hud_dist_lbl: "DISTANCE",
        hud_vel_lbl: "CLOSING VELOCITY",
        hud_align_lbl: "AXIAL ALIGNMENT",
        hud_fuel_lbl: "SHIP PROPELLANT",
        hud_rcs_lbl: "MANUAL RCS THRUSTERS:",
        hud_instructions: "💡 <strong>Instruction:</strong> Align the probe with the tanker drogue at relative speed under <strong>0.25 m/s</strong> and angular offset under <strong>2.0°</strong> for hard capture!",
        hud_align_ok: "ALIGNMENT: NOMINAL",
        hud_align_bad: "ALIGNMENT: CRITICAL OFFSET!",
        hud_dock_latched: "0.0 m (LATCHED)",
        modal_title: "🎯 HARD CAPTURE CONFIRMED!",
        modal_desc: "Docking mechanism locked. Cryogenic liquid methane and LOX transfer lines connected to Ares-1 tanks.",
        btn_ullage: "🔥 Ullage Burn Maneuver",
        btn_pump: "⚡ Transfer 1,200 Tons Propellant",
        btn_tmi: "🚀 UNDOCK & INITIATE TMI BURN ➔",
        toast_dock_success: "Docking latch engaged! Cryogenic umbilicals connected.",
        toast_ullage: "Ullage burn complete! Propellant settled at tank sumps.",
        toast_refuel_done: "Tanks full! 1,200 tons of liquid methane & LOX transferred.",
        toast_tmi: "Raptors ignited! On trajectory to Mars!",
        toast_bounce: "⚠️ Excessive closing speed! Rebound!"
      }
    };

    function toggleLanguage() {
      currentLang = currentLang === 'ru' ? 'en' : 'ru';
      document.getElementById('lang-btn').innerText = currentLang === 'ru' ? 'RU | EN' : 'EN | RU';
      applyLanguage();
    }

    function applyLanguage() {
      const d = DICT[currentLang];
      document.getElementById('sci-nav-btn').innerText = d.sci_nav_btn;
      document.getElementById('i18n-intro-year').innerText = d.intro_year;
      document.getElementById('i18n-intro-title').innerText = d.intro_title;
      document.getElementById('i18n-intro-text').innerText = d.intro_text;
      document.getElementById('i18n-btn-start').innerText = d.btn_start;
      document.getElementById('i18n-crew-heading').innerText = d.crew_heading;
      document.getElementById('i18n-crew-briefing').innerHTML = d.crew_briefing;
      document.getElementById('i18n-tab-canon').innerText = d.tab_canon;
      document.getElementById('i18n-tab-custom').innerText = d.tab_custom;

      // Agency tags
      document.getElementById('i18n-agency-1').innerText = d.agency_1;
      document.getElementById('i18n-agency-2').innerText = d.agency_2;
      document.getElementById('i18n-agency-3').innerText = d.agency_3;
      document.getElementById('i18n-agency-4').innerText = d.agency_4;

      // Specialization labels
      for (let i = 1; i <= 4; i++) {
        const el = document.getElementById('i18n-spec-lbl-' + i);
        if (el) el.innerText = d.spec_lbl;
        const st = document.getElementById('i18n-status-' + i);
        if (st) st.innerText = d.crew_status;
      }

      // Crew names, roles & specializations
      document.getElementById('i18n-crew-cmdr-name').innerText = d.crew_cmdr_name;
      document.getElementById('i18n-crew-cmdr-role').innerText = d.crew_cmdr_role;
      document.getElementById('i18n-crew-cmdr-spec').innerText = d.crew_cmdr_spec;

      document.getElementById('i18n-crew-plt-name').innerText = d.crew_plt_name;
      document.getElementById('i18n-crew-plt-role').innerText = d.crew_plt_role;
      document.getElementById('i18n-crew-plt-spec').innerText = d.crew_plt_spec;

      document.getElementById('i18n-crew-eng-name').innerText = d.crew_eng_name;
      document.getElementById('i18n-crew-eng-role').innerText = d.crew_eng_role;
      document.getElementById('i18n-crew-eng-spec').innerText = d.crew_eng_spec;

      document.getElementById('i18n-crew-med-name').innerText = d.crew_med_name;
      document.getElementById('i18n-crew-med-role').innerText = d.crew_med_role;
      document.getElementById('i18n-crew-med-spec').innerText = d.crew_med_spec;

      // Custom crew skills
      document.getElementById('i18n-custom-desc').innerText = d.custom_desc;
      document.getElementById('i18n-skill-pilot').innerText = d.skill_pilot;
      document.getElementById('i18n-skill-eng').innerText = d.skill_eng;
      document.getElementById('i18n-skill-med').innerText = d.skill_med;
      document.getElementById('i18n-skill-psy').innerText = d.skill_psy;

      document.getElementById('i18n-btn-confirm-crew').innerText = d.btn_confirm_crew;
      
      // Science Briefing translation
      document.getElementById('i18n-sci-tag').innerText = d.sci_tag;
      updateScienceTitle();
      document.getElementById('i18n-sci-tab1').innerText = d.sci_tab1;
      document.getElementById('i18n-sci-tab2').innerText = d.sci_tab2;
      document.getElementById('i18n-sci-tab3').innerText = d.sci_tab3;
      document.getElementById('i18n-sci-tab4').innerText = d.sci_tab4;

      // Tab 1
      document.getElementById('i18n-sci-f1-val').innerText = d.sci_f1_val;
      document.getElementById('i18n-sci-f1-lbl').innerText = d.sci_f1_lbl;
      document.getElementById('i18n-sci-f1-desc').innerText = d.sci_f1_desc;
      document.getElementById('i18n-sci-f2-val').innerText = d.sci_f2_val;
      document.getElementById('i18n-sci-f2-lbl').innerText = d.sci_f2_lbl;
      document.getElementById('i18n-sci-f2-desc').innerText = d.sci_f2_desc;
      document.getElementById('i18n-sci-f3-val').innerText = d.sci_f3_val;
      document.getElementById('i18n-sci-f3-lbl').innerText = d.sci_f3_lbl;
      document.getElementById('i18n-sci-f3-desc').innerText = d.sci_f3_desc;
      document.getElementById('i18n-sci-f4-val').innerText = d.sci_f4_val;
      document.getElementById('i18n-sci-f4-lbl').innerText = d.sci_f4_lbl;
      document.getElementById('i18n-sci-f4-desc').innerText = d.sci_f4_desc;
      document.getElementById('i18n-sci-body-launch').innerHTML = d.sci_body_launch;

      // Tab 2
      document.getElementById('i18n-sci-formula-desc').innerText = d.sci_formula_desc;
      document.getElementById('i18n-sci-t1-val').innerText = d.sci_t1_val;
      document.getElementById('i18n-sci-t1-lbl').innerText = d.sci_t1_lbl;
      document.getElementById('i18n-sci-t1-desc').innerText = d.sci_t1_desc;
      document.getElementById('i18n-sci-t2-val').innerText = d.sci_t2_val;
      document.getElementById('i18n-sci-t2-lbl').innerText = d.sci_t2_lbl;
      document.getElementById('i18n-sci-t2-desc').innerText = d.sci_t2_desc;
      document.getElementById('i18n-sci-t3-val').innerText = d.sci_t3_val;
      document.getElementById('i18n-sci-t3-lbl').innerText = d.sci_t3_lbl;
      document.getElementById('i18n-sci-t3-desc').innerText = d.sci_t3_desc;
      document.getElementById('i18n-sci-t4-val').innerText = d.sci_t4_val;
      document.getElementById('i18n-sci-t4-lbl').innerText = d.sci_t4_lbl;
      document.getElementById('i18n-sci-t4-desc').innerText = d.sci_t4_desc;
      document.getElementById('i18n-sci-body-tsiolk').innerHTML = d.sci_body_tsiolk;

      // Tab 3
      document.getElementById('i18n-sci-u1-val').innerText = d.sci_u1_val;
      document.getElementById('i18n-sci-u1-lbl').innerText = d.sci_u1_lbl;
      document.getElementById('i18n-sci-u1-desc').innerText = d.sci_u1_desc;
      document.getElementById('i18n-sci-u2-val').innerText = d.sci_u2_val;
      document.getElementById('i18n-sci-u2-lbl').innerText = d.sci_u2_lbl;
      document.getElementById('i18n-sci-u2-desc').innerText = d.sci_u2_desc;
      document.getElementById('i18n-sci-u3-val').innerText = d.sci_u3_val;
      document.getElementById('i18n-sci-u3-lbl').innerText = d.sci_u3_lbl;
      document.getElementById('i18n-sci-u3-desc').innerText = d.sci_u3_desc;
      document.getElementById('i18n-sci-u4-val').innerText = d.sci_u4_val;
      document.getElementById('i18n-sci-u4-lbl').innerText = d.sci_u4_lbl;
      document.getElementById('i18n-sci-u4-desc').innerText = d.sci_u4_desc;
      document.getElementById('i18n-sci-body-ullage').innerHTML = d.sci_body_ullage;

      // Tab 4
      document.getElementById('i18n-sci-r1-val').innerText = d.sci_r1_val;
      document.getElementById('i18n-sci-r1-lbl').innerText = d.sci_r1_lbl;
      document.getElementById('i18n-sci-r1-desc').innerText = d.sci_r1_desc;
      document.getElementById('i18n-sci-r2-val').innerText = d.sci_r2_val;
      document.getElementById('i18n-sci-r2-lbl').innerText = d.sci_r2_lbl;
      document.getElementById('i18n-sci-r2-desc').innerText = d.sci_r2_desc;
      document.getElementById('i18n-sci-r3-val').innerText = d.sci_r3_val;
      document.getElementById('i18n-sci-r3-lbl').innerText = d.sci_r3_lbl;
      document.getElementById('i18n-sci-r3-desc').innerText = d.sci_r3_desc;
      document.getElementById('i18n-sci-r4-val').innerText = d.sci_r4_val;
      document.getElementById('i18n-sci-r4-lbl').innerText = d.sci_r4_lbl;
      document.getElementById('i18n-sci-r4-desc').innerText = d.sci_r4_desc;
      document.getElementById('i18n-sci-body-reality').innerHTML = d.sci_body_reality;

      document.getElementById('i18n-btn-back-crew').innerText = d.btn_back_crew;
      document.getElementById('i18n-btn-start-docking').innerText = d.btn_start_docking;

      // Gameplay HUD & Refuel Modal
      document.getElementById('i18n-hud-mode').innerText = d.hud_mode_lbl;
      document.getElementById('i18n-hud-mode-val').innerText = d.hud_mode_val;
      document.getElementById('i18n-hud-target').innerText = d.hud_target_lbl;
      document.getElementById('i18n-hud-target-val').innerText = d.hud_target_val;
      document.getElementById('i18n-hud-dist').innerText = d.hud_dist_lbl;
      document.getElementById('i18n-hud-vel').innerText = d.hud_vel_lbl;
      document.getElementById('i18n-hud-align').innerText = d.hud_align_lbl;
      document.getElementById('i18n-hud-fuel').innerText = d.hud_fuel_lbl;
      document.getElementById('i18n-hud-rcs-lbl').innerText = d.hud_rcs_lbl;
      document.getElementById('i18n-hud-instructions').innerHTML = d.hud_instructions;
      document.getElementById('i18n-modal-title').innerText = d.modal_title;
      document.getElementById('i18n-modal-desc').innerText = d.modal_desc;
      document.getElementById('i18n-btn-ullage').innerText = d.btn_ullage;
      document.getElementById('i18n-btn-pump').innerText = d.btn_pump;
      document.getElementById('i18n-btn-tmi').innerText = d.btn_tmi;
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
       3. ПЕРЕКЛЮЧЕНИЕ ЭКРАНОВ И ВКЛАДОК
       ========================================================== */
    function showScreen(id) {
      document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
      document.getElementById(id).classList.add('active');
    }

    function showIntroScreen() {
      showScreen('screen-intro');
    }

    function showCrewScreen() {
      showScreen('screen-crew');
    }

    function showScienceScreen() {
      showScreen('screen-science');
    }

    function switchCrewTab(tab, btn) {
      document.querySelectorAll('.crew-tabs .tab-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      if (tab === 'canon') {
        document.getElementById('canon-crew-grid').style.display = 'grid';
        document.getElementById('custom-crew-box').style.display = 'none';
      } else {
        document.getElementById('canon-crew-grid').style.display = 'none';
        document.getElementById('custom-crew-box').style.display = 'block';
      }
    }

    let currentScienceTab = 'tab-launch';

    function switchScienceTab(tabId, btn) {
      currentScienceTab = tabId;
      document.querySelectorAll('.science-tabs .tab-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      document.querySelectorAll('.science-content-box').forEach(box => box.style.display = 'none');
      const target = document.getElementById(tabId);
      if (target) target.style.display = 'flex';
      updateScienceTitle();
    }

    function updateScienceTitle() {
      const d = DICT[currentLang];
      const key = 'sci_title_' + currentScienceTab.replace('-', '_');
      if (d && d[key]) {
        document.getElementById('i18n-sci-title').innerText = d[key];
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

      // Земля внизу на горизонте
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

      // Закрылки
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

      // Солнечные батареи танкера
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

        // Расчет дистанции
        const dist = Math.abs(shipPos.z - (-7.0));
        const approachVel = shipVel.z;
        const alignOffset = Math.sqrt(shipPos.x * shipPos.x + shipPos.y * shipPos.y);

        // Обновление HUD
        const distUnit = currentLang === 'ru' ? ' м' : ' m';
        const velUnit = currentLang === 'ru' ? ' м/с' : ' m/s';
        document.getElementById('hud-dist').innerText = dist.toFixed(1) + distUnit;
        document.getElementById('hud-vel').innerText = approachVel.toFixed(2) + velUnit;
        document.getElementById('hud-align').innerText = '±' + (alignOffset * 0.8).toFixed(1) + '°';

        const alignStatusEl = document.getElementById('hud-alignment-status');
        if (alignOffset < 1.2) {
          alignStatusEl.innerText = DICT[currentLang].hud_align_ok;
          alignStatusEl.style.color = '#00f0ff';
        } else {
          alignStatusEl.innerText = DICT[currentLang].hud_align_bad;
          alignStatusEl.style.color = '#ff4757';
        }

        // Движение маркера прицела
        const targetMarker = document.getElementById('target-marker');
        targetMarker.style.transform = `translate(${shipPos.x * 12}px, ${-shipPos.y * 12}px)`;

        // Проверка жесткой сцепки (Hard Capture)
        if (dist < 1.4 && dist > -1.0) {
          if (approachVel <= 0.25 && alignOffset < 1.2) {
            completeDocking();
          } else if (approachVel > 0.4) {
            showToast(DICT[currentLang].toast_bounce);
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

      document.getElementById('hud-dist').innerText = DICT[currentLang].hud_dock_latched;
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
        const tonsStr = currentLang === 'ru' ? `${tons} / 1200 тонн` : `${tons} / 1,200 tons`;
        document.getElementById('modal-fuel-text').innerText = `${p}% (${tonsStr})`;
        const shipFuelStr = currentLang === 'ru' ? `${tons} т` : `${tons} t`;
        document.getElementById('hud-propellant').innerText = `${p}% (${shipFuelStr})`;

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

# Perform replacements of inlined three.js, orbitControls, textures, and crew
final_html = HTML_CONTENT.replace('__THREE_SRC__', three_src)
final_html = final_html.replace('__ORBIT_SRC__', orbit_src)
final_html = final_html.replace('__EARTH_B64__', EARTH_B64)
final_html = final_html.replace('__CLOUDS_B64__', CLOUDS_B64)
final_html = final_html.replace('__SPEC_B64__', SPEC_B64)

final_html = final_html.replace('__VANCE_B64__', VANCE_B64)
final_html = final_html.replace('__ROMANOVA_B64__', ROMANOVA_B64)
final_html = final_html.replace('__CHEN_B64__', CHEN_B64)
final_html = final_html.replace('__REID_B64__', REID_B64)

with open(r'D:\mars-transit-odyssey\index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

with open(r'C:\Users\User\Desktop\Полет на Марс 3D.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

# Also update build_game_v1.py to match so future builds keep this
with open(r'D:\mars-transit-odyssey\build_game_v1.py', 'w', encoding='utf-8') as f:
    with open(__file__, 'r', encoding='utf-8') as current_f:
        f.write(current_f.read())

print("Game v2 with Real Orbital Physics Briefing built successfully on Drive D: and Desktop!")
