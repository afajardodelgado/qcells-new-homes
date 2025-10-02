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
