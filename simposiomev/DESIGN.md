# Design System Strategy: ADAPTA SAÚDE

## 1. Overview & Creative North Star
### The Creative North Star: "Clinical Editorial"
This design system moves beyond the standard medical template to embrace a "Clinical Editorial" aesthetic. It combines the precision of high-end medical technology with the sophisticated whitespace of a premium lifestyle publication (à la Apple). 

The goal is to establish **ADAPTA SAÚDE** as the authoritative voice in physiotherapy education. We break the "generic" mold by utilizing intentional asymmetry—where large, high-contrast typography sits alongside intimate, high-quality medical imagery—and a depth model based on tonal layering rather than rigid containers. The result is an experience that feels breathing, expensive, and deeply professional.

---

## 2. Colors: Tonal Depth & Restraint
While the brand profile provides vibrant greens and blues, this system applies them with extreme restraint to maintain a premium feel.

### Surface Hierarchy & Nesting
We reject the flat UI. Instead, we use a "Layered Paper" approach using Material Design surface tokens:
*   **Base Layer:** `surface` (#f8f9fa) – The canvas for the entire experience.
*   **Sectional Shifts:** Use `surface_container_low` (#f3f4f5) to subtly group related content without lines.
*   **Interactive Containers:** Use `surface_container_lowest` (#ffffff) for cards or floating modules to provide a crisp, "lifted" feel against the background.

### The "No-Line" Rule
**Explicit Instruction:** Do not use 1px solid borders to define sections or card boundaries. Division must be achieved through background color shifts (e.g., a white card on a light grey background) or generous vertical whitespace.

### The "Glass & Gradient" Rule
To elevate the "Apple-esque" feel:
*   **Glassmorphism:** Use `surface` colors at 80% opacity with a `backdrop-filter: blur(20px)` for navigation bars and floating action panels.
*   **Signature Textures:** For primary CTAs, use a subtle linear gradient from `primary` (#0054ca) to `primary_container` (#116bf8) at a 135-degree angle. This adds a "lithographic" depth that flat hex codes lack.

---

## 3. Typography: Authoritative Clarity
The typography leverages **Plus Jakarta Sans** to convey modern clinical precision.

*   **Display (lg/md):** Used for hero statements. Set with tight letter-spacing (-0.02em) to feel like a high-end magazine header.
*   **Headline (sm/md):** The primary driver of authority. Use `on_surface` (#191c1d) for maximum readability.
*   **Body (lg):** The workhorse for educational content. Ensure a line-height of 1.6 to maintain the "breathable" feel.
*   **Label (sm):** Set in all-caps with +0.05em tracking for metadata or small "Category" tags above headlines.

**Hierarchy Strategy:** Use "Scale Contrast." Pair a `display-lg` headline with a `body-md` description. The extreme difference in size creates a professional, curated look that mimics high-end hardware marketing.

---

## 4. Elevation & Depth
Depth is a functional tool, not a decoration. We use **Tonal Layering** to guide the user's eye.

*   **The Layering Principle:** Place a `surface_container_lowest` card on a `surface_container_low` section. This "natural lift" is the hallmark of sophisticated UI.
*   **Ambient Shadows:** For floating elements (like the "Join Congress" button), use a diffused shadow: `box-shadow: 0 20px 40px rgba(0, 84, 202, 0.08);`. Note the blue tint in the shadow; never use pure black or grey shadows.
*   **The "Ghost Border" Fallback:** If a border is required for accessibility, use `outline_variant` at 15% opacity. It should be felt, not seen.
*   **Glassmorphism & Depth:** Navigation menus should use a semi-transparent `surface` color with blur, allowing the vibrant medical imagery to bleed through as the user scrolls, creating an integrated, "living" layout.

---

## 5. Components

### Buttons
*   **Primary (The "High-Conversion" CTA):** High-gloss gradient using `primary` to `primary_container`. Corner radius: `full` (pill shape). Use `on_primary` (#ffffff) for text.
*   **Secondary:** `surface_container_highest` background with `primary` text. No border.
*   **Tertiary:** No background. `primary` text with a subtle underline or chevron.

### Cards & Lists
*   **Rule:** Forbid divider lines.
*   **Implementation:** Use a 48px or 64px gap between list items. For cards, use `surface_container_lowest` with an `xl` (1.5rem) roundedness scale.

### Input Fields
*   **States:** Background should be `surface_container_high`. On focus, transition to `surface_container_lowest` with a 2px `primary` "Ghost Border" (20% opacity).

### Congress-Specific Components
*   **Speaker Profile Glass-Card:** A frosted-glass card (`backdrop-blur`) that overlays speaker photos, containing their name in `title-md` and specialty in `label-sm`.
*   **Live-Stream Status Chip:** Uses `tertiary_fixed` (#7dff46) with `on_tertiary_fixed` (#062100) text. This provides a "high-alert" but professional signal of live activity.

---

## 6. Do's and Don'ts

### Do
*   **Do** use extreme whitespace. If you think there is enough space, add 16px more.
*   **Do** use high-resolution photography of medical professionals in natural light.
*   **Do** use `tertiary` (green) strictly for "Success," "Live," or "Growth" indicators to maintain its impact.
*   **Do** ensure all CTAs have a minimum touch target of 48px.

### Don't
*   **Don't** use 1px solid black or dark grey borders.
*   **Don't** use drop shadows with opacities higher than 10%.
*   **Don't** use "default" system blues. Stick strictly to the `primary` (#0054ca) and its variants.
*   **Don't** crowd the layout. If a section feels "busy," move secondary information into a "Learn More" progressive disclosure.