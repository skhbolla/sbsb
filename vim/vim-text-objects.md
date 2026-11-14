Vim and Neovim include a powerful set of native text objects out of the box that require zero plugins or Tree-sitter setup. 

They follow a simple grammar pattern: [action] + [a/i] + [object].
• a = "around" (includes the target object and its surrounding whitespace/brackets).
• i = "inner" (only the contents inside the target object).

Here is the complete reference list of native text objects available for yanking (y), deleting (d), changing (c), or selecting (v).

1. Containers (Brackets & Quotes)

These are ideal for code. The structural bracket objects work flawlessly across multiple lines, while quote objects are designed for a single line.

Text Object	Target	Example Action	What it does
( or ) or b	Parentheses	di(	Deletes everything inside ( )
{ or } or B	Curly Braces	ya{	Yanks a brace block including the { }
[ or ]	Square Brackets	ci[	Changes everything inside [ ]
< or >	Angle Brackets	di<	Deletes text inside < > (great for HTML/XML tags)
"	Double Quotes	di"	Deletes text inside " "
'	Single Quotes	yi'	Yanks text inside ' '


2. Text & Structure

These are built for editing prose, strings, or general paragraphs of text.

Text Object	Target	Example Action	What it does
w	Word	daw	Deletes a word (includes the trailing space)
W	WORD	diW	Deletes a WORD (consecutive non-blank characters, e.g., sys.argv[1] is one WORD but multiple words)
s	Sentence	cis	Changes inside a sentence
p	Paragraph	yap	Yanks a paragraph (blocks of text separated by blank lines)


3. Markup & Tags (HTML/XML)

If you ever edit HTML, XML, or JSX, this native object is an absolute lifesaver.

Text Object	Target	Example Action	What it does
t	XML/HTML Tag	cit	Changes inside an HTML tag block (e.g., cleans out everything between <div> and </div>)
at	XML/HTML Tag	dat	Deletes around the tag (removes the inner content and the opening/closing tags)


> NOTE: The "Seek" Behavior
> For quotes (", ', `), yes—the seeking behavior strictly scans forward and only on the current line. 
> If it doesn't find a quote ahead of the cursor on that exact line, it will simply fail and beep.
> However, for brackets ((, {, [, <) and tags (t), it scans forward and downward over multiple lines 

