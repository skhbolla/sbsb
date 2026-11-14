🧱 Section 1: Core Navigation & Mode Switches (Native)

These shortcuts manage basic line scanning, home-row micro-navigation, and structural state switching.
• h — Move the cursor one character to the left.
• j — Move the cursor one line down (hooks downward).
• k — Move the cursor one line up.
• l — Move the cursor one character to the right.
• w — Jump forward to the start of the next alphanumeric/punctuation word.
• e — Jump forward to the end of the current or next alphanumeric/punctuation word.
• b — Jump backward to the start of the previous alphanumeric/punctuation word.
• W — Jump forward past all punctuation to the next whitespace-separated WORD.
• E — Jump forward past all punctuation to the end of the current whitespace-separated WORD.
• B — Jump backward past all punctuation to the start of the previous whitespace-separated WORD.
• 0 (Zero) — Teleport the cursor to the absolute physical start of the line (column 0).
• _ (Underscore) — Teleport the cursor to the first non-whitespace character on the current line (respects indentation).
• ^ (Caret) — Native alternative/equivalent to _; jumps to the first non-whitespace character of the line.
• $ — Teleport the cursor to the absolute last character/end of the line.
• f{char} — Scan forward horizontally on the current line and land directly on the next occurrence of {char}.
• F{char} — Scan backward horizontally on the current line and land directly on the previous occurrence of {char}.
• t{char} — Scan forward horizontally on the current line and land exactly one character before {char}.
• T{char} — Scan backward horizontally on the current line and land exactly one character after {char}.
• ; (Semicolon) — Repeat the last inline character scan (f, F, t, T) in the same direction.
• , (Comma) — Repeat the last inline character scan (f, F, t, T) in the opposite direction.
• i — Enter Insert Mode before the active cursor block.
• a — Enter Insert Mode after the active cursor block (append).
• <Esc> (Escape Key) — Exit any temporary state/Insert Mode and return firmly to Normal Mode (home base).

---

🚀 Section 2: Insert Optimization & Tactical Mutations (Native)

These bindings optimize line-level workspace setups, character-swapping states, and quick normal-state injections.
• I — Instantly jump to the first non-whitespace character of the current line and enter Insert Mode.
• A — Instantly jump to the absolute end of the current line and enter Insert Mode (Append to Line End).
• o — Open a cleanly indented blank line below the current line and enter Insert Mode.
• O — Open a cleanly indented blank line above the current line and enter Insert Mode.
• x — Vaporize the exact single character resting underneath the cursor block without leaving Normal Mode.
• r{char} — Replace Mode Shift: Swap the character under the cursor with {char}, then instantly snap back to Normal Mode.
• s — Substitute character: Wipe out the character under the cursor and instantly drop into Insert Mode.

---

⚔️ Section 3: Native Verbs & Composable Operators (Native)

These act as structural operational modifiers ("Verbs") which pause the state machine and await a scope or range coordinate sequence to execute structural changes.
• d — The Delete operator (awaits a target motion or text object range to cut text into default registers).
• c — The Change operator (deletes the targeted text range and immediately drops into Insert Mode).
• y — The Yank operator (copies the calculated text range into the unnamed clipboard memory buffer).
• = — The Auto-Indent/Reformat operator (queries internal syntax layers to re-align whitespace columns perfectly).
• v — Enter character-wise Visual Mode to physically highlight boundaries before running operations.
• V — Enter line-wise Visual Mode to highlight entire vertical lines sequentially.
• <C-v> (Ctrl + v) — Enter Visual Block Mode for precision column-wise multi-line editing matrix manipulations.
• dd — Shorthand: Wipe out the entire current line completely and close up the vertical real estate gap.
• cc — Shorthand: Purge the entire current line and drop into Insert Mode on a clean line at correct indentation.
• yy — Shorthand: Copy/Yank the entire current line into register memory.
• == — Shorthand: Instantly recalculate and repair the layout columns for the current line alone.
• D — Alternative shorthand for d$; vaporizes everything from the active cursor index to the absolute end of the line.
• dj — Line-wise execution range: Delete the current line plus the line immediately below it.
• dk — Line-wise execution range: Delete the current line plus the line immediately above it.
• p — Paste After: Spit buffer data below the active line (if line-wise) or right after the cursor (if character-wise).
• P — Paste Before: Spit buffer data above the active line or right before the cursor block.
• . (Dot) — Repeat Operator: Re-execute the last native mutation command exactly as it was configured at the next location.

