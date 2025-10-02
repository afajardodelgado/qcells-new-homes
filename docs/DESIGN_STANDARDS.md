# Qcells Design Language Standards

## Grid and Layout

### Desktop

#### Full Sidebar Navigation Layout

**Width/Height**
- Min Width: 1384px
- Min Height: 768px

**Grid**
- 12 Columns
- Content Margin: 24px
- Gutter: 24px

**Navigation**
- Global Navigation Bar: 60px
- Full Sidebar Navigation: 256px

**12 Columns with Full Sidebar Navigation**
- The layout consists of 12 columns in the area excluding the size of the full sidebar and side margin.
- Content is placed only within columns in the screen area.

---

#### Sidebar Navigation Layout

**Width/Height**
- Min Width: 1384px
- Min Height: 768px

**Grid**
- 12 Columns
- Content Margin: 24px
- Gutter: 24px

**Navigation**
- Global Navigation Bar: 60px
- Sidebar Navigation: 64px

**12 Columns with Sidebar Navigation**
- The layout consists of 12 columns in the area excluding the size of the sidebar and side margin.
- Content is placed only within columns in the screen area.

---

#### Basic Web Grid (1384px)

**Width/Height**
- Min Width: 1384px
- Min Height: 768px

**Grid**
- 12 Columns
- Side Margin: 24px
- Gutter: 24px

**Navigation**
- Global Navigation Bar: 60px

**12 Columns System**
- The basic layout consists of 12 columns in the area excluding the side margin.
- Content is placed only within columns in the screen area.

---

#### Web Layout (1384px)

**Grid and Layout**

**12 Rows System**
- The layout consists of 12 rows in the area excluding the global navigation bar and side margin.
- Content is recommended to be placed within rows in the screen area.

---

### Mobile

#### Mobile Grid (376px × 812px)

**Width/Height**
- Width: 376px
- Height: 812px

**Grid**
- 4 Columns
- Margin: 20px – space between content and the left/right screen edges.
- Gutter: 16px – space between columns that helps separate content.

**Navigation (iOS required values)**
- Status Bar: 44px
- Indicator: 20px

**4 Columns System**
- Content is placed only within columns in the screen area.

---

### Shared

#### Module System

- Module with 2 rows – Min Height: 90px
- Module with 3 rows – Min Height: 147px
- Module with 4 rows – Min Height: 204px
- Module with 5 rows – Min Height: 261px
- Module with 6 rows – Min Height: 318px

---

### Glossary of Terms

- **Sidebar Navigation**: A vertical menu on the left side of the layout. Can be collapsed (64px) or expanded to full width (256px).
- **Global Navigation Bar (GNB)**: A horizontal navigation bar across the top of the screen, 60px tall.
- **Content Margin**: The space between the outer edge of the content and the boundary created by the sidebar or screen edge.
- **Side Margin**: Padding on the left and right sides of the layout when no sidebar is present.
- **Gutter**: The spacing between columns that separates and aligns content.
- **Row System**: A horizontal grid structure used to align content vertically across the screen.
- **Column System**: A vertical grid structure used to align content horizontally across the screen.

---

## Typography

### Font Family

We use the **Pretendard** font family to support multilingualism with a consistent appearance across languages.

**Available Weights:**
- Bold
- Semibold
- Medium
- Regular
- Light
- Thin

