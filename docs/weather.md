# Weather and evening light

Calm, storybook weather over the manor map and the festival garden, plus softer light and depth on the map itself. Everything is drawn with code: no pictures, sound files, services or network calls.

## What players see
- **Six weathers:** gentle rain (with ripples on the lawn and soft mist), a soft storm (heavier rain, wind swirls, a few torn leaves and an occasional gentle flash), wind in the leaves, blossom petals, quiet snow and fireflies. "Clear night" turns the effects off.
- **The weather button** (round button, bottom right of the map). Tap it to try the next weather. The last choice, "Surprise me each night", lets the game pick: it follows the season (snow in winter, petals in spring, fireflies in summer, leaves in autumn) and changes each day. The choice is saved as `mapachez_weather_v1`.
- **The caption** under the map title says what the weather is ("Soft rain on the windows").
- **Sound:** when *Gentle sound* is on, rain hisses softly, wind rises with gusts and storms have far-off thunder, all made from filtered noise.
- **Evening light:** a soft blue dusk with warm pools of lamplight that gently breathe, moonlight falling through each room's stained-glass window, warmer floors, soft shadows under every room, and a garden of trees, grass and wildflowers around the manor.

## Comfort and phones
- **Reduce motion** (Settings) freezes the weather into one still picture, with no flashes and no swirls.
- The weather canvas is capped at 1.5x pixel density and the number of drops scales with screen size. Measured on an emulated iPhone 13 with the CPU slowed 4x: about 58 fps with no weather (60 before this change) and 52 to 60 fps with weather on.
- The weather only runs while the map is on screen; it stops with the map.

## Surprise nights (fun list)
If the fun list's surprise nights are in the game, "Surprise me" follows them: storm night brings the storm, wedding night brings blossom petals, the power cut brings gentle rain. Their own caption stays in place on those nights, and the old striped rain on storm nights is replaced by the new rain.

## Code
- `index.html`: the `WEATHER v1` script (just before the main script) and its CSS; `LOOK v2` helpers (`softShadow`, `tree`, `paintGrounds`, `windowLight`) and `ManorWorld.light()`.
- The map calls `window.MapachezWeather.tick()` once per frame.
- Tests: `tests/test_weather.py`.

## Seasonal title paintings
The title screen shows the owner's own painting of the manor for the current season, with matching code weather drifting over it:
spring (March to May, petals), summer (June to August, fireflies), autumn (September and October, leaves), harvest (November, leaves) and winter (December to February, snow).
The five paintings are 1152px WebP files embedded in the `SEASONS v1` script (about 1.1 MB in all), and only the current one is decoded. The older lobby painting is still in the page but no longer shown. Removing it would save about 0.35 MB.