---

🪜 Section 4: Advanced Vertical Teleportation & File Searches (Native)

These structural coordinates manage long-range vertical motion, window viewports, and indexing expression scans across massive scripts.
• {number}j — Multiplier count navigation: Teleport the cursor down exactly {number} of lines.
• {number}k — Multiplier count navigation: Teleport the cursor up exactly {number} of lines.
• gg — Global teleportation: Instantly jump to line 1, column 0 at the very top of the file.
• G — Global teleportation: Instantly jump to the very last line at the bottom of the file workspace.
• {number}G — Absolute targeting: Transport the cursor straight to absolute line number {number} (e.g., 42G).
• } — Paragraph motion forward: Jump down to the next completely empty line break spacer (\n\n).
• { — Paragraph motion backward: Jump up to the previous completely empty line break spacer.
• d} — Directional Vector Sentence: Delete from the active cursor index down to the end of the current paragraph block.
• gg=G — Universal Reformat Macro: Snap the entire document from the absolute top (gg) to the absolute bottom (G) into perfect indentation matching language specifications.
• <C-d> (Ctrl + d) — Window viewport scroll: Pan the code screen view downwards by a half-page.
• <C-u> (Ctrl + u) — Window viewport scroll: Pan the code screen view upwards by a half-page.
• / — Initialize forward expression tracking search interface at the bottom command-line buffer status row.
• ? — Initialize backward expression tracking search interface at the bottom command-line buffer status row.
• n — Step chronologically forward to the next match generated by the active search query.
• N — Step chronologically backward to the previous match in the opposing direction of your search configuration.
• * (Asterisk) — Token Grabber: Instantly capture the exact word under the cursor and execute a global forward search for it.
• # (Hash) — Token Grabber: Instantly capture the exact word under the cursor and execute a global backward search for it.
• [{ — Scope Tracer Backward: Leap backward to the initiating bracket or starting indentation statement of the local scope.
• ]} — Scope Tracer Forward: Leap forward to the terminating bracket or step-out change block of the local scope.
• d]} — Scope Destruction Sentence: Delete from the active cursor position forward to the calculated end boundary of the structural scope.
• <C-w>h / <C-w>j / <C-w>k / <C-w>l — Native window shifting commands to jump focus across split panes.

---

💎 Section 5: Native Text Objects (Cursor-Agnostic Contexts)

