# Satellite reference overlay

Status: Approved for implementation by the user on 2026-09-23.

## Goal

Make the Street/Satellite control smaller and more elegant, and retain useful vector roads, administrative borders, and labels above satellite imagery.

## Scope

- Compact the existing bilingual basemap selector.
- Reuse the existing CARTO vector transportation and boundary layers above Esri imagery.
- Apply satellite-specific contrast and restore the original style in Street mode.
- Preserve operational overlays, markers, labels, and imagery fallback behavior.

## Non-goals

- No new map provider, map engine, dependency, or user setting.
- No change to analytical or operational symbology.

## Acceptance criteria

- Toggle is visibly smaller in desktop and mobile layouts.
- Satellite mode shows roads, administrative borders, and labels over imagery.
- Street mode restores the original vector style.
- Existing analytical layers remain unaffected.
