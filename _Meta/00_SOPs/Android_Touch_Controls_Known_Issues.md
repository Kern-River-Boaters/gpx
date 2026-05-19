# Android Touch Controls Known Issues

## Overview
Touch gestures (pinch-to-zoom, dragging) on Leaflet maps embedded in Obsidian notes on Android can be unreliable due to conflicts between Obsidian's mobile touch-gesture listeners and the Leaflet webview.

This is a **known conflict within the Obsidian mobile ecosystem** rather than a bug in the core Leaflet library. Android's Obsidian app intercepts finger movements for note interactions (scrolling, sidebar gestures, font adjustments) before they reach the map webview.

## Root Cause
When you embed a Leaflet map inside an Obsidian note on Android, Obsidian's own mobile touch-gesture listeners hijack your finger movements. Instead of passing pinches and pans down to the map webview, Android tries to interpret those gestures as standard note interaction—like scrolling the text page, opening sidebars, or executing quick font size adjustments.

## Tested Workarounds

### ✅ Workaround #1: Quick Restart (Most Reliable)
Leaflet can fail to initialize its `touchZoom` and `dragging` parameters properly if Obsidian was opened from a background state.

**The Fix:** Completely swipe Obsidian out of your Android recent apps overview, then relaunch it. Many users report this instantly restores basic pinching functionality for that session.

**Status:** ✅ **WORKS** - Confirmed by user testing

### ❌ Workaround #2: Disable "Quick Font Size Adjustment"
Obsidian has a default setting where pinching two fingers anywhere on a note resizes the text. This can fight with Leaflet's pinch-to-zoom engine.

**Steps:**
1. Open Settings in Obsidian
2. Go to Appearance
3. Scroll down and turn off "Quick font size adjustment"

**Status:** ❌ **DOES NOT HELP** - User already had this disabled, issue persisted

### ❌ Workaround #3: Use Map Focus Taps
Single-tap a dead space on the map (avoiding marker pins) before attempting to pinch or drag. This forces Android's webview window to gain active focus.

**Status:** ❌ **DOES NOT HELP** - Confirmed not effective

### ⚠️ Workaround #4: Force UI Buttons (Not Tested)
Add explicit zoom control parameters to force large, touch-friendly UI buttons:

```yaml
zoomDelta: 1
zoomSnap: 1
```

This forces distinct + and - zoom buttons to anchor onto the screen, providing a tap-to-zoom alternative if multi-touch pinch mechanics break.

**Status:** ⚠️ **NOT TESTED** - Available as fallback option

## Current Map Configuration
All maps in this repository already have optimal touch control parameters:

```yaml
dragging: true
gestureHandling: false
scrollWheelZoom: true
touchZoom: true
doubleClickZoom: true
```

These settings work reliably **after** a fresh Obsidian restart on Android.

## Recommendation
**Document this as a known limitation:** Android users should restart Obsidian before viewing maps for the most reliable touch control experience. The issue is inherent to how Obsidian Android handles embedded webviews and cannot be fully resolved through Leaflet configuration alone.

## References
- [Obsidian Forum: Pinch and zoom difficulties on iOS/Android](https://forum.obsidian.md/t/feature-very-difficult-to-pinch-and-zoom-in-ios-in-graph-view/42074)
- [Obsidian Forum: Zooming content without app interface](https://forum.obsidian.md/t/zooming-in-out-the-content-without-the-rest-of-the-app-interface/58542)
- [Reddit: Obsidian Leaflet map help](https://www.reddit.com/r/ObsidianMD/comments/1bn2pvw/obsidian_leaflet_map_help/)
- [GitHub: Leaflet touch controls issue](https://github.com/ScottLogic/jumpstart-Leaflet/issues/65)
