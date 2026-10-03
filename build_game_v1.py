# -*- coding: utf-8 -*-
"""
Builder v2 for Mars Transit Odyssey: Phase 1 + Science Briefing (Real Orbital Physics, Tsiolkovsky, Cryogenics & Ullage)
"""

import sys
sys.path.append(r'D:\mars-transit-odyssey')
from textures_b64 import EARTH_B64, CLOUDS_B64, SPEC_B64, MARS_B64, SUN_B64, MOON_B64
from crew_b64 import VANCE_B64, ROMANOVA_B64, CHEN_B64, REID_B64
from audio_b64 import MAIN_THEME_B64
import base64 as _b64
with open(r'D:\mars-transit-odyssey\assets\intro_720p.mp4', 'rb') as _vf:
    INTRO_VIDEO_B64 = 'data:video/mp4;base64,' + _b64.b64encode(_vf.read()).decode('ascii')

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
    /* ===== INTRO CINEMATIC ===== */
    #cinematic { position: fixed; inset: 0; z-index: 99999; background: #000; display: flex; align-items: center; justify-content: center; transition: opacity 0.8s; }
    #cinematic.hidden { opacity: 0; pointer-events: none; }
    #cinematic video { width: 100%; height: 100%; object-fit: contain; background: #000; }
    #cine-start { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 18px; background: radial-gradient(circle at center, #0a1a2e 0%, #000 75%); cursor: pointer; }
    #cine-start .cine-title { font-size: 34px; font-weight: 800; letter-spacing: 3px; color: #00f0ff; text-align: center; }
    #cine-start .cine-play { font-size: 20px; padding: 14px 34px; border: 2px solid #00f0ff; border-radius: 40px; color: #fff; background: rgba(0,240,255,0.1); }
    #cine-skip { position: absolute; right: 24px; bottom: 24px; z-index: 2; padding: 10px 22px; background: rgba(0,0,0,0.55); color: #fff; border: 1px solid rgba(255,255,255,0.5); border-radius: 24px; cursor: pointer; font-size: 15px; display: none; }
    #cine-skip:hover { background: rgba(0,240,255,0.25); }
    /* ===== CREW CONSTRUCTOR ===== */
    .cc-wrap { display: grid; grid-template-columns: 1.1fr 1fr; gap: 18px; }
    @media (max-width: 800px) { .cc-wrap { grid-template-columns: 1fr; } }
    .cc-form, .cc-roster { background: rgba(0,0,0,0.4); border: 1px solid rgba(0,210,255,0.2); border-radius: 8px; padding: 16px; display: flex; flex-direction: column; gap: 10px; font-size: 13px; color: #cbd5e1; }
    .cc-title { font-weight: 800; color: #00f0ff; letter-spacing: 1px; }
    .cc-avatars { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
    .cc-av { width: 46px; height: 46px; border-radius: 50%; border: 2px solid transparent; background: rgba(255,255,255,0.07); font-size: 26px; cursor: pointer; display: flex; align-items: center; justify-content: center; overflow: hidden; padding: 0; }
    .cc-av.sel { border-color: #00f0ff; box-shadow: 0 0 10px rgba(0,240,255,0.6); }
    .cc-av img { width: 100%; height: 100%; object-fit: cover; }
    .cc-upload span { cursor: pointer; color: #00f0ff; text-decoration: underline; font-size: 12px; }
    .cc-input { background: rgba(255,255,255,0.07); color: #fff; border: 1px solid rgba(255,255,255,0.2); border-radius: 6px; padding: 9px; font-size: 14px; }
    .cc-input option { background: #0b1220; }
    .cc-pts strong { color: #00f0ff; font-size: 18px; }
    .cc-skill { display: flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.05); padding: 6px 10px; border-radius: 6px; }
    .cc-skill .nm { flex: 1; }
    .cc-skill button { width: 28px; height: 28px; border-radius: 50%; border: 1px solid #00f0ff; background: transparent; color: #00f0ff; font-size: 18px; cursor: pointer; line-height: 1; }
    .cc-skill button:hover { background: rgba(0,240,255,0.2); }
    .cc-skill .val { width: 22px; text-align: center; font-weight: 800; color: #fff; }
    .cc-perks { font-size: 12px; color: #9fb3c8; min-height: 18px; }
    .cc-card { display: flex; gap: 12px; background: rgba(255,255,255,0.05); border-radius: 8px; padding: 10px; align-items: center; margin-bottom: 8px; }
    .cc-card .cc-av { flex: none; cursor: default; width: 52px; height: 52px; }
    .cc-card .info { flex: 1; font-size: 12px; }
    .cc-card .info b { font-size: 14px; color: #fff; }
    .cc-card .del { background: transparent; border: 1px solid #ff4d6d; color: #ff4d6d; border-radius: 6px; cursor: pointer; padding: 4px 8px; }
    .science-content-box .science-card-grid { grid-template-columns: 1fr; }
    .science-content-box .sci-fact-desc { font-size: 14px; line-height: 1.65; color: #b6c4d6; }
    .science-content-box .sci-fact-label { font-size: 13px; color: #00e699; }
    .science-content-box .sci-fact-val { font-size: 24px; }
    .science-content-box .sci-body-text { font-size: 14px; line-height: 1.65; }
  </style>
</head>
<body>

  <!-- INTRO CINEMATIC -->
  <div id="cinematic">
    <video id="cine-video" playsinline src="__INTRO_VIDEO_B64__"></video>
    <div id="cine-start" onclick="playCinematic()">
      <div class="cine-title">АРЕС-1: МАРСИАНСКИЙ ТРАНЗИТ</div>
      <div class="cine-play" id="cine-play-label">▶ СМОТРЕТЬ ЗАСТАВКУ (со звуком)</div>
    </div>
    <button id="cine-skip" onclick="endCinematic()">ПРОПУСТИТЬ ⏭</button>
  </div>

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
            <div class="crew-spec-desc" id="i18n-crew-cmdr-spec">Аварийное управление: аварии устраняются на 15% быстрее</div>
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
            <div class="crew-spec-desc" id="i18n-crew-plt-spec">Пилотирование: +20% к точности ручной стыковки</div>
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
            <div class="crew-spec-desc" id="i18n-crew-eng-spec">Инженерия: -25% износ двигателей и расход запчастей</div>
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
            <div class="crew-spec-desc" id="i18n-crew-med-spec">Биомедицина: +20% к запасу здоровья экипажа в невесомости</div>
          </div>
          <div class="crew-status">
            <span class="status-dot"></span>
            <span id="i18n-status-4">К ПОЛЕТУ ДОПУЩЕН</span>
          </div>
        </div>
      </div>

      <!-- Custom Crew Builder (Toggleable) -->
      <div id="custom-crew-box" style="display: none;">
        <div class="cc-wrap">
          <div class="cc-form">
            <div class="cc-title" id="cc-t-new"></div>
            <div class="cc-avatars" id="cc-avatars"></div>
            <label class="cc-upload"><input type="file" accept="image/*" id="cc-photo" onchange="ccPhoto(this)" style="display:none"><span id="cc-t-upload"></span></label>
            <input class="cc-input" id="cc-name" maxlength="24">
            <select class="cc-input" id="cc-role"></select>
            <select class="cc-input" id="cc-agency"></select>
            <div class="cc-pts"><span id="cc-t-pts"></span> <strong id="cc-pts-left">15</strong></div>
            <div id="cc-skills"></div>
            <div class="cc-perks" id="cc-perks"></div>
            <button class="btn-glow" style="width:100%" onclick="ccAdd()" id="cc-add-btn"></button>
          </div>
          <div class="cc-roster">
            <div class="cc-title"><span id="cc-t-roster"></span> <span id="cc-count">0/4</span></div>
            <div id="cc-list"></div>
          </div>
        </div>
      </div>

      <div style="display: flex; justify-content: flex-end; margin-top: 10px;">
        <button class="btn-glow" onclick="confirmCrew()" id="i18n-btn-confirm-crew">
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
        <div class="sci-body-text" id="i18n-sci-intro-launch">🎓 <strong>Добро пожаловать на экскурсию!</strong> Представьте: нужно поднять в небо многоэтажный дом и разогнать его до 28 000 километров в час. Именно так быстро надо лететь, чтобы остаться на орбите — то есть кружить вокруг Земли по замкнутому пути и не падать. Такой путь называется орбитой. Это делает самая большая ракета в истории. Она состоит из двух частей. Нижняя — ускоритель Super Heavy («Супер Хеви», по-русски «Сверхтяжёлый»): он даёт основной разгон. Верхняя — космический корабль Starship («Старшип», «Звёздный корабль»): в нём летит экипаж, и именно он дойдёт до Марса. Вместе их называют системой Starship. Давайте разберём её по главам.</div>
        <div class="science-card-grid">
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-f1-val">5 000 тонн</div>
            <div class="sci-fact-label" id="i18n-sci-f1-lbl">Глава 1. Огромный вес</div>
            <div class="sci-fact-desc" id="i18n-sci-f1-desc">Полностью заправленная ракета весит 5 000 тонн. Это как 11 больших пассажирских самолётов Боинг-747, сложенных вместе. Почти всё это — топливо: ракета на 90% состоит из него. Для сравнения: Saturn V («Сатурн-5»), ракета, которая в 1969 году доставила людей на Луну, весила около 3 000 тонн — почти вдвое меньше.</div>
          </div>
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-f2-val">7 500 тонн тяги</div>
            <div class="sci-fact-label" id="i18n-sci-f2-lbl">Глава 2. Сила, которая поднимает</div>
            <div class="sci-fact-desc" id="i18n-sci-f2-desc">Тяга — это сила, с которой двигатели толкают ракету вверх. Её измеряют в тоннах силы: тяга 7 500 тонн значит, что двигатели смогли бы удержать на весу груз в 7 500 тонн. Двигателей 33, они называются Raptor («Раптор», хищная птица) и работают на метане и жидком кислороде. А теперь сравните: ракета весит 5 000 тонн, а толкают её вверх с силой 7 500. Тяга больше веса на 2 500 тонн — именно этот излишек и разгоняет ракету. Будь тяга меньше веса, ракета просто осталась бы на земле.</div>
          </div>
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-f3-val">Горячее разделение</div>
            <div class="sci-fact-label" id="i18n-sci-f3-lbl">Глава 3. Огонь вместо паузы</div>
            <div class="sci-fact-desc" id="i18n-sci-f3-desc">Примерно через две с половиной минуты полёта ускоритель отработал своё и должен отцепиться. Обычно двигатели верхней части включают уже после отделения. Здесь иначе: корабль зажигает свои двигатели ещё пока они скреплены и огнём отталкивается от ускорителя. Это называют «горячим разделением» (по-английски hot-staging). Выигрыш в том, что ни секунды не теряется без тяги, и ракета продолжает разгоняться.</div>
          </div>
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-f4-val">28 000 км/ч</div>
            <div class="sci-fact-label" id="i18n-sci-f4-lbl">Глава 4. Скорость, чтобы не упасть</div>
            <div class="sci-fact-desc" id="i18n-sci-f4-desc">Сначала про высоту. 320 километров над поверхностью Земли — это уже почти космос, но притяжение Земли там всё ещё почти такое же, как у нас на земле (около 90%). Если корабль просто повиснет на этой высоте, он упадёт вниз, как камень.<br><br>Как же тогда не упасть? Проведём опыт в уме. Бросьте мяч вперёд, параллельно земле: он пролетит несколько метров и упадёт. Бросьте сильнее — упадёт дальше. Теперь представьте гигантскую пушку, которая стреляет ядром вдоль поверхности Земли, по горизонтали, а не вверх. Ядро летит далеко-далеко, но Земля круглая, и её поверхность по пути загибается вниз. Чем быстрее выстрел, тем дальше успевает улететь ядро, пока падает.<br><br>И при скорости 7,8 километра в секунду (это 28 000 км/ч) происходит удивительное: пока корабль падает вниз, поверхность Земли загибается вниз ровно на столько же. Корабль падает, а земля всё не приближается. Он падает без конца и так обходит всю планету по кругу.<br><br>Этот замкнутый путь вокруг Земли и называется орбитой. А скорость, нужная, чтобы выйти на орбиту рядом с Землёй, называется первой космической. Вот почему главное для ракеты — не подняться вверх, а разогнаться вдоль Земли. Кстати, именно поэтому космонавты на орбите парят: гравитация не пропала, они просто вместе с кораблём в вечном падении.</div>
          </div>
        </div>
        <div class="sci-body-text" id="i18n-sci-body-launch">💡 <strong>Как мы здесь оказались:</strong> подъём на орбиту — это не про высоту, а про скорость. Подняться на 320 км легко, трудно разогнаться до 7,8 км/с. Для этого ракета сожгла около 4 500 тонн топлива: 3 400 в ускорителе и 1 100 в корабле. Корабль на орбите, но баки почти пусты: осталось 96 тонн из 1 200. Именно с этого начинается ваша миссия.</div>
      </div>

      <!-- Tab 2: Tsiolkovsky Equation -->
      <div class="science-content-box" id="tab-tsiolkovsky" style="display: none;">
        <div class="sci-body-text" id="i18n-sci-intro-tsiolk">🎓 <strong>Самая важная формула космонавтики.</strong> В 1903 году её вывел русский учёный Константин Циолковский. Она отвечает на простой вопрос: сколько топлива нужно ракете, чтобы набрать нужную скорость? Ответ неожиданный: гораздо больше, чем кажется. Сейчас разберёмся, почему, и заодно поймём, зачем нашему кораблю на орбите нужна дозаправка.</div>
        <div class="sci-formula-box">
          <div class="sci-formula">Δv = I_sp · g_0 · ln(m_0 / m_k)</div>
          <div class="sci-formula-desc" id="i18n-sci-formula-desc">Ракетное уравнение Циолковского (1903 год). Расшифровка — ниже.</div>
        </div>
        <div class="sci-body-text" id="i18n-sci-formula-explain"><strong>Как читать формулу:</strong><br><strong>Δv</strong> («дельта-вэ») — на сколько ракета может увеличить свою скорость, пока не кончится топливо. Это её «запас хода», только измеряется он не в километрах, а в километрах в секунду.<br><strong>I<sub>sp</sub> · g<sub>0</sub></strong> — скорость, с которой двигатель выбрасывает раскалённый газ назад. У наших двигателей Raptor это около 3,7 км/с. Чем быстрее вылетает струя, тем сильнее толчок.<br><strong>m<sub>0</sub></strong> — масса ракеты с полными баками. <strong>m<sub>k</sub></strong> — масса той же ракеты, когда топливо выгорело.<br><strong>ln</strong> — «натуральный логарифм». Не пугайтесь: для нас он означает одно. Скорость растёт медленно, а нужное топливо — очень быстро. Каждые лишние 3,7 км/с скорости делают полную ракету тяжелее пустой ещё в 2,7 раза. Два таких прироста — уже в 7 раз, три — в 20 раз. Вот что значит «топлива нужно в разы больше».</div>
        <div class="science-card-grid">
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-t1-val">92%</div>
            <div class="sci-fact-label" id="i18n-sci-t1-lbl">Глава 1. Топливо, которое везёт само себя</div>
            <div class="sci-fact-desc" id="i18n-sci-t1-desc">Ракете нужно разогнать не только корабль, но и своё собственное топливо. Чтобы разогнать груз, нужно топливо. Чтобы разогнать это топливо, нужно ещё топливо. И так далее по кругу. Поэтому почти вся масса ракеты — топливо. Из 1 200 тонн топлива нашего корабля на подъём к орбите ушло 1 100 тонн, то есть 92%. Учёные называют это «тиранией ракетного уравнения».</div>
          </div>
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-t2-val">96 тонн</div>
            <div class="sci-fact-label" id="i18n-sci-t2-lbl">Глава 2. Что осталось в баках</div>
            <div class="sci-fact-desc" id="i18n-sci-t2-desc">На орбите в баках осталось 96 тонн, это 8% от полной заправки. По формуле выходит запас скорости около 1,3 км/с. Этого хватит, чтобы маневрировать на орбите, состыковаться с танкером и при необходимости вернуться на Землю. Но для полёта к Марсу — слишком мало.</div>
          </div>
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-t3-val">3,6 км/с</div>
            <div class="sci-fact-label" id="i18n-sci-t3-lbl">Глава 3. Второй мощный толчок</div>
            <div class="sci-fact-desc" id="i18n-sci-t3-desc">Чтобы покинуть орбиту Земли и взять курс на Марс, нужно ещё раз сильно разогнаться: добавить к скорости 3,6 км/с. Двигатели включаются один раз, а потом корабль летит по инерции, как брошенный камень, много месяцев. По формуле для такого толчка нужно около 370 тонн топлива — почти в четыре раза больше, чем осталось в баках.</div>
          </div>
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-t4-val">1 200 тонн</div>
            <div class="sci-fact-label" id="i18n-sci-t4-lbl">Глава 4. Полные баки</div>
            <div class="sci-fact-desc" id="i18n-sci-t4-desc">Если заправить корабль до краёв, его запас скорости вырастет до 6,9 км/с. Этого хватит на разгон к Марсу, торможение, посадку и небольшой запас на непредвиденные ситуации. Недостающие 1 100 тонн топлива привезут танкеры — специальные корабли-заправщики.</div>
          </div>
        </div>
        <div class="sci-body-text" id="i18n-sci-body-tsiolk">💡 <strong>Вся правда без иллюзий:</strong> корабль такого размера не может взять при старте и экипаж, и всё топливо на дорогу до Марса: слишком тяжёлым он получится, и ракета его не поднимет. Поэтому корабль выводят на орбиту почти пустым, а потом танкеры один за другим привозят топливо. Ваша задача — принять его: сначала стыковка, потом перекачка.</div>
      </div>

      <!-- Tab 3: Cryogenics & Ullage -->
      <div class="science-content-box" id="tab-ullage" style="display: none;">
        <div class="sci-body-text" id="i18n-sci-intro-ullage">🎓 <strong>Задача: перекачать ледяную жидкость там, где нет «низа».</strong> На Земле жидкость сама течёт вниз. Но на орбите всё иначе, а нам нужно перелить 1 100 тонн ледяного топлива из танкера в наш корабль. Это самая хитрая инженерная задача нашей миссии. Давайте разберём её по шагам.</div>
        <div class="science-card-grid">
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-u1-val">−161 °C и −183 °C</div>
            <div class="sci-fact-label" id="i18n-sci-u1-lbl">Глава 1. Топливо холоднее Антарктиды</div>
            <div class="sci-fact-desc" id="i18n-sci-u1-desc">Чтобы 1 200 тонн топлива поместились в баки, метан и кислород охлаждают, пока они не превратятся в жидкость. Жидкий метан кипит при −161 °C, жидкий кислород — при −183 °C. Для сравнения: самый сильный мороз в Антарктиде — около −89 °C. Такое сверххолодное топливо называют криогенным (от греческого «криос» — холод). Если баки плохо защищены от тепла, оно закипает и улетучивается.</div>
          </div>
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-u2-val">Невесомость</div>
            <div class="sci-fact-label" id="i18n-sci-u2-lbl">Глава 2. Жидкость без «низа»</div>
            <div class="sci-fact-desc" id="i18n-sci-u2-desc">Жидкость течёт вниз, потому что её тянет гравитация. На орбите корабль и всё внутри него падает вместе — это и есть невесомость. Жидкость больше не прижимается ко дну: она собирается в плавающие шары и липнет к стенкам бака. Как вода на МКС: пролейте — получите шар. А насос стоит у дна бака и может остаться без жидкости.</div>
          </div>
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-u3-val">Кавитация ⚠️</div>
            <div class="sci-fact-label" id="i18n-sci-u3-lbl">Глава 3. Пузырь в насосе — это взрыв</div>
            <div class="sci-fact-desc" id="i18n-sci-u3-desc">Насос (турбонасос) гонит топливо в двигатель: его лопасти делают 30 000 оборотов в минуту. Если вместо жидкости насос засосёт пузырь газа, лопасти теряют опору, нагрузка скачет, и насос разрывает на куски. Это явление называется кавитацией. В невесомости пузыри — обычное дело, поэтому для нас это главная опасность.</div>
          </div>
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-u4-val">Осаждение топлива 🔥</div>
            <div class="sci-fact-label" id="i18n-sci-u4-lbl">Глава 4. Лёгкий толчок возвращает «низ»</div>
            <div class="sci-fact-desc" id="i18n-sci-u4-desc">Решение придумали такое: включить маленькие двигатели ориентации (RCS) и слегка разогнать корабль вперёд. Жидкость по инерции прижмётся к задней стенке — как кофе в машине при разгоне, — и «низ» вернётся. Нужно всего 0,02 g, это в 50 раз слабее земной тяжести. Такой манёвр называют осаждением топлива (по-английски ullage burn).</div>
          </div>
        </div>
        <div class="sci-body-text" id="i18n-sci-body-ullage">💡 <strong>Правило перекачки:</strong> сначала толчок, потом насос. Прежде чем перекачивать сотни тонн метана, экипаж даёт импульс осаждения. Только когда топливо осело на дно, открываются магистрали. Пропустите этот шаг — и насос захлебнётся газом.</div>
      </div>

      <!-- Tab 4: Real XXI Century Engineering -->
      <div class="science-content-box" id="tab-reality" style="display: none;">
        <div class="sci-body-text" id="i18n-sci-intro-reality">🎓 <strong>Всё, о чём мы рассказали, — не выдумка.</strong> Эти технологии строят и испытывают прямо сейчас, в наше время. Вот четыре факта, которые можно проверить.</div>
        <div class="science-card-grid">
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-r1-val">Старбейс</div>
            <div class="sci-fact-label" id="i18n-sci-r1-lbl">Глава 1. Город ракет в Техасе</div>
            <div class="sci-fact-desc" id="i18n-sci-r1-desc">Старбейс (Starbase) — посёлок и космодром на юге Техаса, на берегу океана. Здесь компания SpaceX строит корабли Starship и запускает их в космос.</div>
          </div>
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-r2-val">Мехазилла</div>
            <div class="sci-fact-label" id="i18n-sci-r2-lbl">Глава 2. Ракету поймали на лету</div>
            <div class="sci-fact-desc" id="i18n-sci-r2-desc">13 октября 2024 года, пятый испытательный полёт. 71-метровый ускоритель Super Heavy вернулся к стартовой башне, и она поймала его на лету двумя гигантскими «палочками для еды». Башню прозвали Мехазилла (Mechazilla). Благодаря этому ускоритель можно использовать снова и снова.</div>
          </div>
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-r3-val">NASA и «Артемида»</div>
            <div class="sci-fact-label" id="i18n-sci-r3-lbl">Глава 3. Луна — тоже через дозаправку</div>
            <div class="sci-fact-desc" id="i18n-sci-r3-desc">NASA — это американское космическое агентство. Его программа «Артемида» (Artemis) вернёт людей на Луну. Для посадки выбрали лунную версию Starship, и ей, как и нашему кораблю, нужна дозаправка на орбите.</div>
          </div>
          <div class="sci-fact-card">
            <div class="sci-fact-val" id="i18n-sci-r4-val">«Переломный момент»</div>
            <div class="sci-fact-label" id="i18n-sci-r4-lbl">Глава 4. Заправка в космосе: пока в испытаниях</div>
            <div class="sci-fact-desc" id="i18n-sci-r4-desc">«Переломный момент» (Tipping Point) — программа NASA, которая платит компаниям за испытания новых технологий. По ней SpaceX перекачала жидкий кислород из одного бака в другой внутри корабля. Перекачка между двумя кораблями на орбите — следующий шаг.</div>
          </div>
        </div>
        <div class="sci-body-text" id="i18n-sci-body-reality">💡 <strong>Это не фантастика:</strong> всё, что вы делаете в этой миссии — стыковка, перекачка криогенного топлива — это реальные задачи, над которыми сегодня работают инженеры SpaceX и NASA. Мы лишь перенесли их в 2038 год.</div>
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
        crew_cmdr_spec: "Аварийное управление: аварии устраняются на 15% быстрее",
        crew_plt_name: "Елена Романова",
        crew_plt_role: "Главный пилот",
        crew_plt_spec: "Пилотирование: +20% к точности ручной стыковки",
        crew_eng_name: "Чэнь Вэй",
        crew_eng_role: "Бортинженер",
        crew_eng_spec: "Инженерия: -25% износ двигателей и расход запчастей",
        crew_med_name: "д-р Маркус Рид",
        crew_med_role: "Судовой врач",
        crew_med_spec: "Биомедицина: +20% к запасу здоровья экипажа в невесомости",
        crew_status: "К ПОЛЕТУ ДОПУЩЕН",
        custom_desc: "Распределите очки квалификации экипажа (доступно: 12 очков):",
        skill_pilot: "Пилотирование",
        skill_eng: "Инженерия СЖО/ДУ",
        skill_med: "Биомедицина",
        skill_psy: "Психоустойчивость",
        btn_confirm_crew: "УТВЕРДИТЬ ЭКИПАЖ И ПЕРЕЙТИ К БРИФИНГУ ➔",
        
        // Science Briefing (RU)
        sci_tag: "БОРТОВОЙ СПРАВОЧНИК // РЕАЛЬНАЯ АЭРОКОСМИЧЕСКАЯ ФИЗИКА",
        sci_title_tab_launch: "1. ВЫВЕДЕНИЕ НА ОРБИТУ: СВЕРХТЯЖЁЛЫЙ СТАРТ И СКОРОСТЬ 7,8 КМ/С",
        sci_title_tab_tsiolkovsky: "2. УРАВНЕНИЕ ЦИОЛКОВСКОГО: ПОЧЕМУ РАКЕТЕ НУЖНО ТАК МНОГО ТОПЛИВА И ЗАЧЕМ ДОЗАПРАВКА",
        sci_title_tab_ullage: "3. КРИОГЕННОЕ ТОПЛИВО В НЕВЕСОМОСТИ: КАК ПЕРЕКАЧАТЬ ЖИДКОСТЬ, У КОТОРОЙ НЕТ «НИЗА»",
        sci_title_tab_reality: "4. РЕАЛЬНОСТЬ XXI ВЕКА: МЕХАЗИЛЛА, ДВИГАТЕЛИ РАПТОР И NASA «АРТЕМИДА»",
        sci_tab1: "🚀 1. ВЫВЕДЕНИЕ (7.8 КМ/С)",
        sci_tab2: "⛽ 2. УРАВНЕНИЕ ЦИОЛКОВСКОГО",
        sci_tab3: "❄️ 3. КРИОГЕН И НЕВЕСОМОСТЬ (0g)",
        sci_tab4: "🛠️ 4. РЕАЛЬНОСТЬ XXI ВЕКА",
        sci_f1_val: "5 000 тонн",
        sci_f1_lbl: "Глава 1. Огромный вес",
        sci_f1_desc: "Полностью заправленная ракета весит 5 000 тонн. Это как 11 больших пассажирских самолётов Боинг-747, сложенных вместе. Почти всё это — топливо: ракета на 90% состоит из него. Для сравнения: Saturn V («Сатурн-5»), ракета, которая в 1969 году доставила людей на Луну, весила около 3 000 тонн — почти вдвое меньше.",
        sci_f2_val: "7 500 тонн тяги",
        sci_f2_lbl: "Глава 2. Сила, которая поднимает",
        sci_f2_desc: "Тяга — это сила, с которой двигатели толкают ракету вверх. Её измеряют в тоннах силы: тяга 7 500 тонн значит, что двигатели смогли бы удержать на весу груз в 7 500 тонн. Двигателей 33, они называются Raptor («Раптор», хищная птица) и работают на метане и жидком кислороде. А теперь сравните: ракета весит 5 000 тонн, а толкают её вверх с силой 7 500. Тяга больше веса на 2 500 тонн — именно этот излишек и разгоняет ракету. Будь тяга меньше веса, ракета просто осталась бы на земле.",
        sci_f3_val: "Горячее разделение",
        sci_f3_lbl: "Глава 3. Огонь вместо паузы",
        sci_f3_desc: "Примерно через две с половиной минуты полёта ускоритель отработал своё и должен отцепиться. Обычно двигатели верхней части включают уже после отделения. Здесь иначе: корабль зажигает свои двигатели ещё пока они скреплены и огнём отталкивается от ускорителя. Это называют «горячим разделением» (по-английски hot-staging). Выигрыш в том, что ни секунды не теряется без тяги, и ракета продолжает разгоняться.",
        sci_f4_val: "28 000 км/ч",
        sci_f4_lbl: "Глава 4. Скорость, чтобы не упасть",
        sci_f4_desc: "Сначала про высоту. 320 километров над поверхностью Земли — это уже почти космос, но притяжение Земли там всё ещё почти такое же, как у нас на земле (около 90%). Если корабль просто повиснет на этой высоте, он упадёт вниз, как камень.<br><br>Как же тогда не упасть? Проведём опыт в уме. Бросьте мяч вперёд, параллельно земле: он пролетит несколько метров и упадёт. Бросьте сильнее — упадёт дальше. Теперь представьте гигантскую пушку, которая стреляет ядром вдоль поверхности Земли, по горизонтали, а не вверх. Ядро летит далеко-далеко, но Земля круглая, и её поверхность по пути загибается вниз. Чем быстрее выстрел, тем дальше успевает улететь ядро, пока падает.<br><br>И при скорости 7,8 километра в секунду (это 28 000 км/ч) происходит удивительное: пока корабль падает вниз, поверхность Земли загибается вниз ровно на столько же. Корабль падает, а земля всё не приближается. Он падает без конца и так обходит всю планету по кругу.<br><br>Этот замкнутый путь вокруг Земли и называется орбитой. А скорость, нужная, чтобы выйти на орбиту рядом с Землёй, называется первой космической. Вот почему главное для ракеты — не подняться вверх, а разогнаться вдоль Земли. Кстати, именно поэтому космонавты на орбите парят: гравитация не пропала, они просто вместе с кораблём в вечном падении.",
        sci_body_launch: "💡 <strong>Как мы здесь оказались:</strong> подъём на орбиту — это не про высоту, а про скорость. Подняться на 320 км легко, трудно разогнаться до 7,8 км/с. Для этого ракета сожгла около 4 500 тонн топлива: 3 400 в ускорителе и 1 100 в корабле. Корабль на орбите, но баки почти пусты: осталось 96 тонн из 1 200. Именно с этого начинается ваша миссия.",
        sci_intro_launch: "🎓 <strong>Добро пожаловать на экскурсию!</strong> Представьте: нужно поднять в небо многоэтажный дом и разогнать его до 28 000 километров в час. Именно так быстро надо лететь, чтобы остаться на орбите — то есть кружить вокруг Земли по замкнутому пути и не падать. Такой путь называется орбитой. Это делает самая большая ракета в истории. Она состоит из двух частей. Нижняя — ускоритель Super Heavy («Супер Хеви», по-русски «Сверхтяжёлый»): он даёт основной разгон. Верхняя — космический корабль Starship («Старшип», «Звёздный корабль»): в нём летит экипаж, и именно он дойдёт до Марса. Вместе их называют системой Starship. Давайте разберём её по главам.",
        sci_formula_desc: "Ракетное уравнение Циолковского (1903 год). Расшифровка — ниже.",
        sci_intro_tsiolk: "🎓 <strong>Самая важная формула космонавтики.</strong> В 1903 году её вывел русский учёный Константин Циолковский. Она отвечает на простой вопрос: сколько топлива нужно ракете, чтобы набрать нужную скорость? Ответ неожиданный: гораздо больше, чем кажется. Сейчас разберёмся, почему, и заодно поймём, зачем нашему кораблю на орбите нужна дозаправка.",
        sci_formula_explain: "<strong>Как читать формулу:</strong><br><strong>Δv</strong> («дельта-вэ») — на сколько ракета может увеличить свою скорость, пока не кончится топливо. Это её «запас хода», только измеряется он не в километрах, а в километрах в секунду.<br><strong>I<sub>sp</sub> · g<sub>0</sub></strong> — скорость, с которой двигатель выбрасывает раскалённый газ назад. У наших двигателей Raptor это около 3,7 км/с. Чем быстрее вылетает струя, тем сильнее толчок.<br><strong>m<sub>0</sub></strong> — масса ракеты с полными баками. <strong>m<sub>k</sub></strong> — масса той же ракеты, когда топливо выгорело.<br><strong>ln</strong> — «натуральный логарифм». Не пугайтесь: для нас он означает одно. Скорость растёт медленно, а нужное топливо — очень быстро. Каждые лишние 3,7 км/с скорости делают полную ракету тяжелее пустой ещё в 2,7 раза. Два таких прироста — уже в 7 раз, три — в 20 раз. Вот что значит «топлива нужно в разы больше».",
        sci_intro_ullage: "🎓 <strong>Задача: перекачать ледяную жидкость там, где нет «низа».</strong> На Земле жидкость сама течёт вниз. Но на орбите всё иначе, а нам нужно перелить 1 100 тонн ледяного топлива из танкера в наш корабль. Это самая хитрая инженерная задача нашей миссии. Давайте разберём её по шагам.",
        sci_intro_reality: "🎓 <strong>Всё, о чём мы рассказали, — не выдумка.</strong> Эти технологии строят и испытывают прямо сейчас, в наше время. Вот четыре факта, которые можно проверить.",
        sci_t1_val: "92%",
        sci_t1_lbl: "Глава 1. Топливо, которое везёт само себя",
        sci_t1_desc: "Ракете нужно разогнать не только корабль, но и своё собственное топливо. Чтобы разогнать груз, нужно топливо. Чтобы разогнать это топливо, нужно ещё топливо. И так далее по кругу. Поэтому почти вся масса ракеты — топливо. Из 1 200 тонн топлива нашего корабля на подъём к орбите ушло 1 100 тонн, то есть 92%. Учёные называют это «тиранией ракетного уравнения».",
        sci_t2_val: "96 тонн",
        sci_t2_lbl: "Глава 2. Что осталось в баках",
        sci_t2_desc: "На орбите в баках осталось 96 тонн, это 8% от полной заправки. По формуле выходит запас скорости около 1,3 км/с. Этого хватит, чтобы маневрировать на орбите, состыковаться с танкером и при необходимости вернуться на Землю. Но для полёта к Марсу — слишком мало.",
        sci_t3_val: "3,6 км/с",
        sci_t3_lbl: "Глава 3. Второй мощный толчок",
        sci_t3_desc: "Чтобы покинуть орбиту Земли и взять курс на Марс, нужно ещё раз сильно разогнаться: добавить к скорости 3,6 км/с. Двигатели включаются один раз, а потом корабль летит по инерции, как брошенный камень, много месяцев. По формуле для такого толчка нужно около 370 тонн топлива — почти в четыре раза больше, чем осталось в баках.",
        sci_t4_val: "1 200 тонн",
        sci_t4_lbl: "Глава 4. Полные баки",
        sci_t4_desc: "Если заправить корабль до краёв, его запас скорости вырастет до 6,9 км/с. Этого хватит на разгон к Марсу, торможение, посадку и небольшой запас на непредвиденные ситуации. Недостающие 1 100 тонн топлива привезут танкеры — специальные корабли-заправщики.",
        sci_body_tsiolk: "💡 <strong>Вся правда без иллюзий:</strong> корабль такого размера не может взять при старте и экипаж, и всё топливо на дорогу до Марса: слишком тяжёлым он получится, и ракета его не поднимет. Поэтому корабль выводят на орбиту почти пустым, а потом танкеры один за другим привозят топливо. Ваша задача — принять его: сначала стыковка, потом перекачка.",
        sci_u1_val: "−161 °C и −183 °C",
        sci_u1_lbl: "Глава 1. Топливо холоднее Антарктиды",
        sci_u1_desc: "Чтобы 1 200 тонн топлива поместились в баки, метан и кислород охлаждают, пока они не превратятся в жидкость. Жидкий метан кипит при −161 °C, жидкий кислород — при −183 °C. Для сравнения: самый сильный мороз в Антарктиде — около −89 °C. Такое сверххолодное топливо называют криогенным (от греческого «криос» — холод). Если баки плохо защищены от тепла, оно закипает и улетучивается.",
        sci_u2_val: "Невесомость",
        sci_u2_lbl: "Глава 2. Жидкость без «низа»",
        sci_u2_desc: "Жидкость течёт вниз, потому что её тянет гравитация. На орбите корабль и всё внутри него падает вместе — это и есть невесомость. Жидкость больше не прижимается ко дну: она собирается в плавающие шары и липнет к стенкам бака. Как вода на МКС: пролейте — получите шар. А насос стоит у дна бака и может остаться без жидкости.",
        sci_u3_val: "Кавитация ⚠️",
        sci_u3_lbl: "Глава 3. Пузырь в насосе — это взрыв",
        sci_u3_desc: "Насос (турбонасос) гонит топливо в двигатель: его лопасти делают 30 000 оборотов в минуту. Если вместо жидкости насос засосёт пузырь газа, лопасти теряют опору, нагрузка скачет, и насос разрывает на куски. Это явление называется кавитацией. В невесомости пузыри — обычное дело, поэтому для нас это главная опасность.",
        sci_u4_val: "Осаждение топлива 🔥",
        sci_u4_lbl: "Глава 4. Лёгкий толчок возвращает «низ»",
        sci_u4_desc: "Решение придумали такое: включить маленькие двигатели ориентации (RCS) и слегка разогнать корабль вперёд. Жидкость по инерции прижмётся к задней стенке — как кофе в машине при разгоне, — и «низ» вернётся. Нужно всего 0,02 g, это в 50 раз слабее земной тяжести. Такой манёвр называют осаждением топлива (по-английски ullage burn).",
        sci_body_ullage: "💡 <strong>Правило перекачки:</strong> сначала толчок, потом насос. Прежде чем перекачивать сотни тонн метана, экипаж даёт импульс осаждения. Только когда топливо осело на дно, открываются магистрали. Пропустите этот шаг — и насос захлебнётся газом.",
        sci_r1_val: "Старбейс",
        sci_r1_lbl: "Глава 1. Город ракет в Техасе",
        sci_r1_desc: "Старбейс (Starbase) — посёлок и космодром на юге Техаса, на берегу океана. Здесь компания SpaceX строит корабли Starship и запускает их в космос.",
        sci_r2_val: "Мехазилла",
        sci_r2_lbl: "Глава 2. Ракету поймали на лету",
        sci_r2_desc: "13 октября 2024 года, пятый испытательный полёт. 71-метровый ускоритель Super Heavy вернулся к стартовой башне, и она поймала его на лету двумя гигантскими «палочками для еды». Башню прозвали Мехазилла (Mechazilla). Благодаря этому ускоритель можно использовать снова и снова.",
        sci_r3_val: "NASA и «Артемида»",
        sci_r3_lbl: "Глава 3. Луна — тоже через дозаправку",
        sci_r3_desc: "NASA — это американское космическое агентство. Его программа «Артемида» (Artemis) вернёт людей на Луну. Для посадки выбрали лунную версию Starship, и ей, как и нашему кораблю, нужна дозаправка на орбите.",
        sci_r4_val: "«Переломный момент»",
        sci_r4_lbl: "Глава 4. Заправка в космосе: пока в испытаниях",
        sci_r4_desc: "«Переломный момент» (Tipping Point) — программа NASA, которая платит компаниям за испытания новых технологий. По ней SpaceX перекачала жидкий кислород из одного бака в другой внутри корабля. Перекачка между двумя кораблями на орбите — следующий шаг.",
        sci_body_reality: "💡 <strong>Это не фантастика:</strong> всё, что вы делаете в этой миссии — стыковка, перекачка криогенного топлива — это реальные задачи, над которыми сегодня работают инженеры SpaceX и NASA. Мы лишь перенесли их в 2038 год.",
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
        toast_bounce: "⚠️ Слишком большая скорость сближения! Отскок!",
        toast_music_play: "🎵 Саундтрек: «Арес-1: Марсианский транзит»",
        toast_music_pause: "🔇 Саундтрек приостановлен"
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
        crew_cmdr_spec: "Crisis Management: emergencies fixed 15% faster",
        crew_plt_name: "Elena Romanova",
        crew_plt_role: "Chief Pilot",
        crew_plt_spec: "Piloting: +20% manual docking accuracy",
        crew_eng_name: "Chen Wei",
        crew_eng_role: "Flight Engineer",
        crew_eng_spec: "Engineering: -25% engine wear and spare parts use",
        crew_med_name: "Dr. Marcus Reid",
        crew_med_role: "Chief Medical Officer",
        crew_med_spec: "Biomedicine: +20% crew health reserve in zero-G",
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
        sci_f1_val: "5,000 tons",
        sci_f1_lbl: "Chapter 1. Enormous weight",
        sci_f1_desc: "A fully fueled rocket weighs 5,000 tons. That is like 11 big Boeing 747 airliners put together. Almost all of it is fuel: the rocket is about 90% propellant. For comparison, the Saturn V that took people to the Moon in 1969 weighed about 3,000 tons — nearly half as much.",
        sci_f2_val: "7,500 tons of thrust",
        sci_f2_lbl: "Chapter 2. The force that lifts",
        sci_f2_desc: "Thrust is the force with which engines push a rocket upward. It is measured in tons of force: 7,500 tons of thrust means the engines could hold up a load of 7,500 tons. There are 33 engines called Raptor, burning methane and liquid oxygen. Now compare: the rocket weighs 5,000 tons, but is pushed up with 7,500. The thrust exceeds the weight by 2,500 tons — that surplus is what accelerates the rocket. If thrust were less than weight, the rocket would simply stay on the ground.",
        sci_f3_val: "Hot-Staging",
        sci_f3_lbl: "Chapter 3. Fire instead of a pause",
        sci_f3_desc: "About two and a half minutes into the flight the booster has done its job and must detach. Usually the upper stage lights its engines after separation. Here it is different: the ship ignites its engines while still attached and pushes itself away from the booster with fire. This is called hot staging. The gain is that not a second is lost without thrust, and the rocket keeps accelerating.",
        sci_f4_val: "28,000 km/h",
        sci_f4_lbl: "Chapter 4. The speed that keeps you from falling",
        sci_f4_desc: "First, about height. 320 kilometers above the Earth's surface is almost space, but Earth's pull there is still nearly as strong as down here (about 90%). If a ship simply hung at that height, it would fall like a stone.<br><br>So how do you avoid falling? Try a thought experiment. Throw a ball forward, parallel to the ground: it flies a few meters and lands. Throw harder and it lands farther. Now imagine a giant cannon firing a ball along the Earth's surface — horizontally, not upward. The ball flies very far, but the Earth is round and its surface curves downward along the way. The faster the shot, the farther the ball gets while it falls.<br><br>At 7.8 kilometers per second (28,000 km/h) something remarkable happens: while the ship falls down, the Earth's surface curves down by exactly the same amount. The ship falls, yet the ground never gets closer. It falls endlessly and so travels all the way around the planet.<br><br>This closed path around the Earth is called an orbit. The speed needed to enter orbit close to Earth is called the first cosmic velocity. That is why the main job of a rocket is not to go up, but to speed along the Earth. And that is why astronauts float in orbit: gravity has not vanished, they are simply falling together with the ship, forever.",
        sci_body_launch: "💡 <strong>How we got here:</strong> reaching orbit is not about height, it is about speed. Climbing 320 km is easy; reaching 7.8 km/s is hard. The rocket burned about 4,500 tons of propellant: 3,400 in the booster and 1,100 in the ship. The ship is in orbit, but its tanks are almost empty: 96 tons left out of 1,200. This is where your mission begins.",
        sci_intro_launch: "🎓 <strong>Welcome to the tour!</strong> Imagine lifting a multi-storey building into the sky and accelerating it to 28,000 kilometers per hour. That is how fast you must fly to stay in orbit — to circle the Earth along a closed path without falling. Such a path is called an orbit. The biggest rocket in history does exactly that. It has two parts. The lower one is the Super Heavy booster: it provides the main push. The upper one is the Starship spacecraft: the crew rides in it, and it is the one that will reach Mars. Together they are called the Starship system. Let us go through it chapter by chapter.",
        sci_formula_desc: "Tsiolkovsky's rocket equation (1903). Decoded below.",
        sci_intro_tsiolk: "🎓 <strong>The most important formula in spaceflight.</strong> In 1903 the Russian scientist Konstantin Tsiolkovsky derived it. It answers a simple question: how much fuel does a rocket need to reach a given speed? The answer is surprising: much more than you would think. Let us see why, and why our ship needs refueling in orbit.",
        sci_formula_explain: "<strong>How to read the formula:</strong><br><strong>Δv</strong> («delta-v») — how much a rocket can increase its speed before the fuel runs out. It is its «range», but measured not in kilometers, but in kilometers per second.<br><strong>I<sub>sp</sub> · g<sub>0</sub></strong> — the speed at which the engine throws hot gas backward. For our Raptor engines it is about 3.7 km/s. The faster the jet, the stronger the push.<br><strong>m<sub>0</sub></strong> — the mass of the rocket with full tanks. <strong>m<sub>k</sub></strong> — the mass of the same rocket when the fuel is burned.<br><strong>ln</strong> — the «natural logarithm». Do not be scared: for us it means one thing. Speed grows slowly, while the required fuel grows very fast. Every extra 3.7 km/s makes the full rocket 2.7 times heavier than the empty one. Two such steps mean 7 times, three mean 20 times. That is what «many times more fuel» means.",
        sci_intro_ullage: "🎓 <strong>The task: pump an ice-cold liquid where there is no «down».</strong> On Earth a liquid flows down by itself. In orbit everything is different, and we must move 1,100 tons of ice-cold fuel from a tanker into our ship. This is the trickiest engineering problem of our mission. Let us go through it step by step.",
        sci_intro_reality: "🎓 <strong>Everything we have told you is real.</strong> These technologies are being built and tested right now. Here are four facts you can check.",
        sci_t1_val: "92%",
        sci_t1_lbl: "Chapter 1. Fuel that carries itself",
        sci_t1_desc: "A rocket must accelerate not only the ship, but its own fuel. To accelerate the cargo you need fuel. To accelerate that fuel you need more fuel. And so on, in a circle. That is why most of a rocket is fuel. Of the ship's 1,200 tons of fuel, 1,100 tons (92%) were spent climbing to orbit. Scientists call this the tyranny of the rocket equation.",
        sci_t2_val: "96 tons",
        sci_t2_lbl: "Chapter 2. What is left in the tanks",
        sci_t2_desc: "In orbit 96 tons remain in the tanks, 8% of a full load. By the formula that is about 1.3 km/s of delta-v. Enough to maneuver in orbit, dock with a tanker and, if needed, return to Earth. But far too little for a flight to Mars.",
        sci_t3_val: "3.6 km/s",
        sci_t3_lbl: "Chapter 3. The second big push",
        sci_t3_desc: "To leave Earth orbit and head for Mars you must accelerate hard once more: add 3.6 km/s of speed. The engines fire once, then the ship coasts like a thrown stone for many months. By the formula such a push needs about 370 tons of fuel — nearly four times more than what is left in the tanks.",
        sci_t4_val: "1,200 tons",
        sci_t4_lbl: "Chapter 4. Full tanks",
        sci_t4_desc: "If the ship is filled to the brim, its delta-v grows to 6.9 km/s. That is enough for the push to Mars, braking, landing and a small reserve for unforeseen situations. The missing 1,100 tons of fuel will be delivered by tankers — special refueling ships.",
        sci_body_tsiolk: "💡 <strong>The truth, no illusions:</strong> a ship this size cannot take both the crew and all the fuel for Mars at liftoff: it would be too heavy for the rocket to lift. So the ship goes to orbit almost empty, and tankers then deliver the fuel one by one. Your job is to receive it: docking first, then the transfer.",
        sci_u1_val: "−161 °C and −183 °C",
        sci_u1_lbl: "Chapter 1. Fuel colder than Antarctica",
        sci_u1_desc: "To fit 1,200 tons of fuel into the tanks, methane and oxygen are cooled until they turn into liquid. Liquid methane boils at −161 °C, liquid oxygen at −183 °C. For comparison, the coldest ever in Antarctica is about −89 °C. Such super-cold fuel is called cryogenic (from the Greek «kryos», cold). If the tanks are poorly insulated, it boils and escapes.",
        sci_u2_val: "Zero gravity",
        sci_u2_lbl: "Chapter 2. Liquid with no «down»",
        sci_u2_desc: "A liquid flows down because gravity pulls it. In orbit the ship and everything inside it fall together — that is weightlessness. The liquid no longer presses against the bottom: it gathers into floating blobs and clings to the tank walls. Like water on the ISS: spill it and you get a ball. And the pump sits at the bottom of the tank and may be left without liquid.",
        sci_u3_val: "Cavitation ⚠️",
        sci_u3_lbl: "Chapter 3. A bubble in the pump means an explosion",
        sci_u3_desc: "The turbopump drives fuel into the engine: its blades make 30,000 revolutions per minute. If the pump swallows a gas bubble instead of liquid, the blades lose their support, the load jumps, and the pump is torn apart. This is called cavitation. In zero gravity bubbles are common, so for us this is the main danger.",
        sci_u4_val: "Ullage Burn 🔥",
        sci_u4_lbl: "Chapter 4. A gentle push brings «down» back",
        sci_u4_desc: "The solution: fire the small attitude thrusters (RCS) and nudge the ship forward. The liquid settles against the rear wall by inertia — like coffee in an accelerating car — and «down» returns. It takes only 0.02 g, 50 times weaker than Earth gravity. This maneuver is called an ullage burn.",
        sci_body_ullage: "💡 <strong>The transfer rule:</strong> push first, pump second. Before moving hundreds of tons of methane, the crew fires an ullage burn. Only when the fuel has settled do the transfer lines open. Skip it and the pump chokes on gas.",
        sci_r1_val: "Starbase",
        sci_r1_lbl: "Chapter 1. A rocket town in Texas",
        sci_r1_desc: "Starbase is a town and spaceport in southern Texas, on the ocean shore. Here SpaceX builds Starship vehicles and launches them into space.",
        sci_r2_val: "Mechazilla",
        sci_r2_lbl: "Chapter 2. A rocket caught in mid-air",
        sci_r2_desc: "October 13, 2024, flight 5. The 71-meter Super Heavy booster returned to the launch tower, and it caught it in mid-air with two giant «chopsticks». The tower was nicknamed Mechazilla. Thanks to this the booster can be used again and again.",
        sci_r3_val: "NASA Artemis",
        sci_r3_lbl: "Chapter 3. The Moon needs refueling too",
        sci_r3_desc: "NASA is the US space agency. Its Artemis program will return people to the Moon. A lunar version of Starship was chosen for the landing, and like our ship it needs refueling in orbit.",
        sci_r4_val: "Tipping Point",
        sci_r4_lbl: "Chapter 4. Refueling in space: still in testing",
        sci_r4_desc: "Tipping Point is a NASA program that pays companies to test new technologies. Under it SpaceX moved liquid oxygen from one tank to another inside a ship. Transfer between two ships in orbit is the next step.",
        sci_body_reality: "💡 <strong>This is not science fiction:</strong> everything you do in this mission — docking, cryogenic transfer — are real problems that SpaceX and NASA engineers are working on today. We just moved them to the year 2038.",
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
        toast_bounce: "⚠️ Excessive closing speed! Rebound!",
        toast_music_play: "🎵 Soundtrack: 'Ares-1: Martian Transit'",
        toast_music_pause: "🔇 Soundtrack paused"
      }
    };

    function toggleLanguage() {
      currentLang = currentLang === 'ru' ? 'en' : 'ru';
      document.getElementById('lang-btn').innerText = currentLang === 'ru' ? 'RU | EN' : 'EN | RU';
      applyLanguage();
    }

    function applyLanguage() {
      if (typeof ccApplyLang === 'function') ccApplyLang();
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

      document.getElementById('i18n-btn-confirm-crew').innerText = d.btn_confirm_crew;
      
      // Science Briefing translation
      document.getElementById('i18n-sci-tag').innerHTML = d.sci_tag;
      updateScienceTitle();
      document.getElementById('i18n-sci-tab1').innerHTML = d.sci_tab1;
      document.getElementById('i18n-sci-tab2').innerHTML = d.sci_tab2;
      document.getElementById('i18n-sci-tab3').innerHTML = d.sci_tab3;
      document.getElementById('i18n-sci-tab4').innerHTML = d.sci_tab4;

      // Tab 1
      document.getElementById('i18n-sci-f1-val').innerHTML = d.sci_f1_val;
      document.getElementById('i18n-sci-f1-lbl').innerHTML = d.sci_f1_lbl;
      document.getElementById('i18n-sci-f1-desc').innerHTML = d.sci_f1_desc;
      document.getElementById('i18n-sci-f2-val').innerHTML = d.sci_f2_val;
      document.getElementById('i18n-sci-f2-lbl').innerHTML = d.sci_f2_lbl;
      document.getElementById('i18n-sci-f2-desc').innerHTML = d.sci_f2_desc;
      document.getElementById('i18n-sci-f3-val').innerHTML = d.sci_f3_val;
      document.getElementById('i18n-sci-f3-lbl').innerHTML = d.sci_f3_lbl;
      document.getElementById('i18n-sci-f3-desc').innerHTML = d.sci_f3_desc;
      document.getElementById('i18n-sci-f4-val').innerHTML = d.sci_f4_val;
      document.getElementById('i18n-sci-f4-lbl').innerHTML = d.sci_f4_lbl;
      document.getElementById('i18n-sci-f4-desc').innerHTML = d.sci_f4_desc;
      document.getElementById('i18n-sci-body-launch').innerHTML = d.sci_body_launch;
      document.getElementById('i18n-sci-intro-launch').innerHTML = d.sci_intro_launch;
      document.getElementById('i18n-sci-intro-tsiolk').innerHTML = d.sci_intro_tsiolk;
      document.getElementById('i18n-sci-formula-explain').innerHTML = d.sci_formula_explain;
      document.getElementById('i18n-sci-intro-ullage').innerHTML = d.sci_intro_ullage;
      document.getElementById('i18n-sci-intro-reality').innerHTML = d.sci_intro_reality;

      // Tab 2
      document.getElementById('i18n-sci-formula-desc').innerHTML = d.sci_formula_desc;
      document.getElementById('i18n-sci-t1-val').innerHTML = d.sci_t1_val;
      document.getElementById('i18n-sci-t1-lbl').innerHTML = d.sci_t1_lbl;
      document.getElementById('i18n-sci-t1-desc').innerHTML = d.sci_t1_desc;
      document.getElementById('i18n-sci-t2-val').innerHTML = d.sci_t2_val;
      document.getElementById('i18n-sci-t2-lbl').innerHTML = d.sci_t2_lbl;
      document.getElementById('i18n-sci-t2-desc').innerHTML = d.sci_t2_desc;
      document.getElementById('i18n-sci-t3-val').innerHTML = d.sci_t3_val;
      document.getElementById('i18n-sci-t3-lbl').innerHTML = d.sci_t3_lbl;
      document.getElementById('i18n-sci-t3-desc').innerHTML = d.sci_t3_desc;
      document.getElementById('i18n-sci-t4-val').innerHTML = d.sci_t4_val;
      document.getElementById('i18n-sci-t4-lbl').innerHTML = d.sci_t4_lbl;
      document.getElementById('i18n-sci-t4-desc').innerHTML = d.sci_t4_desc;
      document.getElementById('i18n-sci-body-tsiolk').innerHTML = d.sci_body_tsiolk;

      // Tab 3
      document.getElementById('i18n-sci-u1-val').innerHTML = d.sci_u1_val;
      document.getElementById('i18n-sci-u1-lbl').innerHTML = d.sci_u1_lbl;
      document.getElementById('i18n-sci-u1-desc').innerHTML = d.sci_u1_desc;
      document.getElementById('i18n-sci-u2-val').innerHTML = d.sci_u2_val;
      document.getElementById('i18n-sci-u2-lbl').innerHTML = d.sci_u2_lbl;
      document.getElementById('i18n-sci-u2-desc').innerHTML = d.sci_u2_desc;
      document.getElementById('i18n-sci-u3-val').innerHTML = d.sci_u3_val;
      document.getElementById('i18n-sci-u3-lbl').innerHTML = d.sci_u3_lbl;
      document.getElementById('i18n-sci-u3-desc').innerHTML = d.sci_u3_desc;
      document.getElementById('i18n-sci-u4-val').innerHTML = d.sci_u4_val;
      document.getElementById('i18n-sci-u4-lbl').innerHTML = d.sci_u4_lbl;
      document.getElementById('i18n-sci-u4-desc').innerHTML = d.sci_u4_desc;
      document.getElementById('i18n-sci-body-ullage').innerHTML = d.sci_body_ullage;

      // Tab 4
      document.getElementById('i18n-sci-r1-val').innerHTML = d.sci_r1_val;
      document.getElementById('i18n-sci-r1-lbl').innerHTML = d.sci_r1_lbl;
      document.getElementById('i18n-sci-r1-desc').innerHTML = d.sci_r1_desc;
      document.getElementById('i18n-sci-r2-val').innerHTML = d.sci_r2_val;
      document.getElementById('i18n-sci-r2-lbl').innerHTML = d.sci_r2_lbl;
      document.getElementById('i18n-sci-r2-desc').innerHTML = d.sci_r2_desc;
      document.getElementById('i18n-sci-r3-val').innerHTML = d.sci_r3_val;
      document.getElementById('i18n-sci-r3-lbl').innerHTML = d.sci_r3_lbl;
      document.getElementById('i18n-sci-r3-desc').innerHTML = d.sci_r3_desc;
      document.getElementById('i18n-sci-r4-val').innerHTML = d.sci_r4_val;
      document.getElementById('i18n-sci-r4-lbl').innerHTML = d.sci_r4_lbl;
      document.getElementById('i18n-sci-r4-desc').innerHTML = d.sci_r4_desc;
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

    let bgMusic = null;
    let musicStarted = false;
    const MAIN_THEME_SRC = '__MAIN_THEME_B64__';

    function initBackgroundMusic() {
      if (!bgMusic) {
        bgMusic = new Audio(MAIN_THEME_SRC);
        bgMusic.loop = true;
        bgMusic.volume = 0.0;
      }
    }

    function startBackgroundMusic() {
      if (!audioEnabled) return;
      initBackgroundMusic();
      if (!musicStarted) {
        bgMusic.play().then(() => {
          musicStarted = true;
          let vol = 0.0;
          const fadeInterval = setInterval(() => {
            vol += 0.04;
            if (vol >= 0.40) {
              vol = 0.40;
              clearInterval(fadeInterval);
            }
            if (bgMusic) bgMusic.volume = vol;
          }, 100);
          showToast(DICT[currentLang].toast_music_play);
        }).catch(e => {
          console.log('Audio autoplay prevented, waiting for user click');
        });
      }
    }

    function toggleAudio() {
      audioEnabled = !audioEnabled;
      document.getElementById('audio-btn').innerText = audioEnabled ? '🔊' : '🔇';
      initBackgroundMusic();
      if (bgMusic) {
        if (audioEnabled) {
          bgMusic.play().then(() => {
            bgMusic.volume = 0.40;
            musicStarted = true;
          }).catch(e => {});
          showToast(DICT[currentLang].toast_music_play);
        } else {
          bgMusic.pause();
          showToast(DICT[currentLang].toast_music_pause);
        }
      }
    }

    window.addEventListener('click', function onFirstClick() {
      if (document.getElementById('cinematic') && !document.getElementById('cinematic').classList.contains('hidden')) return;
      if (!musicStarted && audioEnabled) {
        startBackgroundMusic();
      }
      window.removeEventListener('click', onFirstClick);
    });

    /* ===== INTRO CINEMATIC ===== */
    function playCinematic() {
      const v = document.getElementById('cine-video');
      document.getElementById('cine-start').style.display = 'none';
      document.getElementById('cine-skip').style.display = 'block';
      document.getElementById('cine-skip').innerText = currentLang === 'en' ? 'SKIP ⏭' : 'ПРОПУСТИТЬ ⏭';
      v.onended = endCinematic;
      v.play().catch(() => endCinematic());
    }
    function endCinematic() {
      const c = document.getElementById('cinematic');
      const v = document.getElementById('cine-video');
      if (c.classList.contains('hidden')) return;
      v.pause();
      c.classList.add('hidden');
      setTimeout(() => { c.style.display = 'none'; v.removeAttribute('src'); v.load(); }, 900);
      startBackgroundMusic();
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
      startBackgroundMusic();
      showScreen('screen-crew');
    }

    function showScienceScreen() {
      startBackgroundMusic();
      showScreen('screen-science');
    }

    /* ===== CREW CONSTRUCTOR ===== */
    const CC_AVATARS = ['👩‍🚀', '👨‍🚀', '🧑‍🚀', '👩🏾‍🚀', '👨🏿‍🚀', '👩🏻‍🚀', '👨🏽‍🚀', '🤖'];
    const CC_SKILLS = ['pilot', 'eng', 'med', 'psy', 'crisis'];
    const CC_ICONS = { pilot: '🚀', eng: '🔧', med: '🧬', psy: '🧠', crisis: '🚨' };
    const CC_MAX_POINTS = 15, CC_MAX_SKILL = 8, CC_MAX_CREW = 4;
    const CC_T = {
      ru: {
        newm: 'НОВЫЙ ЧЛЕН ЭКИПАЖА', upload: '📷 или загрузить своё фото', name: 'Имя и фамилия', pts: 'Осталось очков:',
        roster: 'ВАШ ЭКИПАЖ', add: '＋ ДОБАВИТЬ В ЭКИПАЖ', del: 'Убрать',
        pilot: 'Пилотирование', eng: 'Инженерия', med: 'Биомедицина', psy: 'Психоустойчивость', crisis: 'Аварийное управление',
        perk_pilot: 'точность стыковки', perk_eng: 'меньше износ двигателей', perk_med: 'запас здоровья в невесомости', perk_psy: 'стойкость к стрессу', perk_crisis: 'быстрее устранение аварий',
        roles: { cdr: 'Командир', plt: 'Пилот', eng: 'Бортинженер', med: 'Врач', sci: 'Учёный' },
        agencies: { nasa: 'NASA', spacex: 'SpaceX', roscosmos: 'Роскосмос', esa: 'ESA', cnsa: 'CNSA', jaxa: 'JAXA', isro: 'ISRO' },
        need_name: 'Введите имя', full: 'Экипаж полный (максимум 4)', need_pts: 'Распределите все 15 очков', empty: 'Добавьте хотя бы одного члена экипажа',
        empty_list: 'Пока никого. Создайте первого!', ok: 'Экипаж утверждён'
      },
      en: {
        newm: 'NEW CREW MEMBER', upload: '📷 or upload your own photo', name: 'Full name', pts: 'Points left:',
        roster: 'YOUR CREW', add: '＋ ADD TO CREW', del: 'Remove',
        pilot: 'Piloting', eng: 'Engineering', med: 'Biomedicine', psy: 'Psychological resilience', crisis: 'Crisis Management',
        perk_pilot: 'docking accuracy', perk_eng: 'less engine wear', perk_med: 'health reserve in zero-G', perk_psy: 'stress resistance', perk_crisis: 'faster emergency fixes',
        roles: { cdr: 'Commander', plt: 'Pilot', eng: 'Flight Engineer', med: 'Medical Officer', sci: 'Scientist' },
        agencies: { nasa: 'NASA', spacex: 'SpaceX', roscosmos: 'Roscosmos', esa: 'ESA', cnsa: 'CNSA', jaxa: 'JAXA', isro: 'ISRO' },
        need_name: 'Enter a name', full: 'Crew is full (max 4)', need_pts: 'Spend all 15 points', empty: 'Add at least one crew member', 
        empty_list: 'Nobody yet. Create your first!', ok: 'Crew approved'
      }
    };
    let ccCrew = [];
    try { ccCrew = JSON.parse(localStorage.getItem('ares1_custom_crew') || '[]'); } catch (e) { ccCrew = []; }
    let ccDraft = { avatar: CC_AVATARS[0], photo: null, skills: { pilot: 0, eng: 0, med: 0, psy: 0, crisis: 0 } };
    let ccTabActive = false;

    function ccLeft() { return CC_MAX_POINTS - CC_SKILLS.reduce((a, k) => a + ccDraft.skills[k], 0); }

    function ccApplyLang() {
      const t = CC_T[currentLang];
      const set = (id, v) => { const el = document.getElementById(id); if (el) el.innerText = v; };
      set('cc-t-new', t.newm); set('cc-t-upload', t.upload); set('cc-t-pts', t.pts);
      set('cc-t-roster', t.roster); set('cc-add-btn', t.add);
      document.getElementById('cc-name').placeholder = t.name;
      const roleSel = document.getElementById('cc-role'), agSel = document.getElementById('cc-agency');
      const rv = roleSel.value, av = agSel.value;
      roleSel.innerHTML = Object.keys(t.roles).map(k => `<option value="${k}">${t.roles[k]}</option>`).join('');
      agSel.innerHTML = Object.keys(t.agencies).map(k => `<option value="${k}">${t.agencies[k]}</option>`).join('');
      if (rv) roleSel.value = rv; if (av) agSel.value = av;
      ccRenderAvatars(); ccRenderSkills(); ccRenderList();
    }

    function ccAvatarHTML(c) { return c.photo ? `<img src="${c.photo}">` : c.avatar; }

    function ccRenderAvatars() {
      const box = document.getElementById('cc-avatars');
      box.innerHTML = CC_AVATARS.map(a => `<button class="cc-av ${(!ccDraft.photo && ccDraft.avatar === a) ? 'sel' : ''}" onclick="ccPickAvatar('${a}')">${a}</button>`).join('') +
        (ccDraft.photo ? `<button class="cc-av sel"><img src="${ccDraft.photo}"></button>` : '');
    }
    function ccPickAvatar(a) { ccDraft.avatar = a; ccDraft.photo = null; ccRenderAvatars(); }

    function ccPhoto(input) {
      const f = input.files && input.files[0];
      if (!f) return;
      const reader = new FileReader();
      reader.onload = e => {
        const img = new Image();
        img.onload = () => {
          const S = 160, cv = document.createElement('canvas');
          cv.width = cv.height = S;
          const m = Math.min(img.width, img.height);
          cv.getContext('2d').drawImage(img, (img.width - m) / 2, (img.height - m) / 2, m, m, 0, 0, S, S);
          ccDraft.photo = cv.toDataURL('image/jpeg', 0.8);
          ccRenderAvatars();
        };
        img.src = e.target.result;
      };
      reader.readAsDataURL(f);
      input.value = '';
    }

    function ccRenderSkills() {
      const t = CC_T[currentLang];
      document.getElementById('cc-skills').innerHTML = CC_SKILLS.map(k =>
        `<div class="cc-skill"><span>${CC_ICONS[k]}</span><span class="nm">${t[k]}</span>
          <button onclick="ccAdj('${k}',-1)">−</button><span class="val">${ccDraft.skills[k]}</span><button onclick="ccAdj('${k}',1)">+</button></div>`).join('');
      document.getElementById('cc-pts-left').innerText = ccLeft();
      document.getElementById('cc-perks').innerText = CC_SKILLS.filter(k => ccDraft.skills[k] > 0)
        .map(k => `${CC_ICONS[k]} +${ccDraft.skills[k] * 5}% ${t['perk_' + k]}`).join('  ·  ');
    }
    function ccAdj(k, d) {
      const v = ccDraft.skills[k] + d;
      if (v < 0 || v > CC_MAX_SKILL || (d > 0 && ccLeft() <= 0)) return;
      ccDraft.skills[k] = v; ccRenderSkills();
    }

    function ccAdd() {
      const t = CC_T[currentLang];
      const name = document.getElementById('cc-name').value.trim();
      if (!name) { showToast(t.need_name); return; }
      if (ccCrew.length >= CC_MAX_CREW) { showToast(t.full); return; }
      if (ccLeft() > 0) { showToast(t.need_pts); return; }
      ccCrew.push({ name, role: document.getElementById('cc-role').value, agency: document.getElementById('cc-agency').value,
        avatar: ccDraft.avatar, photo: ccDraft.photo, skills: Object.assign({}, ccDraft.skills) });
      ccSave();
      document.getElementById('cc-name').value = '';
      ccDraft.skills = { pilot: 0, eng: 0, med: 0, psy: 0, crisis: 0 };
      ccRenderSkills(); ccRenderList();
    }
    function ccDel(i) { ccCrew.splice(i, 1); ccSave(); ccRenderList(); }
    function ccSave() { try { localStorage.setItem('ares1_custom_crew', JSON.stringify(ccCrew)); } catch (e) { } }

    function ccRenderList() {
      const t = CC_T[currentLang];
      document.getElementById('cc-count').innerText = ccCrew.length + '/' + CC_MAX_CREW;
      document.getElementById('cc-list').innerHTML = ccCrew.length ? ccCrew.map((c, i) =>
        `<div class="cc-card"><div class="cc-av">${ccAvatarHTML(c)}</div>
          <div class="info"><b>${c.name.replace(/</g, '&lt;')}</b><br>${t.roles[c.role]} · ${t.agencies[c.agency]}<br>
          ${CC_SKILLS.map(k => `${CC_ICONS[k]}${c.skills[k]}`).join(' ')}</div>
          <button class="del" onclick="ccDel(${i})">✕</button></div>`).join('')
        : `<div style="opacity:.6">${t.empty_list}</div>`;
    }

    function confirmCrew() {
      const t = CC_T[currentLang];
      if (ccTabActive) {
        if (!ccCrew.length) { showToast(t.empty); return; }
        window.activeCrew = { type: 'custom', members: ccCrew };
      } else {
        window.activeCrew = { type: 'canon' };
      }
      showScienceScreen();
    }

    window.addEventListener('DOMContentLoaded', () => { ccApplyLang(); });

    function switchCrewTab(tab, btn) {
      document.querySelectorAll('.crew-tabs .tab-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      ccTabActive = tab !== 'canon';
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
final_html = final_html.replace('__MAIN_THEME_B64__', MAIN_THEME_B64)
final_html = final_html.replace('__INTRO_VIDEO_B64__', INTRO_VIDEO_B64)

with open(r'D:\mars-transit-odyssey\index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

with open(r'C:\Users\User\Desktop\Полет на Марс 3D.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

# Also update build_game_v1.py to match so future builds keep this
with open(r'D:\mars-transit-odyssey\build_game_v1.py', 'w', encoding='utf-8') as f:
    with open(__file__, 'r', encoding='utf-8') as current_f:
        f.write(current_f.read())

print("Game v2 with Real Orbital Physics Briefing built successfully on Drive D: and Desktop!")
