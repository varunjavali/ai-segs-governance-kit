# Design System and Shared Components Governance

Centralize UI conventions so teams do not duplicate or contradict each other.

## Single sources (create at Gate 4 for your stack)
- **Design tokens** (colors, typography, spacing, radii, breakpoints, elevation, motion) in one token file, owned by the design-system owner.
- **Reusable components** in one shared location: forms and validation, navigation, dialogs, tables, buttons, feedback messages.
- **Standard states** for every data-driven screen: loading, empty, error, success.

## Rules
1. No hardcoded colors, font sizes, or spacing in feature code; use tokens. (Automate with a stack-specific lint rule, for example a CSS/style linter; until configured this is a **review checklist item**, not an enforced rule.)
2. Reuse an existing component before creating a new one; new shared components need design-system owner review.
3. Accessibility is part of the component contract: semantic HTML, keyboard operation, visible focus, contrast, labels, error association (target WCAG 2.2 AA).
4. Responsive by default: tested at the breakpoints defined in tokens and on slow networks/low-powered devices for critical journeys.
5. **Changes to tokens or shared components are cross-feature changes:** impact analysis lists every consumer; owner review is required via CODEOWNERS; visual and accessibility tests run for affected screens.

## Review checklist for UI pull requests
Tokens used - existing components reused - loading/empty/error/success states present - keyboard and screen-reader behavior checked - responsive checked - no duplicated styles - shared change reviewed by owner.
