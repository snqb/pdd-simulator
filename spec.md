# ПДД Симулятор Бишкек — Интерактивный тренажёр

## What
- Ученик видит 3D-перекрёсток → нажимает "Старт" → ситуация анимируется → вопрос "Кто проедет первым?" → выбор → ответ + объяснение
- 10+ сценариев из билетов ПДД КР
- Работает в браузере, мобильный, без установки

## Stack
- Single HTML + ES modules (Three.js 0.170)
- Static deploy (GitHub Pages)
- Scenarios from JSON

## Files
- `index.html` — app (scene + quiz + UI)
- `scenarios/*.json` — ПДД situations
- `models/` — 3D assets (Sketchfab CC-BY, ~30MB)

## Ship Criteria
- [ ] Quiz overlay works (question → answer → explanation)
- [ ] 5+ scenarios loadable
- [ ] Mobile responsive (touch + small screen)
- [ ] Russian UI throughout
- [ ] Deployed to GitHub Pages
- [ ] Shareable link

## Not Now
- Sound, voice
- Player-controlled driving
- React rewrite
- >20 scenarios
- User accounts / progress tracking
