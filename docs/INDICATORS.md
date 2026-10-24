Русский перевод: [Индикаторы C и W](ru/INDICATORS.md).

# C and W indicators

The keyboard has two small indicators that show keyboard state:

- **C** shows the Caps Lock state reported by the computer. It follows the
  computer's state, so pressing Caps changes the indicator when the computer
  reports the change. Caps Word is a separate feature and does not turn C on.
- **W** lights when a layer above layer 0 is active. For example, holding a
  Layer-Tap key assigned to layer 1 lights W; releasing it turns W off if no
  other higher layer is active. W shows layer state, not Windows-key lock.

No Vial setting is needed. The indicators work independently of the keyboard
lighting settings. They are dark before USB is configured and while the
computer has suspended the keyboard; they update again after the keyboard
resumes. For installation and verification details, see [Status](STATUS.md).