These function inside operator-pending state structures, mapping boundaries outward using Inside (i) and Around (a) modifiers.
• di{ / dib — Delete all code parameters/properties inside matching curly braces, leaving the outer {} brackets safe.
• da{ / dab — Delete around curly braces, vaporizing the inner payload along with the physical {} brackets themselves.
• ci{ / cib — Change inside brackets: Strip inner contents completely and immediately transition into Insert Mode.
• di( — Delete exclusively the arguments/variables inside a function parameter list (...).
• da( — Delete everything inside the parentheses plus the physical () brackets themselves.
• ci( — Clear out parameter arrays inside parentheses and drop into Insert Mode for clean parameter rewrites.
• di" — Delete the string payload contained strictly inside double quotes, leaving "" blank.
• da" — Delete around double quotes, purging the text string and the literal " characters themselves out of the statement row.
• ci" — Change inside double quotes: Wipe string information text and enter Insert Mode instantly for an asset change.
• di' — Delete the contents held inside single quotes.
• da' — Delete the single quotes along with their contents.
• diw — Delete inside word: Target and delete the entire standalone variable token your cursor is touching, ignoring column alignment.
• daw — Delete around word: Target the alphanumeric string variable plus its single trailing whitespace column for seamless list formatting updates.
• ciw — Change inside word: Purge the active token word and switch the machine status to Insert Mode for rapid name swaps.
• dit — Delete inside web tags: Clear out the inner HTML/XML data blocks while keeping structural layout strings like <div></div> intact.
• dat — Delete around web tags: Purge the text block and both the opening and closing matching element nodes completely.
• di} / dip — Delete inside paragraph: Wipes out every line inside a block of code bounded by empty lines, preserving line breaks.
• da} / dap — Delete around paragraph: Wipes out the entire text block and collapses one empty trailing layout spacer beneath it.
• =i{ — Target reformat: Find block boundaries and auto-indent everything nested inside the curly braces structure.
• =ip / =i} — Target reformat: Find vertical whitespace gaps and auto-indent the entire paragraph/indented function block body.

---

🔌 Non-Native, Ecosystem, & Plugin-Driven Keybinds

This independent group tracks text objects and operational strings injected into your editor system via community extensions or custom framework connections.

🧱 1. vim-indent-object (Whitespace Analytics Engine)

• ii — Inside Indentation Object Modifier: Captures the block sharing the cursor's active indentation depth level, ignoring headers.
• dii — Delete all lines nested strictly inside the current indentation space configuration (leaves loop/conditional statements intact).
• cii — Change inside indentation: Erase the indented body layout and enter Insert Mode directly.
• ai — Around Indentation Object Modifier: Captures the current indentation body level plus the singular statement line sitting directly above it.
• dai — Delete around indentation: Vaporize an entire code block, structure body, and its header declaration (e.g., if state:) simultaneously in Python.
• vii — Step-by-step Visual Mode selection: Highlights the local indentation block; pressing ii repeatedly scales and grows selection boundaries up matching parent columns.
• iI — Inside Indentation (Strict Level): Limits block range calculations explicitly line-by-line.
• aI — Around Indentation (Extended Level): Grabs current block body, its heading line above, and the structural code line following beneath it.

💬 2. vim-commentary (Universal Annotation Operator)

• gcc — Toggle Comment: Annotate or strip comment indicators from the current single line depending on file language syntax.
• gcip — Paragraph Comment Annotation: Comment out an entire standalone code function block or prose paragraph up to the whitespace gap.
• gc{motion} — Composable Comment Sentence: Combines with directional motions (e.g., gciw to comment a single word, gc$ to comment to line end).

🔄 4. vim-surround (Wrapper Token Manipulation Engine)

• cs{old}{new} — Change Surround: Search local boundaries for symbol {old} and cleanly morph it into token {new} (e.g., cs"').
• ds{char} — Delete Surround: Locate the nearest wrapper pair matching {char} and strip them out of the script line completely.
• ys{motion}{char} — You Surround: Calculate text range boundaries using {motion} and wrap that segment inside {char} symbols.
• ysiw" — Structural Sentence: Calculate the limits of the word under the cursor and wrap that entire token cleanly in double quotes ("word").
• ysw" — Motion Sentence: Wrap text in double quotes starting from the active cursor position forward to the end boundary of the word (wo"rd").
• yss" — Line-wise Surround: Wrap the entire current line in double quotes.
• ys$" — Tail Surround: Wrap everything spanning from the current cursor column up to the end of the line in double quotes.
• ysip" — Block Surround: Wrap an entire paragraph layer inside double quotes.
• ysf)" — Targeted Search Surround: Hunt forward for a parenthesis target and wrap the entire calculated text distance inside double quotes.

🌐 6. Conquer of Completion (CoC) (LSP Compiler Links)

• <CR> (Enter Key) — Custom Selection Map: Triggers CoC Range Select to incrementally expand or shrink highlighting across AST node parent levels.
• gd — LSP Action: Teleport the cursor directly to the source declaration/definition code block of the active variable token.
• gy — LSP Action: Jump straight to the structural configuration Type Definition block of the variable token.
• gi — LSP Action: Jump straight into the core Implementation block tracking interface classes or methods.
• gr — LSP Action: Query references across the file layout and display an index map tracking all locations using this symbol.
• <leader>rn — Refactor Command: Trigger global Symbol Rename to update a variable name across all occurrences safely.
• K — Doc preview mapping: Query language servers and display floating window previews displaying compiler definitions and document information.

---
