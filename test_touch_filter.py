"""Test that filtered/dimmed paths cannot be selected on touch devices."""
from playwright.sync_api import sync_playwright


def is_tooltip_visible(page):
    """Check if tooltip has the 'visible' class."""
    return page.locator('.tooltip.visible').count() > 0


def test_touch_filtering():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(has_touch=True, viewport={'width': 1024, 'height': 768})
        page = context.new_page()

        page.goto('http://localhost:8000')
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(1000)

        # Verify initial state
        assert not is_tooltip_visible(page), "Tooltip should not be visible initially"

        # Touch a path to show tooltip
        page.evaluate("""
            const hitPath = document.querySelector('.hitarea path');
            if (hitPath) {
                const touch = new Touch({ identifier: 1, target: hitPath, clientX: 100, clientY: 100 });
                hitPath.dispatchEvent(new TouchEvent('touchstart', {
                    touches: [touch], targetTouches: [touch], changedTouches: [touch], bubbles: true
                }));
            }
        """)
        page.wait_for_timeout(300)
        assert is_tooltip_visible(page), "Tooltip should show after touching a path"

        # Apply brush filter on Price axis
        brush_area = page.locator('.axis .brush').first
        box = brush_area.bounding_box()
        if box:
            x = box['x'] + box['width'] / 2
            page.mouse.move(x, box['y'] + 50)
            page.mouse.down()
            page.mouse.move(x, box['y'] + 150)
            page.mouse.up()
            page.wait_for_timeout(300)

        # Count filtered paths
        dimmed_count = page.locator('.foreground path.dimmed').count()
        non_dimmed_count = page.locator('.foreground path:not(.dimmed)').count()
        print(f"Dimmed: {dimmed_count}, Non-dimmed: {non_dimmed_count}")
        assert dimmed_count > 0, "Brush should filter some paths"
        assert non_dimmed_count > 0, "Brush should leave some paths visible"

        # Verify dimmed hitarea paths have pointer-events: none
        dimmed_pointer_events = page.evaluate("""(() => {
            const foregroundPaths = document.querySelectorAll('.foreground path');
            const hitareaPaths = document.querySelectorAll('.hitarea path');
            for (let i = 0; i < foregroundPaths.length; i++) {
                if (foregroundPaths[i].classList.contains('dimmed')) {
                    return getComputedStyle(hitareaPaths[i]).pointerEvents;
                }
            }
            return 'unknown';
        })()""")
        assert dimmed_pointer_events == 'none', f"Dimmed hitarea should have pointer-events:none, got {dimmed_pointer_events}"

        # Dismiss tooltip and try touching a dimmed path
        page.evaluate("document.querySelector('.tooltip').classList.remove('visible')")
        page.wait_for_timeout(100)

        result = page.evaluate("""(() => {
            const foregroundPaths = document.querySelectorAll('.foreground path');
            const hitareaPaths = document.querySelectorAll('.hitarea path');
            for (let i = 0; i < foregroundPaths.length; i++) {
                if (foregroundPaths[i].classList.contains('dimmed')) {
                    const hitPath = hitareaPaths[i];
                    if (getComputedStyle(hitPath).pointerEvents === 'none') {
                        return 'blocked';
                    }
                    const touch = new Touch({ identifier: 1, target: hitPath, clientX: 100, clientY: 100 });
                    hitPath.dispatchEvent(new TouchEvent('touchstart', {
                        touches: [touch], targetTouches: [touch], changedTouches: [touch], bubbles: true
                    }));
                    return 'dispatched';
                }
            }
            return 'no dimmed paths';
        })()""")
        page.wait_for_timeout(300)
        assert result == 'blocked', f"Dimmed path touch should be blocked, got {result}"
        assert not is_tooltip_visible(page), "Tooltip should NOT show for dimmed path"

        # Touch a non-dimmed path should still work
        page.evaluate("""(() => {
            const foregroundPaths = document.querySelectorAll('.foreground path');
            const hitareaPaths = document.querySelectorAll('.hitarea path');
            for (let i = 0; i < foregroundPaths.length; i++) {
                if (!foregroundPaths[i].classList.contains('dimmed')) {
                    const hitPath = hitareaPaths[i];
                    const touch = new Touch({ identifier: 1, target: hitPath, clientX: 100, clientY: 100 });
                    hitPath.dispatchEvent(new TouchEvent('touchstart', {
                        touches: [touch], targetTouches: [touch], changedTouches: [touch], bubbles: true
                    }));
                    break;
                }
            }
        })()""")
        page.wait_for_timeout(300)
        assert is_tooltip_visible(page), "Tooltip should show for non-dimmed path"

        browser.close()
        print("All tests passed!")


if __name__ == '__main__':
    test_touch_filtering()