**Download Links:**
- [Pretendard Font Family](https://fonts.adobe.com/fonts/pretendard)

---

### Font Colors

- **Default (Light Mode)**: gray 950 – #0A0A0A
- **Default (Dark Mode)**: gray 50 – #FAFAFA
- **Primary Color (Light & Dark)**: Primary – #00C6C1
- **Disabled / Unselected (Light & Dark)**: gray 500 – #8B8B8B

---

### Caption

- `caption-01-xs` → 10px, letter spacing 0.2, line height 14px, weight: xs
- `caption-01-s` → 10px, letter spacing 0.2, line height 14px, weight: s
- `caption-02-xs` → 12px, letter spacing 0.2, line height 16px, weight: xs
- `caption-02-s` → 12px, letter spacing 0.2, line height 16px, weight: s

---

### Body

- `body-01-xs` → 14px, line height 18–20px, weight: xs
- `body-01-s` → 14px, line height 18–20px, weight: s
- `body-01-m` → 14px, line height 18–20px, weight: m
- `body-01-l` → 14px, line height 18–20px, weight: l
- `body-01-xl` → 14px, line height 18–20px, weight: xl
- `body-02-xs` → 16px, line height 20–22px, weight: xs
- `body-02-s` → 16px, line height 20–22px, weight: s
- `body-02-m` → 16px, line height 20–22px, weight: m
- `body-02-l` → 16px, line height 20–22px, weight: l
- `body-02-xl` → 16px, line height 20–22px, weight: xl
- `body-03-xs` → 20px, line height 24–28px, weight: xs
- `body-03-s` → 20px, line height 24–28px, weight: s
- `body-03-m` → 20px, line height 24–28px, weight: m
- `body-03-l` → 20px, line height 24–28px, weight: l
- `body-03-xl` → 20px, line height 24–28px, weight: xl

---

### Subtitle

- `subtitle-01-xs` → 14px, line height 18–20px, weight: xs / s
- `subtitle-01-m` → 14px, line height 18–20px, weight: m
- `subtitle-01-l` → 14px, line height 18–20px, weight: l
- `subtitle-01-xl` → 14px, line height 18–20px, weight: xl
- `subtitle-02-xs` → 16px, line height 20–22px, weight: xs / s
- `subtitle-02-m` → 16px, line height 20–22px, weight: m
- `subtitle-02-l` → 16px, line height 20–22px, weight: l
- `subtitle-02-xl` → 16px, line height 20–22px, weight: xl
- `subtitle-03-xs` → 20px, line height 24–28px, weight: xs / s
- `subtitle-03-m` → 20px, line height 24–28px, weight: m
- `subtitle-03-l` → 20px, line height 24–28px, weight: l

---

### Title

- `title-01-m` → 14px, line height 18–20px, weight: m
- `title-01-l` → 14px, line height 18–20px, weight: l
- `title-01-xl` → 14px, line height 18–20px, weight: xl
- `title-02-m` → 16px, line height 20–22px, weight: m
- `title-02-l` → 16px, line height 20–22px, weight: l
- `title-02-xl` → 16px, line height 20–22px, weight: xl
- `title-03-m` → 20px, line height 24–28px, weight: m
- `title-03-l` → 20px, line height 24–28px, weight: l
- `title-03-xl` → 20px, line height 24–28px, weight: xl

---

### Headline

- `headline-01-l` → 16px, line height 20–22px, weight: l
- `headline-01-xl` → 16px, line height 20–22px, weight: xl
- `headline-02-l` → 20px, line height 24–28px, weight: l
- `headline-02-xl` → 20px, line height 24–28px, weight: xl

---

### Display

- `display-01-xl` → 32px, line height 36px, weight: xl

---

### Exceptional (Special Cases)

- `Module-01` → 4px, line height 8px, weight: Medium
- `Module-02` → 8px, line height 12px, weight: Regular
- `Caption-01` → 10px, line height 14px, weight: Thin
- `Caption-02` → 10px, line height 14px, weight: Light
- `Caption-03` → 10px, line height 14px, weight: Regular

---

### Glossary of Typography Terms

- **Size**: The font size in pixels.
- **Letter Spacing**: Space between characters (in px).
- **Line Height**: The vertical spacing for each line of text.
- **Weight (Token)**: Predefined design system weight (xs, s, m, l, xl).
- **Token**: The unique name identifier used in the design system for each text style.

---

## Components (Web + Mobile)

### 1. Global Components

Foundational UI elements that apply system-wide.

#### Buttons

**Primary Button**
- States: Default, Hover, Pressed, Disabled

**Secondary Button**
- States: Default, Hover, Pressed, Disabled

**Icon Button**
- Sizes: Small, Medium, Large
- States: Default, Hover, Pressed, Disabled

---

#### Inputs

**Text Field**
- States: Default, Focus, Error, Disabled

**Dropdown**
- States: Default, Expanded, Selected

**Checkbox**
- States: Default, Checked, Indeterminate, Disabled

**Radio Button**
- States: Default, Selected, Disabled

---

#### Navigation

**Global Navigation Bar (GNB)**

**Sidebar Navigation**
- Expanded / Collapsed

**Tabs**
- States: Default, Active, Hover

---

#### Feedback

**Tooltip**
- Placement: Top, Bottom, Left, Right

**Modal/Dialog**
- Variations: With action buttons / Without action buttons

**Toast Notification**
- Types: Success, Error, Warning, Info

---

#### Glossary – Global Components

- **Default State**: Baseline style of a component.
- **Hover**: Visual style on mouse-over.
- **Active/Pressed**: Style while clicked or engaged.
- **Disabled**: Non-interactive, reduced opacity.

---

### 2. Single Components

#### Badge

- **Anatomy**: Box, Text
- **Properties**: Size TBD
- **Variations**: Default, Success, Warning, Notice
- **Interaction**: Static
- **Use Cases**: Status indicators, counts

---

#### Banner

- **Anatomy**: Box, Icon, Text
- **Properties**: Mobile max width 360px; Web TBD
- **Variations**: Default, Success, Warning, Notice
- **Use Cases**: Alerts, warnings, success confirmations

---

#### Button

- **Anatomy**: Box, Text, Icon (optional)
- **Properties**: Max width 336px; Regular 48px, Small 40px
- **Variations**: Solid, Outline, Disabled
- **Use Cases**: Text only, With icon

---

#### Checkbox

- **Anatomy**: Background Area, Check Icon
- **Properties**: 20x20px (Mobile); Web TBD
- **Variations**: Selected, Selected Disabled, Unselected, Unselected Disabled
- **Use Cases**: Form inputs, Multi-select lists

---

#### Chips

- **Anatomy**: Box, Text, Icon (optional)
- **Properties**: Height 28–32px
- **Variations**: Default, Active (Primary, Red, Tangerine), Disabled
- **Use Cases**: Filters, Tags, Error codes

---

#### Floating Action Button (FAB)

- **Anatomy**: Circle Box, Icon, Shadow
- **Properties**: Regular 56px, Small 38px
- **Variations**: Site, Refresh, Top
- **Use Cases**: Site navigation, Refresh, Scroll-to-top

---

#### Icon Button

- **Anatomy**: Box, Icon
- **Properties**: Max width 48px; Icon 20px + Padding 14px/8px
- **Variations**: Solid, Outline, Disabled
- **Use Cases**: Delete, Add, Single actions

---

#### Radio Button

- **Anatomy**: Background & Border, Inner Circle
- **Properties**: 18x18px (Mobile); Web TBD
- **Variations**: Selected, Selected Disabled, Unselected, Unselected Disabled
- **Use Cases**: Exclusive form selections

---

#### Segmented Control

- **Anatomy**: Background/Border, Selected Segment, Deselected Segment
- **Properties**: Max width 336px; Regular 32px, Small 28px
- **Variations**: Selected, Deselected, Disabled
- **Use Cases**: Binary toggle, Settings switch

---

#### Slider

- **Anatomy**: Fill, Handle, Track, Label/Value
- **Properties**: Max width 336px; Regular + Small; Icon size 16px
- **Variations**: Single value, Range values
- **Use Cases**: Volume, Brightness, Range selection

---

#### Snack Bar

- **Anatomy**: Box, Text, Icon (optional), Action button (optional)
- **Properties**: Max width 360px; Web TBD
- **Variations**: Icon, Active, Long Active
- **Use Cases**: Short updates, Inline alerts

---

#### Text Field

- **Anatomy**: Title (optional), Placeholder, Icon/Unit (optional), Field, Message (optional)
- **Properties**: Max width 336px; Single/Multi-line
- **Variations**: Default, Entered, Active, Error, Correct, Disabled
- **Use Cases**: Forms, Inputs with validation

---

#### Toast

- **Anatomy**: Box, Text, Icon (optional)
- **Properties**: Max width 360px; Height 1–n lines
- **Variations**: Default, Error
- **Use Cases**: Success or error alerts

---

#### Toggle

- **Anatomy**: Toggle Button, Toggle Box
- **Properties**: 40x20px (Mobile)
- **Variations**: On, Off, Disabled (On/Off)
- **Use Cases**: Settings, Preferences

---

### 3. Notes

- All components defined for Web + Mobile.
- Web = TBD in some cases (to align with mobile or be defined later).
- Global components = system-wide rules.
- Single components = atomic UI elements.

---

## Common Micro-Experiences

### 1. Login

#### Main Page

**Login Textfields**
- Only used on Login page
- No label → placeholder shows usage of each textfield
- Width: 312 px (8px smaller than normal)
- Icon: Textfield characteristic

**Mandatory**
- Branding (Logo)
- Form (ID/Password)
- Action (Login button)
- Find Account

**Optional**
- Region
- Social Login
- Demo Account

---

#### Keyboard Flow

**Next:**
- ID → Password
- Focus shifts automatically to next input field

**Done:**
- Password → Log In
- Same as Log In button action

---

#### Incorrect ID or Password

**1–4 attempts:**
- Error message displayed in Top Snack Bar

**More than 5 attempts:**
- Error message in Top Snack Bar with Text Button
- User must perform "Find Account" to reset password

---

### 2. Sign Up

#### Step 1: Welcome Message

The welcome message is written differently depending on the purpose of the app.

**Example:**
- "Now you can monitor and control your energy anytime, anywhere."
- "Now you can easily install and manage energy products."

---

#### Step 2: Create Account

**Mandatory Fields (with asterisk *)**
- **Common**: Full Name, ID, Password, Confirm Password, Country, Telephone, Email
- **Home**: Home ID, Activation Code
- **Pro**: Company, Registration No.

**Optional Fields**
- **Home**: Building Area
- **Pro**: Company VAT Number

---

#### Password Policy

**Normal Case:** must meet all 3 conditions
1. 8–20 characters
2. At least one number and letter
3. At least one special character

**Error Case:** one or more conditions not met

---

#### Step 3: Terms and Conditions

- **Accept All** → covers Terms of Service, Transfer Cross-Borders (outside EU), Privacy Policy
- User must consent before proceeding

---

## Application UX Patterns

### 1. Auto-Loading Tab Content

**Pattern**: When users navigate to a data-heavy tab, automatically fetch and display content without requiring an explicit "Load" action.

**Implementation**:
```javascript
// Listen for tab click
if (target === 'dataSection') {
  loadDataFunction();
}
```

**Benefits**:
- Reduces user clicks
- Feels more responsive
- Immediate feedback

**Standard**: All data-heavy tabs should auto-load on first view. Provide a "Refresh" button for manual updates.

---

### 2. Scrollable Tables with Sticky Headers

**Pattern**: Large data tables should scroll within their container, not the entire page. Column headers remain visible during scroll.

**Implementation**:
```css
/* Table container */
#tableContainer {
  max-height: calc(100vh - 250px);
  overflow-y: auto;
}

/* Sticky header */
table thead {
  position: sticky;
  top: 0;
  z-index: 1;
  background: #fafafa;
}
```

**Benefits**:
- Users always see column headers
- Maintains context while scrolling
- Better space utilization

**Standard**: Tables with >10 rows should scroll within their container using viewport-relative heights.

---

### 3. Redundancy Reduction

**Pattern**: Avoid duplicating information that's already visible in navigation or context.

**Example**:
- ❌ **Don't**: Show "Builders" heading when user clicked "Builders" tab
- ✅ **Do**: Show only specific content title like "National Builders"

**Benefits**:
- Cleaner UI
- Less visual noise
- More content space

**Standard**: Don't repeat section titles when the navigation already clearly indicates the current section.

---

### 4. Role/View Indicators

**Pattern**: Display user's role or view type in a consistent, persistent location.

**Implementation**:
```html
<!-- Sidebar footer -->
<div class="admin-label">Admin view</div>
```

**Location**: Sidebar footer (bottom-left corner)

**Benefits**:
- Users always know their access level
- Context awareness
- Clear permission boundaries

**Standard**: Show user role/view type in sidebar footer using muted color (gray-500).

---

### 5. Dynamic Viewport Heights

**Pattern**: Use viewport-relative calculations instead of fixed pixel heights to adapt to different screen sizes.

**Implementation**:
```css
/* Adaptive height */
.content-area {
  max-height: calc(100vh - 250px);
}

/* NOT this */
.content-area {
  max-height: 600px; /* ❌ Fixed height */
}
```

**Benefits**:
- Adapts to different screen sizes
- Better space utilization
- Responsive without media queries

**Standard**: Content areas should scale with viewport using `calc(100vh - Xpx)` where X accounts for fixed headers/footers.

---

### 6. Action Button Labeling

**Pattern**: Use precise, context-aware labels for action buttons.

**Guidelines**:
- **"Load"**: Initial data fetch (before any data exists)
- **"Refresh"**: Re-fetch data that's already been loaded
- **"Update"**: Modify existing data
- **"Save"**: Persist changes

**Benefits**:
- Clear user expectations
- Reduced confusion
- Better discoverability

**Standard**: Use "Refresh" for re-fetching existing content, "Load" only for initial fetching.

---

### 7. Card-Based Content Grouping

**Pattern**: Group related content in card components with consistent styling.

**Implementation**:
```css
.card {
  background: #fff;
  border: 1px solid #E6E6E6;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
```

**On Background**: 
- Cards: White (#FFFFFF)
- Page background: Light gray (#FAFAFA)

**Benefits**:
- Clear visual hierarchy
- Content organization
- Professional appearance
- Easier to scan

**Standard**: Use white cards on light gray background for grouping related content. Avoid floating content directly on page background.

---

### 8. Progressive Disclosure

**Pattern**: Show essential information first, allow users to access details on demand.

**Examples**:
- Collapsed sidebar navigation
- Expandable table rows
- Modal dialogs for detailed forms

**Standard**: Default to minimal view, provide clear affordances for accessing additional details.

---

### 9. Contextual Empty States

**Pattern**: When tables or lists are empty, provide helpful context rather than blank space.

**Implementation**:
```javascript
if (data.length === 0) {
  return '<p>No builders found.</p>';
}
```

**Better**:
```javascript
if (data.length === 0) {
  return '<p>No builders found. <a href="/add">Add your first builder</a></p>';
}
```

**Standard**: Empty states should explain why content is missing and suggest next actions when applicable.

---

### 10. Consistent Icon Language

**Pattern**: Use semantic icons that match their function.

**Examples**:
- 🔨 Hammer: Builders/Construction
- ⚙️ Gear: Settings/Configuration/Connectors
- 💰 Dollar: Pricing/Finance
- 📚 Stack: Training/Learning
- 🎯 Target: Marketing
- 🏠 Home: Dashboard/Overview

**Standard**: Icons should be consistent across the application. Use filled icons for active states, outlined for inactive.

---

## Table Design Standards

### Basic Table Structure

**Required Elements**:
1. Table header (sticky when scrollable)
2. Clear column labels
3. Consistent row height
4. Hover state for rows
5. Loading state
6. Empty state

**Spacing**:
- Header padding: 12px 16px
- Cell padding: 12px 16px
- Border: 1px solid gray-200

**Typography**:
- Headers: body-01-l (14px semibold)
- Cells: body-01-xs (14px regular)

---

### Interactive Tables

**Hover State**:
```css
.table tbody tr:hover {
  background: #fafafa;
}
```

**Links in Tables**:
- Color: Primary (#00C6C1)
- No underline by default
- Underline on hover
- Open external links in new tab

---

## Navigation Standards

### Tab Behavior

**Default Tab**:
- First tab should be the most frequently used feature
- Mark as `active` on page load
- Auto-load content if data-heavy

**Tab Switching**:
- Remove `active` class from all tabs
- Add `active` class to clicked tab
- Hide all sections
- Show target section
- Auto-load content if applicable

**Visual States**:
- **Default**: Gray text, no background
- **Hover**: Light gray background
- **Active**: Primary color icon, light primary background

---

### Sidebar Navigation

**Structure** (top to bottom):
1. Brand logo
2. Navigation items
3. **Footer: Role/view indicator**

**Spacing**:
- Logo area: 60px height
- Nav item gap: 6px
- Nav item padding: 10px 12px
- Icon size: 20x20px
- Icon-to-text gap: 12px

---

## Performance Considerations

### Data Loading

**Pattern**: Show loading state → Fetch data → Display results → Handle errors

**Loading States**:
```javascript
container.innerHTML = '<p>Loading builders...</p>';
```

**Error States**:
```javascript
container.innerHTML = '<p class="error">Error: ${err.message}</p>';
```

**Standard**: Always provide immediate visual feedback for async operations.

---

### Caching Strategy

For data that changes infrequently:
- Cache on first load
- Provide manual "Refresh" button
- Auto-refresh on tab re-activation (optional)

---

## Accessibility Guidelines

### Minimum Requirements

1. **Semantic HTML**: Use proper heading hierarchy, nav elements, section tags
2. **Keyboard Navigation**: All interactive elements accessible via keyboard
3. **Focus States**: Visible focus indicators on all interactive elements
4. **Alt Text**: All images and icons have descriptive alt text
5. **Color Contrast**: Minimum 4.5:1 for normal text, 3:1 for large text

### Tables

- Use `<thead>`, `<tbody>`, `<th>`, `<td>` properly
- Include `scope` attribute on header cells
- Provide `aria-label` for complex tables

---

## Notes

- These patterns emerged from the Q.CELLS New Homes Admin Portal development
- They complement the existing Qcells Design Language Standards
- All patterns prioritize user efficiency and clarity
- Adapt patterns to specific use cases while maintaining core principles
